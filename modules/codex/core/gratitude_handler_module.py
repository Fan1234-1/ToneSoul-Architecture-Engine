# file: src/core/gratitude_handler_module.py
import time
from datetime import datetime
from src.schemas.source_trace import TraceStep, TraceStatus, TrustLevel


class GratitudeHandlerModule:
    """感謝處理模組 - 處理感謝和讚美表達"""
    
    def __init__(self):
        self.module_name = "GratitudeHandlerModule"
        self.version = "v0.1"
    
    def process(self, router_output: dict) -> dict:
        """
        處理感謝表達
        
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
            # 簡單的感謝回應邏輯
            response = self._generate_gratitude_response(original_sentence)
            status = TraceStatus.SUCCESS
            evidence = f"Gratitude acknowledged and responded to"
            trust_level = TrustLevel.A  # 感謝回應需要高信任度
            
        except Exception as e:
            response = "謝謝您的善意，我很感激。"
            status = TraceStatus.FAIL
            evidence = f"Gratitude response generation failed: {str(e)}"
            trust_level = TrustLevel.C
        
        # 計算執行時間
        latency_ms = int((time.time() - start_time) * 1000)
        
        # 記錄追溯步驟
        gratitude_step = TraceStep(
            tool=f"core.{self.module_name}.{self.version}",
            status=status,
            evidence=evidence,
            trust_level=trust_level,
            latency_ms=latency_ms,
            ts=datetime.now()
        )
        source_trace.steps.append(gratitude_step)
        
        # 構建輸出
        result = router_output.copy()
        result.update({
            "module_response": response,
            "processing_status": "gratitude_processed",
            "source_trace": source_trace
        })
        
        return result
    
    def _generate_gratitude_response(self, gratitude_text: str) -> str:
        """生成感謝回應（基礎版本）"""
        if "謝謝" in gratitude_text or "感謝" in gratitude_text:
            return "不客氣！能夠幫助您是我的榮幸。如果還有其他需要，請隨時告訴我。"
        elif "太好了" in gratitude_text or "很棒" in gratitude_text:
            return "很高興能得到您的認可！我會繼續努力提供更好的服務。"
        elif "讚" in gratitude_text:
            return "謝謝您的讚美！這對我來說意義重大。"
        else:
            return "感謝您的正面回饋，這激勵我持續改進。"