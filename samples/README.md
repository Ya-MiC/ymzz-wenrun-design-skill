# 雲箋樣本

這三份是依 `references/office-derivations.md` 產生的推導樣本，不是原始母片。v7.1 原始包沒有寫 PPTX、DOCX、XLSX。

| 檔案 | 內容 |
|---|---|
| [yunjian-brief.pptx](yunjian-brief.pptx) | 三頁。一頁一個意思。紙面 `#F8F6EF`，標題 21pt 墨色 |
| [yunjian-brief.docx](yunjian-brief.docx) | 一頁說明加一張四色表。表頭是淺天空藍，字是墨色 |
| [yunjian-brief.xlsx](yunjian-brief.xlsx) | 「雲箋」與「間距」兩張表。表頭凍結，數字靠右 |

只使用雲箋四色、墨色，以及推導出來的卡片實色 `#FCFCF9` 和線 `#E9E7E0`。深藤紫沒有用。主題字型寫的是 Noto Sans SC。電腦沒有這套字時，程式會換成別的字，那不是另一個指定字型。

重新產生：`python3 scripts/build_office_samples.py`
