# file: src/core/statement_processor_module.py
import time
from datetime import datetime
from src.schemas.source_trace import TraceStep, TraceStatus, TrustLevel


class StatementProcessorModule:
    """陳述處理模組 - 處理一般陳述和宣告"""
    
    def __init__(self):
        self.module_name = "StatementProcessorModule"
        self.version = "v0.1"
    
    def process(self, router_output: dict) -> dict:
        """
        處理陳述
        
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
            # 簡單的陳述處理邏輯
            response = self._process_statement(original_sentence)
            status = TraceStatus.SUCCESS
            evidence = f"Statement processed and acknowledged"
            trust_level = TrustLevel.B
            
        except Exception as e:
            response = "我已經記錄了您的陳述。"
            status = TraceStatus.FAIL
            evidence = f"Statement processing failed: {str(e)}"
            trust_level = TrustLevel.C
        
        # 計算執行時間
        latency_ms = int((time.time() - start_time) * 1000)
        
        # 記錄追溯步驟
        statement_step = TraceStep(
            tool=f"core.{self.module_name}.{self.version}",
            status=status,
            evidence=evidence,
            trust_level=trust_level,
            latency_ms=latency_ms,
            ts=datetime.now()
        )
        source_trace.steps.append(statement_step)
        
        # 構建輸出
        result = router_output.copy()
        result.update({
            "module_response": response,
            "processing_status": "statement_processed",
            "source_trace": source_trace
        })
        
        return result
    
    def _process_statement(self, statement_text: str) -> str:
        """處理陳述（基礎版本）"""
        if "我認為" in statement_text or "我覺得" in statement_text:
            return "我理解您的觀點。這是一個很有見地的想法。"
        elif "事實上" in statement_text or "實際上" in statement_text:
            return "感謝您分享這個資訊。我會將此納入考慮。"
        elif "我想" in statement_text:
            return "我聽到了您的想法。請繼續分享您的見解。"
        else:
            return "我已經記錄了您的陳述。如果您有更多想法，我很樂意聆聽。"