/**
 * Purpose: show independent SEISAMUSE PV and estimated browser-visitor counts.
 * Input: the HTTPS counter endpoint, page pathname and an anonymous random UUID.
 * Output: existing counter spans and a last-good cache; no old provider fallback.
 * Run: deferred by base.html; localhost/file previews use read-only GET /views.
 * Parameters: 365-day browser ID; 8-second timeout; no automatic request retries.
 * No IP, user agent, other cookies or URL query/fragment are collected here.
 */
(function () {
  'use strict';
  if (window.__seisamuseIndependentCounterStarted) return;
  window.__seisamuseIndependentCounterStarted = true;
  var script = document.currentScript;
  var endpoint = script && script.dataset ? script.dataset.counterEndpoint : '';
  var site = 'https://www.seis-jun.xyz';
  var visitorKey = 'seisamuse-visitor-v2';
  var siteCache = 'seisamuse-counter-site-v2';
  var pageCache = 'seisamuse-counter-page-v2:' + window.location.pathname;
  var uuid = /^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/;
  var stats = document.querySelector('.site-stats');
  var fields = ['site_pv', 'site_uv', 'page_pv'];
  var url;
  try {
    url = new URL(endpoint);
    if (url.origin !== 'https://stats.seis-jun.xyz' || url.pathname !== '/count' ||
        url.search || url.hash || url.username || url.password) return;
  } catch (error) { return; }

  function read(key) {
    try { return JSON.parse(window.localStorage.getItem(key)); } catch (error) { return null; }
  }
  function store(key, value) {
    try { window.localStorage.setItem(key, JSON.stringify(value)); } catch (error) {}
  }
  function visitorId() {
    try {
      var saved = read(visitorKey);
      if (saved && uuid.test(saved.id) && Number.isSafeInteger(saved.expiresAt) &&
          saved.expiresAt > Date.now() && saved.expiresAt <= Date.now() + 366 * 86400000) return saved.id;
      var value = { id: window.crypto.randomUUID(), expiresAt: Date.now() + 365 * 86400000 };
      window.localStorage.setItem(visitorKey, JSON.stringify(value));
      return value.id;
    } catch (error) { return null; }
  }
  function count(value) { return Number.isSafeInteger(value) && value >= 0; }
  function valid(data) {
    return data && data.version === 2 && data.path === window.location.pathname &&
      typeof data.since === 'string' && Number.isFinite(Date.parse(data.since)) &&
      fields.every(function (field) { return data[field] === null || count(data[field]); }) &&
      data.new_pv && count(data.new_pv.site) && count(data.new_pv.page) &&
      data.history && ['unknown', 'imported', 'estimated'].indexOf(data.history.site) >= 0 &&
      ['unknown', 'imported', 'estimated'].indexOf(data.history.page) >= 0;
  }
  function display(data, cachedAt, onlySite) {
    if (!valid(data)) return;
    var title = cachedAt ? '缓存统计：' + new Date(cachedAt).toISOString() + '；' : '';
    var shown = false;
    fields.forEach(function (field) {
      if (onlySite && field === 'page_pv') return;
      var value = data[field];
      var prefix = '';
      var description = title;
      if (field === 'page_pv' && value === null) {
        value = data.new_pv.page;
        prefix = '切换后 ';
        description += '自 ' + data.since + ' 起记录；此前的按篇浏览量未知。';
      } else if (value === null) return;
      if (field === 'site_uv' || data.history[field === 'page_pv' ? 'page' : 'site'] === 'estimated') {
        prefix = '≈' + prefix;
        description += field === 'site_uv' ? '历史估算基数加切换后的匿名浏览器计数，不等于精确人数。' : '包含手动估算的历史基数。';
      }
      var node = document.getElementById('busuanzi_value_' + field);
      var container = document.getElementById('busuanzi_container_' + field);
      if (node && container) {
        node.textContent = prefix + value.toLocaleString('en-US');
        container.title = description;
        container.setAttribute('aria-label', description || '独立访问统计');
        container.style.display = '';
        if (field !== 'page_pv') shown = true;
      }
    });
    if (shown && stats) stats.style.display = '';
  }

  fields.forEach(function (field) {
    var container = document.getElementById('busuanzi_container_' + field);
    if (container) container.style.display = 'none';
  });
  if (stats) stats.style.display = 'none';
  var cached = read(pageCache);
  if (cached && count(cached.at) && cached.at <= Date.now()) display(cached.data, cached.at, false);
  else {
    var globalCache = read(siteCache);
    if (globalCache && count(globalCache.at) && globalCache.at <= Date.now()) {
      display(Object.assign({}, globalCache.data, {path:window.location.pathname}), globalCache.at, true);
    }
  }

  return (async function () {
    var writing = window.location.origin === site;
    var controller = new AbortController();
    var timer = setTimeout(function () { controller.abort(); }, 8000);
    try {
      var options = {method:writing ? 'POST' : 'GET', credentials:'omit', cache:'no-store',
        referrerPolicy:'no-referrer', signal:controller.signal};
      var target = url.href;
      if (writing) {
        options.headers = {'Content-Type':'application/json'};
        options.body = JSON.stringify({path:window.location.pathname,
          event_id:window.crypto.randomUUID(), visitor_id:visitorId()});
      } else {
        url.pathname = '/views';
        url.searchParams.set('path', window.location.pathname);
        target = url.href;
      }
      var response = await window.fetch(target, options);
      if (!response.ok) return;
      var data = await response.json();
      if (!valid(data)) return;
      display(data, null, false);
      var snapshot = {at:Date.now(),data:data};
      store(pageCache, snapshot);
      store(siteCache, snapshot);
    } catch (error) {
      // Preserve a labelled last-good snapshot; do not fabricate or retry counts.
    } finally { clearTimeout(timer); }
  })();
})();
