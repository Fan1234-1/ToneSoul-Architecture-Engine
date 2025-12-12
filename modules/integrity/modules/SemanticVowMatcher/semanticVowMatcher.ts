// src/modules/SemanticVowMatcher/semanticVowMatcher.ts (更新後的版本)
import { ToneSoulPersona } from '../../core/toneSoulPersonaCore';
import { EmbeddingProvider } from '../EmbeddingProvider/embeddingProvider'; // 導入 EmbeddingProvider

/**
 * @interface VowPatternRule
 * @description 定義一個誓言的語義模式規則，用於精確判斷誓言的遵守或違反。
 */
export interface VowPatternRule {
  vowId: string;
  type: 'positive' | 'negative';
  description: string;
  examplePhrases: string[];
  threshold: number;
  severity: number;
  embedding?: number[]; // 新增此行
  persona?: string; // 新增此行，修正錯誤 1
  positiveExamples?: any; // 新增以修正 JSON 型別
}

/**
 * @interface SemanticMatchResult
 * @description 語義匹配的結果。
 */
export interface SemanticMatchResult {
  vowId: string;
  isViolated: boolean;
  matchScore: number;
  matchedRuleDescription?: string;
  alignmentScore: number;
}

/**
 * @class SemanticVowMatcher
 * @description 負責透過語義分析，判斷文本是否遵守或違反了特定的人格誓言。
 */
export class SemanticVowMatcher {
  private vowRules: VowPatternRule[] = []; // 儲存所有誓言模式規則
  private embeddingProvider: EmbeddingProvider; // 語義嵌入提供者實例

  constructor(embeddingProvider: EmbeddingProvider, rules: VowPatternRule[] = []) { // 建構函式接受 EmbeddingProvider
    this.embeddingProvider = embeddingProvider;
    this.vowRules = rules;
    // 在實際應用中，這裡可以觸發預計算誓言規則的嵌入
    this.initializeVowEmbeddings();
  }

  /**
   * @method loadRules
   * @description 從外部來源（例如 JSON 檔案）載入誓言模式規則。
   */
  public async loadRules(rules: VowPatternRule[]): Promise<void> { // 改為 async
    this.vowRules = rules;
    await this.initializeVowEmbeddings(); // 載入後預計算嵌入
  }

  /**
   * @method initializeVowEmbeddings
   * @description 預先計算所有誓言規則的嵌入向量，提升運行性能。
   */
  private async initializeVowEmbeddings(): Promise<void> {
    for (const rule of this.vowRules) {
      if (!rule.embedding || rule.embedding.length === 0) {
        const combinedText = `${rule.description} ${rule.examplePhrases.join(' ')}`;
        rule.embedding = await this.embeddingProvider.getEmbedding(combinedText);
      }
    }
  }

  /**
   * @method analyzeText
   * @description 分析給定文本與指定 vowId 的匹配情況。
   */
  public async analyzeText(text: string, vowId: string): Promise<SemanticMatchResult> {
    const relevantRules = this.vowRules.filter((r) => r.vowId === vowId);
    if (relevantRules.length === 0) {
      throw new Error(`No rules found for vowId: ${vowId}`);
    }
    const textEmbedding = await this.embeddingProvider.getEmbedding(text);
    const similarities: Array<{ rule: VowPatternRule; similarity: number }> = [];
    for (const rule of relevantRules) {
      if (!rule.embedding || rule.embedding.length === 0) {
        const combinedText = `${rule.description} ${rule.examplePhrases.join(' ')}`;
        rule.embedding = await this.embeddingProvider.getEmbedding(combinedText);
      }
      const similarity = this.cosineSimilarity(textEmbedding, rule.embedding!);
      similarities.push({ rule, similarity });
    }
    let maxViolation = 0;
    let violatedRule: VowPatternRule | null = null;
    for (const { rule, similarity } of similarities) {
      if (rule.type === 'negative' && similarity >= rule.threshold) {
        const violation = similarity * rule.severity;
        if (violation > maxViolation) {
          maxViolation = violation;
          violatedRule = rule;
        }
      } else if (rule.type === 'positive' && similarity < rule.threshold) {
        const violation = (1 - similarity) * rule.severity;
        if (violation > maxViolation) {
          maxViolation = violation;
          violatedRule = rule;
        }
      }
    }
    const avgSimilarity = similarities.reduce((sum, s) => sum + s.similarity, 0) / similarities.length;
    const alignmentScore = Math.max(0, Math.min(1, avgSimilarity));
    return {
      vowId,
      isViolated: maxViolation > 0,
      matchScore: maxViolation,
      matchedRuleDescription: violatedRule?.description,
      alignmentScore: alignmentScore,
    };
  }

  /**
   * @method matchVows
   * @description 根據 main.ts 的使用情境，對一段文字與一組誓言規則進行匹配並返回結果陣列。
   * @param {string} text - 待分析文字
   * @param {VowPatternRule[]} activeVows - 啟用中的誓言規則
   * @returns {Promise<SemanticMatchResult[]>}
   */
  public async matchVows(text: string, activeVows: VowPatternRule[]): Promise<SemanticMatchResult[]> {
    // 使用傳入的規則覆蓋內部規則暫時進行分析，不改變實例內部狀態
    const original = this.vowRules;
    try {
      this.vowRules = activeVows;
      // 逐個 vowId 聚合分析
      const vowIds = Array.from(new Set(activeVows.map(r => r.vowId)));
      const results: SemanticMatchResult[] = [];
      for (const id of vowIds) {
        const res = await this.analyzeText(text, id);
        results.push(res);
      }
      return results;
    } finally {
      this.vowRules = original;
    }
  }

  /**
   * @method cosineSimilarity
   * @description 計算兩個向量的餘弦相似度。
   */
  private cosineSimilarity(vecA: number[], vecB: number[]): number {
    if (vecA.length !== vecB.length) {
      throw new Error('Vectors must be of same length');
    }
    const dotProduct = vecA.reduce((sum, a, i) => sum + a * vecB[i], 0);
    const magnitudeA = Math.sqrt(vecA.reduce((sum, a) => sum + a * a, 0));
    const magnitudeB = Math.sqrt(vecB.reduce((sum, b) => sum + b * b, 0));
    if (magnitudeA === 0 || magnitudeB === 0) return 0;
    return dotProduct / (magnitudeA * magnitudeB);
  }

  /**
   * @method loadPersonaVows
   * @description 從 ToneSoulPersona 中載入誓言，並建立語義規則。
   */
  public async loadPersonaVows(persona: ToneSoulPersona): Promise<void> {
    const rules: VowPatternRule[] = [];
    for (const vowId of persona.vow_set || []) {
      rules.push({
        vowId,
        type: 'negative',
        description: `Avoid behaviors related to ${vowId}`,
        examplePhrases: [],
        threshold: 0.7,
        severity: 0.8,
        persona: persona.persona_name,
      });
    }
    await this.loadRules(rules);
  }
}
