# file: src/core/vow_checker.py
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from src.schemas.vow_object import VowObject, WithdrawalConditions, VowStatus, VowPriority
from src.schemas.source_trace import SourceTrace, TraceStep, TraceStatus, TrustLevel


class VowChecker:
    """系統的契約官，負責承諾的解析、創建和管理"""
    
    def __init__(self):
        # 承諾解析模式
        self.commitment_patterns = {
            "我承諾": {"priority": VowPriority.HIGH, "confidence": 0.9},
            "我保證": {"priority": VowPriority.HIGH, "confidence": 0.9},
            "我發誓": {"priority": VowPriority.CRITICAL, "confidence": 0.95},
            "我答應": {"priority": VowPriority.MEDIUM, "confidence": 0.8}
        }
        
        # 預設撤回條件模板
        self.default_withdrawal_templates = {
            VowPriority.CRITICAL: WithdrawalConditions(
                conditions=["不可抗力", "系統性錯誤"],
                repair_owner="system_admin",
                deadline=None,
                repair_actions=["公開道歉", "制定補救措施"]
            ),
            VowPriority.HIGH: WithdrawalConditions(
                conditions=["重大變更", "技術限制"],
                repair_owner="module_owner",
                repair_actions=["解釋原因", "提供替代方案"]
            ),
            VowPriority.MEDIUM: WithdrawalConditions(
                conditions=["情況變更", "資源限制"],
                repair_owner="task_owner",
                repair_actions=["說明情況"]
            ),
            VowPriority.LOW: WithdrawalConditions(
                conditions=["一般變更"],
                repair_owner="user",
                repair_actions=["簡單說明"]
            )
        }
    
    def process_vow(self, classifier_output: dict) -> dict:
        """
        處理承諾宣告，創建 VowObject
        
        Args:
            classifier_output: ToneFunctionClassifier 的輸出字典
            
        Returns:
            包含新創建的 VowObject 和更新 SourceTrace 的字典
        """
        start_time = time.time()
        
        # 提取必要資訊
        original_sentence = classifier_output.get("original_sentence", "")
        source_trace = classifier_output.get("source_trace")
        
        if not source_trace:
            raise ValueError("Missing source_trace in classifier_output")
        
        try:
            # 解析承諾內容
            vow_data = self._parse_commitment(original_sentence)
            
            # 創建 VowObject
            vow_object = self._create_vow_object(vow_data, source_trace.id)
            
            status = TraceStatus.SUCCESS
            evidence = f"Created VowObject {vow_object.id} with commitment: '{vow_object.commitment}'"
            trust_level = TrustLevel.B
            
        except Exception as e:
            # 創建失敗時的處理
            vow_object = None
            status = TraceStatus.FAIL
            evidence = f"VowObject creation failed: {str(e)}"
            trust_level = TrustLevel.C
        
        # 計算執行時間
        latency_ms = int((time.time() - start_time) * 1000)
        
        # 記錄追溯步驟
        vow_step = TraceStep(
            tool="core.VowChecker.v0.1",
            status=status,
            evidence=evidence,
            trust_level=trust_level,
            latency_ms=latency_ms,
            ts=datetime.now()
        )
        source_trace.steps.append(vow_step)
        
        # 構建輸出
        result = classifier_output.copy()
        result.update({
            "vow_object": vow_object,
            "processing_result": "vow_created" if vow_object else "vow_creation_failed",
            "source_trace": source_trace
        })
        
        return result
    
    def _parse_commitment(self, sentence: str) -> Dict[str, Any]:
        """
        解析承諾內容的核心邏輯
        
        Args:
            sentence: 原始承諾語句
            
        Returns:
            解析後的承諾資料
        """
        if not sentence or not sentence.strip():
            raise ValueError("Empty sentence provided")
        
        sentence = sentence.strip()
        
        # 找到承諾關鍵字
        commitment_keyword = None
        for keyword in self.commitment_patterns:
            if keyword in sentence:
                commitment_keyword = keyword
                break
        
        if not commitment_keyword:
            raise ValueError("No commitment keyword found in sentence")
        
        # 提取承諾內容（關鍵字之後的部分）
        keyword_index = sentence.find(commitment_keyword)
        commitment_content = sentence[keyword_index + len(commitment_keyword):].strip()
        
        if not commitment_content:
            raise ValueError("No commitment content found after keyword")
        
        # 智慧範圍推斷（基礎版本）
        scope = self._infer_scope(commitment_content)
        
        # 期限推斷（基礎版本）
        deadline = self._extract_deadline(commitment_content)
        
        return {
            "keyword": commitment_keyword,
            "content": commitment_content,
            "scope": scope,
            "priority": self.commitment_patterns[commitment_keyword]["priority"],
            "confidence": self.commitment_patterns[commitment_keyword]["confidence"],
            "deadline": deadline
        }
    
    def _create_vow_object(self, vow_data: Dict[str, Any], source_trace_id: str) -> VowObject:
        """
        根據解析資料創建 VowObject
        
        Args:
            vow_data: 解析後的承諾資料
            source_trace_id: 關聯的 SourceTrace ID
            
        Returns:
            新創建的 VowObject
        """
        # 獲取對應優先級的撤回條件模板
        withdrawal_conditions = self.default_withdrawal_templates[vow_data["priority"]]
        
        return VowObject(
            commitment=vow_data["content"],
            original_sentence=vow_data["keyword"] + vow_data["content"],
            scope=vow_data["scope"],
            status=VowStatus.ACTIVE,
            priority=vow_data["priority"],
            deadline=vow_data.get("deadline"),
            withdrawal=withdrawal_conditions,
            bindings={"original_keyword": vow_data["keyword"]},
            source_trace_id=source_trace_id,
            confidence_score=vow_data["confidence"]
        )
    
    def _infer_scope(self, commitment_content: str) -> List[str]:
        """
        智慧推斷承諾範圍（基礎版本）
        
        Args:
            commitment_content: 承諾內容
            
        Returns:
            推斷的範圍列表
        """
        # TODO: 未來實作智慧推斷邏輯
        # 目前使用簡單的關鍵字匹配
        scope = ["general"]
        
        # 時間相關
        if any(word in commitment_content for word in ["明天", "今天", "下週", "本週"]):
            scope.append("time_bound")
        
        # 工作相關
        if any(word in commitment_content for word in ["完成", "交付", "實現", "做好"]):
            scope.append("task_completion")
        
        # 品質相關
        if any(word in commitment_content for word in ["品質", "標準", "要求", "準時"]):
            scope.append("quality_assurance")
        
        return scope
    
    def _extract_deadline(self, commitment_content: str) -> Optional[datetime]:
        """
        從承諾內容中提取期限（基礎版本）
        
        Args:
            commitment_content: 承諾內容
            
        Returns:
            推斷的期限時間，如果無法推斷則返回 None
        """
        # TODO: 未來實作更智慧的時間解析
        # 目前使用簡單的關鍵字匹配
        now = datetime.now()
        
        if "明天" in commitment_content:
            return now.replace(hour=23, minute=59, second=59) + timedelta(days=1)
        elif "今天" in commitment_content:
            return now.replace(hour=23, minute=59, second=59)
        elif "下週" in commitment_content:
            return now + timedelta(weeks=1)
        elif "本週" in commitment_content:
            # 本週末
            days_until_sunday = (6 - now.weekday()) % 7
            return now + timedelta(days=days_until_sunday, hours=23-now.hour, minutes=59-now.minute)
        
        return None
    
    def get_vow_summary(self, vow_object: VowObject) -> Dict[str, Any]:
        """
        獲取誓言摘要資訊
        
        Args:
            vow_object: VowObject 實例
            
        Returns:
            誓言摘要字典
        """
        return {
            "id": vow_object.id,
            "commitment": vow_object.commitment,
            "status": vow_object.status,
            "priority": vow_object.priority,
            "created_at": vow_object.created_at,
            "deadline": vow_object.deadline,
            "is_active": vow_object.is_active(),
            "is_expired": vow_object.is_expired()
        }