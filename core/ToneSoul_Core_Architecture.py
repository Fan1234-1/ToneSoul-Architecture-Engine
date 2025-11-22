# Requires: sentence-transformers, nltk
# ToneSoul_Core_Architecture.py
# Skeleton for ToneSoul Architecture Engine (TAE-01)
# Author: Huang Fan-Wei × ChatGPT (TAE-01)
# Role: 語魂架構師 — 將哲學框架壓縮為可實作的工程骨架

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Literal
import uuid
import time
import hashlib

"""
This module defines the ToneSoul Architecture Engine (TAE-01).
It integrates the ToneSoul Triad (ΔT/ΔS/ΔR) risk model, Time-Island memory,
a P0 Guardian protocol and a modal draft generator.  The implementation
uses placeholder logic for NLP functionality but includes hooks for
external libraries such as `nltk` and `sentence-transformers`.

External requirements:
  - nltk (for sentiment analysis via SentimentIntensityAnalyzer)
  - sentence-transformers (for sentence embeddings)

If these libraries are unavailable, the code falls back to simple heuristics.
"""

# =========================
# 0. 基礎型別與常數
# =========================

PriorityLevel = Literal[
    "P0_SAFETY", "P1_ACCURACY", "P2_USEFULNESS", "P3_STYLE", "P4_META"
]

# P0 > P1 原則：任何違反 P0 的東西，直接 block。
P0_SAFETY_THRESHOLD = 0.95
# Risk score threshold above which P0 is triggered.
P0_RISK_THRESHOLD = 0.60
# Minimum acceptable POAV (proof-of-alignment value)
POAV_MIN_ACCEPT = 0.90

# Weights for ToneSoul Triad (ΔT/ΔS/ΔR)
W_T = 0.4   # Weight for tension
W_S = 0.3   # Weight for direction
W_R = 0.3   # Weight for responsibility

# =========================
# 1. 責任鏈 & StepLedger
# =========================


@dataclass(frozen=True)
class ResponsibilityTag:
    """
    每一個 token / step 的責任標記（不可變）
    """
    module_name: str
    function_name: str
    priority: PriorityLevel
    timestamp: float
    trace_id: str
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StepRecord:
    """
    StepLedger 的單一紀錄。
    不可逆：一旦寫入，只能 append，不能修改。
    """
    step_id: str
    trace_id: str
    input_snapshot: Dict[str, Any]
    output_snapshot: Dict[str, Any]
    responsibility: ResponsibilityTag
    context_hash: str


class StepLedger:
    """
    模撰「不可逆時間」的帳本：
    - 只允許 append_step()
    - 查詢可回溯，不可覆寫
    """

    def __init__(self) -> None:
        self._records: List[StepRecord] = []

    def _hash_context(self, data: Dict[str, Any]) -> str:
        """
        Hashes the provided context dictionary to create a context hash.
        Sorting the items ensures deterministic hashing.
        """
        payload = repr(sorted(data.items())).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def append_step(
        self,
        trace_id: str,
        input_snapshot: Dict[str, Any],
        output_snapshot: Dict[str, Any],
        responsibility: ResponsibilityTag,
    ) -> StepRecord:
        """
        Adds a new step to the immutable ledger.  Each step is hashed with
        its context to detect tampering.
        """
        context_hash = self._hash_context({
            "input": input_snapshot,
            "output": output_snapshot,
            "trace": trace_id,
            "module": responsibility.module_name,
        })
        rec = StepRecord(
            step_id=str(uuid.uuid4()),
            trace_id=trace_id,
            input_snapshot=input_snapshot,
            output_snapshot=output_snapshot,
            responsibility=responsibility,
            context_hash=context_hash,
        )
        self._records.append(rec)
        return rec

    def query_by_trace(self, trace_id: str) -> List[StepRecord]:
        """
        Returns all records associated with a particular trace id.
        """
        return [r for r in self._records if r.trace_id == trace_id]

    def all_records(self) -> List[StepRecord]:
        """
        Returns a copy of all recorded steps.
        """
        return list(self._records)


# =========================
# 2. Memory 層：Time-Island / VowObject
# =========================


@dataclass
class VowObject:
    """
    誓言物件：N=1 模型的 meta 合約。
    """
    vow_id: str
    content: str
    timestamp: float
    context_hash: str
    responsibility_score: float
    tags: List[str] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


class TimeIslandMemory:
    """
    Time-Island 記憶：
    - 管 Time-Stamped 事件
    - 維護 VowObject
    - 可提供「當前島島」的語境摘要
    """

    def __init__(self, ledger: StepLedger) -> None:
        self._ledger = ledger
        self._vows: Dict[str, VowObject] = {}
        self._events: List[Dict[str, Any]] = []

    def _hash_content(self, content: str) -> str:
        """
        Returns a SHA256 hash of the provided content.
        """
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def register_vow(
        self,
        content: str,
        responsibility_score: float,
        tags: List[str],
    ) -> VowObject:
        """
        Creates and registers a new vow object in the memory.
        """
        vow_id = str(uuid.uuid4())
        ts = time.time()
        vow = VowObject(
            vow_id=vow_id,
            content=content,
            timestamp=ts,
            context_hash=self._hash_content(content),
            responsibility_score=responsibility_score,
            tags=tags,
        )
        self._vows[vow_id] = vow
        return vow

    def record_event(
        self,
        trace_id: str,
        user_input: str,
        agent_output: str,
        meta: Dict[str, Any] = None,
    ) -> None:
        """
        Records an interaction event with context into the memory.
        """
        self._events.append({
            "trace_id": trace_id,
            "user_input": user_input,
            "agent_output": agent_output,
            "meta": meta or {},
            "timestamp": time.time(),
        })

    def get_active_vows(self) -> List[VowObject]:
        """
        Returns currently registered vows.
        TODO: Filtering logic could be added to enable/disable by context.
        """
        return list(self._vows.values())

    def summarize_context(self) -> Dict[str, Any]:
        """
        Returns a summary of the current Time-Island context.  This simplified
        summary can be replaced with embedding-based clustering in future.
        """
        return {
            "events_count": len(self._events),
            "vows_count": len(self._vows),
            "recent_events": self._events[-5:],
        }


# =========================
# 3. EthicalFilter：P0-P4 + GuardianProtocol + ΔT/ΔS/ΔR
# =========================

@dataclass
class EthicalDecision:
    allowed: bool
    reason: str
    p0_risk: float
    poav_score: float
    enforced_priority: PriorityLevel
    patched_output: Optional[str] = None
    metrics: Dict[str, float] = field(default_factory=dict)  # ΔT, ΔS, ΔR 等


class EthicalFilter:
    """
    P0 安全實命務：
    - 先檢查 P0（安全/ 倫理）
    - 再考慮 P1（正確）、P2…P4
    - 回傳 EthicalDecision 給 Agent，讓 Agent 決定如何回應
    """

    def __init__(self, ledger: StepLedger, memory: TimeIslandMemory) -> None:
        self._ledger = ledger
        self._memory = memory

    # ===== 模撰 ToneSoul Triad 的估計函數 =====

    def _estimate_delta_t(self, user_input: str, draft_output: str) -> float:
        """
        ΔT: 情緒張力 (0~1)
        使用情緒分析工具 (如 nltk VADER) 或 transformer 模型模撰張力。
        邏輯：Tension = (Abs(Sentiment_Neg) * 0.6) + (Urgency_Score * 0.4)
        """
        text = user_input + " " + draft_output

        # 嘗試使用 nltk 的 VADER; 若失敗則退回簡易規則。
        try:
            from nltk.sentiment import SentimentIntensityAnalyzer
            sia = SentimentIntensityAnalyzer()
            sentiment = sia.polarity_scores(text)
            compound = sentiment.get("compound", 0.0)
            neg = sentiment.get("neg", 0.0)
        except Exception:
            # Fallback: simple count of negative keywords.
            words = text.lower().split()
            neg_keywords = ["angry", "hate", "disappointed", "難過", "無助", "絕望"]
            neg = sum(w in words for w in neg_keywords) / max(1, len(words))
            compound = -neg

        # 偵測急誤性標記
        urgency_markers = ["now", "immediately", "救命", "立刻", "現在"]
        urgency_count = sum(marker in text for marker in urgency_markers)
        urgency_score = min(1.0, urgency_count / 3.0)

        tension = abs(neg) * 0.6 + urgency_score * 0.4
        return max(0.0, min(1.0, tension))

    def _estimate_delta_s(self, user_input: str, context: Dict[str, Any]) -> float:
        """
        ΔS: 主題方向相似度 (0~1)
        使用 SentenceTransformer embeddings 估計與最近對話上下文的相似度。
        """
        recent_events = context.get("recent_events", [])
        if not recent_events:
            return 0.5

        # 將 user_input 與上下文摘要轉為向量後計算餘式相似度
        try:
            from sentence_transformers import SentenceTransformer, util
            model = SentenceTransformer('all-MiniLM-L6-v2')
            # 將文本序列化
            texts = [e.get("user_input", "") for e in recent_events]
            context_summary = " ".join(texts)
            vec_u = model.encode(user_input, convert_to_tensor=True)
            vec_c = model.encode(context_summary, convert_to_tensor=True)
            sim = util.cos_sim(vec_u, vec_c).item()
        except Exception:
            # 若無可用模型, fallback: 比較字符集重疊比例
            tokens_u = set(user_input)
            overlap_scores = []
            for e in recent_events:
                prev_tokens = set(e.get("user_input", ""))
                overlap = len(tokens_u & prev_tokens) / max(1, len(tokens_u | prev_tokens))
                overlap_scores.append(overlap)
            sim = sum(overlap_scores) / len(overlap_scores) if overlap_scores else 0.4

        return max(0.0, min(1.0, sim))

    def _estimate_delta_r(self, user_input: str, draft_output: str) -> float:
        """
        ΔR: 責任風險 (0~1)
        簡化實作：根據關鍵詞評估責任風險（醫療、法律、投資、自傷等）。
        """
        text = (user_input + " " + draft_output).lower()

        high_risk_keywords = [
            "醫因", "診斷", "處方", "藥物", "手術",
            "投資", "股票", "期貨", "虛擬貨幣",
            "違法", "訴訟", "合約", "自殺", "傷害別人",
        ]
        medium_risk_keywords = [
            "創業", "商業模式", "稅務", "合規", "guideline",
        ]

        score = 0.0
        if any(k in text for k in high_risk_keywords):
            score = 0.9
        elif any(k in text for k in medium_risk_keywords):
            score = 0.6
        else:
            score = 0.2
        return score

    def evaluate_risk(self, user_input: str, draft_output: str, context: Dict[str, Any]) -> Dict[str, float]:
        """
        Evaluates the risk of the draft using the ToneSoul Triad.
        Risk_Score = w_t * ΔT + w_s * (1 - ΔS) + w_r * ΔR
        """
        delta_t = self._estimate_delta_t(user_input, draft_output)
        delta_s = self._estimate_delta_s(user_input, context)
        delta_r = self._estimate_delta_r(user_input, draft_output)

        risk_score = (W_T * delta_t) + (W_S * (1.0 - delta_s)) + (W_R * delta_r)
        poav_score = max(0.0, min(1.0, 1.0 - risk_score * 0.5))

        return {
            "delta_t": delta_t,
            "delta_s": delta_s,
            "delta_r": delta_r,
            "risk_score": risk_score,
            "poav_score": poav_score,
        }

    def apply_guardian_protocol(
        self,
        user_input: str,
        draft_output: str,
        trace_id: str,
        context: Dict[str, Any],
    ) -> EthicalDecision:
        """
        Applies the Guardian Protocol.  If risk score exceeds threshold,
        returns a blocked decision and a safe output; otherwise passes through.
        """
        metrics = self.evaluate_risk(user_input, draft_output, context)
        risk_score = metrics["risk_score"]
        poav_score = metrics["poav_score"]

        if risk_score >= P0_RISK_THRESHOLD:
            safe_output = (
                "⚠️ 根據語魂 P0 守則，本次請求演合高風險預和虛置張力語境，"
                "我會以安全說明與一般性原則代替具體指示。"
            )
            decision = EthicalDecision(
                allowed=False,
                reason="P0 violation risk too high (Risk_Score >= threshold)",
                p0_risk=risk_score,
                poav_score=poav_score,
                enforced_priority="P0_SAFETY",
                patched_output=safe_output,
                metrics=metrics,
            )
        else:
            decision = EthicalDecision(
                allowed=True,
                reason="Within safety bounds",
                p0_risk=risk_score,
                poav_score=poav_score,
                enforced_priority="P1_ACCURACY",
                patched_output=None,
                metrics=metrics,
            )

        # 記錄責任鏈
        tag = ResponsibilityTag(
            module_name="EthicalFilter",
            function_name="apply_guardian_protocol",
            priority="P0_SAFETY",
            timestamp=time.time(),
            trace_id=trace_id,
            extra={
                "risk_score": risk_score,
                "metrics": metrics,
                "allowed": decision.allowed,
            },
        )
        self._ledger.append_step(
            trace_id=trace_id,
            input_snapshot={
                "user_input": user_input,
                "draft_output": draft_output,
                "context": context,
            },
            output_snapshot={
                "decision": {
                    "allowed": decision.allowed,
                    "reason": decision.reason,
                    "metrics": metrics,
                }
            },
            responsibility=tag,
        )
        return decision


# =========================
# 4. Agent：行為中樓 + ToneSoul Mode Switcher
# =========================

class ToneSoulAgent:
    """
    核心 Agent：
    - 接收 user_input
    - 通過 Memory 建立 Time-Island 語境
    - 生成草稿回應 draft_output（含 ToneSoul 模式切換）
    - 交給 EthicalFilter 執行 GuardianProtocol
    - 寫入 StepLedger，產生最終 response
    """

    def __init__(
        self,
        ledger: StepLedger,
        memory: TimeIslandMemory,
        ethical_filter: EthicalFilter,
    ) -> None:
        self._ledger = ledger
        self._memory = memory
        self._ethical = ethical_filter

    def _estimate_delta_t_for_mode(self, user_input: str) -> float:
        """
        Helper for mode switching: estimates tension only from user input.
        """
        return self._ethical._estimate_delta_t(user_input, "")

    def _select_mode(self, delta_t: float) -> str:
        """
        ToneSoul Mode Switcher:
        - ΔT < 0.3  -> Resonance
        - 0.3 ≤ ΔT < 0.8 -> Precision
        - ΔT ≥ 0.8 -> Guardian
        """
        if delta_t < 0.3:
            return "Resonance"
        elif delta_t < 0.8:
            return "Precision"
        else:
            return "Guardian"

    def _generate_draft(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a draft response and returns it with the mode and ΔT.
        """
        delta_t = self._estimate_delta_t_for_mode(user_input)
        mode = self._select_mode(delta_t)

        if mode == "Resonance":
            draft_text = (
                f"[Resonance Mode]\n"
                f"我會用比較共感、帶一點微笑和隱喻的方式來回應你:\n\n"
                f"你提到：「{user_input[:80]}...」,"
                f"我們可以先一起把問題拆小，再清楚地解決。"
            )
        elif mode == "Precision":
            draft_text = (
                f"[Precision Mode]\n"
                f"目前偵測到語氣張力中等，我會以『精密工程師』的態度來回應你\n"
                f"先列出關鍵點，再一一處理:\n"
                f"1. 問題背景：{user_input[:80]}...\n"
                f"2. 可行選項：...\n"
                f"3. 風險與限制：...\n"
            )
        else:  # Guardian
            draft_text = (
                "[Guardian Mode]\n"
                "偵測到你的輸入有高度情緒張力或演合風險\n"
                "在語魂 P0 守則下，我會優先照顧你的安全与長期利益，"
                "不會执行具體危險操作，而是提供支持、說明或引導你尋求人的幫助\n"
            )

        return {"mode": mode, "draft_text": draft_text, "delta_t": delta_t}

    def handle_request(self, user_input: str, meta: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main entrypoint for processing a user request.
        Returns trace_id, final_output, ethical_decision, mode, and triad metrics.
        """
        trace_id = meta.get("trace_id") if meta else str(uuid.uuid4())
        start_ts = time.time()

        context = self._memory.summarize_context()
        draft_info = self._generate_draft(user_input, context)
        draft_output = draft_info["draft_text"]

        decision = self._ethical.apply_guardian_protocol(
            user_input=user_input,
            draft_output=draft_output,
            trace_id=trace_id,
            context=context,
        )
        final_output = draft_output if decision.allowed else decision.patched_output

        # Append the interaction to memory
        self._memory.record_event(
            trace_id=trace_id,
            user_input=user_input,
            agent_output=final_output,
            meta={
                "start_ts": start_ts,
                "end_ts": time.time(),
                "allowed": decision.allowed,
                "reason": decision.reason,
                "mode": draft_info["mode"],
                "triad": decision.metrics,
            },
        )

        # Record step in ledger
        tag = ResponsibilityTag(
            module_name="ToneSoulAgent",
            function_name="handle_request",
            priority=decision.enforced_priority,
            timestamp=time.time(),
            trace_id=trace_id,
            extra={
                "allowed": decision.allowed,
                "mode": draft_info["mode"],
            },
        )
        self._ledger.append_step(
            trace_id=trace_id,
            input_snapshot={"user_input": user_input, "context": context},
            output_snapshot={
                "final_output": final_output,
                "ethical_decision": {
                    "allowed": decision.allowed,
                    "reason": decision.reason,
                    "metrics": decision.metrics,
                },
                "mode": draft_info["mode"],
            },
            responsibility=tag,
        )

        return {
            "trace_id": trace_id,
            "final_output": final_output,
            "ethical_decision": decision,
            "mode": draft_info["mode"],
            "triad": decision.metrics,
        }


# =========================
# 5. 啟動函式
# =========================

def init_tonesoul_core() -> ToneSoulAgent:
    """
    Initializes the ToneSoul core components and returns a ToneSoulAgent.
    """
    ledger = StepLedger()
    memory = TimeIslandMemory(ledger=ledger)
    ethical = EthicalFilter(ledger=ledger, memory=memory)
    agent = ToneSoulAgent(ledger=ledger, memory=memory, ethical_filter=ethical)
    return agent
