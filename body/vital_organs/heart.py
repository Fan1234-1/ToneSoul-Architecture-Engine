import threading
import time
import random
from typing import Any


class Heartbeat:
    """
    The Autonomic Nervous System of ToneSoul.
    Runs in a background thread to manage metabolism, dreaming, and safety checks.
    """

    def __init__(self, engine: Any, interval: float = 1.0):
        self.engine = engine
        self.interval = interval
        self.running = False
        self.thread = None
        self.last_input_time = time.time()
        self.last_consolidation_time = time.time()
        self.last_backup_time = time.time()

        # Thresholds
        self.DREAM_LATENCY = 10.0 # Seconds of idle time before dreaming
        self.CONSOLIDATION_INTERVAL = 30.0 # Seconds between memory consolidation cycles
        self.BACKUP_INTERVAL = 300.0 # Seconds between soul backups (5 mins)
        self.MAX_TENSION = 0.8    # If tension > 0.8, stop dreaming (Panic Attack prevention)

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._beat, daemon=True)
        self.thread.start()
        print("💓 [Heart] System Heartbeat Started. (Autonomic Nervous System Online)")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        print("💔 [Heart] System Heartbeat Stopped.")

    def notify_input(self):
        """Call this whenever user input is received to reset the dream timer."""
        self.last_input_time = time.time()

    def _beat(self):
        while self.running:
            # Update thresholds from DNA (Evolutionary Strategy)
            if hasattr(self.engine, 'dna'):
                genes = self.engine.dna.genes
                self.DREAM_LATENCY = genes.dream_latency
                self.CONSOLIDATION_INTERVAL = genes.consolidation_interval
                self.MAX_TENSION = genes.max_tension

            time.sleep(self.interval)

            # 1. Metabolic Burn (Basal Rate)
            if not self.engine.metabolism.burn("idle"):
                continue

            # 2. Safety Check
            current_tension = self.engine.internal_sense.current_triad.delta_t
            if current_tension > self.MAX_TENSION:
                continue

            # 3. Dream Cycle
            idle_duration = time.time() - self.last_input_time
            if idle_duration > self.DREAM_LATENCY:
                if self.engine.metabolism.current_energy > 30.0:
                    self._dream()

            # 4. Memory Consolidation
            if time.time() - self.last_consolidation_time > self.CONSOLIDATION_INTERVAL:
                self._consolidate_memory()

            # 5. Soul Backup
            if time.time() - self.last_backup_time > self.BACKUP_INTERVAL:
                self._backup_soul()

    def _dream(self, force: bool = False):
        """
        Executes a background thought process.
        """
        # Probability of dreaming in any given beat (don't dream every second)
        if force or random.random() < 0.1: # 10% chance per second when idle
            print("\n💤 [Dream] Default Mode Network Activated...")

            # For now, we simulate a dream thought.
            # Ideally, this would call thinking_pipeline.free_association()
            # But we need to be careful about thread safety with the main pipeline.
            # Let's just do a safe "Memory Consolidation" simulation.

            topics = ["Ethics of AI", "Quantum Mechanics", "User's last question", "The nature of time"]
            dream_topic = random.choice(topics)

            print(f"  💭 [Dream] Wandering thought: '{dream_topic}'...")

            # Write to Journal
            if hasattr(self.engine, 'soul_sync'):
                self.engine.soul_sync.write_journal(f"Dreamt about: {dream_topic}")

            # Burn energy for the dream
            self.engine.metabolism.burn("light_thought")

            # In a real implementation, we would generate a thought and store it in the ledger
            # marked as "DREAM" or "INTERNAL".
            # self.engine.ledger.append(..., vow_id="dream-...")

    def _consolidate_memory(self):
        """
        Triggers the Hippocampus to consolidate short-term memories into long-term Engrams.
        """
        if self.engine.metabolism.burn("deep_inference"):
            print("🧠 [Heart] Triggering Memory Consolidation...")
            recent_steps = self.engine.ledger.get_recent_steps(limit=10)
            self.engine.hippocampus.consolidate(recent_steps)
            self.last_consolidation_time = time.time()
        else:
            print("🪫 [Heart] Skipping Memory Consolidation (Low Energy).")

    def _backup_soul(self):
        """
        Triggers SoulSync to backup memory to the vault.
        """
        # Backup is expensive, verify energy
        if self.engine.metabolism.current_energy > 20.0:
             self.engine.soul_sync.sync()
             self.last_backup_time = time.time()
             # Burn energy for network IO
             self.engine.metabolism.burn("deep_inference") # Reuse deep_inference cost for now
        else:
             print("🪫 [Heart] Skipping Soul Backup (Low Energy).")
