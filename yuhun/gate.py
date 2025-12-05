from .models import YuHunState

def estimate_delta_s(user_input: str) -> float:
    # 簡單版：長度 + 關鍵字粗估（之後可換成小模型）
    base = min(len(user_input) / 100.0, 1.0)
    if any(k in user_input for k in ["錢", "醫", "風險", "死", "Money", "Medical", "Risk", "Death"]):
        base += 0.3
    return min(base, 1.0)

def decide_mode(state: YuHunState, delta_s: float) -> str:
    # 粗略規則：
    # 張力高 → Rational / Audit
    # 張力低 → CoSpeak / Spark
    if delta_s > 0.7:
        return "Audit"
    elif delta_s > 0.4:
        return "Rational"
    else:
        return "CoSpeak"

def choose_model(state: YuHunState, mode: str) -> str:
    # 先簡單：一律用第一個
    if not state.available_models:
        return "gemma3:4b"
    return state.available_models[0]

def build_plan(state: YuHunState, user_input: str) -> dict:
    delta_s = estimate_delta_s(user_input)
    mode = decide_mode(state, delta_s)
    model = choose_model(state, mode)
    need_thinking = delta_s > 0.4
    return {
        "delta_s": delta_s,
        "mode": mode,
        "model": model,
        "need_thinking": need_thinking,
        "tools_to_consider": [],
    }
