# file: src/schemas/vow_object.py
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class VowStatus(str, Enum):
    """誓言狀態枚舉"""
    ACTIVE = "active"           # 生效中
    FULFILLED = "fulfilled"     # 已履行
    WITHDRAWN = "withdrawn"     # 已撤回
    VIOLATED = "violated"       # 已違背
    EXPIRED = "expired"         # 已過期


class VowPriority(str, Enum):
    """誓言優先級"""
    CRITICAL = "critical"       # 關鍵承諾
    HIGH = "high"              # 高優先級
    MEDIUM = "medium"          # 中等優先級
    LOW = "low"                # 低優先級


class WithdrawalConditions(BaseModel):
    """撤回承諾的條件結構"""
    conditions: List[str] = Field(..., description="撤回承諾的條件列表")
    repair_owner: str = Field(..., description="負責修復或解釋的角色")
    deadline: Optional[datetime] = Field(None, description="修復的最後期限")
    repair_actions: List[str] = Field(default_factory=list, description="修復行動清單")


class VowObject(BaseModel):
    """誓言物件的完整資料結構"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="誓言的唯一 UUID")
    commitment: str = Field(..., description="承諾的具體內容")
    original_sentence: str = Field(..., description="原始承諾語句")
    scope: List[str] = Field(..., description="承諾的適用範圍或場景")
    
    # 狀態管理
    status: VowStatus = Field(default=VowStatus.ACTIVE, description="誓言當前狀態")
    priority: VowPriority = Field(default=VowPriority.MEDIUM, description="誓言優先級")
    
    # 時間管理
    created_at: datetime = Field(default_factory=datetime.now, description="創建時間")
    deadline: Optional[datetime] = Field(None, description="承諾履行期限")
    fulfilled_at: Optional[datetime] = Field(None, description="履行時間")
    
    # 條件與綁定
    withdrawal: WithdrawalConditions = Field(..., description="撤回承諾的詳細條件")
    bindings: Dict[str, Any] = Field(default_factory=dict, description="與此誓言綁定的其他系統對象")
    
    # 追溯與驗證
    source_trace_id: str = Field(..., description="關聯的 SourceTrace ID")
    confidence_score: float = Field(default=0.8, description="承諾解析的信心度", ge=0.0, le=1.0)
    
    def is_active(self) -> bool:
        """檢查誓言是否仍然生效"""
        return self.status == VowStatus.ACTIVE
    
    def is_expired(self) -> bool:
        """檢查誓言是否已過期"""
        if self.deadline and datetime.now() > self.deadline:
            return True
        return self.status == VowStatus.EXPIRED
    
    def fulfill(self) -> None:
        """標記誓言為已履行"""
        self.status = VowStatus.FULFILLED
        self.fulfilled_at = datetime.now()
    
    def withdraw(self) -> None:
        """撤回誓言"""
        self.status = VowStatus.WITHDRAWN