# ToneSoul Canonical Protocol

**Version:** 1.0
**Status:** Draft

This module defines the **Single Source of Truth** for data structures in the ToneSoul ecosystem. All implementations (Python, TypeScript, Rust, etc.) must adhere to these schemas to ensure interoperability and ledger integrity.

## Schemas

| Schema | Description | File |
| :--- | :--- | :--- |
| **ToneSoulTriad** | The atomic emotional state vector ($\Delta T, \Delta S, \Delta R$). | [triad.schema.json](schemas/triad.schema.json) |
| **SoulVow** | The cryptographic attestation of integrity. | [vow.schema.json](schemas/vow.schema.json) |
| **StepRecord** | The immutable ledger entry format. | [step_record.schema.json](schemas/step_record.schema.json) |

## Usage

### Python
Use `jsonschema` to validate dictionaries before persistence.
```python
import json
import jsonschema

with open('modules/protocol/schemas/step_record.schema.json') as f:
    schema = json.load(f)

jsonschema.validate(instance=record_dict, schema=schema)
```

### TypeScript
Use `ajv` or `zod` to validate objects at runtime.
```typescript
import Ajv from "ajv";
import schema from "./schemas/step_record.schema.json";

const ajv = new Ajv();
const validate = ajv.compile(schema);
const valid = validate(data);
```
