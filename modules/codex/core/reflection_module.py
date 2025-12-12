# file: src/core/reflection_module.py
import time
from datetime import datetime
from src.schemas.source_trace import TraceStep, TraceStatus, TrustLevel


class ReflectionModule:
    """反思模組 - 處理意見尋求和深度思考"""
    
    def __init__(self):
        self.module_name = "ReflectionModule"
        self.version = "v0.1"
    
    def process(self, router_output: dict) -> dict:
        """
        處理反思請求
        
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
            # 簡單的反思處理邏輯
            response = self._generate_reflection(original_sentence)
            status = TraceStatus.SUCCESS
            evidence = f"Reflection generated for: '{original_sentence[:50]}...'"
            trust_level = TrustLevel.B
            
        except Exception as e:
            response = "讓我思考一下這個問題..."
            status = TraceStatus.FAIL
            evidence = f"Reflection generation failed: {str(e)}"
            trust_level = TrustLevel.C
        
        # 計算執行時間
        latency_ms = int((time.time() - start_time) * 1000)
        
        # 記錄追溯步驟
        reflection_step = TraceStep(
            tool=f"core.{self.module_name}.{self.version}",
            status=status,
            evidence=evidence,
            trust_level=trust_level,
            latency_ms=latency_ms,
            ts=datetime.now()
        )
        source_trace.steps.append(reflection_step)
        
        # 構建輸出
        result = router_output.copy()
        result.update({
            "module_response": response,
            "processing_status": "reflection_processed",
            "source_trace": source_trace
        })
        
        return result
    
    def _generate_reflection(self, input_text: str) -> str:
        """生成反思回應（基礎版本）"""
        if "怎麼樣" in input_text or "覺得" in input_text:
            return "這是一個值得深思的問題。從多個角度來看，我認為..."
        elif "意見" in input_text or "看法" in input_text:
            return "基於我的理解和分析，我的看法是..."
        else:
            return "讓我仔細思考這個問題的各個層面..."