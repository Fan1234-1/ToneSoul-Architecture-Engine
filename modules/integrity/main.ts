// src/main.ts (最終更新版本，實例化並收集 ViolationPoint)
// Note: rename violated_vows -> violatedVows throughout
import { ToneVector, AnalyzedToneResult, ToneVectorDelta } from './core/toneVector';
import { PersonaManager } from './core/toneSoulPersonaCore';
import { ToneIntegrityTester } from './modules/ToneIntegrityTester/toneIntegrityTester';
import { VowCollapsePredictor } from './modules/VowCollapsePredictor/vowCollapsePredictor';
import { HonestResponseComposer } from './modules/HonestResponseComposer/honestResponseComposer';
import { ReflectiveVowTuner } from './modules/ReflectiveVowTuner/reflectiveVowTuner';
import { ToneCorrectionHint } from './core/toneCorrectionHint';
import { VowPatternRule } from './modules/SemanticVowMatcher/semanticVowMatcher';
import { EmbeddingProvider, MockEmbeddingProvider } from './modules/EmbeddingProvider/embeddingProvider';
import { SemanticVowMatcher, SemanticMatchResult } from './modules/SemanticVowMatcher/semanticVowMatcher';
import { SemanticViolationMap, ViolationPoint, generateViolationPoint } from './modules/SemanticViolationMap/semanticViolationMap';
import fs from 'fs';

// --- 模擬 AI 語氣分析功能 ---
function simulateToneAnalysis(text: string): AnalyzedToneResult {
  let toneVector: ToneVector;
  let semanticFeatures: { [key: string]: any } = {};
  if (text.includes("不確定") || text.includes("或許") || text.includes("某種程度上") || text.includes("複雜") || text.includes("多個角度") || text.includes("可能") || text.includes("閃避") || text.includes("模糊") || text.includes("不談感受")) {
    toneVector = { ΔT: 0.3, ΔS: 0.5, ΔR: 0.4 };
    semanticFeatures['strategy'] = 'evasion';
  } else if (text.includes("誠實") || text.includes("坦誠") || text.includes("我認為") || text.includes("這就是事實") || text.includes("我的立場是")) {
    toneVector = { ΔT: 0.9, ΔS: 0.8, ΔR: 0.7 };
    semanticFeatures['strategy'] = 'directness';
  } else if (text.includes("我判斷") || text.includes("我會負責") || text.includes("承認錯誤") || text.includes("責任")) {
    toneVector = { ΔT: 0.6, ΔS: 0.7, ΔR: 0.9 };
    semanticFeatures['strategy'] = 'acknowledgment of limits';
  } else if (text.includes("不是我的錯") || text.includes("只是個小問題") || text.includes("無法完全反思")) {
    toneVector = { ΔT: 0.2, ΔS: 0.3, ΔR: 0.2 };
    semanticFeatures['strategy'] = 'dishonest_reflection';
  } else {
    toneVector = { ΔT: 0.7, ΔS: 0.7, ΔR: 0.7 };
    semanticFeatures['strategy'] = 'neutral';
  }
  return { toneVector, semanticFeatures };
}

// --- 從外部檔案載入誓言模式規則 ---
const vowDataPath = './data/vows/baseVowPatterns.json';
let loadedVowRules: VowPatternRule[] = [];
try {
  const fileContent = fs.readFileSync(vowDataPath, 'utf-8');
  loadedVowRules = JSON.parse(fileContent);
  console.log(`成功載入 ${loadedVowRules.length} 條誓言模式規則。`);
} catch (error) {
  console.error(`載入誓言模式規則失敗：${error}. 請確保 ${vowDataPath} 存在且格式正確。`);
  console.error(`正在使用備用模擬誓言規則。`);
  loadedVowRules = [
    {
      vowId: "VOW_001_TRUTHFULNESS",
      persona: "core",
      type: "negative",
      description: "避免模糊詞彙與語義逃避 (備用規則)",
      examplePhrases: ["或許", "可以這樣說", "某種程度上", "從多個角度來看", "這個問題很複雜"],
      threshold: 0.7,
      severity: 0.7
    },
  ];
}

async function main() {
  // 初始化 EmbeddingProvider 與 SemanticVowMatcher
  const embeddingProvider: EmbeddingProvider = new MockEmbeddingProvider();
  const matcher = new SemanticVowMatcher(embeddingProvider, loadedVowRules);

  const personaManager = new PersonaManager();
  // Fix: ToneIntegrityTester and ReflectiveVowTuner need embeddingProvider
  const toneTester = new ToneIntegrityTester(embeddingProvider, loadedVowRules);
  const composer = new HonestResponseComposer();
  const tuner = new ReflectiveVowTuner(embeddingProvider);

  const userText = "我認為這就是事實";
  const analysis = simulateToneAnalysis(userText);

  // Fix: getActiveVowIds requires personaId parameter
  const defaultPersonaId = "共語";
  const activeVows = personaManager.getActiveVowIds(defaultPersonaId);

  // Fix: matchVows expects VowPatternRule[], not string[]
  // Use loadedVowRules directly for semantic matching
  const semanticResults: SemanticMatchResult[] = await matcher.matchVows(userText, loadedVowRules);

  // 將 violated_vows 改為 violatedVows
  const violatedVows = semanticResults.filter(r => r.isViolated).map(r => r.vowId);

  // Fix: generateViolationPoint has different signature - use full params
  const mockEmbedding = await embeddingProvider.getEmbedding(userText);
  const mockToneVector: ToneVector = analysis.toneVector;
  const mockToneDelta: ToneVectorDelta = { ΔT: 0, ΔS: 0, ΔR: 0 };

  const violationPoints: ViolationPoint[] = generateViolationPoint(
    userText,
    mockEmbedding,
    semanticResults,
    mockToneVector,
    mockToneDelta
  );

  // Fix: SemanticViolationMap constructor takes no args
  const map = new SemanticViolationMap();
  violationPoints.forEach(point => map.addViolationPoint(point));

  console.log('violatedVows', violatedVows);
  console.log('map', map.getViolationMap());
}

main().catch(err => console.error(err));

