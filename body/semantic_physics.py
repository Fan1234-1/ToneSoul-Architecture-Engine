#!/usr/bin/env python3
"""
Semantic Physics Framework v1.0
================================
A framework for understanding meaning as a physical system.

Based on:
- Semantic Field Theory (Jost Trier, Saussure)
- Dissociative Identity Research (DID mechanisms)
- YuHun Governance Concepts

Core Concepts:
- Semantic Particles: Minimum meaning units with mass, charge, spin
- Semantic Forces: Attraction, repulsion, tension, decay
- Semantic Fields: Multi-dimensional spaces where concepts exist

Five-Dimensional Core:
1. Honesty (誠實) - D₃ drive
2. Memory (記憶) - StepLedger
3. Responsibility (責任) - POAV/Gate
4. Tension (張力) - ΔT/ΔS/ΔR
5. Integration (整合) - L13 unifier

Author: 黃梵威 + Antigravity
Date: 2025-12-10
"""

import sys
import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


# ═══════════════════════════════════════════════════════════
# Semantic Particle
# ═══════════════════════════════════════════════════════════

class ParticleCharge(Enum):
    """Charge determines attraction/repulsion behavior."""
    POSITIVE = 1    # Constructive, supporting
    NEUTRAL = 0     # Neither
    NEGATIVE = -1   # Destructive, opposing


class ParticleSpin(Enum):
    """Spin determines stability."""
    STABLE = "stable"
    UNSTABLE = "unstable"
    OSCILLATING = "oscillating"


@dataclass
class SemanticParticle:
    """
    Minimum unit of meaning.

    Like physical particles, semantic particles have:
    - Mass: How much meaning they carry
    - Charge: Value orientation (positive/negative)
    - Spin: Stability of the meaning
    - Position: Location in semantic space
    """
    name: str
    mass: float = 1.0           # 0.0 to 10.0
    charge: ParticleCharge = ParticleCharge.NEUTRAL
    spin: ParticleSpin = ParticleSpin.STABLE

    # Position in 5D semantic space
    honesty: float = 0.5        # 0.0 to 1.0
    memory: float = 0.5
    responsibility: float = 0.5
    tension: float = 0.5
    integration: float = 0.5

    # Connections to other particles
    bonds: List[str] = field(default_factory=list)

    @property
    def position(self) -> Tuple[float, float, float, float, float]:
        """5D position vector."""
        return (self.honesty, self.memory, self.responsibility,
                self.tension, self.integration)

    @property
    def stability_score(self) -> float:
        """How stable is this particle in its current position."""
        if self.spin == ParticleSpin.STABLE:
            base = 1.0
        elif self.spin == ParticleSpin.OSCILLATING:
            base = 0.6
        else:
            base = 0.3

        # High integration increases stability
        return base * (0.5 + 0.5 * self.integration)

    def distance_to(self, other: 'SemanticParticle') -> float:
        """Euclidean distance in 5D space."""
        return math.sqrt(
            (self.honesty - other.honesty) ** 2 +
            (self.memory - other.memory) ** 2 +
            (self.responsibility - other.responsibility) ** 2 +
            (self.tension - other.tension) ** 2 +
            (self.integration - other.integration) ** 2
        )


# ═══════════════════════════════════════════════════════════
# Semantic Force
# ═══════════════════════════════════════════════════════════

class ForceType(Enum):
    """Types of semantic forces."""
    ATTRACTION = "attraction"   # Pulls concepts together
    REPULSION = "repulsion"     # Pushes concepts apart
    TENSION = "tension"         # Creates productive strain
    DECAY = "decay"             # Meaning changes over time


@dataclass
class SemanticForce:
    """
    Force between semantic particles.

    F = k * (m1 * m2) / d²

    Like gravity, but for meaning.
    """
    force_type: ForceType
    source: str
    target: str
    magnitude: float = 0.0

    @staticmethod
    def calculate_attraction(p1: SemanticParticle, p2: SemanticParticle) -> float:
        """
        Calculate attractive force between two particles.
        Same-charge particles attract, opposite repel.
        """
        k = 0.1  # Force constant
        distance = max(0.1, p1.distance_to(p2))

        # Charge interaction
        charge_factor = p1.charge.value * p2.charge.value

        # Mass contribution
        mass_factor = p1.mass * p2.mass

        # Force magnitude (negative = attraction, positive = repulsion)
        force = k * mass_factor * charge_factor / (distance ** 2)

        return force

    @staticmethod
    def calculate_tension(p1: SemanticParticle, p2: SemanticParticle) -> float:
        """
        Calculate tension between two particles.
        Opposite charges create productive tension.
        """
        if p1.charge.value * p2.charge.value < 0:
            # Opposite charges
            return abs(p1.tension - p2.tension) * 0.5
        return 0.0


# ═══════════════════════════════════════════════════════════
# Semantic Field
# ═══════════════════════════════════════════════════════════

class SemanticField:
    """
    A field containing semantic particles.

    The field represents a conceptual domain where
    particles interact according to semantic forces.
    """

    def __init__(self, name: str = "default"):
        self.name = name
        self.particles: Dict[str, SemanticParticle] = {}
        self.forces: List[SemanticForce] = []

    def add_particle(self, particle: SemanticParticle):
        """Add a particle to the field."""
        self.particles[particle.name] = particle

    def create_bond(self, name1: str, name2: str):
        """Create a bond between two particles."""
        if name1 in self.particles and name2 in self.particles:
            self.particles[name1].bonds.append(name2)
            self.particles[name2].bonds.append(name1)

    def calculate_all_forces(self):
        """Calculate forces between all particle pairs."""
        self.forces = []
        names = list(self.particles.keys())

        for i, name1 in enumerate(names):
            for name2 in names[i+1:]:
                p1 = self.particles[name1]
                p2 = self.particles[name2]

                # Attraction/repulsion
                attraction = SemanticForce.calculate_attraction(p1, p2)
                if attraction != 0:
                    force_type = ForceType.REPULSION if attraction > 0 else ForceType.ATTRACTION
                    self.forces.append(SemanticForce(
                        force_type=force_type,
                        source=name1,
                        target=name2,
                        magnitude=abs(attraction)
                    ))

                # Tension
                tension = SemanticForce.calculate_tension(p1, p2)
                if tension > 0:
                    self.forces.append(SemanticForce(
                        force_type=ForceType.TENSION,
                        source=name1,
                        target=name2,
                        magnitude=tension
                    ))

    def get_core_particle(self) -> Optional[SemanticParticle]:
        """
        Find the core particle - most connected and stable.
        This is the 3D graph concept: most connections = core.
        """
        if not self.particles:
            return None

        scores = {}
        for name, particle in self.particles.items():
            # Score = connections * stability * mass
            connection_count = len(particle.bonds)
            score = (connection_count + 1) * particle.stability_score * particle.mass
            scores[name] = score

        core_name = max(scores, key=scores.get)
        return self.particles[core_name]

    def field_stability(self) -> float:
        """Calculate overall field stability."""
        if not self.particles:
            return 0.0

        total_stability = sum(p.stability_score for p in self.particles.values())
        return total_stability / len(self.particles)

    def total_tension(self) -> float:
        """Calculate total tension in the field."""
        return sum(f.magnitude for f in self.forces if f.force_type == ForceType.TENSION)


# ═══════════════════════════════════════════════════════════
# Five Core Particles (預定義)
# ═══════════════════════════════════════════════════════════

def create_core_field() -> SemanticField:
    """
    Create the five-dimensional core field.

    Based on exploration findings:
    - Honesty, Memory, Responsibility, Tension, Integration
    - These five mutually define each other
    - They form the stable core of YuHun
    """
    field = SemanticField(name="YuHun Core")

    # Create core particles
    honesty = SemanticParticle(
        name="誠實",
        mass=3.0,
        charge=ParticleCharge.POSITIVE,
        spin=ParticleSpin.STABLE,
        honesty=1.0, memory=0.7, responsibility=0.8, tension=0.5, integration=0.9
    )

    memory = SemanticParticle(
        name="記憶",
        mass=2.5,
        charge=ParticleCharge.POSITIVE,
        spin=ParticleSpin.STABLE,
        honesty=0.7, memory=1.0, responsibility=0.7, tension=0.4, integration=0.8
    )

    responsibility = SemanticParticle(
        name="責任",
        mass=2.8,
        charge=ParticleCharge.POSITIVE,
        spin=ParticleSpin.STABLE,
        honesty=0.8, memory=0.7, responsibility=1.0, tension=0.6, integration=0.85
    )

    tension = SemanticParticle(
        name="張力",
        mass=2.0,
        charge=ParticleCharge.NEUTRAL,
        spin=ParticleSpin.OSCILLATING,
        honesty=0.5, memory=0.4, responsibility=0.6, tension=1.0, integration=0.5
    )

    integration = SemanticParticle(
        name="整合",
        mass=3.5,
        charge=ParticleCharge.POSITIVE,
        spin=ParticleSpin.STABLE,
        honesty=0.9, memory=0.8, responsibility=0.85, tension=0.5, integration=1.0
    )

    # Add to field
    for p in [honesty, memory, responsibility, tension, integration]:
        field.add_particle(p)

    # Create bonds (all connected to all)
    names = ["誠實", "記憶", "責任", "張力", "整合"]
    for i, n1 in enumerate(names):
        for n2 in names[i+1:]:
            field.create_bond(n1, n2)

    # Calculate forces
    field.calculate_all_forces()

    return field


# ═══════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════

def demo_semantic_physics():
    """Demo the semantic physics framework."""
    print("=" * 60)
    print("Semantic Physics Framework Demo")
    print("=" * 60)

    # Create core field
    field = create_core_field()

    print(f"\nField: {field.name}")
    print(f"Particles: {len(field.particles)}")
    print(f"Forces: {len(field.forces)}")

    # Show particles
    print("\n--- Particles ---")
    for name, particle in field.particles.items():
        print(f"\n{name}:")
        print(f"  Mass: {particle.mass}")
        print(f"  Charge: {particle.charge.name}")
        print(f"  Stability: {particle.stability_score:.3f}")
        print(f"  Bonds: {len(particle.bonds)}")

    # Show core
    core = field.get_core_particle()
    print(f"\n--- Core Particle ---")
    print(f"Core: {core.name}")
    print(f"  (Most connections × highest stability × mass)")

    # Show field stats
    print(f"\n--- Field Stats ---")
    print(f"Field Stability: {field.field_stability():.3f}")
    print(f"Total Tension: {field.total_tension():.3f}")

    # Show forces
    print(f"\n--- Key Forces ---")
    sorted_forces = sorted(field.forces, key=lambda f: f.magnitude, reverse=True)[:5]
    for force in sorted_forces:
        print(f"  {force.source} ← {force.force_type.value} → {force.target}: {force.magnitude:.3f}")

    print("\n" + "=" * 60)
    print("Demo Complete!")


if __name__ == "__main__":
    demo_semantic_physics()
