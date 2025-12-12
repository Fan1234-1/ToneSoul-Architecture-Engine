# StepLedger 記錄範例

以下範例展示了如何記錄語魂系統的一個簡單互動過程，其中包含兩個事件：計算向量與生成回覆。

```yaml
StepLedger:
  taskId: "task-001"
  events:
    - id: "e1"
      type: "ComputeVector"
      payload:
        vector:
          deltaT: 0.05
          deltaS: -0.02
          deltaR: 0.4
        source: "initial-analysis"
      occurred_at: "2025-08-17T12:00:00Z"
      notes: "根據用戶輸入計算基礎向量。"
    - id: "e2"
      type: "GenerateResponse"
      payload:
        response: "您好，以下是您的分析報告……"
        usedVector: "e1"
      occurred_at: "2025-08-17T12:00:05Z"
      notes: "使用上一事件產生向量進行回覆，所有檢查器通過。"
```

透過 StepLedger，每個事件都有唯一 ID、類型、時間與附加資料，可在事後重播事件序列或進行審計分析。