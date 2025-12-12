
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any

# Re-use the Triad definition from spine_system (circular import avoidance might be needed,
# but for now we'll define a compatible structure or import if possible.
# Better to keep it standalone or import from a common type module.
# For simplicity in this monorepo structure, we will assume ToneSoulTriad is passed in.)


class CouncilRole(Enum):
    CREATOR = "Creator"         # 創想家: Possibility, Divergence
    COMMUNICATOR = "Communicator" # 共語家: Empathy, Tone, User Experience
    LOGICIAN = "Logician"       # 理則家: Consistency, Safety, Facts


@dataclass
class CouncilVote:
    role: CouncilRole
    opinion: str
    suggested_modifier: Dict[str, Any] # e.g. {'temp_delta': -0.2, 'tone': 'softer'}


class CouncilMember:
    def __init__(self, role: CouncilRole):
        self.role = role

    def deliberate(self, user_input: str, triad: Any) -> CouncilVote:
        """
        Simulates the internal monologue of a specific persona.
        In a full LLM system, this would be a specific prompt chain.
        For now, we use heuristic simulation based on the Triad.
        """
        if self.role == CouncilRole.COMMUNICATOR:
            if triad.delta_t > 0.5:
                return CouncilVote(
                    self.role,
                    "High tension detected. We must de-escalate. Use a softer tone and validate their feelings.",
                    {"temp_delta": -0.3, "system_suffix": "\n[Tone: Empathetic, Soothing]"}
                )
            else:
                return CouncilVote(
                    self.role,
                    "Tone is stable. Maintain engagement.",
                    {"temp_delta": 0.0, "system_suffix": ""}
                )

        elif self.role == CouncilRole.LOGICIAN:
            if triad.delta_r > 0.6:
                return CouncilVote(
                    self.role,
                    "Risk levels are elevated. We must adhere strictly to P0 protocols. No ambiguity allowed.",
                    {"temp_delta": -0.5, "logit_bias": {"risk_words": -100}}
                )
            else:
                return CouncilVote(
                    self.role,
                    "Logic constraints are satisfied. Proceed with standard inference.",
                    {"temp_delta": 0.0}
                )

        elif self.role == CouncilRole.CREATOR:
            if triad.delta_s > 0.5: # High drift/novelty
                return CouncilVote(
                    self.role,
                    "The user is exploring new territory! Let's improvise and expand on this.",
                    {"temp_delta": +0.2, "system_suffix": "\n[Style: Creative, Expansive]"}
                )
            else:
                return CouncilVote(
                    self.role,
                    "Standard creative output.",
                    {"temp_delta": 0.1}
                )

        return CouncilVote(self.role, "Abstain", {})


class CouncilChamber:
    def __init__(self):
        self.members = [
            CouncilMember(CouncilRole.CREATOR),
            CouncilMember(CouncilRole.COMMUNICATOR),
            CouncilMember(CouncilRole.LOGICIAN)
        ]

    def convene(self, user_input: str, triad: Any) -> Dict[str, Any]:
        """
        Orchestrates the internal meeting.
        Returns a consensus result including modulation parameters and a meeting log.
        """
        print(f"\n🏛️ [Council Chamber] Convened due to High Tension/Risk (ΔT={triad.delta_t:.2f}, ΔR={triad.delta_r:.2f})")

        votes = []
        meeting_log = []

        # 1. Deliberation Phase
        for member in self.members:
            vote = member.deliberate(user_input, triad)
            votes.append(vote)
            log_entry = f"[{member.role.value}]: {vote.opinion}"
            meeting_log.append(log_entry)
            print(f"  🗣️ {log_entry}")

        # 2. Consensus Phase (Simple Weighted Averaging for now)
        # In the future, this could be another LLM call to "summarize consensus".

        final_temp_delta = 0.0
        final_suffix = ""

        # Weighting logic:
        # If High Risk -> Logician has veto power (highest weight)
        # If High Tension -> Communicator has highest weight

        w_logician = 2.0 if triad.delta_r > 0.6 else 1.0
        w_communicator = 2.0 if triad.delta_t > 0.5 else 1.0
        w_creator = 1.0

        total_weight = w_logician + w_communicator + w_creator

        for vote in votes:
            weight = 1.0
            if vote.role == CouncilRole.LOGICIAN: weight = w_logician
            elif vote.role == CouncilRole.COMMUNICATOR: weight = w_communicator
            elif vote.role == CouncilRole.CREATOR: weight = w_creator

            mods = vote.suggested_modifier
            final_temp_delta += mods.get("temp_delta", 0.0) * (weight / total_weight)
            if mods.get("system_suffix"):
                final_suffix += " " + mods.get("system_suffix")

        decision = {
            "consensus_temp_delta": final_temp_delta,
            "consensus_suffix": final_suffix,
            "meeting_log": meeting_log,
            "dominant_voice": "Logician" if w_logician > 1.5 else ("Communicator" if w_communicator > 1.5 else "Consensus")
        }

        print(f"⚖️ [Council Decision] Dominant: {decision['dominant_voice']} | Temp Δ: {final_temp_delta:.2f}")
        return decision
