# file: src/core/knowledge_base_module.py
import time
from datetime import datetime
from src.schemas.source_trace import TraceStep, TraceStatus, TrustLevel


class KnowledgeBaseModule:
    """知識庫模組 - 處理事實性查詢"""
    
    def __init__(self):
        self.module_name = "KnowledgeBaseModule"
        self.version = "v0.1"
    
    def process(self, router_output: dict) -> dict:
        """
        處理知識庫查詢
        
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
            # 簡單的知識查詢處理邏輯
            response = self._query_knowledge_base(original_sentence)
            status = TraceStatus.SUCCESS
            evidence = f"Knowledge base queried for: '{original_sentence[:50]}...'"
            trust_level = TrustLevel.B
            
        except Exception as e:
            response = "抱歉，我在知識庫中找不到相關資訊。"
            status = TraceStatus.FAIL
            evidence = f"Knowledge base query failed: {str(e)}"
            trust_level = TrustLevel.C
        
        # 計算執行時間
        latency_ms = int((time.time() - start_time) * 1000)
        
        # 記錄追溯步驟
        kb_step = TraceStep(
            tool=f"core.{self.module_name}.{self.version}",
            status=status,
            evidence=evidence,
            trust_level=trust_level,
            latency_ms=latency_ms,
            ts=datetime.now()
        )
        source_trace.steps.append(kb_step)
        
        # 構建輸出
        result = router_output.copy()
        result.update({
            "module_response": response,
            "processing_status": "knowledge_base_processed",
            "source_trace": source_trace
        })
        
        return result
    
    def _query_knowledge_base(self, query: str) -> str:
        """查詢知識庫（基礎版本）"""
        if "人工智慧" in query or "AI" in query:
            return "人工智慧是一種模擬人類智能的技術，包括機器學習、深度學習等領域。"
        elif "程式設計" in query:
            return "程式設計是創建電腦程式的過程，涉及邏輯思維和問題解決能力。"
        else:
            return "這是一個有趣的問題，讓我為您查找相關資訊。"