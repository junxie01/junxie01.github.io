/**
 * 功能：显式传递页面路径，显示不蒜子的按篇浏览量、全站浏览量和访客数。
 * 输入：当前页面路径、script 的 data-counter-endpoint、限时加密访客会话。
 * 输出：现有 busuanzi DOM 字段；会话保存在 localStorage，不输出到日志。
 * 运行：由 templates/base.html 以 defer 加载；仅正式站点发送统计请求。
 * 参数：data-counter-endpoint 留空时沿用原脚本；启用时填写 HTTPS /count 地址。
 * 验证：离线测试不访问真实计数；部署后仍需核对 Safari 和访客数的连续性。
 */
(function () {
  'use strict';

  if (window.__seisamuseArticleCounterStarted) return;
  window.__seisamuseArticleCounterStarted = true;

  // currentScript 只在同步执行期间可靠；在第一个 await 前读取配置。
  var script = document.currentScript;
  var endpoint = script && script.dataset ? script.dataset.counterEndpoint || '' : '';
  var storageKey = 'seisamuse-counter-session';
  var fields = ['page_pv', 'site_pv', 'site_uv'];
  var productionOrigin = 'https://www.seis-jun.xyz';
  var stats = document.querySelector('.site-stats');

  function hideCounters() {
    fields.forEach(function (field) {
      var container = document.getElementById('busuanzi_container_' + field);
      if (container) container.style.display = 'none';
    });
    if (stats) stats.style.display = 'none';
  }

  function clearSession() {
    try { window.localStorage.removeItem(storageKey); } catch (_) { /* 存储可能被禁用。 */ }
  }

  function isSession(session) {
    return session && typeof session === 'object' && !Array.isArray(session) &&
      typeof session.token === 'string' && session.token.length > 0 &&
      session.token.length <= 8192 && Number.isSafeInteger(session.expiresAt) &&
      session.expiresAt > Date.now();
  }

  function storedSession() {
    try {
      var value = window.localStorage.getItem(storageKey);
      if (!value) return null;
      var session = JSON.parse(value);
      if (isSession(session)) return session.token;
      clearSession();
    } catch (_) {
      clearSession();
    }
    return null;
  }

  function saveSession(session) {
    if (session === null) {
      clearSession();
      return;
    }
    try {
      window.localStorage.setItem(storageKey, JSON.stringify({
        token: session.token,
        expiresAt: session.expiresAt,
      }));
    } catch (_) { /* 禁用存储时，仍显示本次成功返回的计数。 */ }
  }

  function validEndpoint(value) {
    try {
      var url = new URL(value);
      return url.protocol === 'https:' && url.pathname === '/count' &&
        !url.username && !url.password && !url.search && !url.hash;
    } catch (_) {
      return false;
    }
  }

  function validCounts(value) {
    return value && typeof value === 'object' && !Array.isArray(value) &&
      fields.every(function (field) {
        return Number.isSafeInteger(value[field]) && value[field] >= 0;
      }) && (value.session === null || isSession(value.session));
  }

  async function countPage() {
    hideCounters();
    // 本地预览、其他域名均不触发生产计数，也不加载旧统计脚本。
    if (window.location.origin !== productionOrigin) return;

    endpoint = endpoint.trim();
    if (!endpoint) {
      var legacy = document.createElement('script');
      legacy.src = 'https://busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js';
      legacy.async = true;
      legacy.onerror = hideCounters;
      if (stats) stats.style.display = '';
      document.head.appendChild(legacy);
      return;
    }
    if (!validEndpoint(endpoint)) return;

    var controller = new AbortController();
    var timeout = setTimeout(function () { controller.abort(); }, 10000);
    try {
      var response = await window.fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: window.location.pathname, session: storedSession() }),
        credentials: 'omit',
        cache: 'no-store',
        signal: controller.signal,
      });
      var result = await response.json();
      if (!response.ok) {
        if (result && result.error === 'invalid_session') clearSession();
        return;
      }
      if (!validCounts(result)) return;

      saveSession(result.session);
      fields.forEach(function (field) {
        var value = document.getElementById('busuanzi_value_' + field);
        var container = document.getElementById('busuanzi_container_' + field);
        if (value && container) {
          value.textContent = String(result[field]);
          container.style.display = '';
        }
      });
      if (stats) stats.style.display = '';
    } catch (_) {
      // 计数请求可能已经到达上游；失败时不重试，也不回退以免重复计数。
      hideCounters();
    } finally {
      clearTimeout(timeout);
    }
  }

  return countPage();
})();
