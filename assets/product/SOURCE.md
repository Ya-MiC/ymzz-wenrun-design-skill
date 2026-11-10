# 稟冊 v0.21 畫面來源

| 項目 | 值 |
|---|---|
| 儲存庫 | https://github.com/Ya-MiC/ymzz-loop |
| 分支 | `cursor/v021-integrated-app-e023` |
| 提交 | `4d59b866db00a4cb8e8e05253772dcdc49ae988e` |
| 色 | `app/ui/tokens.css`，與 `assets/tokens/tokens.css` 逐字節相同 |
| 版面 | `app/ui/app.css`，抄本 `assets/product/bingce-app.css`，SHA-256 `f1f24928a9d6c9c4aa34b2ec4ce888260dccfa98d9fd5bcf9dcca3690eb4e42b` |
| 頁面 | `app/ui/index.html`、`app/ui/app.js`。程式沒有整份搬進這個儲存庫 |
| 截圖 | `assets/product/screens/`，由 `scripts/capture_bingce_ui.py` 打開上述頁面 |
| 字型 | 執行截圖時讀取該提交的 woff2。這個儲存庫不收字型檔，也不改 OFL |

`app.css` 使用了 `var(--paper)`。`tokens.css` 沒有定義 `--paper`。
