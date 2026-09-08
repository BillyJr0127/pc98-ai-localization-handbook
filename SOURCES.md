# 參考與證據層級

查核日期：2026-09-08。連結內容及軟體介面可能更新；實際研究要記錄當時版本。這裡只列官方機構、原作者專案與原廠文件，不附下載所得的第三方內容。

## 音訊與介面

| 來源 | 用途 | 不應推論 |
|---|---|---|
| [ymfm 原作者專案](https://github.com/aaronsgiles/ymfm) | Yamaha 核心系列、時鐘／產生樣本介面與授權入口 | 支援核心就等於整張音效板已完成或與實機逐樣本一致 |
| [Standard MIDI Files](https://midi.org/standard-midi-files) | 事件時間、曲軌與標準格式入口 | 任意 `.M` 或專有樂譜都是 SMF |
| [MIDI 1.0 訊息概要](https://midi.org/summary-of-midi-1-0-messages) | 訊息種類與規格查詢入口 | 概要取代完整規格或接收器手冊 |
| [General MIDI](https://midi.org/general-midi) | 區分 GM 相容性與具體音源 | 所有 GM 接收器的聲音完全相同 |
| [Roland SC-55 手冊](https://cdn.roland.com/assets/media/pdf/SC-55_OM.pdf) | 查核目標模組及 SysEx | 所有 SC 型號／版本都相同 |
| [Munt](https://github.com/munt/munt) | MT-32／CM 系列模型研究入口 | 模型程式授權也授權了 ROM |
| [DOSBox MIDI 設定](https://www.dosbox.com/wiki/Configuration%3AMIDI) | 介面模式與主機 MIDI 路由 | 已在真正 DOS 內完成軟體合成 |
| [DOSBox-X MPU 實作](https://dosbox-x.com/doxygen/html/mpu401_8cpp_source.html) | 研究介面模式及機器差異 | 文件快照一定對應使用者的執行檔版本 |

晶片完整暫存器表、特定 MIDI 裝置及專有樂譜格式，應另取得可用的原廠規格或以已授權資料分析。本手冊刻意不填入未核對的硬體常數。

## 權利範圍

- [智財局：方法與表達的區分](https://www.tipo.gov.tw/tw/copyright/692-15175.html)
- [智財局：軟體中文化與公開](https://www.tipo.gov.tw/tw/copyright/692-12272.html)
- [智財局：相容性還原工程與限制](https://www.tipo.gov.tw/tw/tipo1/209-21676.html)
- [美國著作權局：方法與系統](https://www.copyright.gov/circs/circ31.pdf)
- [Microsoft：字型使用及再散布](https://learn.microsoft.com/en-us/typography/fonts/font-faq)

這些是一般查核入口，不是對特定遊戲、使用者所在地或發布行為的法律結論。

## 本機研究經驗

LESSONS 的經驗來自一次實際移植、原驅動事件比對、模擬器參考、即時音訊量測與使用者回饋。這些內容屬本教材的方法整理；原始檔案與私人驗證紀錄不在本包內。不能把原實驗中的特定數值、晶片或腳本處理方式當成其他遊戲的既定結論。

MIDI／OPNA 分支是供後續研究的設計與驗證方向，沒有聲稱在該個案中已實作完成。本包的合成範例通過，只表示範例的預期判斷成立。
