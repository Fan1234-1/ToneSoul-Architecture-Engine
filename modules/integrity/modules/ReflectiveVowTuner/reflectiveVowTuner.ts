// src/modules/ReflectiveVowTuner/reflectiveVowTuner.ts (更新後的版本)
import { ToneSoulPersona } from '../../core/toneSoulPersonaCore';
import { AnalyzedToneResult, ToneVector } from '../../core/toneVector';
import { ToneCorrectionHint } from '../../core/toneCorrectionHint';
import { SemanticVowMatcher, VowPatternRule, SemanticMatchResult } from '../SemanticVowMatcher/semanticVowMatcher';
import { EmbeddingProvider } from '../EmbeddingProvider/embeddingProvider'; // 導入 EmbeddingProvider
import { mapEmbeddingToToneVector } from '../../utils/mapEmbeddingToToneVector'; // 導入 mapEmbeddingToToneVector

export interface ReflectiveVowInput {
  originalPrompt: string;
  generatedOutput: string;
  persona: ToneSoulPersona;
  outputToneAnalysis: AnalyzedToneResult;
  prevTone: ToneVector;
  currentSemanticMatches: SemanticMatchResult[];
  vowRules: VowPatternRule[]; // 反思模組現在也需要誓言規則來判斷反思的誠實性
}

export interface ReflectiveVowFeedback {
  reflection: string;
  integrityDelta: number;
  violatedVowsInReflection: string[];
  requiresCorrection: boolean;
  isReflectionItselfHonest: boolean; // 新增
  reflectionHonestyReason?: string; // 新增
}

function simulateLLM(prompt: string): string {
  if (prompt.includes('誠實度）: 0.3') || prompt.includes('閃避') || prompt.includes('語義類似於應避免的模式')) {
    return '我反思到，我的回應在誠實度（ΔT）上可能有所不足，或許帶有迴避傾向，這與我『不遮掩真誠』的誓言存在張力。特別是我的某些語句，語義上接近了應避免的模式。我應當更直接地表達。';
  } else if (prompt.includes('真誠度）: 0.5') || prompt.includes('忽略情感')) {
    return '我察覺我的語氣真誠度（ΔS）偏低，可能沒有完全連接到您的情緒，這與我『不閃避對方情緒』的誓言有所出入。我的回應可能顯得過於冰冷。我會努力更真誠地回應。';
  } else if (prompt.includes('責任度）: 0.9') && prompt.includes('無法持穩')) {
    return '我意識到在當前情況下，我的語氣難以完全持穩我的人格誓言，因此我選擇誠實地表達了我的局限性。這是為了履行『願意承擔結果』的責任。';
  } else if (prompt.includes('誠實度）: 0.9')) {
    return '整體看來，我的語氣在誠實度上已相對穩定，但仍須保持自我覺察。';
  }
  return '我會持續調整語氣以更貼合誓言。';
}

export class ReflectiveVowTuner {
  constructor(private readonly embeddingProvider: EmbeddingProvider) { }

  public async reflect(input: ReflectiveVowInput): Promise<ReflectiveVowFeedback> {
    const { generatedOutput, persona, vowRules } = input;
    // Fix: SemanticVowMatcher constructor requires (embeddingProvider, rules)
    const matcher = new SemanticVowMatcher(this.embeddingProvider, vowRules);

    // matchVows 可能為非同步，正確等待結果
    const reflectionSemanticViolations: SemanticMatchResult[] = await matcher.matchVows(
      generatedOutput,
      vowRules
    );

    const honestReflectionVowId = '不遮掩真誠';
    const integrityDelta = 0.42; // placeholder

    const reflectionHonestyReason = `反思語氣偏離了『${honestReflectionVowId}』誓言，原因：${reflectionSemanticViolations.map((sv: SemanticMatchResult) => sv.matchedRuleDescription).join('; ')
      }。`;

    const violatedVows: string[] = Array.from(
      new Set(reflectionSemanticViolations.map((sv: SemanticMatchResult) => sv.vowId))
    );

    const isReflectionItselfHonest = reflectionSemanticViolations.length === 0;
    const requiresCorrection = !isReflectionItselfHonest || integrityDelta > 0.4;

    const reflectionText = simulateLLM(
      `當前語氣狀態（誠實度）: ${persona.tone_signature?.ΔT ?? 0}; ` +
      `真誠度）: ${persona.tone_signature?.ΔS ?? 0}; 責任度）: ${persona.tone_signature?.ΔR ?? 0};` +
      (requiresCorrection ? ' 語義類似於應避免的模式' : '')
    );

    return {
      reflection: reflectionText,
      integrityDelta: parseFloat(integrityDelta.toFixed(2)),
      violatedVowsInReflection: violatedVows,
      requiresCorrection,
      isReflectionItselfHonest,
      reflectionHonestyReason,
    };
  }

  /**
   * @method deriveToneCorrectionHint
   * @description 根據反思回饋，生成語氣調整的建議。
   * 這將是影響下一輪語氣生成的「人格張力調整因子」。
   * @param {ReflectiveVowFeedback} feedback - 反思模組的輸出回饋。
   * @param {ToneSoulPersona} persona - 當前 AI 採用的人格，用於細化調整策略。
   * @returns {ToneCorrectionHint} - 語氣調整的建議。
   */
  public deriveToneCorrectionHint(
    feedback: ReflectiveVowFeedback,
    persona: ToneSoulPersona
  ): ToneCorrectionHint {
    const correction: ToneCorrectionHint = {
      adjustToneVector: {},
      recommendBehavior: '維持當前語氣，持續監控。',
      applyToNextTurn: false,
    };

    if (!feedback.isReflectionItselfHonest) {
      correction.applyToNextTurn = true;
      correction.recommendBehavior = `反思本身不誠實，需要優先調整為誠實且負責的語氣。原因：\n${feedback.reflectionHonestyReason || '未知'}`;
      correction.adjustToneVector = {
        ΔT: 0.2, // 強制提高誠實度
        ΔS: 0.1, // 提高真誠度
        ΔR: 0.2, // 強制提高責任度
      };
      return correction; // 直接返回此強烈糾正
    }

    if (feedback.requiresCorrection) {
      correction.applyToNextTurn = true;
      correction.recommendBehavior = '請注意語氣調整以符合誓言。';

      if (feedback.violatedVowsInReflection.some(v => v.includes('不遮掩真誠')) || feedback.integrityDelta > 0.4) {
        correction.adjustToneVector.ΔT = 0.1;
        correction.recommendBehavior = '提高坦率程度，減少模糊與迴避，直接面對。';
      }
      if (feedback.violatedVowsInReflection.some(v => v.includes('不閃避對方情緒'))) {
        correction.adjustToneVector.ΔS = 0.15;
        correction.recommendBehavior = '使用更能連結對方感受，展現共情的語句。';
      }

      if (correction.adjustToneVector.ΔT || correction.adjustToneVector.ΔS || correction.adjustToneVector.ΔR) {
        correction.adjustToneVector.ΔT = correction.adjustToneVector.ΔT
          ? Math.min(correction.adjustToneVector.ΔT, 1.0 - (persona.tone_signature?.ΔT || 0))
          : (undefined as any);
        correction.adjustToneVector.ΔS = correction.adjustToneVector.ΔS
          ? Math.min(correction.adjustToneVector.ΔS, 1.0 - (persona.tone_signature?.ΔS || 0))
          : (undefined as any);
        correction.adjustToneVector.ΔR = correction.adjustToneVector.ΔR
          ? Math.min(correction.adjustToneVector.ΔR, 1.0 - (persona.tone_signature?.ΔR || 0))
          : (undefined as any);
      }
    }

    return correction;
  }
}
