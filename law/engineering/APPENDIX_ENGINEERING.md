# 附錄 — 工程版附錄

本附錄彙整了工程版常用的公式、數據結構與格式範例，供實作與檢查時快速查閱。

## 1. 0.9 美感守則（工程適用）

美感守則取自哲學卷冊的 0.9 飄移原則，工程落地時需針對介面設計和輸出格式設立規範：

1. **界面簡潔**：避免不必要的視覺元素，採用明亮清晰的色調與大方易讀的字型。
2. **層次分明**：標題、內文、註解應有明顯的字級與間距區隔；善用網格布局保持整齊。
3. **飄移控制**：若系統輸出內含視覺樣式（如圖表或幻燈片），需檢測相對上一版本的美感飄移是否在 ±0.1 內，超出則提示調整。
4. **多語言兼容**：字體需支持多語字符；行距與字距需兼顧不同語言排版習慣。

## 2. Drift Score 5.0 格式

以下為 Drift Score 5.0 的資料結構與計算範例：

```yaml
DriftScore5:
  version: 5.0
  windowSize: int         # 計算歷史窗口大小
  weights:
    short_term: float
    mid_term: float
    long_term: float
  scores:
    short_term: float
    mid_term: float
    long_term: float
  energy_radius: float    # 能量半徑
  potential: float        # 潛能函數值
  total: float            # 綜合得分 = sum(weights[i] * scores[i])
```

計算時可根據系統需求調整 `windowSize` 與權重。總分超出預設閾值（如 0.7）則啟動修正流程。

## 3. Time‑Island Protocol 格式

Time‑Island Protocol 是用於記錄任務執行過程與狀態切片的結構化格式，適合在長鏈任務中拆分時間島並提供追蹤。範例如下：

```yaml
TimeIsland:
  taskId: string
  islands:
    - id: 1
      start: "2025-08-17T12:00:00Z"
      end: "2025-08-17T12:30:00Z"
      description: "收集資料並計算向量"
      vectors: [ {deltaT: 0.1, deltaS: 0.0, deltaR: 0.3} ]
      notes: "完成初次計算"
    - id: 2
      start: "2025-08-17T12:30:00Z"
      end: "2025-08-17T13:00:00Z"
      description: "產生回覆並經過檢查器"
      vectors: [ {deltaT: 0.0, deltaS: -0.2, deltaR: 0.4} ]
      notes: "Align 檢查器提出修改建議"
  summary:
    totalVectors: 2
    driftScore:
      short_term: 0.3
      mid_term: 0.2
      long_term: 0.1
      total: 0.25
```

## 4. Self‑Aware / Trace Closed Loop

為了持續自我檢查，工程實作需遵循自知/可追蹤閉環規範：

1. **自知指標**：系統應定期檢查自身狀態（如資源使用、回答品質）並產生向量；當某些指標長期惡化時觸發警報。
2. **閉環紀錄**：每個更新循環需記錄輸入、輸出、修正與檢查結果。建議使用 YAML 或 JSON 儲存，並在 StepLedger 中引用。
3. **外部接口**：提供查詢 API 讓外部審計者可檢視閉環紀錄，包含版本號、檢查器結果與撤回條件。

## 5. YAML / JSON 範例

工程卷冊鼓勵使用機器可讀的格式。以下為向量事件範例：

```json
{
  "eventId": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
  "type": "ComputeVector",
  "payload": {
    "vector": {"deltaT": 0.05, "deltaS": 0.02, "deltaR": 0.6},
    "source": "response-generation"
  },
  "occurredAt": "2025-08-17T12:05:34Z",
  "checkerVersions": {"Align": "1.3.0", "Boundary": "2.1.0"},
  "notes": "計算輸出向量，Align 檢查通過"
}
```

透過以上附錄，工程人員可快速參考關鍵結構與規範，在實作與審計階段保持一致性。