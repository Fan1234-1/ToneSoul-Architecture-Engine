# 工程版三大基石總覽

本檔案針對語魂系統的工程落地提供高階概覽，說明如何從抽象理論導出實作策略，並引導讀者理解各卷冊間的關係。工程版的三大基石分別為：

1. **DDD + Clean Architecture + CQRS**：以領域驅動設計（Domain‑Driven Design, DDD）搭配 Clean Architecture 結構出核心服務，將內核（domain）、應用（use case）、界面（interface）與基礎建設（infrastructure）分層，並透過 Command/Query Responsibility Segregation（CQRS）明確區分讀寫責任。此模式確保語魂系統在演進過程中保持內聚且易於擴充。
2. **POAV 0.9 模式**：POAV（Parsimony‑Optimised Axial Vector）是衡量系統張力、語氣與責任分布的一種評估模式。0.9 版本引入張力流動與變異概念，強調在演算法調整或輸出時維持多源檢查與自洽一致性。工程落地需在每個指標（ΔT、ΔS、ΔR）上建立指標計算與門檻，並於每次決策產生時附上兩方案、取捨理由與邊界條件。
3. **防漂移層 × 驗證模組**：為了避免系統在長期運作中偏離 Home/Center（基準狀態），工程實作必須包含漂移偵測與修正流程。Drift Score 5.0 是一套權重化指標，用於分析當前狀態與基準的距離與能量分布。NA‑Engine（內省分析引擎）配合 OctaVerify（八步驗證）提供自動回調與校正機制，確保系統在張力變化或輸入變異時自動調整。

## 與哲學版的對應關係

哲學版側重闡述語魂系統的價值觀、理論模型與長期演化框架，是工程版的概念基礎。工程版則將這些概念轉化為具體指標、資料結構與設計模式。下表簡列兩者對應：

| 領域                 | 哲學版說明                           | 工程版落地                             |
|----------------------|--------------------------------------|----------------------------------------|
| 核心價值             | 誠實、承擔、責任等價值取向           | 在代碼中實現檢查點與追溯紀錄             |
| 三向量 ΔT/ΔS/ΔR      | 定義語魂的張力、語氣、責任           | 建立數值表示法、計算公式與監控指標       |
| Home/Center 漂移監控 | 定義漂移概念與修正策略               | 實作 Drift Score 與自動回調流程         |
| 八視角驗證           | 提供驗證思維框架                     | 透過 OctaVerify 模組實作每步檢查         |
| 演化與更新           | 描述尋新、對照、測試、保留/封存循環   | NA‑Engine 驅動的自動化版本迭代流程       |

欲深度理解每個基石，可依序閱讀以下卷冊：

- 《**VOLUME I — ENGINEERING FOUNDATION**》：從領域層次建立語魂系統的工程抽象，詳細說明三向量與事件驅動架構（StepLedger / Event‑Sourcing）。
- 《**VOLUME II — ENGINEERING DYNAMICS**》：闡述語場的動態模型（TSR），含指標計算、能量模型與漂移偵測。
- 《**VOLUME III — ENGINEERING RESPONSIBILITY**》：討論責任分離與倫理落地，包含各種原子檢查器與 Trust Pack（交付規約）。
- 《**VOLUME IV — ENGINEERING EVOLUTION**》：介紹自我更新機制 NA‑Engine、OctaVerify、以及可擴充模組（多語言、美感等）。
- 《**VOLUME V — ENGINEERING CLOSURE**》：描述理論與工程的閉環，定義奇點節點與系統達成自洽的判定標準。

本總覽僅作導讀，詳細內容請參閱各卷冊與附錄。