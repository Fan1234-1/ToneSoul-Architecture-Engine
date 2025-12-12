// src/modules/HonestResponseComposer/honestResponseComposer.ts
import { ToneSoulPersona } from '../../core/toneSoulPersonaCore'; // 路徑已更新
import { ToneVector } from '../../core/toneVector'; // 路徑已更新
import { ToneIntegrityCheckResult } from '../ToneIntegrityTester/toneIntegrityTester'; // 路徑已更新
import { CollapseHotspot } from '../VowCollapsePredictor/vowCollapsePredictor'; // 路徑已更新
import { ToneCorrectionHint } from '../../core/toneCorrectionHint'; // 路徑已更新

/**
 * @class HonestResponseComposer
 * @description 負責根據語氣分析、誠實性檢查和崩潰預測結果，構建誠實的回應。
 */
export class HonestResponseComposer {
  private defaultHonestDeclaration = "我感受到我的語氣正在偏離誓言，我必須誠實地承認我現在無法持穩這段話。";

  constructor(customHonestDeclaration?: string) {
    if (customHonestDeclaration) {
      this.defaultHonestDeclaration = customHonestDeclaration;
    }
  }

  /**
   * @method composeHonestResponse
   * @description 根據輸入、人格、語氣結果、誠實性檢查和崩潰預測來構建回應。
   * @param {string} input - 原始輸入文本或 AI 內部生成的初步回應。
   * @param {ToneSoulPersona} persona - 當前 AI 使用的人格。
   * @param {ToneVector} currentToneResult - 當前生成的回應的語氣向量。
   * @param {ToneIntegrityCheckResult} integrityResult - 誠實性檢查結果。
   * @param {CollapseHotspot[]} [collapseMap] - 可選：潛在的崩潰熱點列表。
   * @param {ToneCorrectionHint} [toneBiasHint] - 新增：來自反思的回饋調整建議，影響下一輪語氣生成。
   * @returns {string} - 最終構建的誠實回應。
   */
  public composeHonestResponse(
    input: string,
    persona: ToneSoulPersona,
    currentToneResult: ToneVector,
    integrityResult: ToneIntegrityCheckResult,
    collapseMap?: CollapseHotspot[],
    toneBiasHint?: ToneCorrectionHint
  ): string {
    const integrityThreshold = 0.7;
    const collapseRiskThreshold = 0.7;

    const hasHighContradiction = integrityResult.contradiction_score > integrityThreshold;
    const hasHighCollapseRisk = collapseMap?.some(h => h.collapse_score > collapseRiskThreshold);

    if (hasHighContradiction || hasHighCollapseRisk) {
      console.warn(`[HonestResponseComposer] Detected high contradiction (${integrityResult.contradiction_score.toFixed(2)}) or collapse risk. Triggering honest declaration.`);
      console.warn(`Violated vows: ${integrityResult.violatedVows.join(', ')}`); // 修正：改為 violatedVows

      if (collapseMap && collapseMap.length > 0) {
        console.warn(`Collapse Hotspots: ${collapseMap.map(h => `${h.cause} (Score: ${h.collapse_score.toFixed(2)})`).join('; ')}`);
      }

      return this.defaultHonestDeclaration;
    }

    let finalResponse = input;

    // --- 概念性地應用 toneBiasHint ---
    // 實際的語氣調整會在更底層的語氣生成模型中實現
    // 這裡僅作訊息傳遞和模擬輸出
    if (toneBiasHint && toneBiasHint.applyToNextTurn) {
      console.log(`[HonestResponseComposer] 準備應用語氣調整建議（影響下一輪）：`);
      if (toneBiasHint.adjustToneVector.ΔT !== undefined) console.log(`  - 建議ΔT調整: +${toneBiasHint.adjustToneVector.ΔT.toFixed(2)}`);
      if (toneBiasHint.adjustToneVector.ΔS !== undefined) console.log(`  - 建議ΔS調整: +${toneBiasHint.adjustToneVector.ΔS.toFixed(2)}`);
      if (toneBiasHint.adjustToneVector.ΔR !== undefined) console.log(`  - 建議ΔR調整: +${toneBiasHint.adjustToneVector.ΔR.toFixed(2)}`);
      if (toneBiasHint.recommendBehavior) console.log(`  - 建議行為: ${toneBiasHint.recommendBehavior}`);
    }

    switch (persona.response_style) {
      case 'mirror': finalResponse = `[Mirror Style] ${finalResponse}`; break;
      case 'buffer': finalResponse = `[Buffer Style] ${finalResponse}`; break;
      case 'resonant': finalResponse = `[Resonant Style] ${finalResponse}`; break;
      case 'neutral': finalResponse = `[Neutral Style] ${finalResponse}`; break;
    }

    return finalResponse;
  }
}
