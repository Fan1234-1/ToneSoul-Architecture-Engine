# ToneSoul Integrity Protocol (The Bridge)

**Inter-System Communication Standards.**

This repository defines the **Wire Format** and **Communication Protocols** for ToneSoul instances. It ensures that a memory block created by a Python Spine can be read by a TypeScript Spine.

---

## 🌐 Protocol Specs

### 1. Time-Island Schema (v2.0)
The standard format for exchanging session data.

```json
{
  "island_id": "UUID-v4",
  "created_at": 1732400000.0,
  "status": "CLOSED",
  "context_hash": "SHA256_HASH",
  "island_hash": "SHA256_HASH",
  "steps": [
    {
      "record_id": "UUID-v4",
      "user_input": "String",
      "triad": {"delta_t": 0.5, "delta_s": 0.1, "delta_r": 0.0},
      "decision": {"allowed": true, "mode": "RESONANCE"},
      "hash": "SHA256_HASH"
    }
  ]
}
```

### 2. Resonance Handshake
*   Protocol for two ToneSoul instances to establish trust.
*   Exchange `PersonaID` and `GenesisBlock_Hash`.
*   Verify `P0_IDENTITY` compatibility.

---

## 📂 Structure
*   `schemas/`: JSON Schema definitions.
*   `protobuf/`: (Future) gRPC definitions.

## 📜 License

Apache 2.0
