from .models import YuHunState, TimeIsland

def build_prompt(
    state: YuHunState,
    island: TimeIsland,
    plan: dict,
    user_input: str,
) -> str:
    # system 區：告訴模型 YuHun 狀態 + 要求 meta
    system_block = f"""你是一個啟動 YuHun-Engine 的助理。

當前 Time-Island:
- id: {island.island_id}
- title: {island.title}
- kairos_tags: {", ".join(island.kairos_tags)}
- FS 向量: C={state.fs.C:.2f}, M={state.fs.M:.2f}, R={state.fs.R:.2f}, Γ={state.fs.Gamma:.2f}
- 當前模式建議: {plan["mode"]}

請在回答最後，用 [YUHUN_META] ... [/YUHUN_META] 區塊輸出：
- mode_used: 你實際採用的模式名稱（例如 Rational / CoSpeak / Audit）
- fs_delta: 你估計這次回答對 FS 四向量的影響（粗略即可）
- open_new_island: 是否建議開新島 (true/false)
- close_current_island: 是否建議關閉當前島 (true/false)
- recommend_tool: 若覺得需要額外工具，填 "python" / "web" / "none"
"""

    user_block = f"使用者說：{user_input}\n\n請先給出自然語言回答，再給出 YUHUN_META。"

    return system_block + "\n\n" + user_block
