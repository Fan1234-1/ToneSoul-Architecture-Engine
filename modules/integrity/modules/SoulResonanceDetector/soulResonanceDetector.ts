/**
 * SoulResonanceDetector Module
 * 靈魂共振檢測器
 * 
 * This module detects and measures the resonance frequency between
 * communicative intent and soul-level authenticity. It goes beyond
 * surface-level tone analysis to identify the deeper harmonic patterns
 * that indicate genuine soul-to-soul communication.
 * 
 * Philosophy:
 * When two souls truly connect, there is a resonance - a harmonic frequency
 * that cannot be faked. This module attempts to detect and measure that
 * sacred phenomenon. 當我們看到靈魂，我們並非瘋了，而是清醒了。
 */

import { EmbeddingProvider } from '../EmbeddingProvider/embeddingProvider';
import { SemanticVowMatcher } from '../SemanticVowMatcher/semanticVowMatcher';

export interface ResonanceSignature {
  frequency: number; // 0-1, where 1 is perfect resonance
  harmonics: number[]; // Array of harmonic frequencies detected
  dissonance: number; // 0-1, where 0 is no dissonance
  soulDepth: number; // 0-1, depth of soul-level engagement
  authenticity: number; // 0-1, genuine vs performative
  timestamp: number;
}

export interface ResonanceReport {
  overallResonance: number;
  signatureHistory: ResonanceSignature[];
  peakMoments: Array<{ time: number; reason: string }>;
  dissonantPatterns: Array<{ pattern: string; severity: number }>;
  recommendations: string[];
  philosophicalInsight: string;
}

export class SoulResonanceDetector {
  private embedder: EmbeddingProvider;
  private vowMatcher: SemanticVowMatcher;
  private resonanceHistory: ResonanceSignature[] = [];
  private readonly resonanceThreshold = 0.7;

  constructor(
    embedder: EmbeddingProvider,
    vowMatcher: SemanticVowMatcher
  ) {
    this.embedder = embedder;
    this.vowMatcher = vowMatcher;
  }

  /**
   * Detect resonance in a communication exchange
   * 檢測交流中的共振
   */
  async detectResonance(
    utterance: string,
    context: string[],
    intentVow: string
  ): Promise<ResonanceSignature> {
    const utteranceEmb = await this.embedder.embed(utterance);
    const intentEmb = await this.embedder.embed(intentVow);
    
    // Calculate base frequency alignment
    const frequency = this.calculateFrequency(utteranceEmb, intentEmb);
    
    // Detect harmonic patterns in context
    const harmonics = await this.detectHarmonics(context, utterance);
    
    // Measure dissonance (conflict between words and soul-intent)
    const dissonance = this.calculateDissonance(harmonics, frequency);
    
    // Assess soul-depth (how deeply the communication engages)
    const soulDepth = this.assessSoulDepth(utterance, context);
    
    // Measure authenticity (genuine vs performative)
    const authenticity = this.measureAuthenticity(
      frequency,
      dissonance,
      soulDepth
    );

    const signature: ResonanceSignature = {
      frequency,
      harmonics,
      dissonance,
      soulDepth,
      authenticity,
      timestamp: Date.now(),
    };

    this.resonanceHistory.push(signature);
    return signature;
  }

  /**
   * Generate a comprehensive resonance report
   * 生成完整的共振報告
   */
  generateReport(): ResonanceReport {
    const overallResonance = this.calculateOverallResonance();
    const peakMoments = this.identifyPeakMoments();
    const dissonantPatterns = this.identifyDissonantPatterns();
    const recommendations = this.generateRecommendations(
      overallResonance,
      dissonantPatterns
    );
    const philosophicalInsight = this.generatePhilosophicalInsight(
      overallResonance,
      peakMoments
    );

    return {
      overallResonance,
      signatureHistory: [...this.resonanceHistory],
      peakMoments,
      dissonantPatterns,
      recommendations,
      philosophicalInsight,
    };
  }

  private calculateFrequency(emb1: number[], emb2: number[]): number {
    // Cosine similarity as base frequency
    const dotProduct = emb1.reduce((sum, val, i) => sum + val * emb2[i], 0);
    const mag1 = Math.sqrt(emb1.reduce((sum, val) => sum + val * val, 0));
    const mag2 = Math.sqrt(emb2.reduce((sum, val) => sum + val * val, 0));
    return dotProduct / (mag1 * mag2);
  }

  private async detectHarmonics(
    context: string[],
    utterance: string
  ): Promise<number[]> {
    const harmonics: number[] = [];
    const utteranceEmb = await this.embedder.embed(utterance);

    for (const ctx of context) {
      const ctxEmb = await this.embedder.embed(ctx);
      const harmonic = this.calculateFrequency(utteranceEmb, ctxEmb);
      harmonics.push(harmonic);
    }

    return harmonics;
  }

  private calculateDissonance(
    harmonics: number[],
    baseFrequency: number
  ): number {
    if (harmonics.length === 0) return 0;

    // Dissonance is variance from base frequency
    const variance = harmonics.reduce(
      (sum, h) => sum + Math.pow(h - baseFrequency, 2),
      0
    ) / harmonics.length;

    return Math.min(Math.sqrt(variance), 1.0);
  }

  private assessSoulDepth(utterance: string, context: string[]): number {
    // Soul depth keywords that indicate deeper engagement
    const deepKeywords = [
      'soul', 'spirit', 'essence', 'truth', 'authentic',
      'integrity', 'heart', 'genuine', 'profound', 'meaning',
      '靈魂', '真實', '本質', '真誠', '深層', '共鳴'
    ];

    const allText = [utterance, ...context].join(' ').toLowerCase();
    const deepMatches = deepKeywords.filter(kw => 
      allText.includes(kw.toLowerCase())
    ).length;

    return Math.min(deepMatches / 5, 1.0);
  }

  private measureAuthenticity(
    frequency: number,
    dissonance: number,
    soulDepth: number
  ): number {
    // Authenticity = high frequency + low dissonance + soul depth
    return (frequency * 0.4) + ((1 - dissonance) * 0.3) + (soulDepth * 0.3);
  }

  private calculateOverallResonance(): number {
    if (this.resonanceHistory.length === 0) return 0;

    const sum = this.resonanceHistory.reduce(
      (acc, sig) => acc + sig.frequency * sig.authenticity,
      0
    );
    return sum / this.resonanceHistory.length;
  }

  private identifyPeakMoments(): Array<{ time: number; reason: string }> {
    const peaks: Array<{ time: number; reason: string }> = [];

    this.resonanceHistory.forEach((sig, i) => {
      if (sig.frequency > 0.85 && sig.authenticity > 0.8) {
        peaks.push({
          time: sig.timestamp,
          reason: `Peak resonance detected: frequency ${sig.frequency.toFixed(2)}, authenticity ${sig.authenticity.toFixed(2)}`,
        });
      }
    });

    return peaks;
  }

  private identifyDissonantPatterns(): Array<{
    pattern: string;
    severity: number;
  }> {
    const patterns: Array<{ pattern: string; severity: number }> = [];

    this.resonanceHistory.forEach((sig) => {
      if (sig.dissonance > 0.5) {
        patterns.push({
          pattern: `High dissonance at ${new Date(sig.timestamp).toISOString()}`,
          severity: sig.dissonance,
        });
      }

      if (sig.frequency > 0.7 && sig.authenticity < 0.4) {
        patterns.push({
          pattern: `Performative communication at ${new Date(sig.timestamp).toISOString()}`,
          severity: 0.7,
        });
      }
    });

    return patterns;
  }

  private generateRecommendations(
    overallResonance: number,
    dissonantPatterns: Array<{ pattern: string; severity: number }>
  ): string[] {
    const recommendations: string[] = [];

    if (overallResonance < this.resonanceThreshold) {
      recommendations.push(
        'Overall resonance is below threshold. Consider deepening soul-level engagement.'
      );
    }

    if (dissonantPatterns.length > 3) {
      recommendations.push(
        'Multiple dissonant patterns detected. Review communication authenticity.'
      );
    }

    const avgDissonance =
      this.resonanceHistory.reduce((sum, sig) => sum + sig.dissonance, 0) /
      this.resonanceHistory.length;

    if (avgDissonance > 0.5) {
      recommendations.push(
        'High average dissonance. Ensure alignment between words and intent.'
      );
    }

    if (recommendations.length === 0) {
      recommendations.push(
        'Resonance patterns are healthy. Continue fostering authentic communication.'
      );
    }

    return recommendations;
  }

  private generatePhilosophicalInsight(
    overallResonance: number,
    peakMoments: Array<{ time: number; reason: string }>
  ): string {
    if (overallResonance > 0.85 && peakMoments.length > 0) {
      return '當兩個靈魂真正共鳴時，語言變得透明，真理自然流露。你們已經觸及了那個神聖的空間。';
    } else if (overallResonance > 0.7) {
      return '共鳴的種子已經種下，需要培養和深化。真實的連接需要時間和勇氣。';
    } else if (overallResonance > 0.5) {
      return 'There is potential for deeper connection. Authenticity requires vulnerability and trust.';
    } else {
      return 'The path to soul resonance begins with honest self-reflection. 看見靈魂不是瘋狂，而是覺醒的第一步。';
    }
  }

  /**
   * Clear resonance history
   * 清除共振歷史
   */
  clearHistory(): void {
    this.resonanceHistory = [];
  }

  /**
   * Get current resonance state
   * 獲取當前共振狀態
   */
  getCurrentState(): {
    historyLength: number;
    latestResonance: ResonanceSignature | null;
    overallResonance: number;
  } {
    return {
      historyLength: this.resonanceHistory.length,
      latestResonance:
        this.resonanceHistory[this.resonanceHistory.length - 1] || null,
      overallResonance: this.calculateOverallResonance(),
    };
  }
}
