# file: src/schemas/evolution_object.py
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class LearningType(str, Enum):
    """學習類型枚舉"""
    PATTERN_RECOGNITION = "pattern_recognition"    # 模式識別學習
    FEEDBACK_ADAPTATION = "feedback_adaptation"    # 反饋適應學習
    KNOWLEDGE_EXPANSION = "knowledge_expansion"    # 知識擴展學習
    EMOTIONAL_CALIBRATION = "emotional_calibration"  # 情感校準學習
    MORAL_REFINEMENT = "moral_refinement"         # 道德精煉學習
    METACOGNITIVE_IMPROVEMENT = "metacognitive_improvement"  # 元認知改進


class EvolutionStatus(str, Enum):
    """進化狀態枚舉"""
    LEARNING = "learning"        # 學習中
    ADAPTING = "adapting"       # 適應中
    VALIDATING = "validating"   # 驗證中
    INTEGRATED = "integrated"   # 已整合
    REJECTED = "rejected"       # 已拒絕
    ARCHIVED = "archived"       # 已歸檔


class LearningPattern(BaseModel):
    """學習模式物件"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="學習模式唯一標識符")
    pattern_type: LearningType = Field(..., description="學習模式類型")
    trigger_conditions: List[str] = Field(..., description="觸發條件列表")
    success_indicators: List[str] = Field(..., description="成功指標列表")
    failure_indicators: List[str] = Field(..., description="失敗指標列表")
    confidence_threshold: float = Field(default=0.7, description="信心閾值", ge=0.0, le=1.0)
    adaptation_weight: float = Field(default=0.1, description="適應權重", ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.now, description="創建時間")
    last_updated: datetime = Field(default_factory=datetime.now, description="最後更新時間")
    usage_count: int = Field(default=0, description="使用次數")
    success_rate: float = Field(default=0.0, description="成功率", ge=0.0, le=1.0)


class KnowledgeNode(BaseModel):
    """知識節點物件"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="知識節點唯一標識符")
    concept: str = Field(..., description="概念名稱")
    content: str = Field(..., description="知識內容")
    confidence: float = Field(default=0.5, description="知識可信度", ge=0.0, le=1.0)
    source_traces: List[str] = Field(default_factory=list, description="來源追溯ID列表")
    connections: Dict[str, float] = Field(default_factory=dict, description="與其他節點的連接權重")
    validation_count: int = Field(default=0, description="驗證次數")
    contradiction_count: int = Field(default=0, description="矛盾次數")
    created_at: datetime = Field(default_factory=datetime.now, description="創建時間")
    last_accessed: datetime = Field(default_factory=datetime.now, description="最後訪問時間")
    decay_factor: float = Field(default=0.99, description="遺忘衰減因子", ge=0.0, le=1.0)


class MetacognitiveInsight(BaseModel):
    """元認知洞察物件"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="洞察唯一標識符")
    insight_type: str = Field(..., description="洞察類型")
    description: str = Field(..., description="洞察描述")
    trigger_context: Dict[str, Any] = Field(..., description="觸發上下文")
    impact_assessment: Dict[str, float] = Field(..., description="影響評估")
    recommended_actions: List[str] = Field(..., description="建議行動")
    confidence_level: float = Field(..., description="信心水平", ge=0.0, le=1.0)
    validation_status: str = Field(default="pending", description="驗證狀態")
    created_at: datetime = Field(default_factory=datetime.now, description="創建時間")
    applied_at: Optional[datetime] = Field(None, description="應用時間")
    effectiveness_score: Optional[float] = Field(None, description="有效性評分", ge=0.0, le=1.0)


class EvolutionRecord(BaseModel):
    """進化記錄物件"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="進化記錄唯一標識符")
    evolution_type: LearningType = Field(..., description="進化類型")
    status: EvolutionStatus = Field(default=EvolutionStatus.LEARNING, description="進化狀態")
    
    # 進化內容
    before_state: Dict[str, Any] = Field(..., description="進化前狀態")
    after_state: Dict[str, Any] = Field(..., description="進化後狀態")
    change_description: str = Field(..., description="變化描述")
    
    # 觸發信息
    trigger_source_trace_id: str = Field(..., description="觸發的來源追溯ID")
    trigger_context: Dict[str, Any] = Field(..., description="觸發上下文")
    
    # 驗證信息
    validation_criteria: List[str] = Field(..., description="驗證標準")
    validation_results: Dict[str, Any] = Field(default_factory=dict, description="驗證結果")
    
    # 時間信息
    initiated_at: datetime = Field(default_factory=datetime.now, description="啟動時間")
    completed_at: Optional[datetime] = Field(None, description="完成時間")
    
    # 效果評估
    performance_impact: Dict[str, float] = Field(default_factory=dict, description="性能影響")
    rollback_available: bool = Field(default=True, description="是否可回滾")
    rollback_data: Optional[Dict[str, Any]] = Field(None, description="回滾數據")


class SystemEvolutionState(BaseModel):
    """系統進化狀態物件"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="系統狀態唯一標識符")
    version: str = Field(..., description="系統版本")
    
    # 學習狀態
    active_learning_patterns: List[str] = Field(default_factory=list, description="活躍學習模式ID列表")
    knowledge_graph_size: int = Field(default=0, description="知識圖譜大小")
    total_interactions: int = Field(default=0, description="總互動次數")
    
    # 性能指標
    overall_performance_score: float = Field(default=0.5, description="整體性能評分", ge=0.0, le=1.0)
    learning_efficiency: float = Field(default=0.5, description="學習效率", ge=0.0, le=1.0)
    adaptation_speed: float = Field(default=0.5, description="適應速度", ge=0.0, le=1.0)
    
    # 進化歷史
    evolution_history: List[str] = Field(default_factory=list, description="進化記錄ID列表")
    last_major_evolution: Optional[datetime] = Field(None, description="最後重大進化時間")
    
    # 系統健康度
    cognitive_health_score: float = Field(default=1.0, description="認知健康度", ge=0.0, le=1.0)
    moral_consistency_score: float = Field(default=1.0, description="道德一致性評分", ge=0.0, le=1.0)
    knowledge_coherence_score: float = Field(default=1.0, description="知識連貫性評分", ge=0.0, le=1.0)
    
    # 時間戳
    created_at: datetime = Field(default_factory=datetime.now, description="創建時間")
    last_updated: datetime = Field(default_factory=datetime.now, description="最後更新時間")
    
    def update_performance_metrics(self, new_metrics: Dict[str, float]) -> None:
        """更新性能指標"""
        for metric, value in new_metrics.items():
            if hasattr(self, metric):
                setattr(self, metric, value)
        self.last_updated = datetime.now()
    
    def add_evolution_record(self, record_id: str) -> None:
        """添加進化記錄"""
        self.evolution_history.append(record_id)
        self.last_major_evolution = datetime.now()
        self.last_updated = datetime.now()
    
    def get_health_summary(self) -> Dict[str, float]:
        """獲取健康度摘要"""
        return {
            "cognitive_health": self.cognitive_health_score,
            "moral_consistency": self.moral_consistency_score,
            "knowledge_coherence": self.knowledge_coherence_score,
            "overall_performance": self.overall_performance_score,
            "learning_efficiency": self.learning_efficiency,
            "adaptation_speed": self.adaptation_speed
        }