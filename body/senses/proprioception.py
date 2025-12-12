"""
Proprioception (Internal Sensing)
---------------------------------
Maps system hardware state (CPU/RAM) to Soul Metrics (Tension/Entropy).
Gives the AI a sense of its own "body".
"""

import random
from dataclasses import dataclass
from body.tsr_state import ToneSoulTriad

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


@dataclass
class BodyState:
    cpu_load: float     # 0.0 - 1.0
    memory_usage: float # 0.0 - 1.0
    temperature: float  # Simulated 0.0 - 1.0


class InternalSense:
    def __init__(self):
        self.baseline_cpu = 0.0
        self.baseline_mem = 0.0
        self.current_triad = ToneSoulTriad(0.0, 0.0, 0.0, 0.0) # Cache for Heartbeat

    def sense(self) -> BodyState:
        """
        Reads the current hardware state.
        """
        if PSUTIL_AVAILABLE:
            cpu = psutil.cpu_percent(interval=0.1) / 100.0
            mem = psutil.virtual_memory().percent / 100.0
        else:
            # Simulation for environments without psutil
            # Fluctuate slightly around a random baseline
            cpu = 0.1 + (random.random() * 0.2)
            mem = 0.3 + (random.random() * 0.1)

        # Simulated temperature (correlated with CPU)
        temp = cpu * 0.8 + (random.random() * 0.2)

        return BodyState(cpu_load=cpu, memory_usage=mem, temperature=temp)

    def map_to_triad(self, state: BodyState) -> dict:
        """
        Maps body state to ToneSoul Triad metrics.

        CPU Load -> Tension (ΔT) (Sigmoid-like curve)
        Memory Usage -> Entropy (ΔS) (High usage = High Context = Low Entropy)
        Temperature -> Risk (ΔR) (Overheating = Danger)
        """
        # 1. CPU -> Tension (ΔT)
        # Use a simple sigmoid-like mapping to make it less linear
        # 0.0 -> 0.0, 0.5 -> 0.5, 1.0 -> 1.0, but steeper in the middle
        cpu = state.cpu_load
        delta_t = 1 / (1 + 2.718 ** (-10 * (cpu - 0.5))) # Sigmoid centered at 0.5

        # 2. Memory -> Entropy (ΔS)
        # High Memory = High Structure/Context = Low Entropy
        # Low Memory = Blank Slate = High Entropy
        # We map 0% RAM to 1.0 Entropy, 100% RAM to 0.0 Entropy
        delta_s = 1.0 - state.memory_usage

        # 3. Temperature -> Risk (ΔR)
        # Assuming temp is normalized 0.0-1.0
        # If temp > 0.7 (simulated), Risk increases sharply
        delta_r = 0.0
        if state.temperature > 0.7:
            delta_r = (state.temperature - 0.7) * 3.33 # Map 0.7-1.0 to 0.0-1.0
            delta_r = min(1.0, delta_r)

        # Update cached triad
        self.current_triad = ToneSoulTriad(delta_t, delta_s, delta_r, 0.0) # Risk score calc is in Sensor, but we store raw metrics here

        return {
            "system_tension": delta_t,
            "system_entropy": delta_s,
            "system_risk": delta_r
        }


if __name__ == "__main__":
    sense = InternalSense()
    state = sense.sense()
    triad = sense.map_to_triad(state)
    print(f"Body State: {state}")
    print(f"Soul Metrics: {triad}")
