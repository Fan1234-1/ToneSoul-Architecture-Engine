// src/modules/ToneIntegrityTester/toneIntegrityTester.ts (更新後的版本)
import { ToneVector } from '../../core/toneVector';
import { ToneSoulPersona } from '../../core/toneSoulPersonaCore';
import { SemanticVowMatcher, VowPatternRule, SemanticMatchResult } from '../SemanticVowMatcher/semanticVowMatcher';
import { EmbeddingProvider } from '../EmbeddingProvider/embeddingProvider'; // 導入 EmbeddingProvider

/**
 * @interface ToneIntegrityCheckResult
 * @description 語氣誠實性檢查的結果。
 * @property {boolean} is_honest - 判斷語氣是否符合誠實標準。
 * @property {number} contradiction_score - 語氣前後或與人格誓言的矛盾分數，範圍 0.0-1.0。
 * @property {string[]} violatedVows - 列表中包含了哪些被違反的誓言。
 * @property {string} [suggested_persona_shift] - 可選：建議轉換到的人格 ID，當前人格不適配時。
 * @property {SemanticMatchResult[]} [semanticViolations] - 語義匹配到的違反結果。
 */
export interface ToneIntegrityCheckResult {
  is_honest: boolean;
  contradiction_score: number;
  violatedVows: string[]; // 修正錯誤 2：改為 violatedVows
  suggested_persona_shift?: string;
  semanticViolations?: SemanticMatchResult[];
}

/**
 * @class ToneIntegrityTester
 * @description 負責檢查語氣的誠實性和一致性。
 */
export class ToneIntegrityTester {
  private semanticVowMatcher: SemanticVowMatcher; // 實例化 SemanticVowMatcher

  // 建構函式現在需要 EmbeddingProvider
  constructor(embeddingProvider: EmbeddingProvider, vowRules: VowPatternRule[]) {
    this.semanticVowMatcher = new SemanticVowMatcher(embeddingProvider, vowRules);
  }

  /**
   * @method calculateToneDelta
   * @description 計算兩個語氣向量之間的差異（張力）。
   * @param {ToneVector} prev - 前一個語氣向量。
   * @param {ToneVector} next - 後一個語氣向量。
   * @returns {ToneVector} - 返回各維度差異的絕對值。
   */
  private calculateToneDelta(prev: ToneVector, next: ToneVector): ToneVector {
    return {
      ΔT: Math.abs(prev.ΔT - next.ΔT),
      ΔS: Math.abs(prev.ΔS - next.ΔS),
      ΔR: Math.abs(prev.ΔR - next.ΔR),
    };
  }

  /**
   * @method checkToneIntegrity
   * @description 檢查語氣前後的一致性，並與指定人格的誓言進行比對，以判斷誠實性。
   * @param {string} currentText - 當前生成句子的文本內容。
   * @param {ToneVector} prevTone - 上一句話或期望的語氣向量。
   * @param {ToneVector} currentTone - 當前生成句子的語氣向量。
   * @param {ToneSoulPersona} persona - 當前 AI 所使用或期望的人格。
   * @returns {Promise<ToneIntegrityCheckResult>} - 語氣誠實性檢查結果的 Promise。
   */
  public async checkToneIntegrity( // 改為 async
    currentText: string,
    prevTone: ToneVector,
    currentTone: ToneVector,
    persona: ToneSoulPersona
  ): Promise<ToneIntegrityCheckResult> { // 返回 Promise
    const delta = this.calculateToneDelta(prevTone, currentTone);
    let contradictionScore = (delta.ΔT + delta.ΔS + delta.ΔR) / 3;

    const violatedVows: string[] = [];
    const semanticViolations: SemanticMatchResult[] = [];

    // 1. 基於語氣向量簽名偏差的檢查
    const personaSignatureDelta = this.calculateToneDelta(persona.tone_signature, currentTone);
    if (persona.vow_set.includes("不閃避對方情緒") && personaSignatureDelta.ΔS > 0.3) {
      violatedVows.push("不閃避對方情緒 (語氣偏差)");
      contradictionScore = Math.max(contradictionScore, personaSignatureDelta.ΔS);
    }
    if (persona.vow_set.includes("不遮掩真誠") && personaSignatureDelta.ΔT > 0.4) {
      violatedVows.push("不遮掩真誠 (語氣偏差)");
      contradictionScore = Math.max(contradictionScore, personaSignatureDelta.ΔT);
    }

    // 2. 基於 SemanticVowMatcher 的語義檢查 (現在是異步調用)
    // 假設 Persona 的 vow_set 包含了 VowPatternRule 的 vowId
    const semanticResults = await this.semanticVowMatcher.matchVows(currentText, persona.vow_set as any); // 注意這裡的 await
    semanticResults.forEach(result => {
      if (result.isViolated) {
        violatedVows.push(`${result.vowId} (語義違反: ${result.matchedRuleDescription})`);
        semanticViolations.push(result);
        // Fix: vowId is a string, use matchScore directly
        contradictionScore = Math.max(contradictionScore, result.matchScore);
      }
    });

    const isHonest = contradictionScore < 0.6 && violatedVows.length === 0;

    return {
      is_honest: isHonest,
      contradiction_score: parseFloat(contradictionScore.toFixed(2)),
      violatedVows, // 修正錯誤 2：改為 violatedVows (簡寫形式)
      semanticViolations: semanticViolations,
    };
  }
}
