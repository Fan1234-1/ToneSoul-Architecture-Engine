# file: src/core/qa_module.py
import time
from datetime import datetime
from src.schemas.source_trace import TraceStep, TraceStatus, TrustLevel


class QAModule:
    """問答模組 - 處理指導性問題和知識查詢"""
    
    def __init__(self):
        self.module_name = "QAModule"
        self.version = "v0.1"
    
    def process(self, router_output: dict) -> dict:
        """
        處理問答請求
        
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
            # 簡單的問答處理邏輯
            response = self._generate_qa_response(original_sentence)
            status = TraceStatus.SUCCESS
            evidence = f"QA Module processed question: '{original_sentence[:50]}...'"
            trust_level = TrustLevel.B
            
        except Exception as e:
            response = "抱歉，我無法回答這個問題。"
            status = TraceStatus.FAIL
            evidence = f"QA processing failed: {str(e)}"
            trust_level = TrustLevel.C
        
        # 計算執行時間
        latency_ms = int((time.time() - start_time) * 1000)
        
        # 記錄追溯步驟
        qa_step = TraceStep(
            tool=f"core.{self.module_name}.{self.version}",
            status=status,
            evidence=evidence,
            trust_level=trust_level,
            latency_ms=latency_ms,
            ts=datetime.now()
        )
        source_trace.steps.append(qa_step)
        
        # 構建輸出
        result = router_output.copy()
        result.update({
            "module_response": response,
            "processing_status": "qa_processed",
            "source_trace": source_trace
        })
        
        return result
    
    def _generate_qa_response(self, question: str) -> str:
        """生成問答回應（基礎版本）"""
        if "如何" in question:
            return "這是一個很好的問題。建議您可以通過以下步驟來解決..."
        elif "什麼" in question:
            return "根據我的理解，這個概念是指..."
        else:
            return "感謝您的提問，我會盡力為您提供幫助。"