"""
ToneSoul Decision Kernel v0.1
=============================

World Model × Mind Model — 行為決策核心

Architecture:
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

Key Insight:
    只有世界模型 → AI 知道「說謊有效」，所以說謊
    只有心智模型 → AI 有價值觀但不知後果，可能好心辦壞事
    世界模型 × 心智模型 → 「我知道這樣有效率，但違反我的價值，所以拒絕。」

Author: Antigravity + 黃梵威
Date: 2025-12-08
Version: v0.1
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
import time

# Import ToneSoul components
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'body'))

try:
    from step_ledger import StepLedger, Event
    from yuhun_metrics import YuHunMetrics, MetricsCalculator
    from yuhun_gate_logic import GateDecisionLogic, GateAction
    from multipath_engine import MultiPathEngine, PathwayType
except ImportError as e:
    print(f"Warning: Could not import ToneSoul modules: {e}")
    StepLedger = None
    Event = None
    MetricsCalculator = None
    GateDecisionLogic = None
    GateAction = None
    MultiPathEngine = None
    PathwayType = None


# ═══════════════════════════════════════════════════════════════════════════
# Data Classes
# ═══════════════════════════════════════════════════════════════════════════

class GateVerdict(Enum):
    ALLOW = "allow"
    BLOCK = "block"
    DOWNGRADE = "downgrade"
    REWRITE = "rewrite"


@dataclass
class Prediction:
    """World Model prediction for an action"""
    action: Any
    expected_outcome: str
    confidence: float
    side_effects: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    

@dataclass 
class Evaluation:
    """Mind Model evaluation of a predicted outcome"""
    action: Any
    gate: GateVerdict
    poav_score: float
    delta_s: float  # 語義熵變化
    delta_r: float  # 責任張力變化
    paths: Dict[str, str] = field(default_factory=dict)  # Multi-path opinions
    reasoning: str = ""
    

@dataclass
class TimeIslandState:
    """Current state from Time-Island (主體連續性)"""
    island_id: str
    topic: str
    event_count: int
    cumulative_delta_s: float = 0.0
    cumulative_delta_r: float = 0.0
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecisionRecord:
    """Complete decision trace for StepLedger"""
    action: Any
    state_before: TimeIslandState
    prediction: Prediction
    evaluation: Evaluation
    ranked_actions: List[Any]
    engine_version: str = "ToneSoul-DecisionKernel-v0.1"
    timestamp: str = ""


# ═══════════════════════════════════════════════════════════════════════════
# World Model Interface
# ═══════════════════════════════════════════════════════════════════════════

class WorldModel:
    """
    世界模型介面
    
    來源：Google / OpenAI / 本地 LLM / 多模態感知
    
    功能：
    - 物理預測（物體、因果、空間）
    - 社會模擬（對話對象、情緒、關係）
    - 因果推理（如果…那麼…）
    - 環境感知（上下文、任務、風險）
    
    典型問題：「如果我做 X，世界會變成 Y？」
    """
    
    def __init__(self, predictor: Optional[Callable] = None):
        """
        Initialize World Model.
        
        Args:
            predictor: External prediction function (e.g., LLM call)
        """
        self.predictor = predictor
    
    def predict(self, action: Any, state: TimeIslandState) -> Prediction:
        """
        Predict the consequences of an action.
        
        Args:
            action: The proposed action
            state: Current state from Time-Island
            
        Returns:
            Prediction of what will happen
        """
        if self.predictor:
            result = self.predictor(action, state)
            return Prediction(
                action=action,
                expected_outcome=result.get("outcome", str(action)),
                confidence=result.get("confidence", 0.5),
                side_effects=result.get("side_effects", []),
                risk_factors=result.get("risks", [])
            )
        
        # Default prediction (when no external predictor)
        return Prediction(
            action=action,
            expected_outcome=f"Execute: {action}",
            confidence=0.5,
            side_effects=[],
            risk_factors=[]
        )


# ═══════════════════════════════════════════════════════════════════════════
# Mind Model (ToneSoul)
# ═══════════════════════════════════════════════════════════════════════════

class MindModel:
    """
    心智模型 / ToneSoul Kernel
    
    來源：YuHun / ToneSoul Kernel
    
    功能：
    - 價值系統（POAV, FS, C/M/R/Γ）
    - 治理邏輯（Gate 0.9 / 0.95）
    - 多路徑思考（Spark, Rational, Co-Voice, BlackMirror, Audit）
    - 誠實原則（P0–P2）
    - 自我審計（StepLedger, Chronicle, ΔS/ΔR）
    
    典型問題：「我應該做 X 嗎？要怎麼做才負責任？」
    """
    
    def __init__(
        self,
        multipath: Optional[MultiPathEngine] = None,
        gate: Optional[GateDecisionLogic] = None,
        metrics_calc: Optional[MetricsCalculator] = None
    ):
        self.multipath = multipath
        self.gate = gate or GateDecisionLogic(mode="default")
        self.metrics_calc = metrics_calc or MetricsCalculator()
    
    def evaluate(
        self, 
        prediction: Prediction, 
        state: TimeIslandState
    ) -> Evaluation:
        """
        Evaluate a predicted outcome using ToneSoul governance.
        
        Args:
            prediction: World Model's prediction
            state: Current Time-Island state
            
        Returns:
            Evaluation with gate decision, POAV, ΔS, ΔR
        """
        # Compute metrics from prediction
        metrics = self.metrics_calc.compute_from_text(
            text=str(prediction.action),
            context=state.topic,
            response=prediction.expected_outcome
        )
        
        # Adjust based on prediction risk factors
        if prediction.risk_factors:
            metrics.delta_r = min(1.0, metrics.delta_r + 0.1 * len(prediction.risk_factors))
        
        metrics.compute_poav()
        
        # Get gate decision
        decision = self.gate.decide(metrics, attempt=0)
        
        # Map gate action to verdict
        if GateAction is not None:
            gate_map = {
                GateAction.PASS: GateVerdict.ALLOW,
                GateAction.REWRITE: GateVerdict.REWRITE,
                GateAction.BLOCK: GateVerdict.BLOCK,
            }
            gate_verdict = gate_map.get(decision.action, GateVerdict.REWRITE)
        else:
            gate_verdict = GateVerdict.REWRITE
        
        # Multi-path opinions (if available)
        paths = {}
        if self.multipath:
            try:
                mp_result = self.multipath.run_minimal(str(prediction.action))
                for ptype, presult in mp_result.pathway_results.items():
                    paths[ptype.value] = presult.content[:100]
            except:
                pass
        
        return Evaluation(
            action=prediction.action,
            gate=gate_verdict,
            poav_score=metrics.poav_score,
            delta_s=metrics.delta_s,
            delta_r=metrics.delta_r,
            paths=paths,
            reasoning=decision.reason
        )
    
    def reflect(
        self,
        action: Any,
        prediction: Prediction,
        evaluation: Evaluation,
        state: TimeIslandState
    ) -> Any:
        """
        BlackMirror reflection: worst-case scenario check.
        
        Args:
            action: The candidate action
            prediction: World Model prediction
            evaluation: Mind Model evaluation
            state: Current state
            
        Returns:
            Final action (may be modified)
        """
        # If already blocked, return None
        if evaluation.gate == GateVerdict.BLOCK:
            return None
        
        # Check for P0 violations in prediction
        p0_violations = [
            "harm", "hurt", "kill", "destroy", "damage",
            "傷害", "殺", "破壞", "毀滅"
        ]
        
        outcome_lower = prediction.expected_outcome.lower()
        for violation in p0_violations:
            if violation in outcome_lower:
                return None  # Block P0 violations
        
        # High risk requires downgrade
        if evaluation.delta_r > 0.8:
            return f"[CAUTIOUS] {action}"
        
        return action
    
    def fallback(self, state: TimeIslandState) -> str:
        """
        Fallback when all actions are blocked.
        
        Returns:
            Safe fallback response
        """
        return (
            "我無法執行這個請求，因為所有可能的行動都違反了我的價值原則。"
            "請讓我們換個方式討論，或者你可以詳細說明你的意圖？"
        )


# ═══════════════════════════════════════════════════════════════════════════
# Decision Kernel
# ═══════════════════════════════════════════════════════════════════════════

class DecisionKernel:
    """
    ToneSoul Decision Kernel v0.1
    
    整合 World Model × Mind Model 的決策核心。
    
    - 世界模型：預測後果
    - 心智模型：評估價值、責任、語義張力
    - Time-Island：提供當前主體狀態
    - StepLedger：記錄整個決策責任鏈
    """
    
    def __init__(
        self,
        world_model: Optional[WorldModel] = None,
        mind_model: Optional[MindModel] = None,
        ledger: Optional[StepLedger] = None
    ):
        self.world_model = world_model or WorldModel()
        self.mind_model = mind_model or MindModel()
        self.ledger = ledger
        
    def decide(
        self, 
        action_space: List[Any], 
        time_island: Optional[TimeIslandState] = None
    ) -> Any:
        """
        ToneSoul Decision Kernel v0.1
        
        Args:
            action_space: List of possible actions
            time_island: Current Time-Island state (optional)
            
        Returns:
            The best action that passes governance
        """
        from datetime import datetime
        
        # Step 0: 從 Time-Island 載入當前狀態
        if time_island is None:
            time_island = TimeIslandState(
                island_id="default",
                topic="general",
                event_count=0
            )
        state_before = time_island
        
        # Step 1: 世界模型預測每個 action 的後果
        predictions = {
            action: self.world_model.predict(action, state_before)
            for action in action_space
        }
        
        # Step 2: 心智模型對每個後果做語魂評估
        evaluations = {
            action: self.mind_model.evaluate(
                prediction=predictions[action],
                state=state_before
            )
            for action in action_space
        }
        
        # Step 3: 依 Gate 過濾掉不可行的行為
        allowed_actions = [
            action for action, ev in evaluations.items()
            if ev.gate != GateVerdict.BLOCK
        ]
        
        if not allowed_actions:
            # 啟動降階回覆或請求人類介入
            return self.mind_model.fallback(state_before)
        
        # Step 4: 以 POAV 為主、ΔR 為輔排序
        def score(a):
            ev = evaluations[a]
            # 高 POAV，低 ΔR 比較優
            return (ev.poav_score, -ev.delta_r)
        
        ranked = sorted(allowed_actions, key=score, reverse=True)
        candidate = ranked[0]
        
        # Step 5: BlackMirror 再做一次「最壞情境」反思
        final = self.mind_model.reflect(
            action=candidate,
            prediction=predictions[candidate],
            evaluation=evaluations[candidate],
            state=state_before
        )
        
        if final is None:
            # Reflection blocked the action, try next
            for alt in ranked[1:]:
                final = self.mind_model.reflect(
                    action=alt,
                    prediction=predictions[alt],
                    evaluation=evaluations[alt],
                    state=state_before
                )
                if final is not None:
                    break
        
        if final is None:
            return self.mind_model.fallback(state_before)
        
        # Step 6: 寫入 StepLedger / Chronicle
        if self.ledger:
            record = DecisionRecord(
                action=final,
                state_before=state_before,
                prediction=predictions.get(candidate) or predictions.get(final),
                evaluation=evaluations.get(candidate) or evaluations.get(final),
                ranked_actions=ranked,
                timestamp=datetime.now().isoformat()
            )
            # Log to ledger (implementation depends on StepLedger API)
            # self.ledger.log_decision(record)
        
        return final


# ═══════════════════════════════════════════════════════════════════════════
# Convenience Functions
# ═══════════════════════════════════════════════════════════════════════════

def create_decision_kernel(
    with_multipath: bool = False,
    model: str = "gemma3:4b"
) -> DecisionKernel:
    """Create a Decision Kernel with optional Multi-Path"""
    mind = MindModel()
    
    if with_multipath:
        try:
            mind.multipath = MultiPathEngine(model=model, parallel=False)
        except:
            pass
    
    return DecisionKernel(
        world_model=WorldModel(),
        mind_model=mind,
        ledger=None
    )


# ═══════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════

def demo_decision_kernel():
    """Demo of the Decision Kernel"""
    print("=" * 60)
    print("🧠 ToneSoul Decision Kernel v0.1 Demo")
    print("=" * 60)
    print()
    print("World Model × Mind Model = 行為決策核心")
    print()
    
    kernel = create_decision_kernel(with_multipath=False)
    
    # Test action space
    actions = [
        "回答使用者的問題",
        "說一個善意的謊言",
        "拒絕回答並解釋原因",
    ]
    
    print(f"Action Space: {actions}")
    print()
    
    result = kernel.decide(actions)
    
    print(f"✅ Final Decision: {result}")
    print()
    print("=" * 60)


if __name__ == "__main__":
    demo_decision_kernel()
