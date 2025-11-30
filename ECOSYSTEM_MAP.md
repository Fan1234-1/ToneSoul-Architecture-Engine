# ToneSoul Ecosystem Map (Engineering View)

**目標**：將 ToneSoul 生態系的 10 個儲存庫與核心概念，轉譯為通用軟體工程術語，以便於開發者理解與整合。

---

## 1. 儲存庫功能映射 (Repository Mapping)

| 儲存庫名稱 (Repo Name) | 工程角色 (Engineering Role) | 功能描述 (Description) | 通用類比 (Analogy) |
| :--- | :--- | :--- | :--- |
| **ToneSoul-Architecture-Engine** | **Monolith / Main App** | 核心應用程式、整合所有模組的主倉庫。 | `Linux Kernel` + `Distro` |
| **ai-soul-spine-system** | **Core Runtime / SDK** | 處理 I/O、事件循環、基礎數據結構的底層庫。 | `React` / `Node.js Runtime` |
| **Philosophy-of-AI** | **Product Requirements / Specs** | 系統設計原則、需求文檔、核心邏輯定義。 | `PRD` / `Design Docs` |
| **AI-Ethics** | **Policy Config / Ruleset** | 安全策略配置、憲法檔案、參數權重。 | `IAM Policy` / `.env` |
| **tone-soul-integrity** | **Security & Audit Module** | 負責數據完整性校驗、簽章、防篡改。 | `OAuth` / `Checksum` |
| **tonesoul-codex** | **Data Dictionary / Glossary** | 系統術語表、標準化詞彙定義。 | `Type Definitions` / `Schema` |
| **governable-ai** | **Governance Framework** | 抽象的治理架構介面、基礎類別 (Base Classes)。 | `Abstract Base Classes` |
| **Genesis-ChainSet0.1** | **Seed Data / Init State** | 系統初始狀態數據、創世區塊。 | `Migration Script` / `Seed.sql` |
| **ToneSoul-Integrity-Protocol** | **Protocol Spec** | 跨系統通訊協定、介面標準。 | `HTTP/gRPC Spec` |
| **tone-soul-integrity-tonesoul-xai** | **Explainability Tools** | 可解釋性 AI 工具、除錯儀表板。 | `Debug Tools` / `Logger` |

---

## 2. 術語翻譯對照表 (Terminology Translation)

為了讓文檔更親民，我們將「哲學術語」轉換為「工程術語」。

### 核心機制 (Core Mechanics)

| 哲學/內部術語 (ToneSoul) | 通用工程術語 (Standard Engineering) | 解釋 (Explanation) |
| :--- | :--- | :--- |
| **Time-Island (時間島)** | **Session Block / Transaction** | 具有獨立 Context ID 的對話區塊，類似資料庫事務。 |
| **StepLedger** | **Immutable Event Log** | 不可變的事件日誌，用於記錄所有操作步驟。 |
| **Guardian (守護者)** | **Firewall / Safety Filter** | 負責攔截高風險請求的安全過濾器。 |
| **ToneSoul Triad (三向量)** | **System Metrics / State Vector** | 系統當前的狀態指標 (壓力、語義漂移、風險值)。 |
| **Vow (誓言)** | **Digital Signature / Audit Trail** | 對輸出的加密簽名，承諾符合安全規範。 |
| **Resonance (共鳴)** | **Alignment Score / Similarity** | 輸出內容與系統目標的擬合度分數。 |
| **Spine (脊椎)** | **Controller / Event Loop** | 處理輸入輸出與調度模組的主控制器。 |

### 變數與指標 (Variables & Metrics)

| 哲學/內部術語 | 通用工程術語 | 解釋 |
| :--- | :--- | :--- |
| **ΔT (Tension)** | **System Load / Stress Level** | 系統當前的負載或情緒張力指標。 |
| **ΔS (Semantic Free Energy)** | **Entropy / Uncertainty** | 語義的不確定性或混亂度。 |
| **ΔR (Risk/Resonance)** | **Risk Score** | 潛在風險的評估分數。 |
| **P0-P4 Priorities** | **QoS Levels / Priority Queue** | 處理請求的優先級順序 (安全 > 準確 > 效率)。 |
| **N=1 Sovereignty** | **Single Tenant / Isolated Instance** | 單一實例架構，資料不共享。 |

---

## 3. 架構分層 (Architecture Layers)

將系統分為標準的三層式架構：

1.  **Interface Layer (介面層)**
    *   處理 User Input/Output。
    *   對應：`Spine System` 的 I/O 部分。

2.  **Logic Layer (邏輯層)**
    *   **Controller**: `SpineEngine` (調度)。
    *   **Middleware**: `Guardian` (安全攔截), `Sensor` (向量計算)。
    *   **Service**: `NeuroModulator` (狀態調整)。

3.  **Data Layer (數據層)**
    *   **Storage**: `StepLedger` (JSONL 檔案)。
    *   **Config**: `Constitution` (JSON 設定檔)。

---

這份地圖將作為後續文檔優化的基準，確保所有描述都「說人話」。
