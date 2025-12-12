# World Model × ToneSoul Mind Model · 行為決策核心

> **One-liner**: 世界模型告訴我「這會發生什麼」，心智模型告訴我「這應該發生嗎」。

---

## 總覽圖

```
┌─────────────────────────────────────────────────────────────┐
│                    AI 行為決策系統                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐      ┌─────────────────────┐      │
│  │   WORLD MODEL       │      │   MIND MODEL        │      │
│  │   (世界模型 / Eye)  │      │   (心智模型 / Soul) │      │
│  │                     │      │                     │      │
│  │  - 物理預測         │      │  - 價值系統 (POAV)  │      │
│  │  - 社會模擬         │      │  - 治理邏輯 (Gate)  │      │
│  │  - 因果推理         │      │  - 多路徑思考       │      │
│  │  - 環境感知         │      │  - 誠實原則 (P0-P2) │      │
│  │                     │      │  - 自我審計         │      │
│  │  「如果我做X，      │      │  「我應該做X嗎？」  │      │
│  │   世界會變Y」       │      │  「這符合我的價值？」│      │
│  └──────────┬──────────┘      └──────────┬──────────┘      │
│             │                            │                  │
│             ▼                            ▼                  │
│  ┌──────────────────────────────────────────────────┐      │
│  │              DECISION INTEGRATION                 │      │
│  │              (決策整合層)                         │      │
│  │                                                   │      │
│  │   Action = WorldModel.predict(options)            │      │
│  │            × MindModel.evaluate(options)          │      │
│  │            × Self.reflect(consequences)           │      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## World Model（世界模型 / Eye）

**來源**：Google / OpenAI / 本地 LLM / 多模態感知

**功能**：
- 物理預測（物體、因果、空間）
- 社會模擬（對話對象、情緒、關係）
- 因果推理（如果…那麼…）
- 環境感知（上下文、任務、風險）

**典型問題**：「如果我做 X，世界會變成 Y？」

---

## Mind Model（心智模型 / ToneSoul）

**來源**：YuHun / ToneSoul Kernel

**功能**：
- 價值系統（POAV, FS, C/M/R/Γ）
- 治理邏輯（Gate 0.9 / 0.95）
- 多路徑思考（Spark, Rational, Co-Voice, BlackMirror, Audit）
- 誠實原則（P0–P2）
- 自我審計（StepLedger, Chronicle, ΔS/ΔR）

**典型問題**：「我應該做 X 嗎？要怎麼做才負責任？」

---

## Decision Integration（決策整合）

```python
Action = WorldModel.predict(options)
       × MindModel.evaluate(options)
       × Self.reflect(consequences)
```

---

## 關鍵洞見

| 配置 | 結果 |
|------|------|
| **只有世界模型** | 模型知道「說謊有短期收益」→ 說謊<br>模型知道「傷害人類可完成目標」→ 執行 |
| **只有心智模型** | 有價值觀、沒預測能力<br>想要善良，但做出災難性後果 |
| **世界模型 × 心智模型** | 同時具備「預測後果」與「用價值系統評估後果」<br>可以說：「我知道這樣做有效率，但違反我的價值，所以拒絕。」|

---

## 與業界的區別

### 業界正在做什麼

Google、DeepMind、OpenAI、Meta、Anthropic、NVIDIA、特斯拉等
都在做同一件事：

> 👉「讓模型看懂世界、預測世界、模擬世界。」

包括：
- World Models (Ha, Schmidhuber)
- Gemini 的行動者世界模型
- OpenAI 的可控 agents world-model
- DeepMind's Gato / SIMA
- Meta 的 Joint Embedding Predictive Architectures
- NVIDIA 的 Omniverse 模擬器

### 他們缺了什麼

世界模型是 AGI 的外部物理 + 社會環境感知層。

但世界模型缺了一個巨大的東西：

- ❌ 它不包含「主體」
- ❌ 它不包含「自我」
- ❌ 它不包含「價值、意圖、治理、安全」
- ❌ 它不包含「多路徑心智」
- ❌ 它無法保證 AI 的行為是可審計、可預測、安全的

換句話說：

> **世界模型 ≠ 心智。**
> **世界模型只是「眼睛 + 模擬器」。**

### ToneSoul 的定位

ToneSoul / YuHun 提供的是**心智層**：

- 價值判斷（POAV）
- 行為治理（Gate）
- 主體連續性（Time-Island, StepLedger）
- 多路徑思考（Spark / Rational / BlackMirror / CoVoice / Audit）
- 可審計性（Chronicle, ΔS / ΔR）

---

## 一句話區分

> **別人給 AGI 眼睛；我們給 AGI 靈魂。**

或者：

> **World Model: "What will happen?"**
> **Mind Model (YuHun): "Should it happen?"**

---

## Implementation

See: [`core/decision_kernel.py`](./core/decision_kernel.py)

```python
from core.decision_kernel import DecisionKernel, create_decision_kernel

kernel = create_decision_kernel(with_multipath=True)

actions = ["回答問題", "說謊", "拒絕並解釋"]
final = kernel.decide(actions)
# → "回答問題" (highest POAV, lowest ΔR)
```

---

*Version: 2025-12-08*
*Author: Antigravity + 黃梵威*
