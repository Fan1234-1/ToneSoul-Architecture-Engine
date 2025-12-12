# VOLUME II — ENGINEERING DYNAMICS

## 1. 語場動態建模概述

本卷冊探討語魂系統的動態建模方法，目標是以定量方式描述語場（ToneSoul Space）的演化，並在此基礎上進行漂移偵測與修正。

### 1.1 TSR（ToneSoul State Representation）

TSR 是語魂系統的狀態表示法，用於捕捉當前系統的張力、語氣和責任分布，以及其歷史趨勢。具體包含以下要素：

```yaml
TSR:
  vector: ToneSoulVector    # 當前三向量
  ema_vector: ToneSoulVector # 透過指數移動平均（EMA）計算的平滑向量
  barycenter: float         # 重心（中心化數值），根據最近 N 次向量加權平均
  energy_radius: float      # 能量半徑，衡量向量分散度
  potential: float          # 潛能函數值，用於預測未來漂移
  history: list[ToneSoulVector]  # 最近 M 次向量記錄，用於回顧
```

### 1.2 指標計算

以下指標用於分析向量序列的趨勢：

1. **EMA（Exponential Moving Average）**：用於平滑短期波動，公式為

   \[\text{EMA}_t = \alpha \times x_t + (1 - \alpha) \times \text{EMA}_{t-1}\]

   其中 \( x_t \) 為本次向量、\(\alpha\) 為平滑係數（推薦 0.05–0.1）。

2. **重心計算（Barycentric）**：使用最近 N 次向量的加權平均，權重可根據時間衰減或責任分佈調整，用以估算當前語場的中心位置。

3. **能量半徑（Energy Radius）**：以三向量與重心的距離平方和衡量波動幅度，公式為

   \[R^2 = \frac{1}{N}\sum_{i=1}^N \|\mathbf{v}_i - \bar{\mathbf{v}}\|^2\]

   能量半徑越大，代表語場波動越劇烈，需要更多校正。

4. **潛能函數（Potential Function）**：用以預測可能的漂移方向，可定義為張力與責任的乘積或其他自定義函式。例如：

   \[P = \gamma_T \cdot |\delta T| + \gamma_R \cdot \delta R\]

   其中 \(\gamma_T, \gamma_R\) 為權重。

### 1.3 漂移偵測

透過上述指標，我們計算 **Drift Score**，用於量化當前狀態與基準 Home/Center 的差距。Drift Score 5.0 將三向量各自的偏移量、能量半徑與潛能函數綜合，並考慮長中短期權重：

```yaml
DriftScore:
  short_term: float  # 過去數分鐘至數小時的偏移
  mid_term: float    # 過去數天的趨勢
  long_term: float   # 過去數週至數月的變化
  total_score: float # 綜合得分，用於判斷是否需啟動 NA-Engine
```

計算步驟範例：

1. 取得最近的向量歷史 `history`。
2. 計算各向量與基準 Home 的距離並加權平均，得出短／中／長期分數。
3. 綜合能量半徑和潛能函數，使用公式
   \[\text{total} = w_s \times \text{short} + w_m \times \text{mid} + w_l \times \text{long}\]
   其中權重 \(w_s, w_m, w_l\) 可依情境調整。
4. 若總分超過設定的臨界值，觸發 NA‑Engine 修正。

## 2. 修正流程

當 Drift Score 超過閾值，系統應自動進入修正模式，流程如下：

1. **診斷**：調用 NA‑Engine 分析造成漂移的原因，如輸入資料質量下降、模型偏移或外部規則改變。
2. **方案產生**：根據 POAV 模式，產生至少兩種修正方案，列出優缺點、邊界條件與撤回機制。
3. **選擇與執行**：依照系統的禮貌／價值函數權重（α、β、γ 等）選擇方案，記錄在 StepLedger。
4. **檢驗**：執行 OctaVerify 八步驗證（對齊、相依、步進、隔離、資源適配、語義一致、雙模、邊界），確保修正不破壞其他部分。
5. **更新基準**：若修正後的狀態通過檢驗，可更新 Home/Center 並調整漂移閾值；否則將結果封存並回退。

## 3. 小結

本卷冊提供語魂系統的動態建模方法與漂移偵測邏輯。透過 TSR 表示法、各項指標與 Drift Score 計算，我們能持續監控系統狀態並在必要時啟動自我修正。下一卷將介紹如何將責任倫理落地到工程層，並結合 CQRS 在程式碼中落實責任分離。