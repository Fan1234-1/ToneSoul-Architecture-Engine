# file: src/core/default_handler_module.py
import time
from datetime import datetime
from src.schemas.source_trace import TraceStep, TraceStatus, TrustLevel


class DefaultHandlerModule:
    """預設處理模組 - 處理無法分類的請求（回退策略）"""
    
    def __init__(self):
        self.module_name = "DefaultHandlerModule"
        self.version = "v0.1"
    
    def process(self, router_output: dict) -> dict:
        """
        處理預設情況
        
        Args:
            router_output: ToneStrategicRouter 的輸出字典
            
        Returns:
            包含處理結果和更新 SourceTrace 的字典
        """
        start_time = time.time()
        
        # 提取必要資訊
        original_sentence = router_output.get("original_sentence", "")
        source_trace = router_output.get("source_trace")
        
        if not source_trace:
            raise ValueError("Missing source_trace in router_output")
        
        try:
            # 簡單的預設處理邏輯
            response = self._generate_default_response(original_sentence)
            status = TraceStatus.SUCCESS
            evidence = f"Default handler processed unclassified input"
            trust_level = TrustLevel.C  # 預設處理的信任度較低
            
        except Exception as e:
            response = "我正在學習如何更好地理解您的需求。"
            status = TraceStatus.FAIL
            evidence = f"Default handling failed: {str(e)}"
            trust_level = TrustLevel.C
        
        # 計算執行時間
        latency_ms = int((time.time() - start_time) * 1000)
        
        # 記錄追溯步驟
        default_step = TraceStep(
            tool=f"core.{self.module_name}.{self.version}",
            status=status,
            evidence=evidence,
            trust_level=trust_level,
            latency_ms=latency_ms,
            ts=datetime.now()
        )
        source_trace.steps.append(default_step)
        
        # 構建輸出
        result = router_output.copy()
        result.update({
            "module_response": response,
            "processing_status": "default_processed",
            "source_trace": source_trace
        })
        
        return result
    
    def _generate_default_response(self, input_text: str) -> str:
        """生成預設回應（基礎版本）"""
        if len(input_text.strip()) == 0:
            return "我沒有收到明確的輸入。請告訴我您需要什麼幫助。"
        elif len(input_text) > 200:
            return "您提供了很多資訊。讓我仔細理解您的需求，然後為您提供適當的回應。"
        else:
            return "我理解您的輸入，但我需要更多資訊來提供最佳的回應。請告訴我更多詳細資訊。"