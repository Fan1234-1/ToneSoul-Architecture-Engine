# file: src/core/adaptive_learning_module.py
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque

from src.schemas.source_trace import SourceTrace, TraceStep, TraceStatus, TrustLevel
from src.schemas.evolution_object import (
    LearningPattern, LearningType, EvolutionRecord, EvolutionStatus,
    SystemEvolutionState
)


class AdaptiveLearningModule:
    """
    自適應學習模組
    
    這個模組負責從系統互動中學習，識別模式，並動態調整系統行為。
    它是 ToneSoul 系統自我進化能力的核心組件。
    """
    
    def __init__(self):
        # 學習模式存儲
        self.learning_patterns: Dict[str, LearningPattern] = {}
        self.interaction_history: deque = deque(maxlen=10000)  # 保留最近10000次互動
        self.performance_metrics: Dict[str, List[float]] = defaultdict(list)
        
        # 進化記錄
        self.evolution_records: Dict[str, EvolutionRecord] = {}
        self.system_state = SystemEvolutionState(version="1.0.0")
        
        # 學習參數
        self.learning_rate = 0.01
        self.pattern_detection_threshold = 0.8
        self.adaptation_cooldown = timedelta(hours=1)  # 適應冷卻時間
        self.last_adaptation_time = datetime.now() - self.adaptation_cooldown
        
        # 初始化基礎學習模式
        self._initialize_base_patterns()
    
    def _initialize_base_patterns(self):
        """初始化基礎學習模式"""
        base_patterns = [
            LearningPattern(
                pattern_type=LearningType.FEEDBACK_ADAPTATION,
                trigger_conditions=["user_satisfaction_low", "response_time_high"],
                success_indicators=["user_satisfaction_improved", "response_time_reduced"],
                failure_indicators=["user_satisfaction_decreased", "error_rate_increased"],
                confidence_threshold=0.7,
                adaptation_weight=0.1
            ),
            LearningPattern(
                pattern_type=LearningType.PATTERN_RECOGNITION,
                trigger_conditions=["repeated_query_type", "similar_context"],
                success_indicators=["accurate_classification", "appropriate_routing"],
                failure_indicators=["misclassification", "wrong_module_routing"],
                confidence_threshold=0.8,
                adaptation_weight=0.05
            ),
            LearningPattern(
                pattern_type=LearningType.EMOTIONAL_CALIBRATION,
                trigger_conditions=["emotional_mismatch", "tone_inconsistency"],
                success_indicators=["emotional_alignment", "positive_feedback"],
                failure_indicators=["emotional_disconnect", "negative_feedback"],
                confidence_threshold=0.75,
                adaptation_weight=0.08
            )
        ]
        
        for pattern in base_patterns:
            self.learning_patterns[pattern.id] = pattern
            self.system_state.active_learning_patterns.append(pattern.id)
    
    def process_interaction(self, source_trace: SourceTrace, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        處理互動並進行學習
        
        Args:
            source_trace: 完整的處理追溯
            context: 互動上下文信息
            
        Returns:
            學習結果和建議
        """
        start_time = datetime.now()
        
        # 記錄互動
        interaction_record = {
            "trace_id": source_trace.id,
            "timestamp": start_time,
            "context": context,
            "steps": len(source_trace.steps),
            "total_latency": sum(step.latency_ms for step in source_trace.steps),
            "success_rate": self._calculate_success_rate(source_trace.steps)
        }
        self.interaction_history.append(interaction_record)
        
        # 更新系統狀態
        self.system_state.total_interactions += 1
        
        # 檢測學習機會
        learning_opportunities = self._detect_learning_opportunities(source_trace, context)
        
        # 執行學習
        learning_results = []
        for opportunity in learning_opportunities:
            result = self._execute_learning(opportunity, source_trace, context)
            if result:
                learning_results.append(result)
        
        # 更新性能指標
        self._update_performance_metrics(interaction_record)
        
        # 檢查是否需要適應
        adaptation_suggestions = self._check_adaptation_needs()
        
        # 創建追溯步驟
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return {
            "learning_opportunities_detected": len(learning_opportunities),
            "learning_results": learning_results,
            "adaptation_suggestions": adaptation_suggestions,
            "system_performance": self._get_current_performance_summary(),
            "processing_time_ms": processing_time
        }
    
    def _calculate_success_rate(self, steps: List[TraceStep]) -> float:
        """計算步驟成功率"""
        if not steps:
            return 0.0
        
        success_count = sum(1 for step in steps if step.status == TraceStatus.SUCCESS)
        return success_count / len(steps)
    
    def _detect_learning_opportunities(self, source_trace: SourceTrace, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """檢測學習機會"""
        opportunities = []
        
        # 檢查每個學習模式
        for pattern_id, pattern in self.learning_patterns.items():
            if self._matches_trigger_conditions(pattern, source_trace, context):
                opportunity = {
                    "pattern_id": pattern_id,
                    "pattern_type": pattern.pattern_type,
                    "confidence": self._calculate_pattern_confidence(pattern, source_trace, context),
                    "context": context,
                    "trace_id": source_trace.id
                }
                opportunities.append(opportunity)
        
        return opportunities
    
    def _matches_trigger_conditions(self, pattern: LearningPattern, source_trace: SourceTrace, context: Dict[str, Any]) -> bool:
        """檢查是否符合觸發條件"""
        # 這裡實現具體的條件匹配邏輯
        # 簡化版本：檢查上下文中是否包含觸發條件
        context_keys = set(context.keys())
        trigger_conditions = set(pattern.trigger_conditions)
        
        # 如果至少有一個觸發條件匹配，則返回True
        return len(context_keys.intersection(trigger_conditions)) > 0
    
    def _calculate_pattern_confidence(self, pattern: LearningPattern, source_trace: SourceTrace, context: Dict[str, Any]) -> float:
        """計算模式匹配信心度"""
        base_confidence = 0.5
        
        # 基於歷史成功率調整
        if pattern.usage_count > 0:
            base_confidence = pattern.success_rate
        
        # 基於當前上下文調整
        context_match_score = self._calculate_context_match_score(pattern, context)
        
        # 基於追溯質量調整
        trace_quality_score = self._calculate_trace_quality_score(source_trace)
        
        # 綜合計算
        confidence = (base_confidence * 0.5 + context_match_score * 0.3 + trace_quality_score * 0.2)
        return min(max(confidence, 0.0), 1.0)
    
    def _calculate_context_match_score(self, pattern: LearningPattern, context: Dict[str, Any]) -> float:
        """計算上下文匹配分數"""
        # 簡化實現：基於關鍵詞匹配
        total_conditions = len(pattern.trigger_conditions)
        if total_conditions == 0:
            return 0.5
        
        matched_conditions = 0
        for condition in pattern.trigger_conditions:
            if condition in context or any(condition in str(v) for v in context.values()):
                matched_conditions += 1
        
        return matched_conditions / total_conditions
    
    def _calculate_trace_quality_score(self, source_trace: SourceTrace) -> float:
        """計算追溯質量分數"""
        if not source_trace.steps:
            return 0.0
        
        # 基於成功率和信任等級
        success_rate = self._calculate_success_rate(source_trace.steps)
        
        # 計算平均信任等級
        trust_scores = {"A": 1.0, "B": 0.7, "C": 0.4}
        avg_trust = sum(trust_scores.get(step.trust_level.value, 0.0) for step in source_trace.steps) / len(source_trace.steps)
        
        return (success_rate * 0.6 + avg_trust * 0.4)
    
    def _execute_learning(self, opportunity: Dict[str, Any], source_trace: SourceTrace, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """執行學習過程"""
        pattern_id = opportunity["pattern_id"]
        pattern = self.learning_patterns[pattern_id]
        
        if opportunity["confidence"] < pattern.confidence_threshold:
            return None
        
        # 更新模式使用統計
        pattern.usage_count += 1
        pattern.last_updated = datetime.now()
        
        # 根據學習類型執行不同的學習邏輯
        learning_result = None
        
        if pattern.pattern_type == LearningType.FEEDBACK_ADAPTATION:
            learning_result = self._learn_from_feedback(pattern, source_trace, context)
        elif pattern.pattern_type == LearningType.PATTERN_RECOGNITION:
            learning_result = self._learn_pattern_recognition(pattern, source_trace, context)
        elif pattern.pattern_type == LearningType.EMOTIONAL_CALIBRATION:
            learning_result = self._learn_emotional_calibration(pattern, source_trace, context)
        
        if learning_result and learning_result.get("success", False):
            # 更新成功率
            current_success_rate = pattern.success_rate
            new_success_rate = current_success_rate + (1.0 - current_success_rate) * self.learning_rate
            pattern.success_rate = new_success_rate
        
        return learning_result
    
    def _learn_from_feedback(self, pattern: LearningPattern, source_trace: SourceTrace, context: Dict[str, Any]) -> Dict[str, Any]:
        """從反饋中學習"""
        # 分析反饋信號
        feedback_signals = context.get("feedback_signals", {})
        
        # 識別改進機會
        improvements = []
        if "response_time" in feedback_signals and feedback_signals["response_time"] > 1000:
            improvements.append("optimize_response_time")
        
        if "user_satisfaction" in feedback_signals and feedback_signals["user_satisfaction"] < 0.7:
            improvements.append("improve_response_quality")
        
        return {
            "success": len(improvements) > 0,
            "learning_type": "feedback_adaptation",
            "improvements_identified": improvements,
            "confidence": self._calculate_pattern_confidence(pattern, source_trace, context)
        }
    
    def _learn_pattern_recognition(self, pattern: LearningPattern, source_trace: SourceTrace, context: Dict[str, Any]) -> Dict[str, Any]:
        """學習模式識別"""
        # 分析處理模式
        processing_pattern = {
            "input_type": context.get("input_type", "unknown"),
            "processing_path": [step.tool for step in source_trace.steps],
            "success_indicators": [step.evidence for step in source_trace.steps if step.status == TraceStatus.SUCCESS]
        }
        
        return {
            "success": True,
            "learning_type": "pattern_recognition",
            "pattern_learned": processing_pattern,
            "confidence": self._calculate_pattern_confidence(pattern, source_trace, context)
        }
    
    def _learn_emotional_calibration(self, pattern: LearningPattern, source_trace: SourceTrace, context: Dict[str, Any]) -> Dict[str, Any]:
        """學習情感校準"""
        # 分析情感匹配度
        emotional_context = context.get("emotional_context", {})
        response_tone = context.get("response_tone", "neutral")
        
        calibration_adjustments = []
        if "user_emotion" in emotional_context:
            user_emotion = emotional_context["user_emotion"]
            if user_emotion == "frustrated" and response_tone != "empathetic":
                calibration_adjustments.append("increase_empathy")
            elif user_emotion == "happy" and response_tone == "formal":
                calibration_adjustments.append("match_positive_tone")
        
        return {
            "success": len(calibration_adjustments) > 0,
            "learning_type": "emotional_calibration",
            "calibration_adjustments": calibration_adjustments,
            "confidence": self._calculate_pattern_confidence(pattern, source_trace, context)
        }
    
    def _update_performance_metrics(self, interaction_record: Dict[str, Any]):
        """更新性能指標"""
        # 更新各種性能指標
        self.performance_metrics["response_time"].append(interaction_record["total_latency"])
        self.performance_metrics["success_rate"].append(interaction_record["success_rate"])
        
        # 保持指標歷史在合理範圍內
        for metric_name, values in self.performance_metrics.items():
            if len(values) > 1000:
                self.performance_metrics[metric_name] = values[-1000:]
        
        # 更新系統狀態
        if self.performance_metrics["success_rate"]:
            avg_success_rate = sum(self.performance_metrics["success_rate"][-100:]) / min(100, len(self.performance_metrics["success_rate"]))
            self.system_state.overall_performance_score = avg_success_rate
        
        self.system_state.last_updated = datetime.now()
    
    def _check_adaptation_needs(self) -> List[Dict[str, Any]]:
        """檢查適應需求"""
        suggestions = []
        
        # 檢查是否在冷卻期內
        if datetime.now() - self.last_adaptation_time < self.adaptation_cooldown:
            return suggestions
        
        # 檢查性能下降
        if len(self.performance_metrics["success_rate"]) >= 50:
            recent_performance = sum(self.performance_metrics["success_rate"][-20:]) / 20
            historical_performance = sum(self.performance_metrics["success_rate"][-50:-20]) / 30
            
            if recent_performance < historical_performance * 0.9:  # 性能下降超過10%
                suggestions.append({
                    "type": "performance_degradation",
                    "severity": "medium",
                    "description": "Recent performance has declined",
                    "recommended_action": "review_and_adjust_patterns"
                })
        
        # 檢查響應時間
        if len(self.performance_metrics["response_time"]) >= 20:
            avg_response_time = sum(self.performance_metrics["response_time"][-20:]) / 20
            if avg_response_time > 2000:  # 響應時間超過2秒
                suggestions.append({
                    "type": "response_time_high",
                    "severity": "high",
                    "description": "Average response time is too high",
                    "recommended_action": "optimize_processing_pipeline"
                })
        
        return suggestions
    
    def _get_current_performance_summary(self) -> Dict[str, Any]:
        """獲取當前性能摘要"""
        summary = {
            "total_interactions": self.system_state.total_interactions,
            "active_patterns": len(self.system_state.active_learning_patterns),
            "overall_performance": self.system_state.overall_performance_score,
            "system_health": self.system_state.get_health_summary()
        }
        
        # 添加最近的性能指標
        if self.performance_metrics["response_time"]:
            summary["avg_response_time"] = sum(self.performance_metrics["response_time"][-10:]) / min(10, len(self.performance_metrics["response_time"]))
        
        if self.performance_metrics["success_rate"]:
            summary["recent_success_rate"] = sum(self.performance_metrics["success_rate"][-10:]) / min(10, len(self.performance_metrics["success_rate"]))
        
        return summary
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """獲取學習洞察"""
        insights = {
            "most_active_patterns": [],
            "learning_trends": {},
            "adaptation_history": [],
            "performance_trends": {}
        }
        
        # 最活躍的學習模式
        pattern_usage = [(pattern.id, pattern.usage_count, pattern.success_rate) 
                        for pattern in self.learning_patterns.values()]
        pattern_usage.sort(key=lambda x: x[1], reverse=True)
        insights["most_active_patterns"] = pattern_usage[:5]
        
        # 性能趨勢
        if len(self.performance_metrics["success_rate"]) >= 10:
            recent_avg = sum(self.performance_metrics["success_rate"][-10:]) / 10
            older_avg = sum(self.performance_metrics["success_rate"][-20:-10]) / 10 if len(self.performance_metrics["success_rate"]) >= 20 else recent_avg
            insights["performance_trends"]["success_rate_trend"] = "improving" if recent_avg > older_avg else "declining"
        
        return insights
    
    def create_evolution_record(self, evolution_type: LearningType, before_state: Dict[str, Any], 
                              after_state: Dict[str, Any], trigger_trace_id: str, 
                              context: Dict[str, Any]) -> str:
        """創建進化記錄"""
        record = EvolutionRecord(
            evolution_type=evolution_type,
            before_state=before_state,
            after_state=after_state,
            change_description=f"System evolved through {evolution_type.value}",
            trigger_source_trace_id=trigger_trace_id,
            trigger_context=context,
            validation_criteria=["performance_improvement", "consistency_check", "safety_validation"]
        )
        
        self.evolution_records[record.id] = record
        self.system_state.add_evolution_record(record.id)
        
        return record.id