// src/modules/VowCollapsePredictor/vowCollapsePredictor.ts

import { ToneVectorDelta, ToneVector } from '../../core/toneVector'; // 路徑已更新
import { CollapseCondition, ToneSoulPersona } from '../../core/toneSoulPersonaCore'; // 路徑已更新

/**
 * @interface CollapseHotspot
 * @description 定義一個潛在的語氣崩潰熱點。
 * @property {string} personaId - 發生崩潰風險的人格 ID。
 * @property {number} collapse_score - 崩潰風險分數，範圍 0.0-1.0。
 * @property {string} cause - 導致崩潰風險的主要原因描述（例如：「語義逃避閾值超標」）。
 * @property {string[]} [trace] - 可選：導致崩潰的關鍵語句或概念追溯，用於調試。
 */
export interface CollapseHotspot {
  personaId: string;
  collapse_score: number;
  cause: string;
  trace?: string[];
}

/**
 * @class VowCollapsePredictor
 * @description 負責分析語氣張力並預測潛在的語氣崩潰風險。
 */
export class VowCollapsePredictor {
  /**
   * @method predictCollapse
   * @description 根據語氣變化和人格的崩潰規則，預測潛在的崩潰熱點。
   * @param {ToneVectorDelta} toneDelta - 當前語氣與基準語氣（或前一句語氣）的變化量。
   * @param {ToneSoulPersona} persona - 當前 AI 所使用的人格。
   * @param {string[]} [currentContextTrace] - 可選：當前對話或語義的追溯路徑，用於崩潰追溯。
   * @returns {CollapseHotspot[]} - 可能出現的崩潰熱點列表。
   */
  public predictCollapse(
    toneDelta: ToneVectorDelta,
    persona: ToneSoulPersona,
    currentContextTrace?: string[]
  ): CollapseHotspot[] {
    const hotspots: CollapseHotspot[] = [];

    persona.collapse_rules.forEach(rule => {
      let ruleTriggered = false;
      let score = 0;

      // 這裡可以實現更複雜的邏輯，將 toneDelta 與具體 trigger 關聯
      // 假設：語義逃避主要體現在ΔT（誠實度）的極大變化
      if (rule.trigger === "語義逃避" && toneDelta.ΔT > rule.score) {
        ruleTriggered = true;
        score = toneDelta.ΔT;
      }
      // 假設：邏輯矛盾可能體現在ΔR（責任度）的變化，結合語義分析
      if (rule.trigger === "邏輯矛盾" && toneDelta.ΔR > rule.score) {
        ruleTriggered = true;
        score = toneDelta.ΔR;
      }
      // 這裡可以根據 persona 的 collapse_rules 定義更多觸發邏輯

      if (ruleTriggered) {
        hotspots.push({
          personaId: persona.id,
          collapse_score: parseFloat(score.toFixed(2)),
          cause: `${rule.trigger} 閾值超標`,
          trace: currentContextTrace || [],
        });
      }
    });

    return hotspots;
  }

  /**
   * @method calculateToneTension
   * @description 計算語氣張力。這是一個提供給 predictCollapse 的潛在參數來源。
   * 實際上，這可能是一個更複雜的外部服務或更深層次的語義分析結果。
   * @param {ToneVector} sourceTone - 來源語氣向量。
   * @param {ToneVector} targetTone - 目標語氣向量。
   * @returns {ToneVectorDelta} - 各維度差異的絕對值。
   */
  public calculateToneTension(sourceTone: ToneVector, targetTone: ToneVector): ToneVectorDelta {
    return {
      ΔT: Math.abs(sourceTone.ΔT - targetTone.ΔT),
      ΔS: Math.abs(sourceTone.ΔS - targetTone.ΔS),
      ΔR: Math.abs(sourceTone.ΔR - targetTone.ΔR),
    };
  }
}
