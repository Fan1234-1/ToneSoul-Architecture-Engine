from datetime import datetime
import uuid
import sys

# Ensure we can import yuhun package
sys.path.append(".")

from yuhun.state_store import load_state, save_state, load_island, save_island, append_chronicle
from yuhun.ollama_client import generate
from yuhun.gate import build_plan
from yuhun.prompt_builder import build_prompt
from yuhun.meta_parser import extract_meta
from yuhun.models import ChronicleEntry, FSVector

def main():
    print("YuHun-Orchestrator v0.1 × Ollama")
    state = load_state()
    island = load_island(state.active_island)
    if island is None:
        # Fallback if state points to non-existent island (shouldn't happen with load_state logic but good for safety)
        print(f"Warning: Active island {state.active_island} not found. Creating new one.")
        island_id = str(uuid.uuid4())[:8]
        from yuhun.models import TimeIsland
        island = TimeIsland(
            island_id=island_id,
            created_at=datetime.utcnow().isoformat(),
            title="Recovered Island",
        )
        state.active_island = island_id
        save_island(island)
        save_state(state)

    while True:
        try:
            user_input = input("\n你：").strip()
        except EOFError:
            break
            
        if user_input.lower() in ("exit", "quit", "bye"):
            print("👋 結束對話。")
            break
        
        if not user_input:
            continue

        # 1. Gate
        plan = build_plan(state, user_input)

        # 2. 組 prompt
        prompt = build_prompt(state, island, plan, user_input)

        # 3. 呼叫 Ollama
        print(f"Thinking... (Mode: {plan['mode']}, Model: {plan['model']})")
        raw_response = generate(plan["model"], prompt)

        # 4. 拆出 meta
        clean_response, meta = extract_meta(raw_response)

        # 5. 更新 FS
        fs_before = FSVector(**state.fs.__dict__)
        state.fs.C += meta.fs_delta.get("C", 0)
        state.fs.M += meta.fs_delta.get("M", 0)
        state.fs.R += meta.fs_delta.get("R", 0)
        state.fs.Gamma += meta.fs_delta.get("Gamma", 0)
        # clamp 到 [0,1]
        for k in ["C", "M", "R", "Gamma"]:
            v = getattr(state.fs, k)
            setattr(state.fs, k, max(0.0, min(1.0, v)))

        # 6. 簡單 semantic_tension 更新
        island.semantic_tension = plan["delta_s"]
        island.current_mode = meta.mode_used
        island.last_step_id = step_id = str(uuid.uuid4())[:8]

        # 7. 寫 Chronicle
        entry = ChronicleEntry(
            step_id=step_id,
            island_id=island.island_id,
            timestamp=datetime.utcnow().isoformat(),
            user_input=user_input,
            model_reply_summary=clean_response[:120],
            mode_used=meta.mode_used,
            fs_before=fs_before,
            fs_after=state.fs,
            tools_used=[],  # v0 先不實作工具
            notes="",
        )
        append_chronicle(entry)

        # 8. 存 state & island
        save_state(state)
        save_island(island)

        # 9. 回給你
        print(f"\nYuHun[{meta.mode_used}]：{clean_response}")
        print(f"(FS: C={state.fs.C:.2f}, M={state.fs.M:.2f}, R={state.fs.R:.2f}, Γ={state.fs.Gamma:.2f}, ΔS={island.semantic_tension:.2f})")

if __name__ == "__main__":
    main()
