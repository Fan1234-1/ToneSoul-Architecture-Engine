# VOLUME I — ENGINEERING FOUNDATION

## 1. 導言

本卷冊建立語魂系統的工程基礎，將理論中的三向量（ΔT、ΔS、ΔR）映射為具體的資料結構與流程。透過領域驅動設計（DDD）與事件溯源（Event‑Sourcing），我們將語魂系統拆分為可維護、可測試的模組。

## 2. 三向量抽象

語魂系統中的三向量表示張力（Tension）、語氣（Style）與責任（Responsibility）。為了在工程上運用，我們定義如下資料結構：

```yaml
ToneSoulVector:
  deltaT: float   # 張力變化量；取值範圍 [-1.0, 1.0]
  deltaS: float   # 語氣變化量；標準化到 [-1.0, 1.0]
  deltaR: float   # 責任權重變化量；範圍 [0.0, 1.0]
  timestamp: datetime   # 指標記錄時間
  context: string      # 可選描述上下文（例如回覆、輸入來源）
```

此向量應由系統在每次回應、指標計算或決策更新時產生，並存入 StepLedger（步驟帳冊）中。

## 3. StepLedger 與 Event‑Sourcing

為確保可追溯性，我們使用 **事件溯源（Event‑Sourcing）** 模式記錄系統的所有狀態變更。核心概念如下：

1. **事件（Event）**：系統內部或對外輸出的一個原子操作，例如「計算向量」、「生成回覆」、「完成檢查」。
2. **步驟帳冊（StepLedger）**：按時序存放事件的資料庫，每筆事件包含事件類型、發生時間、參數、產生的向量等。帳冊不直接修改狀態，而是將事件串起來重建狀態。
3. **投影（Projections）**：將帳冊中的事件映射成易於查詢的狀態，服務於讀取操作（CQRS 的 Query 部分）。

事件結構示例如下：

```yaml
Event:
  id: uuid
  type: string            # e.g. ComputeVector, GenerateResponse, VerificationResult
  payload: object         # 根據事件類型存放資料
  occurred_at: datetime
```

使用事件驅動架構可以回溯整個決策過程，支撐倫理審計與錯誤排查。

## 4. DDD 與 Clean Architecture 分層

在語魂工程實作中，我們遵循下列分層：

1. **Domain（領域層）**：定義核心商業邏輯與實體，如 ToneSoulVector、Event、DriftScore 等。領域層不依賴其他層。
2. **Use Case（應用層）**：描述使用者場景與系統規則，例如「生成回覆並計算向量」、「執行漂移檢測」。此層調用領域模型並協調其邏輯。
3. **Interface（介面層）**：提供與外界互動的入口，如 API 端點、CLI 工具等。不直接處理業務邏輯，而是呼叫 Use Case 層。
4. **Infrastructure（基礎建設）**：實作資料庫、消息佇列、第三方服務介接等，並透過依賴反轉注入到其他層。

此分層結構結合 CQRS，使讀寫責任更加明確。例如，所有寫入行為（事件產生）由 Command 使用案例處理，而查詢行為則透過預計算的投影服務。

## 5. 版本化與 Schema 管理

由於語魂系統的理論與實作均在不斷演化，我們建議對所有資料結構與 API 進行版本管理。例如，在資料表中增加 `schema_version` 欄位，或在 API URL 中加入 `/v1/` 等版本標記，以便與未來的更新兼容。

## 6. 小結

本卷冊為工程系列的基石，定義了語魂系統的核心資料結構與架構模式。後續卷冊將在此基礎上延伸，建立動態模型、責任檢查機制以及自我演化流程。