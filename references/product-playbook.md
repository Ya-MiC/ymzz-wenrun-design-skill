# 怎麼做成一個能交出去的產品

繁體中文在前，英文在後。這一章是做法，不是另一套色。色仍然只來自 `assets/tokens/tokens.css`。稟冊 v0.21 的那份 `app/ui/tokens.css` 與這份檔案逐字節相同，SHA-256 `217ca41de8a15fc612b17ec33b428470ffa155bedb8ddec73a47dba67aa85ad4`，提交 `4d59b866`。

## 對照的產品

業主點名兩件已經在市面上的產品，用來對「做得像一個產品」，不用來換色。

- **T3 Code**，[pingdotgg/t3code](https://github.com/pingdotgg/t3code)，網站 [t3.codes](https://t3.codes)。公開頁面寫的是桌面、網頁、手機都能控管本機上的代理；有 Welcome 頁、命令面板、以及 macOS、Windows、Linux 的安裝檔。這裡沒有複製它的程式。
- **Nowledge Mem**，[mem.nowledge.co](https://mem.nowledge.co)。公開文件寫的是本機優先的記憶：先存一則，找得到，檔案可以直接丟進去，安裝檔是產品的門面。請求裡的「newnodge mem」對得上這個產品。沒有找到另一個就叫這個拼法的產品。這裡沒有複製它的程式。

稟冊自己的門面是 [ymzz-loop 的 README](https://github.com/Ya-MiC/ymzz-loop/blob/cursor/v021-integrated-app-e023/README.md)。視窗標題是「稟冊」，安裝檔名是 `ymzz-bingce`。第一次打開的第一屏是稱呼。

## 要守住的八條

1. **第一屏先問稱呼。** 稟冊 `app/ui/index.html` 的第一步標題是「怎麼稱呼你」。說明寫：稱呼只留在這台電腦。電話可留空。主按鈕只有一個「下一步」，旁邊才是「先不填電話」。進度寫「第 1 步，共 6 步」。
2. **不要叫人打路徑。** 目標是原生選擇器、拖放、自動判斷。稟冊還沒做到：資料夾那一步仍有一個可打字的路徑欄，旁邊才是「瀏覽」。文件頁有 `<input type="file">`。新做的產品不要再放路徑欄。稟冊這點要照實說，不要改寫成已經沒有。
3. **每個數字、每張卡點得進明細。** 稟冊的彙報把檔案數、對話數寫成定義清單的文字，點不進去。檔案頁的類型名稱點了會打開該組。新產品要讓彙報上的每一個數點進那一頁。這是做法，不是 v0.21 已經有的行為。
4. **側欄、路徑屑、命令面板。** 稟冊有側欄，窄螢幕改成底部五個按鈕。鍵盤是 `1`、`2`、`3` 和 `/`，沒有 `Cmd/Ctrl+K`，也沒有路徑屑，只有頁首一行說明。T3 Code 的公開說明有命令面板。新產品要有側欄路由、路徑屑，以及 `Cmd/Ctrl+K`。不要把稟冊的三個數字鍵說成命令面板。
5. **空、載入、錯誤都有人話。** 稟冊已經寫了「尚未查詢。」「這裡沒有子資料夾。」「這組沒有檔案。」「還沒有對話。」「沒有找到。」錯誤句子由介面自己說，不把伺服器的英文原句直接貼上。載入和取消沿用 `references/backend-contracts.md`：量得到才顯示進度，不造一個到達時間。
6. **本機優先，用使用者的話寫。** 隱私步寫「東西留在這台電腦」「沒有你的同意，不會把內容送出去。」金鑰「只留在這台電腦」。不要在畫面上寫開發者備註。稟冊還沒完全做到：筆記路徑的預設文字是 `notes/today.md`，匯入框裡有一段 JSON 例子。新產品拿掉這種字。
7. **安裝檔和 README 就是產品的臉。** 使用者先看見的是 README 和安裝檔，不是倉庫內部的目錄說明。這個技能儲存庫的臉是根目錄的 `README.md`。
8. **一個畫面一套色。** 雲箋或陶土。正文只用墨色。深藤紫仍是提案，不拿來做連結色。

## 稟冊畫面裡已經量到的值

這些值在 `app/ui/app.css` 和 `index.html`，不在 `tokens.css`。原檔抄在 `assets/product/bingce-app.css`。

| 項目 | 稟冊實際寫法 | 怎麼對待 |
|---|---|---|
| 八個鎖定色 | 與 tokens.css 相同 | 保持 |
| 圓角 | 按鈕、輸入、橫幅 12px；卡片、畫布 16px；藥丸 999px | 元件規則。tokens.css 沒有 `--radius` |
| 陰影 | tokens.css 的 `--shadow-rest`、`--shadow-float`，暖墨，不是冷黑 | 沿用 token |
| 密度 | `index.html` 寫 `data-density="compact"` | 出廠畫面是緊湊，不是 token 裡的舒適預設 |
| 字 | Noto Sans SC Variable，正文 14px，行高 1.7 | 沿用 token。字檔不放進這個儲存庫 |
| 動效 | `--ease-ink`、`--t-press` 50ms、`--t-micro` 120ms、`--t-panel` 240ms | 沿用 token。`prefers-reduced-motion` 時關掉 |
| `--paper` | `app.css` 的引導頁用了 `var(--paper)` | tokens.css 沒有這個變量。引導頁的底其實是 body 的 `--bg-0` |
| 焦點 | token 的 `--focus-halo` 隨主題變 | `.input-warm:focus-within` 另外寫死淡紫 45% 透明，沒有走 `--focus-halo` |
| 窄螢幕 | 860px 以下側欄改欄、導覽改底欄 | 側欄同時是 `height: 100vh` 而且 sticky。手機上第一屏會被側欄占滿，再捲動時側欄蓋住內容。新產品不要抄這一段 |

## 桌面、企業後台、手機

- **桌面。** 側欄加主區。主區寬度用 `--content-wide`。一頁一件事。
- **企業後台。** 稟冊的「連接」就是這類畫面：選一種服務、金鑰留在本機、先預覽再送出、同意要勾選。句子仍是使用者的話。不要為了後台另做一套藍灰。
- **手機。** 底欄負責換頁，命中不小於 48px。側欄收起。第一屏必須看見這頁的標題和主按鈕，不能先被一條 100vh 的側欄擋住。

## 和後端契約怎麼接

畫面要的載入、取消、錯誤、校驗，對應 `references/backend-contracts.md`。那份契約寫明：原始包沒有分頁格式、時區格式、重試次數、保留天數。稟冊的彙報會顯示時區標籤，那是畫面文案，不是一份已經定死的時間戳規格。不要把推導的 JSON 說成白皮書裡的原句。

這個技能包沒有收款頁，也沒有接上支付寶。稟冊裡的「沙箱收款」是那個程式自己的示範，不屬於這份視覺技能。

## English

This chapter is the product bar. It is not a second palette. `assets/tokens/tokens.css` is byte-identical to 稟冊 v0.21 `app/ui/tokens.css` at commit `4d59b866`.

T3 Code is the public product at [pingdotgg/t3code](https://github.com/pingdotgg/t3code) and [t3.codes](https://t3.codes): desktop, web, and mobile around local agents, with a welcome page, a command palette, and installers. Nowledge Mem is [mem.nowledge.co](https://mem.nowledge.co), a local-first memory product. The wording "newnodge mem" matches that product. No other product was found under that spelling. Neither codebase is copied here.

稟冊 already opens on a nickname, keeps copy on the machine, and has empty sentences. It still has a typed folder field, report numbers that are not links, no breadcrumbs, and no `Cmd/Ctrl+K`. Keys are `1`, `2`, `3`, and `/`. The phone layout uses a sticky sidebar of `100vh`, so the work scrolls underneath it. New work follows the eight rules above and does not describe those gaps as finished features.

Office files stay derivations. See `references/office-derivations.md` and `samples/`.
