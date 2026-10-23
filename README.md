# 工務備忘錄擬稿

豐譽營造「衛生福利部防疫中心興建工程」工務備忘錄的擬稿工具。
選擇提送類別、填入本次變動的欄位，即時預覽，按一下就下載與原稿格式相同的 Word 檔（擬稿、正本、副本三聯）。

## 使用方式

- **線上：** 開啟 GitHub Pages 網址（設定方式見下方）。
- **離線：** 下載 `index.html`，雙擊用瀏覽器開啟即可，不需要網路。

### 提送類別

| 類別 | 需要填的欄位 |
|---|---|
| A. 監測相關－月報、周報 | 監測對象（捷運及基地／歷史建築）、報表週期（周報／月報）、日期或月份、版次 |
| B. 材料暨廠商資格送審 | 材料名稱、廠商名稱、版次、來文資料 |
| C. 計畫書送審 | 計畫名稱、版次、來文資料 |
| D. 施工圖說送審 | 圖說名稱、版次、依據字號 |
| F. 模型送審 | 模型名稱、版次、依據字號、送審內容、上傳內容 |
| 其他（自由填寫） | 主旨、說明自行輸入 |

送審版次：第一版 → 修正一版 → 審定版 → 增修＋N版 → 審定＋N版。

### 自動處理的部分

- 文號依「UN023–備＋發文日期＋當日流水號」自動組成。
- 正本、副本、承辦人為下拉選單，可自行新增、移除（清單記在各自電腦的瀏覽器裡）。
- 說明一行一項，自動編號「一、二、」；行首加「-」為子項「(一)(二)」。
- 審定版份數自動帶一式三份；模型送審修正／增修版光碟自動帶二份。

## 開啟 GitHub Pages

儲存庫 **Settings → Pages → Build and deployment**，Source 選 `Deploy from a branch`，
Branch 選 `main`、資料夾 `/ (root)`，按 Save。約一分鐘後即可用
`https://<帳號>.github.io/<儲存庫名稱>/` 開啟。

## 修改程式

| 檔案 | 用途 |
|---|---|
| `src/memo-drafter.src.html` | 主程式原始檔（類別規則、畫面、Word 填寫邏輯都在這裡） |
| `src/template.docx` | Word 範本（三聯格式，變動欄位已換成 `{{…}}` 標記） |
| `src/protos.json` | 說明清單的段落格式（一、與 (一) 兩層） |
| `tools/build_offline.py` | 把原始檔組成可離線使用的 `index.html` |
| `tools/build_template.py` | 由原始備忘錄 .docx 產生 `template.docx` 與 `protos.json` |

修改 `src/memo-drafter.src.html` 後：

```bash
npm install
python3 tools/build_offline.py
```

> 範本與說明格式已內嵌在 html 中（`TEMPLATE_B64`、`PROTOS`）；若更換 `template.docx`，需一併更新這兩個值。
