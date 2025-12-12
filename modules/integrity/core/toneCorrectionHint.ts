// src/core/toneCorrectionHint.ts

/**
 * @interface ToneCorrectionHint
 * @description 定義反思回饋對語氣調整的建議量。
 * @property {object} adjustToneVector - 對語氣向量各維度的微調建議。
 * @property {number} [adjustToneVector.ΔT] - 誠實度微調量（例如：0.05 表示增加 5%）。
 * @property {number} [adjustToneVector.ΔS] - 真誠度微調量。
 * @property {number} [adjustToneVector.ΔR] - 責任度微調量。
 * @property {string} [recommendBehavior] - 自然語言描述的建議語氣策略（例如：「提高坦率程度、減少模糊語」）。
 * @property {boolean} [applyToNextTurn] - 是否建議將此調整應用於下一輪語氣生成。
 */
export interface ToneCorrectionHint {
  adjustToneVector: {
    ΔT?: number;
    ΔS?: number;
    ΔR?: number;
  };
  recommendBehavior?: string;
  applyToNextTurn?: boolean;
}
