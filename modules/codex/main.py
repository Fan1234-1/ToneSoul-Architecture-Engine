# file: src/main.py
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

# 導入核心服務
from src.core.tone_bridge import ToneBridge
from src.core.tone_function_classifier import ToneFunctionClassifier, ToneFunction
from src.core.tone_strategic_router import ToneStrategicRouter
from src.core.vow_checker import VowChecker

# 導入功能模組
from src.core.qa_module import QAModule
from src.core.knowledge_base_module import KnowledgeBaseModule
from src.core.reflection_module import ReflectionModule
from src.core.empathy_module import EmpathyModule
from src.core.gratitude_handler_module import GratitudeHandlerModule
from src.core.complaint_handler_module import ComplaintHandlerModule
from src.core.action_executor_module import ActionExecutorModule
from src.core.assistance_module import AssistanceModule
from src.core.conversation_module import ConversationModule
from src.core.statement_processor_module import StatementProcessorModule
from src.core.default_handler_module import DefaultHandlerModule

# 導入進化模組
from src.core.adaptive_learning_module import AdaptiveLearningModule
from src.core.metacognitive_module import MetacognitiveModule
from src.core.knowledge_evolution_module import KnowledgeEvolutionModule

# 導入數據模型
from src.schemas.source_trace import SourceTrace, TraceStep
from src.schemas.vow_object import VowObject

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API 數據模型
class ProcessRequest(BaseModel):
    """處理請求的數據模型"""
    sentence: str = Field(..., description="用戶輸入的句子", min_length=1, max_length=500)
    trace_id: Optional[str] = Field(None, description="可選的追溯 ID")

class TraceStepResponse(BaseModel):
    """追溯步驟的響應模型"""
    tool: str
    status: str
    evidence: str
    trust_level: str
    latency_ms: int
    timestamp: datetime

class ProcessResponse(BaseModel):
    """處理響應的數據模型"""
    success: bool = Field(..., description="處理是否成功")
    trace_id: str = Field(..., description="追溯 ID")
    original_sentence: str = Field(..., description="原始輸入句子")
    intent_type: str = Field(..., description="意圖類型")
    tone_function: str = Field(..., description="功能分類")
    next_strategy: Dict[str, Any] = Field(..., description="路由策略")
    module_response: str = Field(..., description="模組回應")
    processing_status: str = Field(..., description="處理狀態")
    vow_object: Optional[Dict[str, Any]] = Field(None, description="誓言物件（如果適用）")
    source_trace: List[TraceStepResponse] = Field(..., description="完整的追溯鏈")
    total_latency_ms: int = Field(..., description="總處理時間")

class HealthResponse(BaseModel):
    """健康檢查響應模型"""
    status: str
    timestamp: datetime
    version: str

# 創建 FastAPI 應用
app = FastAPI(
    title="ToneSoul System API",
    description="語魂系統 - 具備道德記憶的 AI 處理系統",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

class ToneSoulService:
    """語魂系統服務類"""
    
    def __init__(self):
        # 初始化核心服務
        self.bridge = ToneBridge()
        self.classifier = ToneFunctionClassifier()
        self.router = ToneStrategicRouter()
        self.vow_checker = VowChecker()
        
        # 初始化進化模組
        self.adaptive_learning = AdaptiveLearningModule()
        self.metacognitive = MetacognitiveModule()
        self.knowledge_evolution = KnowledgeEvolutionModule()
        
        # 初始化功能模組
        self.modules = {
            "qa_module": QAModule(),
            "knowledge_base_module": KnowledgeBaseModule(),
            "reflection_module": ReflectionModule(),
            "empathy_module": EmpathyModule(),
            "gratitude_handler_module": GratitudeHandlerModule(),
            "complaint_handler_module": ComplaintHandlerModule(),
            "action_executor_module": ActionExecutorModule(),
            "assistance_module": AssistanceModule(),
            "conversation_module": ConversationModule(),
            "statement_processor_module": StatementProcessorModule(),
            "default_handler_module": DefaultHandlerModule(),
            "vow_checker_module": self.vow_checker  # VowChecker 特殊處理
        }
        
        logger.info("ToneSoul System initialized with all modules and evolution capabilities")
    
    def process_sentence(self, sentence: str, trace_id: Optional[str] = None) -> Dict[str, Any]:
        """
        處理用戶輸入的完整流程
        
        Args:
            sentence: 用戶輸入的句子
            trace_id: 可選的追溯 ID
            
        Returns:
            完整的處理結果
        """
        start_time = datetime.now()
        
        try:
            # 第一步：ToneBridge 感知
            logger.info(f"Processing sentence: '{sentence[:50]}...'")
            bridge_output = self.bridge.analyze(sentence, trace_id)
            
            # 第二步：ToneFunctionClassifier 理解
            classifier_output = self.classifier.classify(bridge_output)
            
            # 第三步：ToneStrategicRouter 決策
            router_output = self.router.route(classifier_output)
            
            # 第四步：功能模組執行
            next_module = router_output["next_strategy"]["next_module"]
            
            if next_module in self.modules:
                module = self.modules[next_module]
                # VowChecker 使用特殊的方法名
                if next_module == "vow_checker_module":
                    final_output = module.process_vow(router_output)
                else:
                    final_output = module.process(router_output)
            else:
                # 回退到預設處理模組
                logger.warning(f"Module {next_module} not found, using default handler")
                final_output = self.modules["default_handler_module"].process(router_output)
            
            # 計算總處理時間
            total_latency = int((datetime.now() - start_time).total_seconds() * 1000)
            
            # 執行進化處理
            evolution_context = {
                "original_sentence": sentence,
                "intent_type": final_output.get("intent_type", "unknown"),
                "tone_function": final_output.get("tone_function", ToneFunction.UNKNOWN).value,
                "processing_success": True,
                "user_satisfaction": 0.8,  # 默認滿意度
                "response_time": total_latency
            }
            
            # 自適應學習
            learning_results = self.adaptive_learning.process_interaction(
                final_output["source_trace"], evolution_context
            )
            
            # 元認知監控
            metacognitive_results = self.metacognitive.monitor_cognitive_process(
                final_output["source_trace"], evolution_context
            )
            
            # 知識進化
            knowledge_evolution_results = self.knowledge_evolution.process_knowledge_evolution(
                final_output["source_trace"], evolution_context
            )
            
            # 構建響應
            response = {
                "success": True,
                "trace_id": final_output["source_trace"].id,
                "original_sentence": sentence,
                "intent_type": final_output.get("intent_type", "unknown"),
                "tone_function": final_output.get("tone_function", ToneFunction.UNKNOWN).value,
                "next_strategy": final_output.get("next_strategy", {}),
                "module_response": final_output.get("module_response", "處理完成"),
                "processing_status": final_output.get("processing_status", "completed"),
                "vow_object": self._serialize_vow_object(final_output.get("vow_object")),
                "source_trace": self._serialize_trace_steps(final_output["source_trace"].steps),
                "total_latency_ms": total_latency,
                # 進化能力結果
                "evolution_insights": {
                    "adaptive_learning": learning_results,
                    "metacognitive_analysis": metacognitive_results,
                    "knowledge_evolution": knowledge_evolution_results
                }
            }
            
            logger.info(f"Processing completed successfully in {total_latency}ms")
            return response
            
        except Exception as e:
            logger.error(f"Processing failed: {str(e)}")
            error_latency = int((datetime.now() - start_time).total_seconds() * 1000)
            
            return {
                "success": False,
                "trace_id": trace_id or "error",
                "original_sentence": sentence,
                "intent_type": "error",
                "tone_function": "error",
                "next_strategy": {},
                "module_response": f"處理失敗: {str(e)}",
                "processing_status": "error",
                "vow_object": None,
                "source_trace": [],
                "total_latency_ms": error_latency
            }
    
    def _serialize_vow_object(self, vow_object: Optional[VowObject]) -> Optional[Dict[str, Any]]:
        """序列化 VowObject"""
        if vow_object is None:
            return None
        
        return {
            "id": vow_object.id,
            "commitment": vow_object.commitment,
            "original_sentence": vow_object.original_sentence,
            "scope": vow_object.scope,
            "status": vow_object.status.value,
            "priority": vow_object.priority.value,
            "created_at": vow_object.created_at.isoformat(),
            "deadline": vow_object.deadline.isoformat() if vow_object.deadline else None,
            "confidence_score": vow_object.confidence_score
        }
    
    def _serialize_trace_steps(self, steps: List[TraceStep]) -> List[Dict[str, Any]]:
        """序列化追溯步驟"""
        return [
            {
                "tool": step.tool,
                "status": step.status.value,
                "evidence": step.evidence,
                "trust_level": step.trust_level.value,
                "latency_ms": step.latency_ms,
                "timestamp": step.ts.isoformat()
            }
            for step in steps
        ]

# 創建服務實例
tonesoul_service = ToneSoulService()

# API 端點
@app.get("/", response_model=Dict[str, str])
async def root():
    """根端點"""
    return {
        "message": "Welcome to ToneSoul System API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康檢查端點"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )

@app.post("/v1/process", response_model=ProcessResponse)
async def process_sentence(request: ProcessRequest):
    """
    核心處理端點 - 處理用戶輸入並返回完整的處理結果
    
    Args:
        request: 包含用戶輸入句子的請求
        
    Returns:
        完整的處理結果，包含追溯鏈
    """
    try:
        result = tonesoul_service.process_sentence(
            sentence=request.sentence,
            trace_id=request.trace_id
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["module_response"])
        
        return ProcessResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/v1/modules", response_model=Dict[str, List[str]])
async def list_modules():
    """列出所有可用的功能模組"""
    return {
        "available_modules": list(tonesoul_service.modules.keys()),
        "routing_table": list(tonesoul_service.router.get_available_routes().keys()),
        "evolution_modules": ["adaptive_learning", "metacognitive", "knowledge_evolution"]
    }

@app.get("/v1/evolution/status")
async def get_evolution_status():
    """獲取系統進化狀態"""
    try:
        return {
            "adaptive_learning": tonesoul_service.adaptive_learning.get_learning_insights(),
            "metacognitive": tonesoul_service.metacognitive.get_cognitive_summary(),
            "knowledge_evolution": tonesoul_service.knowledge_evolution.get_knowledge_summary(),
            "system_version": "1.0.0-evolution",
            "evolution_enabled": True
        }
    except Exception as e:
        logger.error(f"Evolution status error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get evolution status: {str(e)}")

@app.get("/v1/evolution/insights")
async def get_evolution_insights():
    """獲取進化洞察"""
    try:
        learning_insights = tonesoul_service.adaptive_learning.get_learning_insights()
        cognitive_summary = tonesoul_service.metacognitive.get_cognitive_summary()
        knowledge_summary = tonesoul_service.knowledge_evolution.get_knowledge_summary()
        
        return {
            "learning_patterns": learning_insights.get("most_active_patterns", []),
            "cognitive_state": cognitive_summary.get("current_state", "unknown"),
            "knowledge_health": knowledge_summary.get("knowledge_health_score", 0.0),
            "self_awareness_score": cognitive_summary.get("system_self_awareness_score", 0.0),
            "total_knowledge_nodes": knowledge_summary.get("total_knowledge_nodes", 0),
            "recent_adaptations": learning_insights.get("adaptation_history", []),
            "evolution_opportunities": knowledge_summary.get("evolution_stats", {})
        }
    except Exception as e:
        logger.error(f"Evolution insights error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get evolution insights: {str(e)}")

@app.post("/v1/evolution/reflect")
async def trigger_reflection():
    """手動觸發系統反思"""
    try:
        # 創建一個虛擬的追溯來觸發反思
        from src.schemas.source_trace import SourceTrace, TraceStep, TraceStatus, TrustLevel
        
        reflection_trace = SourceTrace(
            id=str(uuid.uuid4()),
            steps=[
                TraceStep(
                    tool="manual_reflection_trigger",
                    status=TraceStatus.SUCCESS,
                    evidence="Manual reflection triggered by user",
                    trust_level=TrustLevel.A,
                    latency_ms=0,
                    ts=datetime.now()
                )
            ]
        )
        
        reflection_context = {
            "trigger_type": "manual",
            "timestamp": datetime.now().isoformat(),
            "purpose": "system_health_check"
        }
        
        reflection_results = tonesoul_service.metacognitive.monitor_cognitive_process(
            reflection_trace, reflection_context
        )
        
        return {
            "reflection_triggered": True,
            "reflection_results": reflection_results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Manual reflection error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to trigger reflection: {str(e)}")

# 啟動配置
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )