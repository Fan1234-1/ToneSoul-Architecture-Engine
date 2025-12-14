# file: src/core/action_executor_module.py
import time
from datetime import datetime
from src.schemas.source_trace import TraceStep, TraceStatus, TrustLevel


class ActionExecutorModule:
    """行動執行模組 - 處理具體的行動請求"""
    
    def __init__(self):
        self.module_name = "ActionExecutorModule"
        self.version = "v0.1"
    
    def process(self, router_output: dict) -> dict:
        """
        處理行動執行請求
        
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
            # 簡單的行動執行邏輯
            response = self._execute_action(original_sentence)
            status = TraceStatus.SUCCESS
            evidence = f"Action execution attempted for: '{original_sentence[:50]}...'"
            trust_level = TrustLevel.B
            
        except Exception as e:
            response = "抱歉，我目前無法執行這個行動。"
            status = TraceStatus.FAIL
            evidence = f"Action execution failed: {str(e)}"
            trust_level = TrustLevel.C
        
        # 計算執行時間
        latency_ms = int((time.time() - start_time) * 1000)
        
        # 記錄追溯步驟
        action_step = TraceStep(
            tool=f"core.{self.module_name}.{self.version}",
            status=status,
            evidence=evidence,
            trust_level=trust_level,
            latency_ms=latency_ms,
            ts=datetime.now()
        )
        source_trace.steps.append(action_step)
        
        # 構建輸出
        result = router_output.copy()
        result.update({
            "module_response": response,
            "processing_status": "action_executed",
            "source_trace": source_trace
        })
        
        return result
    
    def _execute_action(self, action_request: str) -> str:
        """執行行動（基礎版本）"""
        if "開啟" in action_request or "打開" in action_request:
            return "我已經嘗試開啟您要求的項目。請檢查是否成功。"
        elif "關閉" in action_request:
            return "我已經嘗試關閉指定的項目。"
        elif "執行" in action_request or "運行" in action_request:
            return "我已經開始執行您要求的操作。"
        elif "停止" in action_request:
            return "我已經嘗試停止相關的操作。"
        else:
            return "我已經記錄了您的行動請求，正在處理中。"