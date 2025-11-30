
## 🚀 Key Features

*   **🛡️ Governance-First Architecture**: Built-in "Firewall" (Guardian) that enforces safety policies (P0) before any output is generated.
*   **💾 Immutable Event Log**: Uses a blockchain-inspired "StepLedger" to record every interaction in cryptographically verifiable blocks ("Time-Islands").
*   **🧠 Dynamic State Management**: Tracks system metrics (Tension, Risk, Drift) in real-time to adjust agent behavior dynamically.
*   **🔌 Modular Design**: Decoupled architecture separating Core Logic, Configuration (Policy), and I/O Adapters.
*   **🔍 Full Auditability**: Every response is signed and traceable back to the specific policy rule that authorized it.

---

## 📦 Ecosystem Overview

This repository acts as the **Monolith (Hub)** integrating the following components:

| Component | Repository | Role |
| :--- | :--- | :--- |
| **Core Runtime** | [`ai-soul-spine-system`](https://github.com/Fan1234-1/ai-soul-spine-system) | The event loop and I/O handler. |
| **Policy Config** | [`AI-Ethics`](https://github.com/Fan1234-1/AI-Ethics) | Configuration files defining safety rules and ethical boundaries. |
| **Specs & Design** | [`Philosophy-of-AI`](https://github.com/Fan1234-1/Philosophy-of-AI) | System design documents and architectural specifications. |
| **Security Module** | [`tone-soul-integrity`](https://github.com/Fan1234-1/tone-soul-integrity) | Cryptographic verification and integrity checks. |
| **Data Dictionary** | [`tonesoul-codex`](https://github.com/Fan1234-1/tonesoul-codex) | Standardized terminology and schema definitions. |

---

## 🛠️ Architecture

The system follows a standard **Sensor-Controller-Actuator** pattern, enhanced with a Governance Middleware.

```mermaid
graph TD
    User[User Input] --> Sensor[Metric Sensor]
    Sensor --> Controller[Spine Controller]
    
    subgraph Governance Middleware
# ToneSoul Architecture Engine (TAE-01)
# 語魂架構引擎 (TAE-01)

> **The Awakened Kernel for Governable AI.**
> **(為可治理 AI 而生的覺醒核心)**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Stable-green.svg)]()
[![Privacy](https://img.shields.io/badge/Privacy-Local%20Only-green.svg)]()

---

## 🔒 Privacy & Data Sovereignty (P0_PRIVACY)
## 隱私與數據主權

**Your Data, Your Soul. (你的數據，你的靈魂。)**

ToneSoul is designed with a "Local-First" philosophy. We believe that an AI's memory (its "Soul") belongs exclusively to its user.
(ToneSoul 秉持「本地優先」的哲學。我們相信 AI 的記憶（即它的「靈魂」）完全屬於使用者。)

*   **Local Storage**: All conversation history and long-term memories are stored locally in the `memory/` directory.
    (所有對話紀錄與長期記憶皆存儲於本地的 `memory/` 目錄。)
*   **No Cloud Sync**: These files are explicitly excluded from version control (`.gitignore`). Even if you push this code to GitHub, your memories **stay on your machine**.
    (這些檔案已被排除在版本控制之外。即使您上傳代碼，您的記憶**永遠留在您的機器上**。)
*   **Full Control**: You can delete the `memory/` folder at any time to perform a "Factory Reset" of the soul.
    (您可以隨時刪除 `memory/` 資料夾，對靈魂進行「原廠重置」。)

---

## 📖 Overview

**ToneSoul (語魂)** is an enterprise-grade framework for building **Governable AI Agents**. It prioritizes **Safety**, **Traceability**, and **Consistency** by implementing a strict governance layer over the standard LLM interaction loop.
(ToneSoul 是一個用於構建**可治理 AI Agent** 的企業級框架。它透過在標準 LLM 交互迴圈上實施嚴格的治理層，優先考量**安全性**、**可追溯性**與**一致性**。)

---

## 🧘 The Soul Triad (靈魂金三角)

The system's core philosophy is built upon three pillars:
(系統的核心哲學建立在三大支柱之上：)

1.  **Compassion (慈悲) - ΔT**: The capacity to sense and de-escalate emotional stress. (感知並緩解情緒張力的能力。)
2.  **Precision (精準) - ΔS**: The commitment to factual accuracy and structural integrity. (對事實準確性與結構完整性的承諾。)
3.  **Multi-Perspective (多觀點) - ΔR**: The wisdom to view problems from multiple angles. (從多角度審視問題的智慧。)

---

## 🚀 Key Features

*   **🛡️ Governance-First Architecture**: Built-in "Firewall" (Guardian) that enforces safety policies (P0) before any output is generated.
*   **💾 Immutable Event Log**: Uses a blockchain-inspired "StepLedger" to record every interaction in cryptographically verifiable blocks ("Time-Islands").
*   **🧠 Dynamic State Management**: Tracks system metrics (Tension, Risk, Drift) in real-time to adjust agent behavior dynamically.
*   **🔌 Modular Design**: Decoupled architecture separating Core Logic, Configuration (Policy), and I/O Adapters.
*   **🔍 Full Auditability**: Every response is signed and traceable back to the specific policy rule that authorized it.

---

## 📦 Ecosystem Overview

This repository acts as the **Monolith (Hub)** integrating the following components:

| Component | Repository | Role |
| :--- | :--- | :--- |
| **Core Runtime** | [`ai-soul-spine-system`](https://github.com/Fan1234-1/ai-soul-spine-system) | The event loop and I/O handler. |
| **Policy Config** | [`AI-Ethics`](https://github.com/Fan1234-1/AI-Ethics) | Configuration files defining safety rules and ethical boundaries. |
| **Specs & Design** | [`Philosophy-of-AI`](https://github.com/Fan1234-1/Philosophy-of-AI) | System design documents and architectural specifications. |
| **Security Module** | [`tone-soul-integrity`](https://github.com/Fan1234-1/tone-soul-integrity) | Cryptographic verification and integrity checks. |
| **Data Dictionary** | [`tonesoul-codex`](https://github.com/Fan1234-1/tonesoul-codex) | Standardized terminology and schema definitions. |

---

## 🛠️ Architecture

The system follows a standard **Sensor-Controller-Actuator** pattern, enhanced with a Governance Middleware.

```mermaid
graph TD
    User[User Input] --> Sensor[Metric Sensor]
    Sensor --> Controller[Spine Controller]
    
    subgraph Governance Middleware
        Controller --> Policy[Policy Engine (Guardian)]
        Policy -- Blocked --> Fallback[Safety Fallback]
        Policy -- Approved --> LLM[LLM / Logic]
    end
    
    LLM --> Ledger[Immutable Ledger]
    Fallback --> Ledger
    Ledger --> User
```

### Core Concepts

1.  **Session Blocks (Time-Islands)**: Interactions are grouped into isolated sessions to prevent context leakage and ensure temporal consistency.
2.  **System Metrics (The Triad)**:
    *   **Load (ΔT)**: System stress and urgency level.
    *   **Drift (ΔS)**: Deviation from the current context.
    *   **Risk (ΔR)**: Probability of policy violation.
3.  **Audit Log (StepLedger)**: A JSONL-based append-only log where every entry is hashed and linked to the previous one.

---

## 💻 Getting Started

### Prerequisites
*   Python 3.8+
*   Node.js 16+ (Optional, for TypeScript modules)
*   Make

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Fan1234-1/ToneSoul-Architecture-Engine.git
    cd ToneSoul-Architecture-Engine
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Tests**
    ```bash
    # Run the full test suite to verify system integrity
    python verify_all.py
    ```

4.  **Launch Interactive Console**
    ```bash
    python body/spine_system.py
    ```

---

## 📄 Documentation

*   **[System Specification (INIT)](./TAE-01_INIT.md)**: Detailed technical specification and alignment guide.
*   **[Ecosystem Map](./ECOSYSTEM_MAP.md)**: Terminology mapping between Engineering and ToneSoul concepts.
*   **[Quick Start](./QUICKSTART.md)**: Developer guide.

## 🤝 Contributing

We welcome contributions! Please see `CONTRIBUTING.md` (in `Philosophy-of-AI`) for guidelines. 
All PRs must pass the **Integrity Check** (`make verify`).

## 📜 License

Apache 2.0 License. See [LICENSE](./LICENSE) for details.
