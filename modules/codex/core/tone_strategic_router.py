# file: src/core/tone_strategic_router.py
import time
from datetime import datetime
from typing import Dict, Any
from src.core.tone_function_classifier import ToneFunction
from src.schemas.source_trace import SourceTrace, TraceStep, TraceStatus, TrustLevel


class RoutingStrategy:
    """路由策略的資料結構"""
    def __init__(self, next_module: str, priority: str = "medium", timeout_ms: int = 3000):
        self.next_module = next_module
        self.priority = priority
        self.timeout_ms = timeout_ms


class ToneStrategicRouter:
    """語魂系統的指揮中樞，負責根據功能意圖做出策略決策"""
    
    def __init__(self):
        # 定義路由表
        self.routing_table: Dict[ToneFunction, RoutingStrategy] = {
            # 資訊尋求類
            ToneFunction.INSTRUCTIONAL: RoutingStrategy(
                next_module="qa_module",
                priority="high",
                timeout_ms=5000
            ),
            ToneFunction.FACTUAL_INQUIRY: RoutingStrategy(
                next_module="knowledge_base_module",
                priority="high", 
                timeout_ms=4000
            ),
            ToneFunction.OPINION_SEEKING: RoutingStrategy(
                next_module="reflection_module",
                priority="medium",
                timeout_ms=3000
            ),
            
            # 承諾與宣告類
            ToneFunction.VOW_DECLARATION: RoutingStrategy(
                next_module="vow_checker_module",
                priority="high",
                timeout_ms=2000
            ),
            ToneFunction.STATEMENT_DECLARATION: RoutingStrategy(
                next_module="statement_processor_module",
                priority="low",
                timeout_ms=2000
            ),
            
            # 情感表達類
            ToneFunction.EMOTIONAL_VENT: RoutingStrategy(
                next_module="empathy_module",
                priority="high",
                timeout_ms=2000
            ),
            ToneFunction.APPRECIATION: RoutingStrategy(
                next_module="gratitude_handler_module",
                priority="medium",
                timeout_ms=1500
            ),
            ToneFunction.COMPLAINT: RoutingStrategy(
                next_module="complaint_handler_module",
                priority="high",
                timeout_ms=3000
            ),
            
            # 行動請求類
            ToneFunction.ACTION_REQUEST: RoutingStrategy(
                next_module="action_executor_module",
                priority="high",
                timeout_ms=4000
            ),
            ToneFunction.ASSISTANCE_SEEKING: RoutingStrategy(
                next_module="assistance_module",
                priority="high",
                timeout_ms=3500
            ),
            
            # 其他
            ToneFunction.CASUAL_CHAT: RoutingStrategy(
                next_module="conversation_module",
                priority="low",
                timeout_ms=2000
            )
        }
        
        # 預設回退策略
        self.fallback_strategy = RoutingStrategy(
            next_module="default_handler_module",
            priority="low",
            timeout_ms=2000
        )
    
    def route(self, classifier_output: dict) -> dict:
        """
        根據分類器輸出做出路由決策
        
        Args:
            classifier_output: ToneFunctionClassifier 返回的字典
            
        Returns:
            包含路由決策和更新 SourceTrace 的字典
        """
        start_time = time.time()
        
        # 提取必要資訊
        tone_function = classifier_output.get("tone_function")
        source_trace = classifier_output.get("source_trace")
        
        if not source_trace:
            raise ValueError("Missing source_trace in classifier_output")
        
        try:
            # 執行路由邏輯
            strategy = self._determine_strategy(tone_function)
            status = TraceStatus.SUCCESS
            
            if tone_function in self.routing_table:
                evidence = f"Routing to {strategy.next_module} based on function {tone_function.value}"
            else:
                evidence = f"Using fallback strategy: routing to {strategy.next_module} for unknown function {tone_function}"
            
            trust_level = TrustLevel.B  # 路由決策有較高的信任度
            
        except Exception as e:
            strategy = self.fallback_strategy
            status = TraceStatus.FAIL
            evidence = f"Routing failed: {str(e)}. Using fallback strategy."
            trust_level = TrustLevel.C
        
        # 計算執行時間
        latency_ms = int((time.time() - start_time) * 1000)
        
        # 記錄追溯步驟
        routing_step = TraceStep(
            tool="core.ToneStrategicRouter.v0.1",
            status=status,
            evidence=evidence,
            trust_level=trust_level,
            latency_ms=latency_ms,
            ts=datetime.now()
        )
        source_trace.steps.append(routing_step)
        
        # 構建最終輸出
        result = classifier_output.copy()
        result.update({
            "next_strategy": {
                "next_module": strategy.next_module,
                "priority": strategy.priority,
                "timeout_ms": strategy.timeout_ms
            },
            "source_trace": source_trace
        })
        
        return result
    
    def _determine_strategy(self, tone_function: ToneFunction) -> RoutingStrategy:
        """
        根據功能分類決定路由策略
        
        Args:
            tone_function: 功能分類結果
            
        Returns:
            對應的路由策略
        """
        if tone_function in self.routing_table:
            return self.routing_table[tone_function]
        else:
            # 使用回退策略
            return self.fallback_strategy
    
    def update_routing_table(self, tone_function: ToneFunction, strategy: RoutingStrategy):
        """
        動態更新路由表
        
        Args:
            tone_function: 要更新的功能分類
            strategy: 新的路由策略
        """
        self.routing_table[tone_function] = strategy
    
    def get_available_routes(self) -> Dict[str, str]:
        """
        獲取所有可用的路由映射
        
        Returns:
            功能分類到模組的映射字典
        """
        routes = {}
        for func, strategy in self.routing_table.items():
            routes[func.value] = strategy.next_module
        routes["fallback"] = self.fallback_strategy.next_module
        return routes