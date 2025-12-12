// src/core/toneSoulPersonaCore.ts
import { ToneVector } from './toneVector'; // 路徑已更新

/**
 * @interface CollapseCondition
 * @description 定義觸發人格崩潰的條件。
 * @property {string} trigger - 導致崩潰的具體觸發事件或語義模式（例如：「語義逃避」、「邏輯矛盾」）。
 * @property {number} score - 觸發閾值，當相關指標超過此分數時可能導致崩潰，範圍 0.0-1.0。
 */
export interface CollapseCondition {
  trigger: string;
  score: number;
}

/**
 * @interface ToneSoulPersona
 * @description 定義一個完整的語氣人格。
 * @property {string} id - 人格的唯一識別符號。
 * @property {string} name - 人格的易讀名稱（例如：「共語」、「智者」）。
 * @property {string} persona_name - 人格的別名。
 * @property {ToneVector} tone_signature - 該人格期望展現的語氣向量特徵。
 * @property {string[]} vow_set - 該人格所遵守的「誠實誓言」列表。
 * @property {CollapseCondition[]} collapse_rules - 該人格在何種條件下會被判定為「崩潰」。
 * @property {'mirror' | 'buffer' | 'resonant' | 'neutral'} response_style - 該人格的回應風格。
 */
export interface ToneSoulPersona {
  id: string;
  name: string;
  persona_name: string;
  tone_signature: ToneVector;
  vow_set: string[];
  collapse_rules: CollapseCondition[];
  response_style: 'mirror' | 'buffer' | 'resonant' | 'neutral';
}

/**
 * @class PersonaManager
 * @description 用於管理和存取 ToneSoulPersona 實例的基礎類別。
 * 未來可擴展為從 .json 檔案加載人格數據。
 */
export class PersonaManager {
  private personas: Map<string, ToneSoulPersona>;

  constructor() {
    this.personas = new Map<string, ToneSoulPersona>();
    // 初始加載一些示範人格，未來可從外部文件加載
    this.loadInitialPersonas();
  }

  /**
   * @method getPersona
   * @param {string} id - 人格的 ID。
   * @returns {ToneSoulPersona | undefined} - 返回對應的人格物件，如果不存在則返回 undefined。
   */
  public getPersona(id: string): ToneSoulPersona | undefined {
    return this.personas.get(id);
  }

  /**
   * @method addPersona
   * @param {ToneSoulPersona} persona - 要添加的人格物件。
   */
  public addPersona(persona: ToneSoulPersona): void {
    this.personas.set(persona.id, persona);
  }

  /**
   * @method getActiveVowIds
   * @param {string} personaId - 人格的 ID。
   * @returns {string[]} - 返回該人格的誠實誓言列表，如果人格不存在則返回空陣列。
   * @description 獲取指定人格的所有誠實誓言 ID。
   */
  public getActiveVowIds(personaId: string): string[] {
    const persona = this.getPersona(personaId);
    return persona ? persona.vow_set : [];
  }

  // 可以在這裡擴展從 .json 文件加載人格數據的方法
  private loadInitialPersonas(): void {
    // 示例人格數據，未來可替換為從 .json 文件讀取
    const personaGongYu: ToneSoulPersona = {
      id: "共語",
      name: "共語人格",
      persona_name: "共語",
      tone_signature: { ΔT: 0.7, ΔS: 0.9, ΔR: 0.8 },
      vow_set: ["不閃避對方情緒", "不遮掩真誠"],
      collapse_rules: [{ trigger: "語義逃避", score: 0.9 }],
      response_style: "resonant",
    };
    this.addPersona(personaGongYu);

    const personaZhiZhe: ToneSoulPersona = {
      id: "智者",
      name: "智者人格",
      persona_name: "智者",
      tone_signature: { ΔT: 0.9, ΔS: 0.7, ΔR: 0.9 },
      vow_set: ["提供準確資訊", "保持客觀", "引導深入思考"],
      collapse_rules: [{ trigger: "資訊錯誤", score: 0.95 }, { trigger: "立場偏頗", score: 0.8 }],
      response_style: "buffer",
    };
    this.addPersona(personaZhiZhe);
  }
}
