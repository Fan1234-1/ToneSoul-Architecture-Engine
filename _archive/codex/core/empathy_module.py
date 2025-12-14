# file: src/core/empathy_module.py
import time
from datetime import datetime
from src.schemas.source_trace import TraceStep, TraceStatus, TrustLevel


class EmpathyModule:
    """同理心模組 - 處理情感宣洩和情緒支持"""
    
    def __init__(self):
        self.module_name = "EmpathyModule"
        self.version = "v0.1"
    
    def process(self, router_output: dict) -> dict:
        """
        處理情感支持請求
        
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
            # 簡單的同理心回應邏輯
            response = self._generate_empathetic_response(original_sentence)
            status = TraceStatus.SUCCESS
            evidence = f"Empathetic response generated for emotional content"
            trust_level = TrustLevel.A  # 情感支持需要高信任度
            
        except Exception as e:
            response = "我理解您的感受，請讓我陪伴您。"
            status = TraceStatus.FAIL
            evidence = f"Empathy response generation failed: {str(e)}"
            trust_level = TrustLevel.C
        
        # 計算執行時間
        latency_ms = int((time.time() - start_time) * 1000)
        
        # 記錄追溯步驟
        empathy_step = TraceStep(
            tool=f"core.{self.module_name}.{self.version}",
            status=status,
            evidence=evidence,
            trust_level=trust_level,
            latency_ms=latency_ms,
            ts=datetime.now()
        )
        source_trace.steps.append(empathy_step)
        
        # 構建輸出
        result = router_output.copy()
        result.update({
            "module_response": response,
            "processing_status": "empathy_processed",
            "source_trace": source_trace
        })
        
        return result
    
    def _generate_empathetic_response(self, emotional_text: str) -> str:
        """生成同理心回應（基礎版本）"""
        if any(word in emotional_text for word in ["難過", "傷心", "沮喪"]):
            return "我能感受到您的難過。情感是人類寶貴的體驗，請允許自己感受這些情緒。"
        elif any(word in emotional_text for word in ["生氣", "憤怒", "不滿"]):
            return "我理解您的憤怒。有時候表達情感是很重要的，我在這裡傾聽您。"
        elif any(word in emotional_text for word in ["焦慮", "擔心", "害怕"]):
            return "我感受到您的擔憂。焦慮是正常的情感反應，讓我們一起面對這些感受。"
        else:
            return "我能感受到您的情感。無論您現在感受如何，我都在這裡支持您。"