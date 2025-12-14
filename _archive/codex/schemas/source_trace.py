from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class TraceStatus(str, Enum):
    """定義追溯步驟的成功或失敗狀態"""
    SUCCESS = "success"
    FAIL = "fail"


class TrustLevel(str, Enum):
    """定義證據的信任等級 (A/B/C)"""
    A = "A"  # Highest trust - verified external sources
    B = "B"  # Medium trust - internal processing with validation
    C = "C"  # Lower trust - heuristic or unverified sources


class TraceStep(BaseModel):
    """
    定義追溯鏈中的單一步驟。
    每個步驟代表一次工具調用或內部處理。
    """
    tool: str = Field(..., description="使用的工具名稱, 例如 'web.run', 'file_search', 'self.reflection_engine'")
    status: TraceStatus = Field(..., description="該步驟的執行狀態")
    input_digest: str | None = Field(None, description="輸入內容的 SHA256 摘要, 用於驗證唯一性")
    evidence: str = Field(..., description="該步驟產生的證據或日誌摘要")
    trust_level: TrustLevel = Field(..., description="該證據的信任等級")
    latency_ms: int = Field(..., description="該步驟的執行耗時 (毫秒)")
    ts: datetime = Field(..., description="該步驟完成時的 ISO8601 時間戳")


class SourceTrace(BaseModel):
    """
    SourceTrace 協議的根物件。
    它是一個不可變的列表, 記錄了從初始請求到最終輸出的完整責任鏈。
    """
    id: str = Field(..., description="本次追溯鏈的唯一 UUID")
    steps: List[TraceStep] = Field(..., description="組成追溯鏈的步驟列表")