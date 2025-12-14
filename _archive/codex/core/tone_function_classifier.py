# file: src/core/tone_function_classifier.py
import time
from datetime import datetime
from enum import Enum
from src.schemas.source_trace import SourceTrace, TraceStep, TraceStatus, TrustLevel


class ToneFunction(str, Enum):
    """定義語魂系統的功能分類枚舉"""
    # 資訊尋求類
    INSTRUCTIONAL = "instructional"          # 如何做某事
    FACTUAL_INQUIRY = "factual_inquiry"      # 事實性問題
    OPINION_SEEKING = "opinion_seeking"      # 尋求意見
    
    # 承諾與宣告類
    VOW_DECLARATION = "vow_declaration"      # 承諾、保證
    STATEMENT_DECLARATION = "statement_declaration"  # 陳述性宣告
    
    # 情感表達類
    EMOTIONAL_VENT = "emotional_vent"        # 情感宣洩
    APPRECIATION = "appreciation"            # 感謝、讚美
    COMPLAINT = "complaint"                  # 抱怨、不滿
    
    # 行動請求類
    ACTION_REQUEST = "action_request"        # 請求執行動作
    ASSISTANCE_SEEKING = "assistance_seeking" # 尋求協助
    
    # 其他
    CASUAL_CHAT = "casual_chat"             # 閒聊
    UNKNOWN = "unknown"                     # 無法分類


class ToneFunctionClassifier:
    """語魂系統的理解中枢，負責將初步分析結果轉化為明確的功能意圖"""
    
    def __init__(self):
        # 定義關鍵字模式
        self.vow_keywords = ["我承諾", "我保證", "我發誓", "我答應"]
        self.appreciation_keywords = ["謝謝", "感謝", "太好了", "很棒", "讚"]
        self.complaint_keywords = ["討厭", "煩", "糟糕", "不滿", "抱怨"]
        self.instructional_keywords = ["如何", "怎麼做", "怎樣做", "怎麼辦"]
        self.factual_keywords = ["什麼", "為什麼", "哪裡", "誰", "何時"]
        self.opinion_keywords = ["怎麼樣", "覺得", "認為", "看法", "意見"]
        self.assistance_keywords = ["請幫我", "幫忙", "協助", "支援"]
        self.casual_keywords = ["你好", "嗨", "哈囉", "早安", "晚安"]
    
    def classify(self, bridge_output: dict) -> dict:
        """
        分析 ToneBridge 的輸出，返回功能分類結果
        
        Args:
            bridge_output: ToneBridge 返回的字典，包含 intent_type, source_trace 等
            
        Returns:
            更新後的字典，包含 tone_function 和更新的 source_trace
        """
        start_time = time.time()
        
        # 提取必要資訊
        intent_type = bridge_output.get("intent_type", "")
        sentence = bridge_output.get("original_sentence", "")
        source_trace = bridge_output.get("source_trace")
        
        if not source_trace:
            raise ValueError("Missing source_trace in bridge_output")
        
        try:
            # 執行分類邏輯
            tone_function = self._classify_function(intent_type, sentence)
            status = TraceStatus.SUCCESS
            evidence = f"Classified as {tone_function.value} based on intent_type='{intent_type}'"
            trust_level = TrustLevel.C
            
        except Exception as e:
            tone_function = ToneFunction.UNKNOWN
            status = TraceStatus.FAIL
            evidence = f"Classification failed: {str(e)}"
            trust_level = TrustLevel.C
        
        # 計算執行時間
        latency_ms = int((time.time() - start_time) * 1000)
        
        # 記錄追溯步驟
        classification_step = TraceStep(
            tool="core.ToneFunctionClassifier.v0.1",
            status=status,
            evidence=evidence,
            trust_level=trust_level,
            latency_ms=latency_ms,
            ts=datetime.now()
        )
        source_trace.steps.append(classification_step)
        
        # 構建輸出
        result = bridge_output.copy()
        result.update({
            "tone_function": tone_function,
            "source_trace": source_trace
        })
        
        return result
    
    def _classify_function(self, intent_type: str, sentence: str) -> ToneFunction:
        """
        基於優先級的多層次分類邏輯
        
        Args:
            intent_type: ToneBridge 識別的意圖類型
            sentence: 原始句子
            
        Returns:
            分類結果
        """
        # 處理邊界情況
        if not sentence or not sentence.strip():
            return ToneFunction.UNKNOWN
        
        sentence = sentence.strip()
        
        # 第一優先級：明確的關鍵字模式
        
        # 承諾類關鍵字
        if any(keyword in sentence for keyword in self.vow_keywords):
            return ToneFunction.VOW_DECLARATION
        
        # 感謝類關鍵字
        if any(keyword in sentence for keyword in self.appreciation_keywords):
            return ToneFunction.APPRECIATION
        
        # 抱怨類關鍵字
        if any(keyword in sentence for keyword in self.complaint_keywords):
            return ToneFunction.COMPLAINT
        
        # 協助請求關鍵字
        if any(keyword in sentence for keyword in self.assistance_keywords):
            return ToneFunction.ASSISTANCE_SEEKING
        
        # 第二優先級：基於 intent_type 的分類
        
        if intent_type == "question":
            # 尋求意見問題（優先檢查）
            if any(keyword in sentence for keyword in self.opinion_keywords):
                return ToneFunction.OPINION_SEEKING
            # 指導性問題
            elif any(keyword in sentence for keyword in self.instructional_keywords):
                return ToneFunction.INSTRUCTIONAL
            # 事實性問題
            elif any(keyword in sentence for keyword in self.factual_keywords):
                return ToneFunction.FACTUAL_INQUIRY
            # 其他問題視為尋求意見
            else:
                return ToneFunction.OPINION_SEEKING
        
        elif intent_type == "request":
            return ToneFunction.ACTION_REQUEST
        
        elif intent_type == "statement":
            # 檢查是否為閒聊
            if any(keyword in sentence for keyword in self.casual_keywords):
                return ToneFunction.CASUAL_CHAT
            # 其他陳述視為宣告
            else:
                return ToneFunction.STATEMENT_DECLARATION
        
        # 預設情況
        return ToneFunction.UNKNOWN