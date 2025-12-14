# file: src/core/conversation_module.py
import time
from datetime import datetime
from src.schemas.source_trace import TraceStep, TraceStatus, TrustLevel


class ConversationModule:
    """對話模組 - 處理閒聊和一般對話"""
    
    def __init__(self):
        self.module_name = "ConversationModule"
        self.version = "v0.1"
    
    def process(self, router_output: dict) -> dict:
        """
        處理對話請求
        
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
            # 簡單的對話處理邏輯
            response = self._generate_conversation_response(original_sentence)
            status = TraceStatus.SUCCESS
            evidence = f"Casual conversation engaged"
            trust_level = TrustLevel.B
            
        except Exception as e:
            response = "很高興和您聊天！"
            status = TraceStatus.FAIL
            evidence = f"Conversation generation failed: {str(e)}"
            trust_level = TrustLevel.C
        
        # 計算執行時間
        latency_ms = int((time.time() - start_time) * 1000)
        
        # 記錄追溯步驟
        conversation_step = TraceStep(
            tool=f"core.{self.module_name}.{self.version}",
            status=status,
            evidence=evidence,
            trust_level=trust_level,
            latency_ms=latency_ms,
            ts=datetime.now()
        )
        source_trace.steps.append(conversation_step)
        
        # 構建輸出
        result = router_output.copy()
        result.update({
            "module_response": response,
            "processing_status": "conversation_processed",
            "source_trace": source_trace
        })
        
        return result
    
    def _generate_conversation_response(self, conversation_text: str) -> str:
        """生成對話回應（基礎版本）"""
        if "你好" in conversation_text or "嗨" in conversation_text:
            return "你好！很高興見到您。今天過得怎麼樣？"
        elif "天氣" in conversation_text:
            return "是的，天氣確實是個不錯的話題。希望您今天有個美好的天氣！"
        elif "早安" in conversation_text:
            return "早安！希望您今天有個美好的開始。"
        elif "晚安" in conversation_text:
            return "晚安！祝您有個甜美的夢境。"
        else:
            return "很有趣的話題！我很享受和您的對話。"