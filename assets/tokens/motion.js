/**
 * motion.js — 動效 token 與彈簧（晏銘湛箴 v3）
 * 原則：CSS 優先；需要速度續接（手勢中斷）才用 JS spring。
 * MIT 一類寬鬆精神：本文件為本產品自寫，無第三方依賴。
 */

export const EASE_INK = 'cubic-bezier(.16, 1, .3, 1)';

export const DURATION = {
  press: 50,
  micro: 120,
  panel: 240,
  overlayIn: 200,
  overlayOut: 250,
  fullscreen: 400,
};

/** 彈簧性格（用戶鐵律） */
export const SPRING = {
  // 過阻尼：吸附雷厲風行。mass=1 時 ζ = c/(2√k)：1200/72 → ζ≈1.04，真正到位即停。
  // v2 的 damping:40 實為欠阻尼（ζ≈0.58 會過衝回彈），已糾正。
  snap: { stiffness: 1200, damping: 72 },
  like: { stiffness: 500, damping: 18 },    // 欠阻尼：點贊歡快 Q 彈（ζ≈0.40，1–2 次過衝）
  copy: { stiffness: 600, damping: 22 },    // 回彈 + 確認感
};

/** 水墨暈開：批次注入逐字節點（單字 120ms，相鄰錯開 30ms） */
export function inkCascade(container, text, batchMs = 30) {
  container.textContent = '';
  let i = 0;
  let buf = [];
  let timer = null;
  const flush = () => {
    for (const ch of buf) {
      const span = document.createElement('span');
      span.className = 'ink-char';
      span.style.setProperty('--i', i);
      span.textContent = ch;
      container.appendChild(span);
      i++;
    }
    // 出視口回收由 IntersectionObserver 在業務側掛接
    buf = [];
  };
  return {
    push(ch) {
      buf.push(ch);
      if (!timer) timer = setTimeout(() => { timer = null; flush(); }, batchMs);
    },
    done() { if (timer) { clearTimeout(timer); timer = null; } flush(); },
  };
}

/** 觸覺語義映射（Tauri haptics 插件；無硬件自動靜默） */
export const HAPTIC = {
  snap: 'light',      // 吸附落位：輕敲
  like: 'double',     // 點贊：雙擊感
  copy: 'confirm',    // 複製成功：確認感
  danger: 'warning',  // 危險操作：警告感
};

/** Toast 時長計算（2500 基準 + 每 20 字 +500，上限 8s） */
export function toastDuration(text) {
  return Math.min(2500 + Math.max(0, text.length - 20) / 20 * 500, 8000);
}

/** prefers-reduced-motion */
export function prefersReducedMotion() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}
