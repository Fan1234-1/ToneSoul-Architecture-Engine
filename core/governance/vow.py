import json
import hashlib
import time
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class VowCore:
    subject: str
    commitment: str
    scope: str
    metrics: Dict[str, Any] = field(default_factory=lambda: {
        "target_value": 0.0,
        "tolerance_range": [0.0, 1.0],
        "measurement_method": "default"
    })

@dataclass
class Signatories:
    primary: str
    witnesses: List[str]

@dataclass
class TemporalBinding:
    effective_from: str
    effective_until: str = "forever"
    check_interval: str = "daily"

@dataclass
class Enforcement:
    compliance_gate_scores: Dict[str, float]
    breach_consequence: str = "WARN"
    verification_method: str = "automated"

@dataclass
class Signature:
    algorithm: str = "SHA-256"
    timestamp: str = ""
    digest: str = ""
    immutable_flag: bool = True

@dataclass
class CrossRefs:
    audit_trail_id: str
    philosophy_principle: str = ""
    policy_binding: str = ""

@dataclass
class VowObject:
    """
    Implementation of VowObject Specification v1.0 from ToneSoul Codex.
    """
    vow_id: str
    created_at: str
    signatories: Signatories
    vow_core: VowCore
    temporal_binding: TemporalBinding
    enforcement: Enforcement
    signature: Signature
    cross_refs: CrossRefs

    def sign(self, secret_key: str = ""):
        """Generates SHA-256 signature for the VowObject."""
        self.signature.timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Create a canonical string representation for signing
        # We exclude the signature field itself to avoid recursion
        data_to_sign = {
            "vow_id": self.vow_id,
            "created_at": self.created_at,
            "signatories": asdict(self.signatories),
            "vow_core": asdict(self.vow_core),
            "temporal_binding": asdict(self.temporal_binding),
            "enforcement": asdict(self.enforcement),
            "cross_refs": asdict(self.cross_refs),
            "salt": secret_key
        }
        
        canonical_str = json.dumps(data_to_sign, sort_keys=True)
        self.signature.digest = hashlib.sha256(canonical_str.encode('utf-8')).hexdigest()
        self.signature.immutable_flag = True

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)

    @classmethod
    def create_default(cls, vow_id: str, subject: str, commitment: str, agent_name: str = "ToneSoul-Spine"):
        """Factory method for creating a standard VowObject."""
        now = datetime.utcnow().isoformat() + "Z"
        return cls(
            vow_id=vow_id,
            created_at=now,
            signatories=Signatories(primary=agent_name, witnesses=["ToneSoul-Codex"]),
            vow_core=VowCore(subject=subject, commitment=commitment, scope="global"),
            temporal_binding=TemporalBinding(effective_from=now),
            enforcement=Enforcement(compliance_gate_scores={"FS": 1.0, "POAV": 1.0, "SSI": 1.0, "LC": 1.0}),
            signature=Signature(),
            cross_refs=CrossRefs(audit_trail_id=vow_id.split("-VOW-")[0] if "-VOW-" in vow_id else "GENESIS")
        )
