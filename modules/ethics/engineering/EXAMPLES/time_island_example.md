# Time‑Island Protocol 輸出範例

Time‑Island Protocol 將長鏈任務拆分為幾個時間段（島），以便追蹤進度與狀態。以下為範例：

```yaml
TimeIsland:
  taskId: "analysis-20250817"
  islands:
    - id: 1
      start: "2025-08-17T10:00:00Z"
      end: "2025-08-17T10:15:00Z"
      description: "蒐集資料並建立初步向量"
      actions:
        - "查詢外部文獻"
        - "提取關鍵概念"
      vectors:
        - {deltaT: 0.04, deltaS: -0.03, deltaR: 0.5}
      notes: "資料品質佳，Align 檢查通過"
    - id: 2
      start: "2025-08-17T10:15:00Z"
      end: "2025-08-17T10:30:00Z"
      description: "計算 Drift Score 並生成報告"
      actions:
        - "計算 EMA 與能量半徑"
        - "生成 POAV 報告選項"
      vectors:
        - {deltaT: 0.02, deltaS: 0.01, deltaR: 0.45}
      notes: "短期漂移增加，需要注意"
  summary:
    totalIslands: 2
    finalVector: {deltaT: 0.02, deltaS: 0.01, deltaR: 0.45}
    driftScore:
      short_term: 0.08
      mid_term: 0.06
      long_term: 0.04
      total: 0.068
    nextAction: "等待用戶確認報告後進行修正"
```

在實作中，Time‑Island Protocol 可串接 StepLedger，使長鏈任務的每段行為皆有跡可循。