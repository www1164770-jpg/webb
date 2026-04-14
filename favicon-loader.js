/**
 * FaviconLoader - 网站图标获取模块
 * 优先级：IndexedDB缓存 → 网络抓取+缓存 → Canvas本地生成
 */

const FaviconLoader = (() => {
  const DB_NAME = 'favicon_cache';
  const DB_VERSION = 1;
  const STORE_NAME = 'favicons';
  const TIMEOUT_MS = 5000; // 网络请求超时时间

  // ============================================================
  // IndexedDB 操作
  // ============================================================
  let db = null;

  const openDB = () => new Promise((resolve, reject) => {
    if (db) return resolve(db);
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = e => {
      e.target.result.createObjectStore(STORE_NAME, { keyPath: 'domain' });
    };
    req.onsuccess = e => { db = e.target.result; resolve(db); };
    req.onerror = () => reject(req.error);
  });

  // 从缓存读取图标（返回 base64 或 null）
  const getFromCache = async (domain) => {
    try {
      const database = await openDB();
      return new Promise((resolve) => {
        const tx = database.transaction(STORE_NAME, 'readonly');
        const req = tx.objectStore(STORE_NAME).get(domain);
        req.onsuccess = () => resolve(req.result ? req.result.data : null);
        req.onerror = () => resolve(null);
      });
    } catch { return null; }
  };

  // 保存图标到缓存
  const saveToCache = async (domain, data) => {
    try {
      const database = await openDB();
      const tx = database.transaction(STORE_NAME, 'readwrite');
      tx.objectStore(STORE_NAME).put({ domain, data, time: Date.now() });
    } catch { /* 缓存失败不影响主流程 */ }
  };

  // ============================================================
  // 网络抓取（带超时控制）
  // ============================================================
  const fetchWithTimeout = (url, timeout = TIMEOUT_MS) => {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeout);
    return fetch(url, { signal: controller.signal })
      .finally(() => clearTimeout(timer));
  };

  // 把图片URL转成base64（用于持久化存储）
  const imageUrlToBase64 = (url) => new Promise((resolve) => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      try {
        const canvas = document.createElement('canvas');
        canvas.width = img.width || 32;
        canvas.height = img.height || 32;
        canvas.getContext('2d').drawImage(img, 0, 0);
        resolve(canvas.toDataURL());
      } catch { resolve(null); }
    };
    img.onerror = () => resolve(null);
    img.src = url;
    setTimeout(() => resolve(null), TIMEOUT_MS);
  });

  // 从HTML中解析 <link rel="icon"> 路径
  const extractIconFromHTML = async (url) => {
    try {
      const res = await fetchWithTimeout(url);
      if (!res.ok) return null;
      const html = await res.text();
      const doc = new DOMParser().parseFromString(html, 'text/html');

      // 按优先级查找 icon link
      const selectors = [
        'link[rel="apple-touch-icon"]',
        'link[rel="apple-touch-icon-precomposed"]',
        'link[rel="icon"][sizes="32x32"]',
        'link[rel="icon"][sizes="16x16"]',
        'link[rel="shortcut icon"]',
        'link[rel="icon"]',
      ];

      for (const sel of selectors) {
        const el = doc.querySelector(sel);
        if (el && el.href) {
          // 处理相对路径
          try {
            return new URL(el.getAttribute('href'), url).href;
          } catch { continue; }
        }
      }
      return null;
    } catch { return null; }
  };

  // 网络抓取图标，成功后存入缓存
  const fetchFromNetwork = async (url, domain) => {
    const origin = new URL(url).origin;

    // 方案1：解析HTML提取icon路径
    const iconUrl = await extractIconFromHTML(url);
    if (iconUrl) {
      const base64 = await imageUrlToBase64(iconUrl);
      if (base64) {
        await saveToCache(domain, base64);
        return base64;
      }
    }

    // 方案2：尝试根目录 /favicon.ico
    const faviconUrl = `${origin}/favicon.ico`;
    const base64 = await imageUrlToBase64(faviconUrl);
    if (base64) {
      await saveToCache(domain, base64);
      return base64;
    }

    // 方案3：第三方服务（优先国内可访问的）
    const services = [
      `https://favicon.cccyun.cc/${domain}`,
      `https://api.iowen.cn/favicon/${domain}.png`,
      `https://statics.dnspod.cn/proxy_favicon/_/favicon?domain=${domain}`,
      `https://favicon.im/${domain}?larger=true`,
    ];
    for (const svc of services) {
      const b64 = await imageUrlToBase64(svc);
      if (b64) {
        await saveToCache(domain, b64);
        return b64;
      }
    }

    return null;
  };

  // ============================================================
  // Canvas 本地生成（完全离线兜底）
  // ============================================================
  const COLORS = [
    '#4CAF50', '#2196F3', '#FF5722', '#9C27B0',
    '#FF9800', '#00BCD4', '#E91E63', '#3F51B5'
  ];

  const hashColor = (str) => {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    return COLORS[Math.abs(hash) % COLORS.length];
  };

  const generateLocalIcon = (domain) => {
    const canvas = document.createElement('canvas');
    canvas.width = 64;
    canvas.height = 64;
    const ctx = canvas.getContext('2d');
    const color = hashColor(domain);
    const letter = domain.replace('www.', '')[0]?.toUpperCase() || '?';

    // 圆角矩形背景
    const r = 14;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(r, 0);
    ctx.lineTo(64 - r, 0);
    ctx.quadraticCurveTo(64, 0, 64, r);
    ctx.lineTo(64, 64 - r);
    ctx.quadraticCurveTo(64, 64, 64 - r, 64);
    ctx.lineTo(r, 64);
    ctx.quadraticCurveTo(0, 64, 0, 64 - r);
    ctx.lineTo(0, r);
    ctx.quadraticCurveTo(0, 0, r, 0);
    ctx.closePath();
    ctx.fill();

    // 白色首字母
    ctx.fillStyle = 'white';
    ctx.font = 'bold 32px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(letter, 32, 33);

    return canvas.toDataURL();
  };

  // ============================================================
  // 主接口：getLogo(url)
  // ============================================================
  const getLogo = async (url) => {
    try {
      const domain = new URL(url).hostname;

      // 1. 优先查本地缓存
      const cached = await getFromCache(domain);
      if (cached) return cached;

      // 2. 有网络时尝试抓取
      if (navigator.onLine) {
        const fetched = await fetchFromNetwork(url, domain);
        if (fetched) return fetched;
      }

      // 3. 完全离线或抓取失败，本地生成
      return generateLocalIcon(domain);

    } catch {
      // URL格式错误等异常，用原始字符串生成图标
      return generateLocalIcon(url);
    }
  };

  return { getLogo, generateLocalIcon };
})();
