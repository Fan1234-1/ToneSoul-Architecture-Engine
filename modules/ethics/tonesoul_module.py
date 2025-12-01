# 魂語模組 - ToneSoul Module
# 核心協同接口與誓語流程實現

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

class SoulIntegrity(Enum):
    """魂語誠信檢查"""
    VERIFIED = "verified"
    PENDING = "pending"
    FAILED = "failed"

@dataclass
class SoulVow:
    """誓語結構 - 責任鏈的起點"""
    vow_id: str
    content: str
    source: str  # 源點責任
    timestamp: str
    integrity_hash: str
    status: SoulIntegrity = SoulIntegrity.PENDING

@dataclass
class SoulCheckpoint:
    """魂語誠信檢查點"""
    checkpoint_id: str
    vow_id: str
    verification_time: str
    result: bool
    checker: str
    notes: str = ""

class ToneSoulModule:
    """魂語模組 - 核心協同接口"""
    
    def __init__(self):
        self.vows: Dict[str, SoulVow] = {}
        self.checkpoints: Dict[str, SoulCheckpoint] = {}
        self.responsibility_chain: List[str] = []
        self.listeners: List[Callable] = []
    
    def register_listener(self, callback: Callable):
        """註冊誓語監聽器"""
        self.listeners.append(callback)
    
    def create_vow(self, content: str, source: str) -> SoulVow:
        """創建新的誓語"""
        vow_id = self._generate_id()
        integrity_hash = self._compute_integrity(content + source)
        
        vow = SoulVow(
            vow_id=vow_id,
            content=content,
            source=source,
            timestamp=datetime.now().isoformat(),
            integrity_hash=integrity_hash
        )
        
        self.vows[vow_id] = vow
        self._notify_listeners("vow_created", vow)
        return vow
    
    def verify_vow(self, vow_id: str, checker: str) -> bool:
        """驗證誓語的誠信"""
        if vow_id not in self.vows:
            return False
        
        vow = self.vows[vow_id]
        recomputed_hash = self._compute_integrity(vow.content + vow.source)
        result = recomputed_hash == vow.integrity_hash
        
        checkpoint = SoulCheckpoint(
            checkpoint_id=self._generate_id(),
            vow_id=vow_id,
            verification_time=datetime.now().isoformat(),
            result=result,
            checker=checker
        )
        
        self.checkpoints[checkpoint.checkpoint_id] = checkpoint
        if result:
            vow.status = SoulIntegrity.VERIFIED
        else:
            vow.status = SoulIntegrity.FAILED
        
        self._notify_listeners("vow_verified", {"vow": vow, "checkpoint": checkpoint})
        return result
    
    def add_to_responsibility_chain(self, actor: str):
        """添加到責任鏈"""
        self.responsibility_chain.append(actor)
        self._notify_listeners("chain_updated", {"actor": actor, "chain": self.responsibility_chain})
    
    def get_vow(self, vow_id: str) -> Optional[SoulVow]:
        """獲取誓語"""
        return self.vows.get(vow_id)
    
    def get_vow_history(self, vow_id: str) -> Dict:
        """獲取誓語的完整歷史"""
        vow = self.vows.get(vow_id)
        if not vow:
            return {}
        
        related_checkpoints = [
            asdict(cp) for cp in self.checkpoints.values() 
            if cp.vow_id == vow_id
        ]
        
        return {
            "vow": asdict(vow),
            "checkpoints": related_checkpoints,
            "responsibility_chain": self.responsibility_chain
        }
    
    def _generate_id(self) -> str:
        """生成唯一ID"""
        timestamp = datetime.now().isoformat()
        return hashlib.sha256(timestamp.encode()).hexdigest()[:16]
    
    def _compute_integrity(self, data: str) -> str:
        """計算數據完整性"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _notify_listeners(self, event: str, data):
        """通知所有監聽器"""
        for listener in self.listeners:
            try:
                listener(event, data)
            except Exception as e:
                print(f"Listener error: {e}")

# 使用示例
if __name__ == "__main__":
    module = ToneSoulModule()
    
    # 註冊監聽器
    def log_events(event, data):
        print(f"[{event}] {json.dumps(data if isinstance(data, dict) else str(data), ensure_ascii=False, indent=2)}")
    
    module.register_listener(log_events)
    
    # 創建誓語
    vow = module.create_vow("確保AI倫理決策透明性", "core_system")
    print(f"Created Vow: {vow.vow_id}")
    
    # 驗證誓語
    is_valid = module.verify_vow(vow.vow_id, "ethics_checker")
    print(f"Vow Valid: {is_valid}")
    
    # 添加責任鏈
    module.add_to_responsibility_chain("AI_Ethics_Board")
    module.add_to_responsibility_chain("Compliance_Team")
    
    # 獲取完整歷史
    history = module.get_vow_history(vow.vow_id)
    print(f"Vow History: {json.dumps(history, ensure_ascii=False, indent=2)}")
