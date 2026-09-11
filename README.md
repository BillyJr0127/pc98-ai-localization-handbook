# 給 AI 的 PC-98 中文化與音訊研究手冊

版本 1.2.1 · 2026-09-10 · 繁體中文

**所有 AI 必須遵守：禁止以重製方式移植，保留原引擎，用最快速度、最少必要修改，依序完成三項核心。**

1. **盡速讓 DOS 下執行。** 原遊戲在 IBM PC 相容 DOS 真正執行並回應基本輸入。
2. **做出導出工具。** 導出該遊戲的台詞／文字至 Excel，保留可逆的原位映射。
3. **做出導入工具。** 將譯文分批放回原遊戲，完成必要編碼、字型及建置，保護存檔。

先讀 [AGENTS.md](AGENTS.md)。不要先重寫引擎、全面翻譯、製作通用框架或等待全路線驗收。能執行後就接著做兩個工具；人工範例與文件不能代替該遊戲的實際工具。

[下載教材 ZIP／AI 單檔版](https://github.com/BillyJr0127/pc98-ai-localization-handbook/releases/latest)

這份手冊把前兩次 PC-98 → IBM DOS 繁體中文移植，以及第三個尚在開發中的案例，整理成可交接給其他 AI 的工作指引。包含研究方法、失敗經驗、聲音驗證及翻譯工具設計；它不是特定商業遊戲的修補包，也不是任意 FDI 的一鍵轉換器。

1.2 新增[先跑穩原日文版](FAST-PORT.md)與[台詞 Excel 往返](TEXT-ROUNDTRIP.md)：提早展示真實操作、最小硬體轉接、增量建置、字庫容量與空白字形教訓，並附可執行的人工 Excel 匯出／匯入範例與明確的引擎適配介面。完整改動見 [CHANGELOG.md](CHANGELOG.md)。

**使用方式：把 [AI-HANDBOOK.md](AI-HANDBOOK.md) 交給你的 AI，再貼上下面的起始指令。** 單檔版包含所有章節；如果 AI 能讀整個資料夾，也可以先讀 [AI-GUIDE.md](AI-GUIDE.md)。其他 AI 不需要看過我們原本的對話。

```text
請閱讀這份 PC-98 中文化研究手冊，依 AI-GUIDE 的階段與證據規則工作。
禁止以重製方式移植，不得另寫引擎、腳本 VM 或遊戲邏輯來模仿原作。
三項核心依序是：1. 盡速讓 DOS 下執行；2. 做出導出工具；3. 做出導入工具。
我提供的輸入檔案位置是：〈填入路徑〉。
我的素材來源與可使用範圍是：〈自製／開源及授權條款／已獲授權／尚待釐清〉。
目標語言是：繁體中文。
執行目標是：〈保留 PC-98／移植 IBM DOS／其他／請先協助比較〉。
我希望聲音：盡量接近指定原版音源，並保留音樂、音效及原作停止／循環行為。
請先保護原檔、建立清單與研究狀態，辨識引擎及所有音源模式。
不要因副檔名或過往案例就假定格式，不要直接全面翻譯或改成 YM2203。
完成初步分析後，提出一個最小、可逆、能驗證假設的實驗並在已授權範圍內執行。
若目標是 IBM DOS，先保留原引擎與日文資料，只修改阻止執行的硬體依賴。
優先展示啟動畫面和一次真實操作，再補換景、存讀檔、焦點切換與音訊基本驗證。
原遊戲可執行並回應基本輸入後，就接著做該遊戲可實際使用的導出工具，再做導入工具。
人工範例只用來理解介面，不能代替實際遊戲工具；完整回歸依變更補齊，不阻擋上述三項交付。
只重建必要變動，保留既有字碼及存檔；不要讓全文翻譯或全路線驗收阻擋第一個展示。
不確定的事項請標示 unknown；完成與否必須附證據，不要只說能啟動或有聲音。
不要上傳我的磁片、程式、劇本、音樂、存檔或研究成果。
```

文件閱讀順序：

1. [AI-GUIDE.md](AI-GUIDE.md)：AI 的任務規則、第一輪行動及交接方式。
2. [WORKFLOW.md](WORKFLOW.md)：辨識、解碼、中文化、可選的 DOS 移植。
3. [AUDIO.md](AUDIO.md)：FM／SSG、OPNA、MIDI、PCM／ADPCM 與混合音源。
4. [VALIDATION.md](VALIDATION.md)：可用來判定成功或失敗的測試。
5. [LESSONS.md](LESSONS.md)：實際經驗及不可盲目套用的修正。
6. [FOLLOW-UP.md](FOLLOW-UP.md)：續作經驗、重新驗證與封裝交接。
7. [FAST-PORT.md](FAST-PORT.md)：第三案例的日版優先與增量建置，IBM DOS 目標請提早閱讀。
8. [TEXT-ROUNDTRIP.md](TEXT-ROUNDTRIP.md)：完整顯示單位、Excel 規格、人工工具操作與證據界線。
9. [RIGHTS.md](RIGHTS.md)：教學範圍、素材來源及公開前檢查。
10. [SOURCES.md](SOURCES.md)：查證入口與證據限制。

`templates/` 提供可填寫的專案、音訊、問題與封裝交接紀錄。`examples/` 的短句、事件與位元組是自製教學資料，沒有遊戲提取內容。`scripts/inspect_inputs.py` 只做唯讀清單；`scripts/check_examples.py` 示範慢播、漏音與佔位符檢查；`scripts/check_binary_examples.py` 示範字元邊界與重排文字時的控制結構檢查。它們只需 Python 3 標準函式庫；不提供磁片解密、遊戲專屬位址或完整轉換程式。

```text
python scripts/inspect_inputs.py example-a.fdi example-b.fdi --out private/inventory.json
python scripts/check_examples.py
python scripts/check_binary_examples.py
```

第一個指令的檔名是使用者自行替換的佔位例子，本包沒有附 FDI。AI 若没有檔案或執行工具，可以先閱讀與規劃，但不能聲稱已分析你的遊戲。

新的 Excel 範例需要 Python 3.10 以上及公開依賴，從自製資料建立三張工作表、配對映射與候選語言狀態：

```text
python -m pip install -r requirements.txt
python scripts/check_translation_workflow.py
python scripts/export_workbook.py examples/translation-catalog.json --out output/demo
python scripts/import_workbook.py examples/translation-catalog.json output/demo/volume-001.xlsx --out output/candidate.json
```

最後一步未填譯文時只產生空的候選狀態。編輯位置、分批匯入及清空規則見 TEXT-ROUNDTRIP.md 第 10 節。新範例只支援自製單呼叫 JSON，**不會解析遊戲映像、產生字庫、編譯或套用遊戲**；新遊戲需要完成 `templates/ENGINE-ADAPTER.md` 的介面。

首個本機案例的最終聲音已獲使用者滿意回饋；續作有另外的事件、畫面及功能測試。兩者都不能證明任意遊戲可用、全曲與實體硬體逐樣本相同，或已完成正常流程全程通關。續作全螢幕錄影尚未完成實測。MIDI／OPNA 章節仍是研究分支，不能把兩次 YM2203 的結果當作這些模式已實作。

第三案例尚未完成全文中文化。1.2.1 發布前只讀查核到一次實際繁中批次導入成功紀錄與通過的建置日誌；這補上先前只有預檢的證據，但仍不等於全文、全路線或中文排版驗收，聲音與速度也有未完整驗證的分支。首作目前使用即時 YM2203 軟體合成，不再只是早期預錄 PCM 方案。

本教材新增的文件、模板與自製腳本採 [MIT License](LICENSE)，可保留授權聲明後分享與改寫。此授權不涵蓋連結中的第三方內容、讀者提供的遊戲、字型或音源資料，也不是個案法律保證。素材與公開邊界見 RIGHTS.md。
