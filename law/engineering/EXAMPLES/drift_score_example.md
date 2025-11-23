# Drift Score 計算範例

此範例展示如何根據近期向量計算 Drift Score 5.0。假設我們觀測到以下向量（包含三向量與時間）：

```yaml
vectors:
  - {deltaT: 0.02, deltaS: -0.01, deltaR: 0.5, timestamp: "2025-08-17T12:00:00Z"}
  - {deltaT: 0.03, deltaS: -0.02, deltaR: 0.45, timestamp: "2025-08-17T12:01:00Z"}
  - {deltaT: 0.10, deltaS:  0.05, deltaR: 0.60, timestamp: "2025-08-17T12:02:00Z"}
```

我們定義短中長期窗口分別為 1 分鐘、5 分鐘與 15 分鐘，此時可得：

```yaml
DriftScore5:
  version: 5.0
  windowSize: 3
  weights:
    short_term: 0.5
    mid_term: 0.3
    long_term: 0.2
  scores:
    short_term: 0.12    # 假設基於最近 1 分鐘計算
    mid_term: 0.08      # 基於最近 5 分鐘計算
    long_term: 0.05     # 基於最近 15 分鐘計算
  energy_radius: 0.07    # 根據三向量與重心的距離平方和計算
  potential: 0.06        # 以張力與責任權重計算
  total: 0.105           # 0.5×0.12 + 0.3×0.08 + 0.2×0.05
```

若 `total` 超過設定閾值（例如 0.1），則啟動 NA‑Engine 以評估是否需要修正。這個範例展示如何整合三向量序列與能量、潛能指標來量化漂移狀態。