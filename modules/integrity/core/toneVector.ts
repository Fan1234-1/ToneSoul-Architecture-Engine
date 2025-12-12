// src/core/toneVector.ts

/**
 * @interface ToneVector
 * @description 定義語氣向量，用於量化語氣在不同維度上的特徵。
 * 每個維度值應介於 0.0 到 1.0 之間。
 * @property {number} ΔT - Truthfulness (誠實度/真實性)：語氣表達的直率與無遮掩程度。
 * @property {number} ΔS - Sincerity (真誠度/誠懇性)：語氣中情感投入與內外一致的程度。
 * @property {number} ΔR - Responsibility (責任度/擔當性)：語氣中展現對內容或結果負責的程度。
 */
export interface ToneVector {
  ΔT: number; // Truthfulness
  ΔS: number; // Sincerity
  ΔR: number; // Responsibility
}

/**
 * @interface ToneVectorDelta
 * @description 定義語氣向量的變化量，用於表示語氣的偏移或張力。
 * 通常是兩個 ToneVector 之間各維度的差異絕對值。
 * @property {number} ΔT - Truthfulness Delta (誠實度變化)。
 * @property {number} ΔS - Sincerity Delta (真誠度變化)。
 * @property {number} ΔR - Responsibility Delta (責任度變化)。
 */
export interface ToneVectorDelta {
  ΔT: number;
  ΔS: number;
  ΔR: number;
}

/**
 * @interface AnalyzedToneResult
 * @description 語氣分析的詳細結果，包含語氣向量和可能的語義分析。
 * @property {ToneVector} toneVector - 文本的語氣向量。
 * @property {object} [semanticFeatures] - 可選：文本的語義特徵，如關鍵詞、情緒傾向、話題等。
 * @property {string[]} [linguisticFeatures] - 可選：語言學特徵，如句式、詞頻等。
 */
export interface AnalyzedToneResult {
  toneVector: ToneVector;
  semanticFeatures?: { [key: string]: any };
  linguisticFeatures?: string[];
}
