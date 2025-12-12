# file: src/core/metacognitive_module.py
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque
from enum import Enum

from src.schemas.source_trace import SourceTrace, TraceStep, TraceStatus, TrustLevel
from src.schemas.evolution_object import MetacognitiveInsight, SystemEvolutionState


class CognitiveState(str, Enum):
    """認知狀態枚舉"""
    OPTIMAL = "optimal"              # 最佳狀態
    LEARNING = "learning"            # 學習狀態
    CONFUSED = "confused"            # 困惑狀態
    OVERCONFIDENT = "overconfident"  # 過度自信
    UNCERTAIN = "uncertain"          # 不確定狀態
    DEGRADED = "degraded"           # 退化狀態


class MetacognitiveModule:
    """
    元認知模組
    
    這個模組負責監控和分析系統自身的認知過程，提供自我反思和自我調節能力。
    它是 ToneSoul 系統自我意識和自我改進的核心組件。
    """
    
    def __init__(self):
        # 元認知狀態
        self.current_cognitive_state = CognitiveState.OPTIMAL
        self.cognitive_history: deque = deque(maxlen=1000)
        self.metacognitive_insights: Dict[str, MetacognitiveInsight] = {}
        
        # 自我監控指標
        self.decision_confidence_history: deque = deque(maxlen=500)
        self.error_pattern_analysis: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.cognitive_load_metrics: Dict[str, float] = {}
        
        # 反思機制
        self.reflection_triggers: List[str] = [
            "low_confidence_decision",
            "repeated_errors",
            "performance_degradation",
            "conflicting_information",
            "unexpected_outcomes"
        ]
        
        # 自我調節參數
        self.confidence_threshold = 0.7
        self.error_pattern_threshold = 3  # 連續錯誤觸發反思
        self.reflection_cooldown = timedelta(minutes=30)
        self.last_reflection_time = datetime.now() - self.reflection_cooldown
        
        # 認知偏差檢測
        self.bias_detectors = {
            "confirmation_bias": self._detect_confirmation_bias,
            "overconfidence_bias": self._detect_overconfidence_bias,
            "anchoring_bias": self._detect_anchoring_bias,
            "availability_bias": self._detect_availability_bias
        }
        
        # 初始化基線指標
        self._initialize_baseline_metrics()
    
    def _initialize_baseline_metrics(self):
        """初始化基線指標"""
        self.cognitive_load_metrics = {
            "processing_complexity": 0.5,
            "decision_difficulty": 0.5,
            "information_overload": 0.0,
            "context_switching_cost": 0.0,
            "memory_usage": 0.3
        }
    
    def monitor_cognitive_process(self, source_trace: SourceTrace, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        監控認知過程
        
        Args:
            source_trace: 處理追溯
            decision_context: 決策上下文
            
        Returns:
            認知監控結果
        """
        start_time = datetime.now()
        
        # 分析決策過程
        decision_analysis = self._analyze_decision_process(source_trace, decision_context)
        
        # 評估認知負荷
        cognitive_load = self._assess_cognitive_load(source_trace, decision_context)
        
        # 檢測認知偏差
        bias_detection = self._detect_cognitive_biases(source_trace, decision_context)
        
        # 評估決策信心度
        decision_confidence = self._evaluate_decision_confidence(source_trace, decision_context)
        
        # 更新認知狀態
        new_cognitive_state = self._update_cognitive_state(decision_analysis, cognitive_load, bias_detection, decision_confidence)
        
        # 檢查是否需要反思
        reflection_needed = self._check_reflection_triggers(source_trace, decision_context, decision_analysis)
        
        # 記錄認知歷史
        cognitive_record = {
            "timestamp": start_time,
            "trace_id": source_trace.id,
            "cognitive_state": new_cognitive_state,
            "decision_confidence": decision_confidence,
            "cognitive_load": cognitive_load,
            "biases_detected": bias_detection,
            "reflection_triggered": reflection_needed
        }
        self.cognitive_history.append(cognitive_record)
        
        # 執行反思（如果需要）
        reflection_results = None
        if reflection_needed:
            reflection_results = self._perform_reflection(source_trace, decision_context, cognitive_record)
        
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return {
            "cognitive_state": new_cognitive_state.value,
            "decision_confidence": decision_confidence,
            "cognitive_load": cognitive_load,
            "biases_detected": bias_detection,
            "reflection_performed": reflection_needed,
            "reflection_results": reflection_results,
            "metacognitive_insights": self._generate_metacognitive_insights(cognitive_record),
            "processing_time_ms": processing_time
        }
    
    def _analyze_decision_process(self, source_trace: SourceTrace, context: Dict[str, Any]) -> Dict[str, Any]:
        """分析決策過程"""
        analysis = {
            "decision_path_length": len(source_trace.steps),
            "decision_complexity": 0.0,
            "information_sources": [],
            "decision_points": [],
            "uncertainty_indicators": []
        }
        
        # 分析決策路徑
        for i, step in enumerate(source_trace.steps):
            # 識別決策點
            if "router" in step.tool.lower() or "classifier" in step.tool.lower():
                analysis["decision_points"].append({
                    "step_index": i,
                    "tool": step.tool,
                    "confidence_indicator": step.trust_level.value
                })
            
            # 識別信息來源
            if step.status == TraceStatus.SUCCESS:
                analysis["information_sources"].append(step.tool)
            
            # 識別不確定性指標
            if step.trust_level == TrustLevel.C or step.status == TraceStatus.FAIL:
                analysis["uncertainty_indicators"].append({
                    "step_index": i,
                    "tool": step.tool,
                    "issue": "low_trust" if step.trust_level == TrustLevel.C else "failure"
                })
        
        # 計算決策複雜度
        complexity_factors = [
            len(source_trace.steps) / 10.0,  # 步驟數量
            len(analysis["decision_points"]) / 5.0,  # 決策點數量
            len(analysis["uncertainty_indicators"]) / 3.0  # 不確定性指標
        ]
        analysis["decision_complexity"] = min(sum(complexity_factors) / len(complexity_factors), 1.0)
        
        return analysis
    
    def _assess_cognitive_load(self, source_trace: SourceTrace, context: Dict[str, Any]) -> Dict[str, float]:
        """評估認知負荷"""
        load_metrics = {}
        
        # 處理複雜度
        processing_steps = len(source_trace.steps)
        load_metrics["processing_complexity"] = min(processing_steps / 15.0, 1.0)
        
        # 決策難度（基於失敗步驟和低信任度步驟）
        difficult_steps = sum(1 for step in source_trace.steps 
                            if step.status == TraceStatus.FAIL or step.trust_level == TrustLevel.C)
        load_metrics["decision_difficulty"] = min(difficult_steps / max(processing_steps, 1) * 2.0, 1.0)
        
        # 信息過載（基於上下文複雜度）
        context_complexity = len(str(context)) / 1000.0  # 簡化的複雜度度量
        load_metrics["information_overload"] = min(context_complexity, 1.0)
        
        # 上下文切換成本（基於工具切換頻率）
        tool_switches = 0
        for i in range(1, len(source_trace.steps)):
            if source_trace.steps[i].tool != source_trace.steps[i-1].tool:
                tool_switches += 1
        load_metrics["context_switching_cost"] = min(tool_switches / max(processing_steps, 1) * 2.0, 1.0)
        
        # 記憶使用（基於歷史記錄大小）
        load_metrics["memory_usage"] = min(len(self.cognitive_history) / 1000.0, 1.0)
        
        # 更新全局指標
        for metric, value in load_metrics.items():
            # 使用指數移動平均更新
            alpha = 0.1
            self.cognitive_load_metrics[metric] = (1 - alpha) * self.cognitive_load_metrics.get(metric, 0.5) + alpha * value
        
        return load_metrics
    
    def _detect_cognitive_biases(self, source_trace: SourceTrace, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """檢測認知偏差"""
        detected_biases = []
        
        for bias_name, detector_func in self.bias_detectors.items():
            bias_result = detector_func(source_trace, context)
            if bias_result["detected"]:
                detected_biases.append({
                    "bias_type": bias_name,
                    "confidence": bias_result["confidence"],
                    "evidence": bias_result["evidence"],
                    "impact_assessment": bias_result.get("impact", "medium")
                })
        
        return detected_biases
    
    def _detect_confirmation_bias(self, source_trace: SourceTrace, context: Dict[str, Any]) -> Dict[str, Any]:
        """檢測確認偏差"""
        # 簡化實現：檢查是否過度依賴某些信息源
        tool_usage = defaultdict(int)
        for step in source_trace.steps:
            tool_usage[step.tool] += 1
        
        if tool_usage:
            max_usage = max(tool_usage.values())
            total_steps = len(source_trace.steps)
            
            if max_usage / total_steps > 0.7:  # 超過70%使用同一工具
                return {
                    "detected": True,
                    "confidence": 0.6,
                    "evidence": f"Over-reliance on {max(tool_usage, key=tool_usage.get)}",
                    "impact": "medium"
                }
        
        return {"detected": False, "confidence": 0.0, "evidence": ""}
    
    def _detect_overconfidence_bias(self, source_trace: SourceTrace, context: Dict[str, Any]) -> Dict[str, Any]:
        """檢測過度自信偏差"""
        # 檢查高信心度但實際表現不佳的情況
        high_confidence_steps = [step for step in source_trace.steps if step.trust_level == TrustLevel.A]
        failed_high_confidence = [step for step in high_confidence_steps if step.status == TraceStatus.FAIL]
        
        if high_confidence_steps and len(failed_high_confidence) / len(high_confidence_steps) > 0.3:
            return {
                "detected": True,
                "confidence": 0.7,
                "evidence": f"{len(failed_high_confidence)} high-confidence steps failed",
                "impact": "high"
            }
        
        return {"detected": False, "confidence": 0.0, "evidence": ""}
    
    def _detect_anchoring_bias(self, source_trace: SourceTrace, context: Dict[str, Any]) -> Dict[str, Any]:
        """檢測錨定偏差"""
        # 檢查是否過度依賴早期信息
        if len(source_trace.steps) >= 3:
            early_tools = set(step.tool for step in source_trace.steps[:2])
            later_tools = set(step.tool for step in source_trace.steps[2:])
            
            # 如果後期步驟過度重複早期工具
            overlap = len(early_tools.intersection(later_tools))
            if overlap / len(early_tools) > 0.8:
                return {
                    "detected": True,
                    "confidence": 0.5,
                    "evidence": "High repetition of early processing tools",
                    "impact": "medium"
                }
        
        return {"detected": False, "confidence": 0.0, "evidence": ""}
    
    def _detect_availability_bias(self, source_trace: SourceTrace, context: Dict[str, Any]) -> Dict[str, Any]:
        """檢測可得性偏差"""
        # 檢查是否過度依賴最近使用的工具
        if len(self.cognitive_history) >= 5:
            recent_tools = []
            for record in list(self.cognitive_history)[-5:]:
                # 這裡需要從歷史記錄中提取工具使用信息
                # 簡化實現
                pass
        
        return {"detected": False, "confidence": 0.0, "evidence": ""}
    
    def _evaluate_decision_confidence(self, source_trace: SourceTrace, context: Dict[str, Any]) -> float:
        """評估決策信心度"""
        if not source_trace.steps:
            return 0.0
        
        # 基於步驟成功率和信任等級
        success_rate = sum(1 for step in source_trace.steps if step.status == TraceStatus.SUCCESS) / len(source_trace.steps)
        
        # 信任等級權重
        trust_weights = {"A": 1.0, "B": 0.7, "C": 0.4}
        avg_trust = sum(trust_weights[step.trust_level.value] for step in source_trace.steps) / len(source_trace.steps)
        
        # 綜合信心度
        confidence = (success_rate * 0.6 + avg_trust * 0.4)
        
        # 記錄信心度歷史
        self.decision_confidence_history.append(confidence)
        
        return confidence
    
    def _update_cognitive_state(self, decision_analysis: Dict[str, Any], cognitive_load: Dict[str, float], 
                               biases: List[Dict[str, Any]], confidence: float) -> CognitiveState:
        """更新認知狀態"""
        # 基於各種指標確定認知狀態
        avg_load = sum(cognitive_load.values()) / len(cognitive_load)
        
        if len(biases) >= 2:
            new_state = CognitiveState.CONFUSED
        elif confidence < 0.3:
            new_state = CognitiveState.UNCERTAIN
        elif confidence > 0.9 and any(bias["bias_type"] == "overconfidence_bias" for bias in biases):
            new_state = CognitiveState.OVERCONFIDENT
        elif avg_load > 0.8:
            new_state = CognitiveState.DEGRADED
        elif confidence < 0.7 and avg_load > 0.6:
            new_state = CognitiveState.LEARNING
        else:
            new_state = CognitiveState.OPTIMAL
        
        self.current_cognitive_state = new_state
        return new_state
    
    def _check_reflection_triggers(self, source_trace: SourceTrace, context: Dict[str, Any], 
                                 decision_analysis: Dict[str, Any]) -> bool:
        """檢查反思觸發條件"""
        # 檢查冷卻時間
        if datetime.now() - self.last_reflection_time < self.reflection_cooldown:
            return False
        
        # 檢查各種觸發條件
        triggers_met = []
        
        # 低信心度決策
        if len(self.decision_confidence_history) >= 3:
            recent_confidence = list(self.decision_confidence_history)[-3:]
            if all(conf < self.confidence_threshold for conf in recent_confidence):
                triggers_met.append("low_confidence_decision")
        
        # 重複錯誤
        failed_steps = [step for step in source_trace.steps if step.status == TraceStatus.FAIL]
        if len(failed_steps) >= self.error_pattern_threshold:
            triggers_met.append("repeated_errors")
        
        # 性能退化
        if self.current_cognitive_state == CognitiveState.DEGRADED:
            triggers_met.append("performance_degradation")
        
        # 衝突信息
        if len(decision_analysis.get("uncertainty_indicators", [])) >= 2:
            triggers_met.append("conflicting_information")
        
        return len(triggers_met) > 0
    
    def _perform_reflection(self, source_trace: SourceTrace, context: Dict[str, Any], 
                          cognitive_record: Dict[str, Any]) -> Dict[str, Any]:
        """執行反思過程"""
        self.last_reflection_time = datetime.now()
        
        reflection_results = {
            "reflection_id": str(uuid.uuid4()),
            "timestamp": self.last_reflection_time,
            "trigger_trace_id": source_trace.id,
            "insights_generated": [],
            "improvement_suggestions": [],
            "cognitive_adjustments": []
        }
        
        # 分析最近的認知模式
        recent_history = list(self.cognitive_history)[-10:]
        
        # 識別問題模式
        problem_patterns = self._identify_problem_patterns(recent_history)
        
        # 生成洞察
        for pattern in problem_patterns:
            insight = self._generate_insight_from_pattern(pattern, source_trace, context)
            if insight:
                reflection_results["insights_generated"].append(insight)
                
                # 創建元認知洞察記錄
                metacognitive_insight = MetacognitiveInsight(
                    insight_type=pattern["type"],
                    description=insight["description"],
                    trigger_context=context,
                    impact_assessment=insight["impact_assessment"],
                    recommended_actions=insight["recommended_actions"],
                    confidence_level=insight["confidence"]
                )
                self.metacognitive_insights[metacognitive_insight.id] = metacognitive_insight
        
        # 生成改進建議
        reflection_results["improvement_suggestions"] = self._generate_improvement_suggestions(problem_patterns)
        
        # 執行認知調整
        reflection_results["cognitive_adjustments"] = self._perform_cognitive_adjustments(problem_patterns)
        
        return reflection_results
    
    def _identify_problem_patterns(self, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """識別問題模式"""
        patterns = []
        
        # 信心度持續下降
        confidences = [record["decision_confidence"] for record in history]
        if len(confidences) >= 5 and all(confidences[i] > confidences[i+1] for i in range(4)):
            patterns.append({
                "type": "declining_confidence",
                "severity": "high",
                "evidence": confidences,
                "description": "Decision confidence has been consistently declining"
            })
        
        # 認知負荷過高
        high_load_count = sum(1 for record in history if record["cognitive_load"].get("processing_complexity", 0) > 0.8)
        if high_load_count / len(history) > 0.6:
            patterns.append({
                "type": "high_cognitive_load",
                "severity": "medium",
                "evidence": {"high_load_ratio": high_load_count / len(history)},
                "description": "Cognitive load has been consistently high"
            })
        
        # 偏差頻繁出現
        bias_count = sum(len(record.get("biases_detected", [])) for record in history)
        if bias_count > len(history) * 0.5:
            patterns.append({
                "type": "frequent_biases",
                "severity": "medium",
                "evidence": {"bias_frequency": bias_count / len(history)},
                "description": "Cognitive biases are occurring frequently"
            })
        
        return patterns
    
    def _generate_insight_from_pattern(self, pattern: Dict[str, Any], source_trace: SourceTrace, 
                                     context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """從模式生成洞察"""
        if pattern["type"] == "declining_confidence":
            return {
                "description": "System confidence is declining, possibly due to encountering unfamiliar scenarios",
                "impact_assessment": {"decision_quality": -0.3, "user_satisfaction": -0.2},
                "recommended_actions": ["increase_learning_rate", "seek_additional_validation", "expand_knowledge_base"],
                "confidence": 0.8
            }
        elif pattern["type"] == "high_cognitive_load":
            return {
                "description": "Cognitive load is consistently high, indicating processing inefficiency",
                "impact_assessment": {"response_time": -0.4, "accuracy": -0.1},
                "recommended_actions": ["optimize_processing_pipeline", "implement_caching", "simplify_decision_trees"],
                "confidence": 0.7
            }
        elif pattern["type"] == "frequent_biases":
            return {
                "description": "Cognitive biases are occurring frequently, affecting decision quality",
                "impact_assessment": {"decision_accuracy": -0.3, "fairness": -0.4},
                "recommended_actions": ["implement_bias_correction", "diversify_information_sources", "add_devil_advocate_mechanism"],
                "confidence": 0.75
            }
        
        return None
    
    def _generate_improvement_suggestions(self, patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """生成改進建議"""
        suggestions = []
        
        for pattern in patterns:
            if pattern["severity"] == "high":
                suggestions.append({
                    "priority": "high",
                    "category": "cognitive_optimization",
                    "suggestion": f"Address {pattern['type']} immediately",
                    "expected_impact": "significant_improvement"
                })
            elif pattern["severity"] == "medium":
                suggestions.append({
                    "priority": "medium",
                    "category": "performance_tuning",
                    "suggestion": f"Monitor and gradually improve {pattern['type']}",
                    "expected_impact": "moderate_improvement"
                })
        
        return suggestions
    
    def _perform_cognitive_adjustments(self, patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """執行認知調整"""
        adjustments = []
        
        for pattern in patterns:
            if pattern["type"] == "declining_confidence":
                # 調整信心度閾值
                self.confidence_threshold = max(self.confidence_threshold - 0.05, 0.5)
                adjustments.append({
                    "adjustment_type": "confidence_threshold",
                    "old_value": self.confidence_threshold + 0.05,
                    "new_value": self.confidence_threshold,
                    "reason": "Adapting to declining confidence pattern"
                })
            
            elif pattern["type"] == "high_cognitive_load":
                # 增加反思冷卻時間
                self.reflection_cooldown = min(self.reflection_cooldown + timedelta(minutes=10), timedelta(hours=2))
                adjustments.append({
                    "adjustment_type": "reflection_cooldown",
                    "new_value": str(self.reflection_cooldown),
                    "reason": "Reducing reflection frequency to manage cognitive load"
                })
        
        return adjustments
    
    def _generate_metacognitive_insights(self, cognitive_record: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成元認知洞察"""
        insights = []
        
        # 基於當前認知狀態生成洞察
        if cognitive_record["cognitive_state"] == CognitiveState.CONFUSED:
            insights.append({
                "type": "state_awareness",
                "message": "System is in a confused state, consider simplifying the current task",
                "confidence": 0.8
            })
        
        elif cognitive_record["cognitive_state"] == CognitiveState.OVERCONFIDENT:
            insights.append({
                "type": "confidence_calibration",
                "message": "System may be overconfident, recommend additional validation",
                "confidence": 0.7
            })
        
        # 基於認知負荷生成洞察
        avg_load = sum(cognitive_record["cognitive_load"].values()) / len(cognitive_record["cognitive_load"])
        if avg_load > 0.8:
            insights.append({
                "type": "load_management",
                "message": "High cognitive load detected, consider breaking down the task",
                "confidence": 0.9
            })
        
        return insights
    
    def get_cognitive_summary(self) -> Dict[str, Any]:
        """獲取認知狀態摘要"""
        recent_history = list(self.cognitive_history)[-20:] if self.cognitive_history else []
        
        summary = {
            "current_state": self.current_cognitive_state.value,
            "recent_confidence_trend": self._calculate_confidence_trend(),
            "cognitive_load_summary": self.cognitive_load_metrics.copy(),
            "bias_frequency": self._calculate_bias_frequency(recent_history),
            "reflection_frequency": len([r for r in recent_history if r.get("reflection_triggered", False)]),
            "total_insights_generated": len(self.metacognitive_insights),
            "system_self_awareness_score": self._calculate_self_awareness_score()
        }
        
        return summary
    
    def _calculate_confidence_trend(self) -> str:
        """計算信心度趨勢"""
        if len(self.decision_confidence_history) < 5:
            return "insufficient_data"
        
        recent = list(self.decision_confidence_history)[-5:]
        older = list(self.decision_confidence_history)[-10:-5] if len(self.decision_confidence_history) >= 10 else recent
        
        recent_avg = sum(recent) / len(recent)
        older_avg = sum(older) / len(older)
        
        if recent_avg > older_avg * 1.1:
            return "improving"
        elif recent_avg < older_avg * 0.9:
            return "declining"
        else:
            return "stable"
    
    def _calculate_bias_frequency(self, history: List[Dict[str, Any]]) -> float:
        """計算偏差頻率"""
        if not history:
            return 0.0
        
        total_biases = sum(len(record.get("biases_detected", [])) for record in history)
        return total_biases / len(history)
    
    def _calculate_self_awareness_score(self) -> float:
        """計算自我意識評分"""
        # 基於多個因素計算自我意識評分
        factors = []
        
        # 反思頻率（適中為好）
        if len(self.cognitive_history) > 0:
            reflection_rate = len([r for r in self.cognitive_history if r.get("reflection_triggered", False)]) / len(self.cognitive_history)
            # 理想反思率在0.1-0.3之間
            if 0.1 <= reflection_rate <= 0.3:
                factors.append(1.0)
            else:
                factors.append(max(0.0, 1.0 - abs(reflection_rate - 0.2) * 5))
        
        # 洞察生成能力
        insight_score = min(len(self.metacognitive_insights) / 10.0, 1.0)
        factors.append(insight_score)
        
        # 認知狀態穩定性
        if len(self.cognitive_history) >= 10:
            recent_states = [r["cognitive_state"] for r in list(self.cognitive_history)[-10:]]
            stability = 1.0 - (len(set(recent_states)) - 1) / 9.0  # 狀態變化越少越穩定
            factors.append(stability)
        
        return sum(factors) / len(factors) if factors else 0.5