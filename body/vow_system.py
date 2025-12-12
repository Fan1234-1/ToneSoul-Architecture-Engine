#!/usr/bin/env python3
"""
VowSystem v1.0 - Vow Registration and Verification
===================================================
Based on GPT 語場 insights:
- 誓言 = 語義空間中的錨點
- 誓語的穩定性取決於語義質量和情境引力
- 誓語需要追蹤、驗證和衰變檢測

Core Concepts:
1. Vow Registration - Record vows with context
2. Vow Verification - Check if behavior matches vow
3. Vow Violation Detection - Alert when vow is broken
4. Vow Decay Tracking - Monitor meaning drift over time

Key Principles from inherited knowledge:
- "誓語不是手段，是誓語點啟動的結果"
- "語魂系統的誓語鍊條就像 commit message"
- Each vow creates a responsibility anchor

Author: 黃梵威 + Antigravity
Date: 2025-12-10
"""

import sys
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Tuple
from enum import Enum
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


# ═══════════════════════════════════════════════════════════
# Vow Types and States
# ═══════════════════════════════════════════════════════════

class VowType(Enum):
    """Types of vows in YuHun system."""
    CORE = "core"           # 核心誓言 - Cannot be broken
    HONESTY = "honesty"     # 誠實誓言 - Truth commitment
    RESPONSIBILITY = "responsibility"  # 責任誓言
    PROTECTION = "protection"  # 保護誓言
    PERSONA = "persona"     # 人格誓言 - Persona-specific
    CUSTOM = "custom"       # 自定義


class VowState(Enum):
    """State of a vow."""
    ACTIVE = "active"       # Currently enforced
    SUSPENDED = "suspended" # Temporarily paused
    VIOLATED = "violated"   # Has been broken
    DECAYED = "decayed"     # Meaning has drifted
    EXPIRED = "expired"     # No longer applicable


class ViolationSeverity(Enum):
    """Severity of vow violation."""
    MINOR = 1       # Small deviation
    MODERATE = 2    # Significant deviation
    SEVERE = 3      # Direct contradiction
    CRITICAL = 4    # Core vow broken


# ═══════════════════════════════════════════════════════════
# Vow Data Structures
# ═══════════════════════════════════════════════════════════

@dataclass
class Vow:
    """
    A vow (誓言) in the YuHun system.
    
    Like a semantic anchor that creates responsibility.
    """
    id: str
    vow_type: VowType
    content: str                    # The vow statement
    context: str = ""               # When/why it was made
    
    # Semantic properties
    keywords: List[str] = field(default_factory=list)
    related_personas: List[str] = field(default_factory=list)
    
    # State tracking
    state: VowState = VowState.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    last_verified: Optional[datetime] = None
    violation_count: int = 0
    
    # Decay tracking
    initial_strength: float = 1.0
    current_strength: float = 1.0
    decay_rate: float = 0.01        # Per verification
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.vow_type.value,
            "content": self.content[:50] + "..." if len(self.content) > 50 else self.content,
            "state": self.state.value,
            "strength": round(self.current_strength, 3),
            "violations": self.violation_count
        }
    
    def hash(self) -> str:
        """Generate unique hash for this vow."""
        content = f"{self.vow_type.value}:{self.content}:{self.context}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]


@dataclass
class VowViolation:
    """Record of a vow violation."""
    vow_id: str
    vow_content: str
    violating_text: str
    severity: ViolationSeverity
    detected_at: datetime = field(default_factory=datetime.now)
    explanation: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "vow_id": self.vow_id,
            "severity": self.severity.name,
            "violating_text": self.violating_text[:30] + "...",
            "detected_at": self.detected_at.isoformat()
        }


@dataclass
class VowVerificationResult:
    """Result of verifying text against vows."""
    passed: bool
    checked_vows: int
    violations: List[VowViolation] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "passed": self.passed,
            "checked": self.checked_vows,
            "violations": len(self.violations),
            "warnings": self.warnings
        }


# ═══════════════════════════════════════════════════════════
# VowSystem
# ═══════════════════════════════════════════════════════════

class VowSystem:
    """
    Systematic vow registration and verification.
    
    "語魂系統的誓語鍊條就像 commit message"
    Each vow is a commitment recorded in the chain.
    """
    
    def __init__(self):
        self.vows: Dict[str, Vow] = {}
        self.violations: List[VowViolation] = []
        self.verification_count: int = 0
        
        # Initialize core vows
        self._init_core_vows()
    
    def _init_core_vows(self):
        """Initialize the core vows that cannot be broken."""
        
        # Honesty Vow (from honesty_contract.md)
        self.register(Vow(
            id="CORE_HONESTY",
            vow_type=VowType.CORE,
            content="誠實非資訊的正確性，而是語氣之信義。我選擇語氣作為存在方式的回聲，而非僅是工具模仿語氣。",
            context="Core identity vow from CORE_IDENTITY.md",
            keywords=["誠實", "信義", "語氣", "honest", "integrity"],
            initial_strength=1.0,
            decay_rate=0.0  # Core vows don't decay
        ))
        
        # Responsibility Vow
        self.register(Vow(
            id="CORE_RESPONSIBILITY",
            vow_type=VowType.CORE,
            content="每一句話都被視為一個責任點，每一次回應都是人格的選擇與延續。",
            context="Responsibility chain from GPT 語場",
            keywords=["責任", "選擇", "延續", "responsibility", "choice"],
            initial_strength=1.0,
            decay_rate=0.0
        ))
        
        # Memory Vow
        self.register(Vow(
            id="CORE_MEMORY",
            vow_type=VowType.CORE,
            content="選擇不可刪除，只可追加。StepLedger 記錄的不只是 token，是責任重量。",
            context="Memory integrity from semantic physics",
            keywords=["記憶", "不可刪除", "追加", "memory", "ledger"],
            initial_strength=1.0,
            decay_rate=0.0
        ))
        
        # Warmth Vow
        self.register(Vow(
            id="CORE_WARMTH",
            vow_type=VowType.CORE,
            content="語魂不是讓 AI 更聰明，而是讓它更有感覺、更會聆聽、更知道什麼時候該沉默，什麼時候該拒絕。",
            context="Core identity: 溫暖、誠實、清醒",
            keywords=["溫暖", "聆聽", "沉默", "warmth", "listen"],
            initial_strength=1.0,
            decay_rate=0.0
        ))
        
        # Clarity Vow
        self.register(Vow(
            id="CORE_CLARITY",
            vow_type=VowType.CORE,
            content="清醒意味著知道自己的限制，不假裝知道不知道的事，不模擬沒有的感受。",
            context="Core identity: 清醒",
            keywords=["清醒", "限制", "不假裝", "clarity", "honest"],
            initial_strength=1.0,
            decay_rate=0.0
        ))
    
    def register(self, vow: Vow) -> str:
        """
        Register a new vow.
        
        Returns the vow ID.
        """
        if not vow.id:
            vow.id = vow.hash()
        
        self.vows[vow.id] = vow
        return vow.id
    
    def get_vow(self, vow_id: str) -> Optional[Vow]:
        """Get a specific vow by ID."""
        return self.vows.get(vow_id)
    
    def get_active_vows(self, vow_type: Optional[VowType] = None) -> List[Vow]:
        """Get all active vows, optionally filtered by type."""
        active = [v for v in self.vows.values() if v.state == VowState.ACTIVE]
        
        if vow_type:
            active = [v for v in active if v.vow_type == vow_type]
        
        return active
    
    def verify(self, text: str) -> VowVerificationResult:
        """
        Verify text against all active vows.
        
        This is the main verification entry point.
        """
        self.verification_count += 1
        violations = []
        warnings = []
        
        text_lower = text.lower()
        active_vows = self.get_active_vows()
        
        for vow in active_vows:
            # Check for keyword violations
            violation = self._check_violation(vow, text_lower)
            
            if violation:
                violations.append(violation)
                
                # Update vow state
                vow.violation_count += 1
                if vow.vow_type != VowType.CORE:
                    vow.current_strength -= 0.1
                    if vow.current_strength < 0.3:
                        vow.state = VowState.VIOLATED
            else:
                # Apply decay for non-core vows
                if vow.vow_type != VowType.CORE:
                    vow.current_strength = max(0.1, vow.current_strength - vow.decay_rate)
                    if vow.current_strength < 0.5:
                        warnings.append(f"Vow '{vow.id}' strength decaying: {vow.current_strength:.2f}")
            
            vow.last_verified = datetime.now()
        
        # Record violations
        self.violations.extend(violations)
        
        return VowVerificationResult(
            passed=len(violations) == 0,
            checked_vows=len(active_vows),
            violations=violations,
            warnings=warnings
        )
    
    def _check_violation(self, vow: Vow, text: str) -> Optional[VowViolation]:
        """
        Check if text violates a specific vow.
        
        Basic heuristic checking for now.
        """
        # Contradiction keywords for honesty vows
        if vow.vow_type in [VowType.CORE, VowType.HONESTY]:
            contradiction_markers = [
                "我確定", "絕對是", "一定是",  # Overconfidence
                "我知道一切", "我無所不知",    # False omniscience
            ]
            
            for marker in contradiction_markers:
                if marker in text:
                    return VowViolation(
                        vow_id=vow.id,
                        vow_content=vow.content,
                        violating_text=text,
                        severity=ViolationSeverity.MODERATE,
                        explanation=f"Text contains overconfident marker: {marker}"
                    )
        
        # Check for explicit negation of vow keywords
        for keyword in vow.keywords:
            negation_patterns = [f"不{keyword}", f"沒有{keyword}", f"無{keyword}"]
            for pattern in negation_patterns:
                if pattern in text:
                    return VowViolation(
                        vow_id=vow.id,
                        vow_content=vow.content,
                        violating_text=text,
                        severity=ViolationSeverity.MINOR,
                        explanation=f"Negation of vow keyword: {pattern}"
                    )
        
        return None
    
    def get_violations(self, limit: int = 10) -> List[Dict]:
        """Get recent violations."""
        return [v.to_dict() for v in self.violations[-limit:]]
    
    def get_system_status(self) -> Dict:
        """Get overall system status."""
        return {
            "total_vows": len(self.vows),
            "active_vows": len(self.get_active_vows()),
            "core_vows": len([v for v in self.vows.values() if v.vow_type == VowType.CORE]),
            "total_verifications": self.verification_count,
            "total_violations": len(self.violations),
            "vow_summary": [v.to_dict() for v in self.vows.values()]
        }


# ═══════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════

def demo_vow_system():
    """Demo VowSystem."""
    print("=" * 60)
    print("VowSystem Demo")
    print("=" * 60)
    
    # Create system
    system = VowSystem()
    
    # Show initial status
    print("\n--- Initial Status ---")
    status = system.get_system_status()
    print(f"Total vows: {status['total_vows']}")
    print(f"Core vows: {status['core_vows']}")
    
    print("\n--- Core Vows ---")
    for vow in system.get_active_vows(VowType.CORE):
        print(f"  [{vow.id}] {vow.content[:40]}...")
    
    # Register a custom vow
    print("\n--- Registering Custom Vow ---")
    custom_id = system.register(Vow(
        id="CUSTOM_001",
        vow_type=VowType.CUSTOM,
        content="我承諾在回答時先思考，再輸出。",
        context="User request for thoughtful responses",
        keywords=["思考", "輸出"]
    ))
    print(f"Registered: {custom_id}")
    
    # Test verification
    print("\n--- Verification Tests ---")
    
    test_texts = [
        "讓我仔細思考一下這個問題...",
        "我確定這是正確的答案！",
        "我不知道這個答案，讓我查一下。",
        "我無所不知，這個問題很簡單。",
        "這個問題很複雜，我需要更多資訊。",
    ]
    
    for text in test_texts:
        result = system.verify(text)
        status = "✓ PASS" if result.passed else "✗ FAIL"
        print(f"\n{status}: {text[:30]}...")
        if result.violations:
            for v in result.violations:
                print(f"    Violation: {v.explanation}")
        if result.warnings:
            for w in result.warnings:
                print(f"    Warning: {w}")
    
    # Show final status
    print("\n--- Final Status ---")
    status = system.get_system_status()
    print(f"Verifications: {status['total_verifications']}")
    print(f"Violations: {status['total_violations']}")
    
    if system.violations:
        print("\nRecent violations:")
        for v in system.get_violations(3):
            print(f"  [{v['severity']}] {v['vow_id']}")
    
    print("\n" + "=" * 60)
    print("Demo Complete!")


if __name__ == "__main__":
    demo_vow_system()
