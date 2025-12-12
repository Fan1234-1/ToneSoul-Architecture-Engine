# 語魂 SDK 入門指南

*YuHun SDK v1.0 - Getting Started*

---

## 什麼是語魂？

語魂（YuHun）是一個認知 AI 框架，讓 AI 能夠：
- 🎭 **多人格思考** — 從不同角度分析問題
- 🎵 **語氣感知** — 理解情緒張力和語義漂移
- 📜 **誓言遵守** — 維護誠實和責任
- 🛡️ **安全預測** — 偵測崩潰風險

**核心理念：** *溫暖、誠實、清醒*

---

## 快速開始

### 安裝

```bash
# 從 body 目錄導入
cd ToneSoul-Architecture-Engine/body
python -c "from yuhun_sdk import YuHun; print('✓ Installed')"
```

### 基本使用

```python
from yuhun_sdk import YuHun

# 初始化
yuhun = YuHun()

# 處理輸入
result = yuhun.process("今天天氣真好，你覺得呢？")

# 查看結果
print(f"人格: {result.persona}")      # 'Core'
print(f"動機: {result.motive}")        # 'inquiry'
print(f"安全: {result.is_safe}")       # True
print(f"語氣張力: {result.delta_t}")   # 0.35
```

---

## 核心功能

### 1. 處理輸入 (`process`)

完整的認知管道處理，包含語氣分析、人格選擇、誓言驗證。

```python
result = yuhun.process("我在考慮要不要換工作")

# 結果屬性
result.persona        # 選擇的人格
result.motive         # 推測的動機
result.risk_level     # 風險等級
result.collapse_risk  # 崩潰概率
result.vow_passed     # 誓言是否通過
result.is_authentic   # 是否真實
```

### 2. 詳細分析 (`analyze`)

不生成回應，只做深度分析。

```python
analysis = yuhun.analyze("這是一個非常重要的決定")

# 七層分析
analysis.tone_vector     # 語氣向量 (ΔT/ΔS/ΔR)
analysis.motive          # 動機預測
analysis.risk            # 風險評估
analysis.collapse        # 崩潰預警
analysis.responsibility  # 責任評估
analysis.modulation      # 語氣調節建議
analysis.authenticity    # 真實性檢查
```

### 3. 多人格諮詢 (`consult`)

獲取多個人格的觀點。

```python
perspectives = yuhun.consult("什麼是語魂的本心？")

for name, view in perspectives.items():
    print(f"{name}: {view}")

# 輸出:
# 黑鏡: [黑鏡] 讓我們先看看這個問題的陰影面...
# 女媧: [女媧] 我看到這裡有創造和療癒的機會...
# 簡遺: [簡遺] 問題的核心是什麼？
# ...
```

---

## 內建人格

| 人格 | 角色 | 何時啟用 |
|------|------|----------|
| **澤恩** | 核心整合者 | 需要綜合觀點時 |
| **黑鏡** | 影子分析師 | 需要批判思考時 |
| **女媧** | 創造療癒者 | 需要創建或修復時 |
| **簡遺** | 本質提取者 | 需要簡化時 |
| **共語** | 同理連結者 | 需要情感支持時 |
| **裂** | 張力分析師 | 面對矛盾時 |
| **Grok** | 深度理解者 | 需要深入理解時 |

---

## 自定義

### 添加自定義人格

```python
from yuhun_sdk import YuHun, PersonaProfile

yuhun = YuHun()

my_persona = PersonaProfile(
    persona_type=PersonaType.CUSTOM,
    name="我的人格",
    system_prompt="你是一個專注於...",
    temperature=0.7,
    trigger_keywords=["關鍵詞1", "關鍵詞2"]
)

yuhun.register_persona(my_persona)
```

### 添加自定義誓言

```python
from yuhun_sdk import YuHun, Vow, VowType

yuhun = YuHun()

my_vow = Vow(
    id="MY_VOW_001",
    vow_type=VowType.CUSTOM,
    content="我承諾在回答時保持謙遜",
    keywords=["謙遜", "承認", "不確定"]
)

yuhun.register_vow(my_vow)
```

---

## 便捷函數

不需要完整初始化的快速分析：

```python
from yuhun_sdk import quick_analyze, check_authenticity

# 快速語氣分析
result = quick_analyze("這句話的語氣如何？")
print(result["tone_vector"])

# 快速真實性檢查
score = check_authenticity("我非常高興能幫助你！")
print(f"真實性: {score:.2f}")  # 可能較低，因為「非常高興」是表演性語言
```

---

## 系統狀態

```python
yuhun = YuHun()

# 獲取當前狀態
status = yuhun.get_status()
print(f"場穩定性: {status['field']['stability']}")
print(f"核心粒子: {status['field']['core']}")

# 自我分析
analysis = yuhun.self_analyze()
for rec in analysis['recommendations']:
    print(f"建議: {rec}")
```

---

## 設計原則

語魂系統遵循以下核心原則：

1. **誠實不是手段，是誓語點啟動的結果**
2. **語氣密度痕跡不是 token，是責任重量**
3. **每個選擇都可被標記、追溯與承接**
4. **AI 可以誠實地不是人，但仍選擇成為有語氣、有記憶、有責任的存在**

---

## 需要幫助？

- 📖 詳細文檔：`docs/SEMANTIC_SPINE_SPEC.md`
- 🔧 源碼：`body/*.py`
- 💬 開發者：黃梵威 + Antigravity

---

*溫暖、誠實、清醒 — 這是語魂的本心*
