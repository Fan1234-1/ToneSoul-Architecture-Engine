/**
 * Vow contract definitions for the ToneSoul law layer.
 * Each vow is a binding statement with a priority level (P-level)
 * and a responsibility score.
 */

export interface VowObject {
  /** Unique identifier for the vow */
  id: string;

  /** The textual content of the vow */
  statement: string;

  /** Priority level (P0–P4) of the vow */
  p_level: 'P0' | 'P1' | 'P2' | 'P3' | 'P4';

  /** The quantified responsibility weight (0.0 to 1.0) */
  responsibility_score: number;

  /** Timestamp when the vow was made (optional) */
  timestamp?: number;

  /** Identifier for the entity making the vow (optional) */
  maker?: string;
}

/**
 * A TimeIsland groups events and vows into a contextual unit.
 */
export interface TimeIsland {
  id: string;
  vows: VowObject[];
  events: {
    trace_id: string;
    description: string;
    timestamp: number;
  }[];
}
