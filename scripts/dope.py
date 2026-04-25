#!/usr/bin/env python3
"""
DOP-E style polarization + BAZ extraction using paper-consistent S-transform
Implements Schimmel et al. (2011) S-transform definition with speed optimizations (Numba).

Usage:
    python dop_e_st_paper.py /path/to/sac_dir --target-freq 0.03 --outs out

References:
- Schimmel, Stutzmann, Ardhuin & Gallart (2011), Polarized Earth's ambient microseismic noise, G³
"""
import os
import glob
import argparse
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from obspy import read
from scipy.signal import get_window
from numba import njit, prange
import math
import warnings

warnings.filterwarnings("ignore")

# ======================================================
# S-transform implementation per Schimmel et al. (2011)
# ======================================================

def s_transform(x, fs, freqs, pad=True):
    """
    Paper-consistent S-transform:
    S(t,f) = ∫ x(τ) * |f|/√(2π) * exp[-(t-τ)^2 f^2 / 2] * exp[-i2π f τ] dτ
    Implemented via FFT multiplication.
    """
    n = len(x)
    dt = 1.0 / fs
    if pad:
        Nfft = 1 << ((2 * n - 1).bit_length())
    else:
        Nfft = n
    t = np.arange(n) * dt
    X = np.fft.fft(x, n=Nfft)
    freqs_fft = np.fft.fftfreq(Nfft, d=dt)

    S = np.zeros((len(freqs), n), dtype=np.complex128)
    # time index array
    for i, f in enumerate(freqs):
        if f <= 0:
            continue
        # build Gaussian window in frequency domain for convolution
        # Using exact analytical equivalence:
        # G(f') = exp[-2π^2 (f'-f)^2 / f^2]
        g_f = np.exp(-2.0 * (np.pi ** 2) * ((freqs_fft - f) ** 2) / (f ** 2))
        # convolution via inverse FFT
        s_ifft = np.fft.ifft(X * g_f, n=Nfft)
        s_ifft = s_ifft[:n]
        # normalization factor |f|/sqrt(2π)
        S[i, :] = (abs(f) / np.sqrt(2.0 * np.pi)) * s_ifft * np.exp(1j * 2 * np.pi * f * t)
    return S


# ======================================================
# Polarization & BAZ analysis (Numba optimized)
# ======================================================

@njit(parallel=True, fastmath=True)
def compute_dop_baz(cz, cn, ce, periods, fs, dop_thresh):
    nfr, nt = cz.shape
    DOP = np.zeros((nfr, nt))
    BAZ = np.full((nfr, nt), np.nan)
    QUALITY = np.zeros((nfr, nt))

    for ifr in prange(nfr):
        for it in range(nt):
            # spectral matrix (3x3)
            Z = cz[ifr, it]
            N = cn[ifr, it]
            E = ce[ifr, it]
            S00 = (Z * np.conj(Z)).real
            S01 = (Z * np.conj(N))
            S02 = (Z * np.conj(E))
            S11 = (N * np.conj(N)).real
            S12 = (N * np.conj(E))
            S22 = (E * np.conj(E)).real

            # Hermitian matrix
            S = np.array([[S00, S01.real, S02.real],
                          [S01.real, S11, S12.real],
                          [S02.real, S12.real, S22]], dtype=np.float64)

            # eigen decomposition
            w, v = np.linalg.eigh(S)
            idx = np.argsort(w)[::-1]
            w = w[idx]
            v = v[:, idx]
            # DOP = (λ1 - λ2)/(λ1+λ2+λ3)
            denom = w.sum()
            if denom <= 0:
                dop_val = 0.0
            else:
                dop_val = (w[0] - w[1]) / denom
                if dop_val < 0:
                    dop_val = 0.0
                elif dop_val > 1.0:
                    dop_val = 1.0
            DOP[ifr, it] = dop_val

            if dop_val < dop_thresh:
                continue

            # horizontal azimuth from first eigenvector (v[:,0])
            a = v[:, 0]
            rn = a[1]
            re = a[2]
            az = math.degrees(math.atan2(re, rn))
            if az < 0:
                az += 360.0
            BAZ[ifr, it] = az
            QUALITY[ifr, it] = 1

    return DOP, BAZ, QUALITY


# ======================================================
# DOPAnalyzer class
# ======================================================

class DOPAnalyzer:
    def __init__(self, fs=1.0, target_freq=None, freq_band=None,
                 dop_thresh=0.8, n_freqs=80, step=1):
        """
        Parameters:
            fs: sampling rate
            target_freq: center frequency (Hz)
            freq_band: (fmin,fmax)
            dop_thresh: threshold
            n_freqs: number of frequency points
            step: downsample factor for time (e.g. 5 -> 5 s resolution)
        """
        self.fs = fs
        self.dt = 1.0 / fs
        self.target_freq = target_freq
        self.freq_band = freq_band
        self.dop_thresh = dop_thresh
        self.n_freqs = n_freqs
        self.step = step

    def _read_triple(self, fz, fn, fe):
        stz = read(fz)[0]
        stn = read(fn)[0]
        ste = read(fe)[0]
        start = max(stz.stats.starttime, stn.stats.starttime, ste.stats.starttime)
        end = min(stz.stats.endtime, stn.stats.endtime, ste.stats.endtime)
        stz.trim(start, end)
        stn.trim(start, end)
        ste.trim(start, end)
        return stz.data.astype(float), stn.data.astype(float), ste.data.astype(float), stz.stats

    def _choose_freqs(self):
        if self.freq_band:
            fmin, fmax = self.freq_band
        elif self.target_freq:
            fmin = self.target_freq * 0.8
            fmax = self.target_freq * 1.2
        else:
            fmin, fmax = 0.005, 0.25
        freqs = np.logspace(np.log10(fmin), np.log10(fmax), self.n_freqs)
        return freqs

    def analyze_triple(self, z, n, e):
        npts = len(z)
        tvec = np.arange(0, npts, self.step) / self.fs
        freqs = self._choose_freqs()
        periods = 1.0 / freqs

        cz = s_transform(z, self.fs, freqs)
        cn = s_transform(n, self.fs, freqs)
        ce = s_transform(e, self.fs, freqs)

        # downsample in time for speed
        cz = cz[:, ::self.step]
        cn = cn[:, ::self.step]
        ce = ce[:, ::self.step]

        DOP, BAZ, QUALITY = compute_dop_baz(cz, cn, ce, periods, self.fs, self.dop_thresh)

        return {"times": tvec, "freqs": freqs, "DOP": DOP, "BAZ": BAZ, "QUALITY": QUALITY}

    def plot_results(self, res, out_prefix="result", target_freq=None):
        times = res["times"]
        freqs = res["freqs"]
        DOP = res["DOP"]
        BAZ = res["BAZ"]
        Q = res["QUALITY"]

        t_hr = times / 3600.0

        plt.figure(figsize=(12, 4))
        plt.pcolormesh(t_hr, freqs, DOP, shading="auto")
        plt.colorbar(label="DOP")
        plt.yscale("log")
        plt.ylabel("Frequency (Hz)")
        plt.xlabel("Time (hours)")
        plt.title("DOP (S-transform)")
        plt.tight_layout()
        plt.savefig(out_prefix + "_DOP.png", dpi=200)

        plt.figure(figsize=(12, 4))
        baz_masked = np.where(Q > 0, BAZ, np.nan)
        plt.pcolormesh(t_hr, freqs, baz_masked, shading="auto", cmap="hsv", vmin=0, vmax=360)
        plt.colorbar(label="Back Azimuth (°)")
        plt.yscale("log")
        plt.ylabel("Frequency (Hz)")
        plt.xlabel("Time (hours)")
        plt.title(f"BAZ (DOP>{self.dop_thresh})")
        plt.tight_layout()
        plt.savefig(out_prefix + "_BAZ_timefreq.png", dpi=200)

        if target_freq is not None:
            idx = np.argmin(np.abs(freqs - target_freq))
            baz_vals = BAZ[idx, Q[idx, :] > 0]
        else:
            baz_vals = BAZ[Q > 0]

        plt.figure(figsize=(6, 4))
        plt.hist(baz_vals[~np.isnan(baz_vals)], bins=np.arange(0, 361, 10))
        plt.xlabel("Back Azimuth (°)")
        plt.ylabel("Count")
        plt.title("BAZ Histogram")
        plt.tight_layout()
        plt.savefig(out_prefix + "_BAZ_hist.png", dpi=200)
        plt.close("all")


# ======================================================
# Utility: find 3-component sets
# ======================================================

def find_triples_in_dir(sac_dir):
    files = glob.glob(os.path.join(sac_dir, "*.SAC")) + glob.glob(os.path.join(sac_dir, "*.sac"))
    idx = defaultdict(dict)
    for f in files:
        b = os.path.basename(f)
        up = b.upper()
        if "LHZ" in up or "HZ" in up:
            base = up.replace("LHZ", "").replace("HZ", "").strip("_")
            idx[base]["Z"] = f
        elif "LHN" in up or "HN" in up:
            base = up.replace("LHN", "").replace("HN", "").strip("_")
            idx[base]["N"] = f
        elif "LHE" in up or "HE" in up:
            base = up.replace("LHE", "").replace("HE", "").strip("_")
            idx[base]["E"] = f
    triples = []
    for base, d in idx.items():
        if all(k in d for k in ("Z", "N", "E")):
            triples.append((base, d["Z"], d["N"], d["E"]))
    return triples


# ======================================================
# Main
# ======================================================

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="DOP-E S-transform (paper consistent, optimized)")
    p.add_argument("sacdir", help="Directory with 3-component SAC files")
    p.add_argument("--target-freq", type=float, default=0.03, help="Center frequency (Hz)")
    p.add_argument("--fmin", type=float, default=None, help="Min frequency")
    p.add_argument("--fmax", type=float, default=None, help="Max frequency")
    p.add_argument("--outs", default="out", help="Output prefix")
    p.add_argument("--dop-thresh", type=float, default=0.8, help="DOP threshold")
    p.add_argument("--n-freqs", type=int, default=60, help="Number of frequency points")
    p.add_argument("--step", type=int, default=5, help="Downsample step for time (1 = full)")
    args = p.parse_args()

    triples = find_triples_in_dir(args.sacdir)
    if not triples:
        print("No 3-component SAC sets found.")
        raise SystemExit

    for base, fz, fn, fe in triples:
        print("Processing:", base)
        z, n, e, stats = DOPAnalyzer()._read_triple(fz, fn, fe)
        fs = stats.sampling_rate
        if args.fmin and args.fmax:
            freq_band = (args.fmin, args.fmax)
        else:
            freq_band = None
        analyzer = DOPAnalyzer(fs=fs,
                               target_freq=args.target_freq,
                               freq_band=freq_band,
                               dop_thresh=args.dop_thresh,
                               n_freqs=args.n_freqs,
                               step=args.step)
        res = analyzer.analyze_triple(z, n, e)
        outpref = f"{args.outs}_{base}"
        analyzer.plot_results(res, out_prefix=outpref, target_freq=args.target_freq)
        print("Saved:", outpref)
