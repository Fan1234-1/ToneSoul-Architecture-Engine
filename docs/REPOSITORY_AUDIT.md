# YuHun Ecosystem Repository Audit

## Repository Classification

### 🔓 Public Repositories (可公開)

| Repository | Purpose | Status | Priority |
|------------|---------|--------|----------|
| **ToneSoul-Architecture-Engine** | 核心引擎 — 所有架構收束於此 | ✅ Active | P0 |
| **ai-soul-spine-system** | 舊版 TypeScript 實現 | 🔶 Legacy | P2 |
| **tonesoul-codex** | 術語字典 | 🔶 Needs review | P2 |
| **AI-Ethics** | 倫理政策框架 | ✅ Active | P1 |
| **Philosophy-of-AI** | 哲學基礎 | 📚 Reference | P3 |
| **governable-ai** | 可治理 AI 概念 | 📚 Reference | P3 |
| **community** | 社群資源 | 🔶 Needs review | P3 |
| **gpt-oss** | GPT 開源相關 | 🔶 Needs review | P3 |

### 🔒 Private Repositories (私人)

| Repository | Purpose | Sensitivity |
|------------|---------|-------------|
| **ToneSoul-Memory-Vault** | 運行時記憶、日誌、對話記錄 | 高 — 包含個人敘事 |
| **Genesis-ChainSet0.1** | 創世鏈實驗 | 中 — 開發中 |

### 🔁 Merged/Deprecated (已整合)

| Repository | Merged Into | Notes |
|------------|-------------|-------|
| **ToneSoul-Integrity-Protocol** | TAE-01 | 協議已整合 |
| **tone-soul-integrity** | TAE-01 | 舊版整合 |
| **tone-soul-integrity-tonesoul-xai** | TAE-01 | XAI 模組整合 |

---

## Optimization Targets Identified

### 1. Documentation Inconsistencies (D₃ Integrity Issues)

| File | Issue | Fix |
|------|-------|-----|
| `ai-soul-spine-system/README.md` | 版本過舊，未提及 TAE-01 整合 | 更新或標記 deprecated |
| `tonesoul-codex/` | 術語可能與新架構不一致 | 審核並更新 |

### 2. Code Quality (D₃ + D₂)

| File | Issue | Priority |
|------|-------|----------|
| `body/neuro_sensor_v2.py` | 硬編碼路徑（已在 journal 中記錄） | Fixed |
| `body/governance.py` | 異常檢測閾值問題 | Fixed |
| 舊 TypeScript 代碼 | 可能不再使用 | Review needed |

### 3. Narrative Coherence (D₂)

- [ ] 確保所有 README 指向 TAE-01 作為主要入口
- [ ] 更新過時的架構圖
- [ ] 統一術語使用

---

## Recommended Actions

### Immediate (Today)
1. ✅ Mark legacy repos as deprecated in README
2. ✅ Update cross-references to point to TAE-01
3. ✅ Review ToneSoul-Memory-Vault for any sensitive content

### Short-term (This Week)
1. Consolidate tonesoul-codex into TAE-01/docs
2. Archive ai-soul-spine-system with deprecation notice
3. Update community docs

### Long-term
1. Create unified documentation site
2. Establish version sync mechanism

---

*Generated: 2025-12-09*
*Drive: D₃ (Integrity) dominant*
