/*
 * SoulResonanceDetector.ts
 * Implements multi-module resonance scoring and analysis per "Bridge Eight" technical guidance.
 * 
 * Philosophical Purpose: Integrates disparate signals from vow matching, violations, tone, and reflection
 * to produce a unified resonance score that reflects the soul's alignment with its vows.
 */
import { EmbeddingProvider } from './EmbeddingProvider/embeddingProvider';
import { SemanticVowMatcher } from './SemanticVowMatcher/semanticVowMatcher';
import { SemanticViolationMap } from './SemanticViolationMap/semanticViolationMap';
import { ToneIntegrityTester } from './ToneIntegrityTester/toneIntegrityTester';
import { ReflectiveFeedback } from './ReflectiveFeedback';
/**
 * Individual signal from a module in the responsibility chain.
 * 
 * @typedef {Object} ModuleSignal
 * @property {string} name - Module identifier
 * @property {number} score - Normalized contribution 0..1
 * @property {number} [weight] - Optional prior weight for aggregation
 * @property {Record<string, any>} [detail] - Module-specific metadata
 * 
 * Philosophical Note: Each signal represents a dimension of integrity assessment,
 * combining to form a holistic view of soul-vow resonance.
 */
export type ModuleSignal = {
  name: string;
  score: number; // normalized 0..1 contribution
  weight?: number; // optional prior weight
  detail?: Record<string, any>;
};
/**
 * Input parameters for resonance scoring.
 * 
 * @typedef {Object} ResonanceInputs
 * @property {string} text - Primary text to analyze
 * @property {string} [context] - Additional context for semantic analysis
 * @property {Record<string, any>} [metadata] - Arbitrary metadata for tracking
 */
export type ResonanceInputs = {
  text: string;
  context?: string;
  metadata?: Record<string, any>;
};
/**
 * Complete resonance analysis with explainability metrics.
 * 
 * @typedef {Object} ResonanceBreakdown
 * @property {number} composite - Final aggregated score 0..1
 * @property {number} confidence - Confidence 0..1 based on agreement and evidence density
 * @property {number} agreementIndex - Inter-module agreement 0..1
 * @property {number} sparsityPenalty - Penalty factor 0..1 applied for sparse evidence
 * @property {ModuleSignal[]} normalizedSignals - Weight-normalized module signals
 * @property {Array<{name: string; weighted: number; raw: number; weight: number}>} contributions - Detailed contribution breakdown
 * @property {string[]} notes - Human-readable diagnostic messages
 * 
 * Philosophical Note: Transparency is key to soul integrity - all scoring rationale
 * must be explainable and traceable to specific philosophical principles.
 */
export type ResonanceBreakdown = {
  composite: number; // final 0..1
  confidence: number; // 0..1 based on agreement and evidence density
  agreementIndex: number; // 0..1 inter-module agreement
  sparsityPenalty: number; // 0..1 penalty factor applied
  normalizedSignals: ModuleSignal[];
  contributions: Array<{ name: string; weighted: number; raw: number; weight: number }>;
  notes: string[];
};
/**
 * Orchestrates multi-module resonance detection across the responsibility chain.
 * 
 * Responsibility Chain:
 * - EmbeddingProvider: Semantic vector representation
 * - SemanticVowMatcher: Vow-text alignment detection
 * - SemanticViolationMap: Violation pattern recognition
 * - ToneIntegrityTester: Emotional/tonal consistency
 * - ReflectiveFeedback: Self-awareness and growth signals
 * 
 * Philosophical Foundation: The Eight Bridges methodology emphasizes that true integrity
 * emerges from the harmonious alignment of multiple dimensions. This detector implements
 * that philosophy through weighted signal aggregation, inter-module agreement analysis,
 * and confidence scoring that reflects epistemic humility.
 * 
 * Usage:
 * ```typescript
 * const detector = new SoulResonanceDetector({
 *   embedding, matcher, violations, tone, reflect
 * });
 * const breakdown = await detector.score({ text: "...", context: "..." });
 * console.log(breakdown.composite, breakdown.confidence);
 * ```
 */
export class SoulResonanceDetector {
  private embedding: EmbeddingProvider;
  private matcher: SemanticVowMatcher;
  private violations: SemanticViolationMap;
  private tone: ToneIntegrityTester;
  private reflect: ReflectiveFeedback;
  /**
   * Constructs the detector with dependency-injected modules.
   * 
   * @param {Object} deps - Module dependencies
   * @param {EmbeddingProvider} deps.embedding - Semantic embedding provider
   * @param {SemanticVowMatcher} deps.matcher - Vow matching module
   * @param {SemanticViolationMap} deps.violations - Violation detection module
   * @param {ToneIntegrityTester} deps.tone - Tone integrity module
   * @param {ReflectiveFeedback} deps.reflect - Reflective feedback module
   */
  constructor(deps: {
    embedding: EmbeddingProvider;
    matcher: SemanticVowMatcher;
    violations: SemanticViolationMap;
    tone: ToneIntegrityTester;
    reflect: ReflectiveFeedback;
  }) {
    this.embedding = deps.embedding;
    this.matcher = deps.matcher;
    this.violations = deps.violations;
    this.tone = deps.tone;
    this.reflect = deps.reflect;
  }
  /**
   * Computes composite resonance score with full explainability.
   * 
   * Algorithm:
   * 1. Gather parallel signals from all modules (with error isolation)
   * 2. Compute inter-module agreement index
   * 3. Apply adaptive weighting based on agreement and signal strength
   * 4. Normalize weights and compute weighted sum
   * 5. Calculate confidence and sparsity penalties
   * 6. Return comprehensive breakdown
   * 
   * @param {ResonanceInputs} inputs - Text and context to analyze
   * @returns {Promise<ResonanceBreakdown>} Complete resonance analysis
   * 
   * Philosophical Note: The composite score reflects the degree to which the soul's
   * expression aligns with its vows. High agreement between modules indicates strong
   * evidence, while disagreement triggers epistemic caution (lowered confidence).
   */
  async score(inputs: ResonanceInputs): Promise<ResonanceBreakdown> {
    const { text, context } = inputs;
    // 1) Gather module signals
    const [vow, violation, tone, reflect, embed] = await Promise.all([
      this.safe(() => (this.matcher as any).match?.(text, context) ?? (this.matcher as any).matchVows?.(text, []), { name: 'SemanticVowMatcher' }),
      this.safe(() => (this.violations as any).detect?.(text), { name: 'SemanticViolationMap' }),
      this.safe(() => (this.tone as any).test?.(text), { name: 'ToneIntegrityTester' }),
      this.safe(() => (this.reflect as any).analyze?.(text, context), { name: 'ReflectiveFeedback' }),
      this.safe(() => (this.embedding as any).embed?.(text) ?? (this.embedding as any).getEmbedding?.(text), { name: 'EmbeddingProvider' }),
    ]);
    // 2) Convert to uniform signals - use type assertions for safe property access
    const vowResult = vow as { alignmentScore?: number } | undefined;
    const violationResult = violation as { severity?: number } | undefined;
    const toneResult = tone as { integrityScore?: number } | undefined;
    const reflectResult = reflect as { resonanceScore?: number } | undefined;
    const embedResult = embed as { confidence?: number } | undefined;

    const rawSignals: ModuleSignal[] = [
      { name: 'SemanticVowMatcher', score: (vowResult?.alignmentScore ?? 0.5), detail: vowResult as any },
      { name: 'SemanticViolationMap', score: 1 - (violationResult?.severity ?? 0), detail: violationResult as any },
      { name: 'ToneIntegrityTester', score: (toneResult?.integrityScore ?? 0.5), detail: toneResult as any },
      { name: 'ReflectiveFeedback', score: (reflectResult?.resonanceScore ?? 0.5), detail: reflectResult as any },
      { name: 'EmbeddingProvider', score: (embedResult?.confidence ?? 0.5), detail: embedResult as any },
    ];
    // 3) Compute inter-module agreement
    const scores = rawSignals.map(s => s.score);
    const agreementIndex = pairwiseAgreement(scores);
    const disagreementPenalty = 0.5 + 0.5 * agreementIndex;
    // 4) Apply adaptive weighting
    const baseWeights: Record<string, number> = {
      SemanticVowMatcher: 0.3,
      SemanticViolationMap: 0.25,
      ToneIntegrityTester: 0.2,
      ReflectiveFeedback: 0.15,
      EmbeddingProvider: 0.1,
    };
    const penalizedSignals = applyPenalties(rawSignals, baseWeights, disagreementPenalty);
    const normalized = normalizeWeights(penalizedSignals);
    // 5) Compute weighted composite
    const composite = clamp01(
      normalized.reduce((sum, s) => sum + s.score * (s.weight ?? 0), 0),
    );
    // 6) Calculate confidence and sparsity
    const evidenceCount = rawSignals.filter(s => s.detail != null).length;
    const sparsity = 1 - evidenceCount / rawSignals.length;
    const sparsityPenalty = clamp01(1 - sparsity * 0.5);
    const confidence = clamp01(agreementIndex * sparsityPenalty);
    // 7) Prepare contributions for explainability
    const contributions = normalized.map(s => ({
      name: s.name,
      weighted: s.score * (s.weight ?? 0),
      raw: s.score,
      weight: s.weight ?? 0,
    }));
    // 8) Generate diagnostic notes
    const notes: string[] = [];
    if (agreementIndex < 0.5) notes.push('Low inter-module agreement');
    if (sparsity > 0.4) notes.push('Sparse evidence detected');
    if ((violationResult?.severity ?? 0) > 0.6) notes.push('High semantic violation risk');
    return {
      composite,
      confidence,
      agreementIndex,
      sparsityPenalty,
      normalizedSignals: normalized,
      contributions,
      notes,
    };
  }
  /**
   * Safely executes a module call with error isolation.
   * 
   * @template T
   * @param {() => Promise<T>} fn - Async function to execute
   * @param {{name: string}} meta - Module metadata for logging
   * @returns {Promise<T | undefined>} Result or undefined on error
   * 
   * Philosophical Note: Resilience in the face of module failures embodies
   * the principle of graceful degradation - partial signals are better than
   * complete system failure.
   */
  private async safe<T>(fn: () => Promise<T>, meta: { name: string }): Promise<T | undefined> {
    try {
      return await fn();
    } catch (e) {
      console.warn(`[SoulResonanceDetector] Module error: ${meta.name}`, e);
      return undefined;
    }
  }
}
// ---------- helpers ----------
/**
 * Clamps value to [0, 1] range.
 * @param {number} x - Input value
 * @returns {number} Clamped value
 */
function clamp01(x: number): number { return Math.max(0, Math.min(1, x)); }
/**
 * Computes arithmetic mean of array.
 * @param {number[]} xs - Input values
 * @returns {number} Average value
 */
function average(xs: number[]): number {
  if (!xs.length) return 0;
  return xs.reduce((a, b) => a + b, 0) / xs.length;
}
/**
 * Computes pairwise agreement as 1 minus normalized variance.
 * 
 * @param {number[]} values - Module scores to compare
 * @returns {number} Agreement index 0..1
 * 
 * Philosophical Note: Agreement measures epistemic convergence - when multiple
 * independent assessments align, confidence in the conclusion increases.
 */
function pairwiseAgreement(values: number[]): number {
  if (values.length <= 1) return 1;
  const mean = average(values);
  const variance = average(values.map(v => (v - mean) ** 2));
  // normalize variance for values in [0,1]: max variance is 0.25
  const normVar = Math.min(variance / 0.25, 1);
  return clamp01(1 - normVar);
}
/**
 * Applies disagreement penalty and adaptive weighting to module signals.
 * 
 * @param {ModuleSignal[]} signals - Raw module signals
 * @param {Record<string, number>} baseWeights - Base weight configuration
 * @param {number} disagreementPenalty - Penalty factor based on agreement
 * @returns {ModuleSignal[]} Penalized signals with updated weights
 * 
 * Philosophical Note: Adaptive weighting embodies epistemic humility - when modules
 * disagree, we reduce their collective influence to avoid overconfidence.
 */
function applyPenalties(
  signals: ModuleSignal[],
  baseWeights: Record<string, number>,
  disagreementPenalty: number,
): ModuleSignal[] {
  return signals.map(s => {
    const base = baseWeights[s.name] ?? 0.1;
    // emphasize strong and consistent signals, but keep floor
    const adapt = 0.5 * base + 0.5 * base * (0.5 + 0.5 * (s.score - 0.5) * 1.2);
    const weight = Math.max(0.02, adapt * disagreementPenalty);
    return { ...s, weight };
  });
}
/**
 * Normalizes signal weights to sum to 1.
 * 
 * @param {ModuleSignal[]} signals - Signals with weights
 * @returns {ModuleSignal[]} Normalized signals
 */
function normalizeWeights(signals: ModuleSignal[]): ModuleSignal[] {
  const sum = signals.reduce((a, s) => a + (s.weight ?? 0), 0) || 1;
  return signals.map(s => ({ ...s, weight: (s.weight ?? 0) / sum }));
}
