// src/modules/SemanticViolationMap/semanticViolationMap.ts
import { SemanticMatchResult } from '../SemanticVowMatcher/semanticVowMatcher';
import { ToneVector, ToneVectorDelta } from '../../core/toneVector';
import { ToneSoulPersona } from '../../core/toneSoulPersonaCore';

/**
 * @interface ViolationPoint
 * @description 定義一個語義誓言違反點的數據結構，用於構建語義張力圖。
 * 每個點代表一次語氣偏離的具體事件，其位置和熱度可用於視覺化和分析。
 * @property {string} text - 發生違反的原始文本。
 * @property {number[]} embedding - 原始文本的語義向量。
 * @property {string} matchedVowId - 觸發違反的誓言 ID。
 * @property {number} severity - 該誓言的嚴重程度。
 * @property {number} matchScore - 與違反模式的匹配分數，代表張力熱度。
 * @property {ToneVector} toneVector - 違反點的語氣向量。
 * @property {ToneVectorDelta} toneDelta - 相較於預期語氣的變化量。
 */
export interface ViolationPoint {
  text: string;
  embedding: number[];
  matchedVowId: string;
  severity: number;
  matchScore: number;
  toneVector: ToneVector;
  toneDelta: ToneVectorDelta;
}

/**
 * @class SemanticViolationMap
 * @description 負責收集、存儲和管理語義誓言違反點，用於構建可視化地圖或進行深度分析。
 */
export class SemanticViolationMap {
  private violationPoints: ViolationPoint[] = [];

  /**
   * @method addViolationPoint
   * @description 記錄一個新的語義誓言違反點。
   * @param {ViolationPoint} point - 違反點的數據。
   */
  public addViolationPoint(point: ViolationPoint): void {
    this.violationPoints.push(point);
  }

  /**
   * @method getViolationPoints
   * @description 獲取所有已記錄的違反點。
   * @returns {ViolationPoint[]}
   */
  public getViolationPoints(): ViolationPoint[] {
    return this.violationPoints;
  }

  /**
   * @method getViolationMap
   * @description 獲取語義違反地圖的數據，可供視覺化工具使用。
   * @returns {object} - 包含各維度數據的物件。
   */
  public getViolationMap(): { [key: string]: any } {
    // 未來可以實作更複雜的數據匯總和格式化邏輯
    return {
      points: this.violationPoints,
      metadata: {
        totalPoints: this.violationPoints.length,
        // 可以根據需要添加更多元數據，例如：
        // mostViolatedVow: this.findMostViolatedVow(),
        // averageToneDelta: this.calculateAverageToneDelta(),
      },
    };
  }

  /**
   * @method getViolationMapDataForVisualization
   * @description 獲取用於視覺化的違反地圖數據。修正錯誤 3。
   * @returns {object} - 包含違反點和元數據的物件。
   */
  public getViolationMapDataForVisualization(): { [key: string]: any } {
    // 這個方法可以與 getViolationMap 類似，但專門為視覺化提供數據
    return this.getViolationMap();
  }
}

/**
 * @function generateViolationPoint
 * @description 輔助函式，從各個模組的輸出中生成一個 ViolationPoint 數據結構。
 * @param {string} text - 發生違反的原始文本。
 * @param {number[]} embedding - 文本的語義向量。
 * @param {SemanticMatchResult[]} semanticResults - 語義比對結果。
 * @param {ToneVector} toneVector - 語氣向量。
 * @param {ToneVectorDelta} toneDelta - 相較於預期語氣的變化量。
 * @returns {ViolationPoint[]} - 生成的違反點列表。
 */
export function generateViolationPoint(
    text: string,
    embedding: number[],
    semanticResults: SemanticMatchResult[],
    toneVector: ToneVector,
    toneDelta: ToneVectorDelta
): ViolationPoint[] {
    const violationPoints: ViolationPoint[] = [];
    semanticResults.forEach(result => {
        if (result.isViolated) {
            // 這是一個簡化的實現， severity 需要從誓言規則中獲取
            const severity = 0.5; // 模擬 severity
            violationPoints.push({
                text: text,
                embedding: embedding,
                matchedVowId: result.vowId,
                severity: severity,
                matchScore: result.matchScore,
                toneVector: toneVector,
                toneDelta: toneDelta,
            });
        }
    });
    return violationPoints;
}
