import re
import yaml
from typing import Tuple
from .models import YuHunMeta

META_PATTERN = re.compile(r"\[YUHUN_META\](.*?)\[/YUHUN_META\]", re.DOTALL)

def extract_meta(response: str) -> Tuple[str, YuHunMeta]:
    match = META_PATTERN.search(response)
    if not match:
        # 沒有 meta 區塊，回傳原回答 + 預設 meta
        return response, YuHunMeta()

    meta_text = match.group(1).strip()
    # 先把 meta 區塊去掉，留給使用者的純文本
    clean_response = META_PATTERN.sub("", response).strip()

    # 嘗試用簡單 YAML 解析
    try:
        # Fix for potential markdown code blocks inside meta tag if model adds them
        meta_text = meta_text.replace("```yaml", "").replace("```", "").strip()
        
        data = yaml.safe_load(meta_text)
        if not isinstance(data, dict):
             data = {}
             
        meta = YuHunMeta(
            mode_used=data.get("mode_used", "Rational"),
            fs_delta=data.get("fs_delta", {"C": 0, "M": 0, "R": 0, "Gamma": 0}),
            open_new_island=data.get("open_new_island", False),
            close_current_island=data.get("close_current_island", False),
            recommend_tool=data.get("recommend_tool", "none"),
        )
    except Exception:
        meta = YuHunMeta()

    return clean_response, meta
