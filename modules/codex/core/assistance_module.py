# file: src/core/assistance_module.py
import time
from datetime import datetime
from src.schemas.source_trace import TraceStep, TraceStatus, TrustLevel


class AssistanceModule:
    """協助模組 - 處理尋求協助的請求"""
    
    def __init__(self):
        self.module_name = "AssistanceModule"
        self.version = "v0.1"
    
    def process(self, router_output: dict) -> dict:
        """
        處理協助請求
        
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
            # 簡單的協助提供邏輯
            response = self._provide_assistance(original_sentence)
            status = TraceStatus.SUCCESS
            evidence = f"Assistance provided for: '{original_sentence[:50]}...'"
            trust_level = TrustLevel.A  # 協助提供需要高信任度
            
        except Exception as e:
            response = "我很樂意幫助您，請告訴我更多詳細資訊。"
            status = TraceStatus.FAIL
            evidence = f"Assistance provision failed: {str(e)}"
            trust_level = TrustLevel.C
        
        # 計算執行時間
        latency_ms = int((time.time() - start_time) * 1000)
        
        # 記錄追溯步驟
        assistance_step = TraceStep(
            tool=f"core.{self.module_name}.{self.version}",
            status=status,
            evidence=evidence,
            trust_level=trust_level,
            latency_ms=latency_ms,
            ts=datetime.now()
        )
        source_trace.steps.append(assistance_step)
        
        # 構建輸出
        result = router_output.copy()
        result.update({
            "module_response": response,
            "processing_status": "assistance_provided",
            "source_trace": source_trace
        })
        
        return result
    
    def _provide_assistance(self, assistance_request: str) -> str:
        """提供協助（基礎版本）"""
        if "幫我" in assistance_request or "幫忙" in assistance_request:
            return "當然！我很樂意幫助您。請告訴我您需要什麼樣的協助。"
        elif "協助" in assistance_request:
            return "我在這裡為您提供協助。請詳細說明您遇到的問題。"
        elif "支援" in assistance_request:
            return "我會全力支援您。讓我們一起解決這個問題。"
        else:
            return "我理解您需要幫助。請讓我知道我能為您做些什麼。"