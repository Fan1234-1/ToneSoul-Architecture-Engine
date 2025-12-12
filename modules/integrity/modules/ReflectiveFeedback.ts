/**
 * ReflectiveFeedback.ts
 * 
 * Security/Privacy: This module stores only client-provided, local-session reflections. Do not transmit.
 * Data Classification: Sensitive-Personal (self-reflection). Storage: Local only. Retention: User-controlled.
 * 
 * Philosophical Purpose: Implements the reflective practice of self-awareness and continuous improvement.
 * This module embodies the principle that growth emerges from honest self-observation and pattern recognition.
 */

/**
 * Sensitivity level for reflection entries.
 * 
 * @typedef {'low' | 'moderate' | 'high'} Sensitivity
 * 
 * Philosophical Note: Sensitivity classification helps manage the emotional and privacy
 * weight of reflections, respecting the sacred nature of inner work.
 */
export type Sensitivity = 'low' | 'moderate' | 'high';

/**
 * A single reflection entry capturing an observation, feeling, insight, and action.
 * 
 * @interface ReflectionEntry
 * @property {Date} timestamp - When the reflection occurred (PII Risk: may correlate to calendar events; keep local only)
 * @property {string[]} context - Contextual tags for retrieval (do not include PII)
 * @property {string} observation - Factual observation without judgment
 * @property {string} [feeling] - Emotional state associated with observation
 * @property {string} [insight] - Learned understanding or pattern recognition
 * @property {string} [actionItem] - Concrete next step or commitment
 * @property {Sensitivity} [sensitivity] - Privacy/sensitivity level of this entry
 * 
 * Philosophical Foundation: The structure mirrors the reflective cycle:
 * 1. Observation (what happened)
 * 2. Feeling (emotional awareness)
 * 3. Insight (understanding)
 * 4. Action (commitment to change)
 */
export interface ReflectionEntry {
  // PII Risk: timestamp may correlate to calendar events; keep local only.
  timestamp: Date;
  // Contextual tags for retrieval; do not include PII.
  context: string[];
  observation: string;
  feeling?: string;
  insight?: string;
  actionItem?: string;
  // Mark whether the entry contains sensitive personal data.
  sensitivity?: Sensitivity;
}

/**
 * Pattern discovered through tag frequency and co-occurrence analysis.
 * 
 * @interface PatternInsight
 * @property {string} tag - The contextual tag being analyzed
 * @property {number} frequency - How many times this tag appears
 * @property {string[]} [cooccurring] - Other tags that frequently appear with this one
 * 
 * Philosophical Note: Patterns reveal hidden habits and recurring themes, making the
 * unconscious conscious and enabling intentional change.
 */
export interface PatternInsight {
  tag: string;
  frequency: number;
  cooccurring?: string[];
}

/**
 * A suggested improvement derived from pattern analysis.
 * 
 * @interface FeedbackSuggestion
 * @property {string} summary - Human-readable summary of the pattern
 * @property {string} [recommendedAction] - Concrete action to address the pattern
 * @property {'now' | 'soon' | 'later'} priority - Urgency level for the suggestion
 * 
 * Philosophical Note: Suggestions transform insights into actionable guidance,
 * bridging awareness and behavioral change.
 */
export interface FeedbackSuggestion {
  summary: string;
  recommendedAction?: string;
  priority: 'now' | 'soon' | 'later';
}

/**
 * Manages collection, storage, and analysis of reflective entries.
 * 
 * Responsibility Chain:
 * - Stores reflection entries locally (never transmitted)
 * - Performs pattern analysis on tags and co-occurrences
 * - Generates improvement suggestions based on patterns
 * 
 * Philosophical Foundation: Reflective feedback implements the Socratic principle
 * of self-examination. By tracking observations, feelings, insights, and actions,
 * this module supports the development of metacognitive awareness - the foundation
 * of integrity alignment.
 * 
 * Usage:
 * ```typescript
 * const feedback = new ReflectiveFeedback();
 * feedback.add({
 *   timestamp: new Date(),
 *   context: ['focus', 'morning'],
 *   observation: 'Easier deep work after clarity session',
 *   insight: 'Intent note helped',
 *   sensitivity: 'moderate'
 * });
 * const suggestions = feedback.suggestImprovements();
 * console.log(suggestions);
 * ```
 */
export class ReflectiveFeedback {
  private entries: ReflectionEntry[] = [];

  /**
   * Adds a new reflection entry to the collection.
   * 
   * @param {ReflectionEntry} entry - The reflection to store
   * @returns {void}
   * 
   * Note: Performs shallow copy to prevent external mutation of internal state.
   */
  add(entry: ReflectionEntry): void {
    // Shallow copy to avoid external mutation
    this.entries.push({ ...entry });
  }

  /**
   * Returns all stored reflection entries.
   * 
   * @returns {ReflectionEntry[]} Copy of all entries
   * 
   * Note: Returns a shallow copy to preserve encapsulation.
   */
  all(): ReflectionEntry[] {
    return [...this.entries];
  }

  /**
   * Analyzes reflection patterns by tag frequency and co-occurrence.
   * 
   * Algorithm:
   * 1. Count tag occurrences across all entries
   * 2. Track which tags appear together
   * 3. Filter by minimum frequency threshold
   * 4. Sort by frequency (descending)
   * 
   * @param {number} [minFrequency=2] - Minimum occurrences for a pattern to be reported
   * @returns {PatternInsight[]} Discovered patterns sorted by frequency
   * 
   * Philosophical Note: Pattern recognition transforms raw data into meaning,
   * revealing hidden structures in behavior and experience.
   */
  analyzePatterns(minFrequency = 2): PatternInsight[] {
    const tagCounts = new Map<string, number>();
    const cooccurrence = new Map<string, Set<string>>();

    for (const e of this.entries) {
      const tags = new Set(e.context);
      for (const t of tags) {
        tagCounts.set(t, (tagCounts.get(t) ?? 0) + 1);
        if (!cooccurrence.has(t)) cooccurrence.set(t, new Set());
        for (const t2 of tags) {
          if (t2 !== t) cooccurrence.get(t)!.add(t2);
        }
      }
    }

    const results: PatternInsight[] = [];
    for (const [tag, count] of tagCounts.entries()) {
      if (count >= minFrequency) {
        results.push({
          tag,
          frequency: count,
          cooccurring: Array.from(cooccurrence.get(tag) ?? [])
        });
      }
    }

    return results.sort((a, b) => b.frequency - a.frequency);
  }

  /**
   * Generates actionable improvement suggestions based on detected patterns.
   * 
   * Algorithm:
   * 1. Analyze patterns across all reflections
   * 2. For each pattern, create a summary and recommended action
   * 3. If no patterns exist, suggest gathering more data
   * 
   * @returns {FeedbackSuggestion[]} List of suggestions prioritized by pattern frequency
   * 
   * Philosophical Note: Transformation requires both awareness and action.
   * Suggestions translate patterns into concrete behavioral experiments,
   * honoring the principle that insight without action is incomplete.
   */
  suggestImprovements(): FeedbackSuggestion[] {
    const insights = this.analyzePatterns();
    const suggestions: FeedbackSuggestion[] = [];

    for (const i of insights) {
      const summary = `Pattern '${i.tag}' appears ${i.frequency} times` +
        (i.cooccurring && i.cooccurring.length ? `, co-occurs with ${i.cooccurring.join(', ')}` : '');
      const recommendedAction = this.defaultActionForTag(i.tag);
      suggestions.push({ summary, recommendedAction, priority: 'soon' });
    }

    // If no patterns, create a meta-suggestion to gather more data
    if (suggestions.length === 0) {
      suggestions.push({
        summary: 'Not enough reflective data to detect patterns',
        recommendedAction: 'Record reflections daily for one week',
        priority: 'later'
      });
    }

    return suggestions;
  }

  /**
   * Maps common tags to default recommended actions.
   * 
   * @param {string} tag - The tag to look up
   * @returns {string | undefined} Recommended action or undefined if no default exists
   * 
   * Philosophical Note: These defaults embody practical wisdom accumulated from
   * common patterns, but remain suggestions rather than prescriptions.
   */
  private defaultActionForTag(tag: string): string | undefined {
    const map: Record<string, string> = {
      stress: 'Schedule a 5-minute breathing break after each focused block',
      focus: 'Adopt 25/5 focus cycles and summarize intent before each block',
      alignment: 'Revisit intent and clarify success criteria before starting',
      fatigue: 'Insert micro-rests and hydrate hourly',
    };
    return map[tag];
  }
}

// Example usage (for docs/tests)
// const feedback = new ReflectiveFeedback();
// feedback.add({ timestamp: new Date(), context: ['focus', 'morning'], observation: 'Easier deep work', insight: 'Intent note helped', sensitivity: 'moderate' });
// console.log(feedback.suggestImprovements());
