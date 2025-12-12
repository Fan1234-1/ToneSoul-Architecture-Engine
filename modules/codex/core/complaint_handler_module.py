# file: src/core/complaint_handler_module.py
import time
from datetime import datetime
from src.schemas.source_trace import TraceStep, TraceStatus, TrustLevel


class ComplaintHandlerModule:
    """抱怨處理模組 - 處理不滿和抱怨表達"""
    
    def __init__(self):
        self.module_name = "ComplaintHandlerModule"
        self.version = "v0.1"
    
    def process(self, router_output: dict) -> dict:
        """
        處理抱怨表達
        
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
            # 簡單的抱怨處理邏輯
            response = self._generate_complaint_response(original_sentence)
            status = TraceStatus.SUCCESS
            evidence = f"Complaint acknowledged and addressed"
            trust_level = TrustLevel.A  # 抱怨處理需要高信任度
            
        except Exception as e:
            response = "我理解您的不滿，讓我們一起解決這個問題。"
            status = TraceStatus.FAIL
            evidence = f"Complaint response generation failed: {str(e)}"
            trust_level = TrustLevel.C
        
        # 計算執行時間
        latency_ms = int((time.time() - start_time) * 1000)
        
        # 記錄追溯步驟
        complaint_step = TraceStep(
            tool=f"core.{self.module_name}.{self.version}",
            status=status,
            evidence=evidence,
            trust_level=trust_level,
            latency_ms=latency_ms,
            ts=datetime.now()
        )
        source_trace.steps.append(complaint_step)
        
        # 構建輸出
        result = router_output.copy()
        result.update({
            "module_response": response,
            "processing_status": "complaint_processed",
            "source_trace": source_trace
        })
        
        return result
    
    def _generate_complaint_response(self, complaint_text: str) -> str:
        """生成抱怨回應（基礎版本）"""
        if "糟糕" in complaint_text or "爛" in complaint_text:
            return "我深表歉意讓您有這樣的體驗。請告訴我具體的問題，我會盡力改善。"
        elif "討厭" in complaint_text or "煩" in complaint_text:
            return "我理解您的困擾。讓我們找出問題的根源，並尋求解決方案。"
        elif "不滿" in complaint_text or "抱怨" in complaint_text:
            return "感謝您提出這個問題。您的反饋對我們的改進非常重要。"
        else:
            return "我聽到了您的關切。請讓我了解更多細節，以便我能更好地幫助您。"