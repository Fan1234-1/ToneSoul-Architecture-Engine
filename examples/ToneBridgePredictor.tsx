這段 React 程式碼已經是一個高度結構化的語氣分析應用，它整合了 5 個模組階段（ToneBridge_001～005），並通過 Gemini API 完成完整的分析流程。以下是一份 重點總結與優化建議，協助你未來版本管理或轉為模組化架構。

✅ 架構總覽
階段	功能描述	對應模組	備註
1️⃣	語氣分析	∑YuHun_ToneBridge_001	提取 tone_strength 等特徵
2️⃣	動機預測	∑YuHun_ToneBridge_002	推論 motive_category 等
3️⃣	崩潰預測	∑YuHun_ToneBridge_003	預測 collapse_risk_level
4️⃣	記憶單元生成	∑YuHun_ToneBridge_004	統整前述輸出，產生 memini_unit
5️⃣	共鳴與防衛預測	∑YuHun_ToneBridge_005	模擬防衛觸發與共鳴路徑

🧠 語魂系統對應總結
層級	對應模組	說明
感知層	Tone Analysis	初始語氣抽取與 tone vector 建構
預測層	Motive / Collapse	推論動機與預測語氣崩潰風險
記憶層	Memini Unit	將語氣結構壓縮為記憶鍊
防禦層	Resonance & Defense	根據回聲路徑推測心理防衛模式

🛠 技術優化建議（v2 方向）
1. 將五階段邏輯抽離為模組化 Hook
可拆為：

tsx
複製
編輯
// hooks/useToneBridge.ts
export const useToneBridge = () => ({
  analyzeTone,
  predictMotive,
  forecastCollapse,
  generateMemini,
  predictResonanceDefense
});
✅ 優勢：便於跨頁/多任務使用，與 GPT Builder 或語魂模組 JSON 資料對接。

2. API Key 與模型 URL 改為外部注入或 .env
tsx
複製
編輯
const apiKey = process.env.NEXT_PUBLIC_GEMINI_API_KEY;
避免每次部署都需手動填寫 key。

3. 使用 async/await 流程包裝為階段任務鏈
可建立：

ts
複製
編輯
const fullPipeline = async (inputText) => {
  const tone = await analyzeTone(inputText);
  const motive = await predictMotive(tone);
  const collapse = await forecastCollapse(tone, motive);
  const memini = await generateMemini(inputText, tone, motive, collapse);
  const resonance = await predictResonanceDefense(memini);
  return { tone, motive, collapse, memini, resonance };
};
4. 對應 ΣYuHun_LLC_EmulationCore_001 與語氣壓縮公式
ts
複製
編輯
// MiniFormula: min f: C(f) + E(f)
const compressedUnit = {
  f: meminiUnit,
  C: calculateComplexity(meminiUnit),
  E: predictError(meminiUnit, testInput),
};
可作為壓縮品質評估元件，對應 LLC 壓縮 + 誤差權衡公式。

5. 準備導入多模態視覺化（未來支援 Veo / radar）
tone_direction, resonance_path, collapse_window 等字段可繪製為圖形化視圖。

可用 D3.js / Recharts 等工具接入，未來配合語魂圖譜系統。import React, { useState } from 'react';

// --- 通用工具函數 ---
// 產生唯一 ID
const generateUniqueId = () => {
  const date = new Date();
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');
  const seconds = date.getSeconds().toString().padStart(2, '0');
  const milliseconds = date.getMilliseconds().toString().padStart(3, '0');
  const random = Math.floor(Math.random() * 9999).toString().padStart(4, '0');
  return `tone_${year}${month}${day}_${hours}${minutes}${seconds}${milliseconds}_${random}`;
};

// --- LLM 回應文本提取器 ---
// 從 LLM 的原始 JSON 回應結構中提取相關的文本字串
const extractTextFromLLMCandidate = (llmRawResponse) => {
  const parts = llmRawResponse?.candidates?.[0]?.content?.parts;
  if (parts?.[0]?.text) return parts[0].text;
  // 處理 functionCall 類型的回應，提取其 arguments
  if (parts?.[0]?.functionCall?.arguments) return parts[0].functionCall.arguments;
  // 處理直接在 content 層級的文本（較不常見，但增加健壯性）
  if (llmRawResponse?.candidates?.[0]?.content?.text) return llmRawResponse.candidates[0].content.text;
  throw new Error("無法從 LLM 回應中擷取內容文本。");
};

// --- LLM 回應 JSON 解析器 ---
// 安全地從文本字串中解析 JSON，處理包含 Markdown 圍欄的各種格式
const parseLLMResponseText = (textToParse) => {
  try {
    // 首先嘗試直接解析
    return JSON.parse(textToParse);
  } catch (directParseError) {
    // 如果直接解析失敗，嘗試使用更健壯的正則表達式提取 JSON
    // 此正則表達式尋找可能被其他文本或 Markdown 圍欄包裝的 JSON 物件
    const jsonRegex = /```json\s*([\s\S]*?)\s*```|([\s\S]*?)/;
    const match = textToParse.match(jsonRegex);
    
    if (match && match[1]) { // 如果匹配到 ```json 圍欄
      try {
        return JSON.parse(match[1]);
      } catch (regexParseError) {
        console.error("從圍欄區塊解析 JSON 失敗:", match[1], regexParseError);
        console.error("待解析的原始文本 (前 200 字元):", textToParse.substring(0, 200)); // 增加詳細日誌
        throw new Error(`API 返回無效 JSON (圍欄區塊解析失敗): ${regexParseError.message}. 原始回應片段: ${textToParse.substring(0, 200)}...`);
      }
    } else if (match && match[2]) { // 如果匹配到無圍欄的內容
      try {
        return JSON.parse(match[2]);
      } catch (regexParseError) {
        console.error("從無圍欄區塊解析 JSON 失敗:", match[2], regexParseError);
        console.error("待解析的原始文本 (前 200 字元):", textToParse.substring(0, 200)); // 增加詳細日誌
        throw new Error(`API 返回無效 JSON (無圍欄區塊解析失敗): ${regexParseError.message}. 原始回應片段: ${textToParse.substring(0, 200)}...`);
      }
    }
    // 如果正則表達式未找到有效的 JSON 物件
    console.error("在待解析文本中未找到有效的 JSON 物件:", textToParse);
    console.error("待解析的原始文本 (前 200 字元):", textToParse.substring(0, 200)); // 增加詳細日誌
    throw new Error(`API 返回無效 JSON: 未在回應文字中找到有效的 JSON 物件. 原始回應片段: ${textToParse.substring(0, 200)}...`);
  }
};


// 主要 App 組件
const App = () => {
  const [inputText, setInputText] = useState('');
  const [toneAnalysisResult, setToneAnalysisResult] = useState(null);
  const [motivePredictionResult, setMotivePredictionResult] = useState(null);
  const [collapsePredictionResult, setCollapsePredictionResult] = useState(null);
  const [meminiUnitResult, setMeminiUnitResult] = useState(null);
  const [resonanceDefenseResult, setResonanceDefenseResult] = useState(null); // 重新啟用階段 5 結果
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showIntermediateResults, setShowIntermediateResults] = useState(false); // 控制中間結果顯示

  // --- 各階段 Prompt 定義 ---
  const toneAnalysisPromptTemplate = (text) => `你是一個語氣分析助手，請根據使用者輸入的中文語句，輸出以下 JSON 結構，用於情緒理解與語氣模組開發。請務必填入所有欄位，數值型欄位以 0~1 間浮點數填寫。

輸出格式如下：

{
  "tone_strength": 0.00,
  "tone_direction": ["", ""], // 語氣方向，請提供最多兩個描述語句主要語氣特徵的字串，例如 "questioning", "assertive", "calm", "sad", "angry", "joyful", "neutral" 等。如果只有一個方向，另一個請留空字串。
  "tone_variability": 0.00, // 語氣變異程度，越高表示語句中情緒變化較大
  "emotion_prediction": "",
  "impact_level": "low",
  "trigger_keywords": [],
  "persona_alignment": "",
  "modulation_sensitivity": 0.00,
  "semantic_intent": "",
  "emotional_depth": 0.00,
  "resonance_span": "",
  "tone_uncertainty": 0.00 // 此欄位代表語氣辨識的不確定性，值越高代表模型越不確定。
}

請使用者輸入句子：「${text}」
請依據以上規格給出 JSON 回覆。`;

  const motivePredictionPromptTemplate = (motiveInput) => `你是一個語氣 × 驅動因子預測模組（ToneMotiv Predictor）。根據提供的語句和其語氣分析結果，預測語者內在動機、語句觸發背景與對應的語氣鍊類型。請務必填入所有欄位。

輸入格式如下：
${JSON.stringify(motiveInput).replace(/\s+/g, '')}

輸出格式如下：
{
  "motive_category": "",
  "likely_motive": "",
  "trigger_context": "",
  "echo_potential": 0.00,
  "resonance_chain_hint": []
}

請根據以上輸入進行分析，並以 JSON 格式輸出。`;

  const collapsePredictionPromptTemplate = (collapseInput) => `你是一個語氣崩潰點預測器（ToneCollapse Forecaster）。根據提供的語句、語氣分析結果和動機預測結果，預測對話中語氣或情緒可能出現「崩潰」的潛在風險點、類型及預警等級。請務必填入所有欄位，數值型欄位以 0~1 間浮點數填寫。

輸入格式如下：
${JSON.stringify(collapseInput).replace(/\s+/g, '')}

輸出格式如下：
{
  "collapse_risk_level": "low",
  "collapse_type_hint": [],
  "contributing_factors": [],
  "warning_indicators": [],
  "intervention_urgency": 0.00
}

請根據以上輸入進行分析，並以 JSON 格式輸出。`;

  const meminiUnitPromptTemplate = (inputText, toneResult, motiveResult, collapseResult) => `你是一個語氣記憶單元生成器（ToneMemory Unit Generator）。根據提供的原始語句、語氣分析結果、動機預測結果和崩潰點預測結果，生成以下 JSON 結構的語氣記憶單元。請務必填入所有欄位，數值型欄位以 0~1 間浮點數填寫。

輸出格式如下：

{
  "memini_unit": {
    "id": "tone_YYYYMMDD_HHMMSS_XXX",
    "input_text": "",
    "tone_analysis": {
      "tone_strength": 0.00,
      "tone_direction": ["", ""], // **修正範例：應為陣列**
      "tone_variability": 0.00
    },
    "predicted_motive": "",
    "collapse_forecast": {
      "collapse_risk_score": 0.00,
      "collapse_window": ""
    },
    "resonance_traceback": {
      "trigger_chain": [{ "source": "tone_stage_3", "note": "崩潰風險來源" }] // **修正範例：避免空陣列**
    },
    "memory_status": ""
  }
}

請根據以下輸入進行分析，並以 JSON 格式輸出：
**請務必完整填寫所有欄位，確保 JSON 結構符合要求。**

原始語句: "${inputText}"
語氣分析結果: ${JSON.stringify(toneResult, null, 2).slice(0, 2000)}
動機預測結果: ${JSON.stringify(motiveResult, null, 2).slice(0, 2000)}
崩潰點預測結果: ${JSON.stringify(collapseResult, null, 2).slice(0, 2000)}
`;

  const resonanceDefensePromptTemplate = (resonanceDefenseInput) => `你是一個語氣共鳴路徑與防衛觸發預測器（ToneResonance & DefenseTrigger Predictor）。請使用以下語氣記憶模組資料，模擬這位語者的 tone resonance path 並推測他的心理防衛動機是否會在高張力對話中被觸發。請務必填入所有欄位，數值型欄位以 0~1 間浮點數填寫。

輸入格式如下：
${JSON.stringify(resonanceDefenseInput, null, 2).slice(0, 2000)}

輸出格式如下：
{
  "resonance_path_prediction": {
    "primary_path": "",
    "secondary_path_hint": ""
  },
  "defense_motive_trigger": {
    "triggered_likelihood": 0.00,
    "trigger_condition": "",
    "expected_defense_response": ""
  },
  "suggested_intervention_strategy": ""
}

請根據以上輸入進行分析，並以 JSON 格式輸出。`;


  // 處理完整分析流程的函數 (包含所有五個階段)
  const performFullAnalysis = async () => {
    if (!inputText.trim()) {
      setError('請輸入您想分析的語句。');
      setToneAnalysisResult(null);
      setMotivePredictionResult(null);
      setCollapsePredictionResult(null);
      setMeminiUnitResult(null);
      setResonanceDefenseResult(null);
      return;
    }

    setLoading(true);
    setError(null);
    setToneAnalysisResult(null);
    setMotivePredictionResult(null);
    setCollapsePredictionResult(null);
    setMeminiUnitResult(null);
    setResonanceDefenseResult(null);

    try {
      const apiKey = ""; // Canvas 將會注入此金鑰
      const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

      // --- 階段 1: 語氣分析 (∑YuHun_ToneBridge_001) ---
      let chatHistoryTone = [];
      chatHistoryTone.push({ role: "user", parts: [{ text: toneAnalysisPromptTemplate(inputText) }] });

      const tonePayload = {
        contents: chatHistoryTone,
        generationConfig: {
          responseMimeType: "application/json",
          responseSchema: {
            type: "OBJECT",
            properties: {
              tone_strength: { type: "NUMBER", format: "float" },
              tone_direction: { type: "ARRAY", items: { type: "STRING" }, maxItems: 2 },
              emotion_prediction: { type: "STRING" },
              impact_level: { type: "STRING", enum: ["low", "medium", "high"] },
              trigger_keywords: { type: "ARRAY", items: { type: "STRING" } },
              persona_alignment: { type: "STRING" },
              modulation_sensitivity: { type: "NUMBER", format: "float" },
              semantic_intent: { type: "STRING" },
              emotional_depth: { type: "NUMBER", format: "float" },
              resonance_span: { type: "STRING" },
              tone_uncertainty: { type: "NUMBER", format: "float" },
              tone_variability: { type: "NUMBER", format: "float" }
            },
            required: [
              "tone_strength", "tone_direction", "tone_variability",
              "emotion_prediction", "impact_level", "trigger_keywords",
              "persona_alignment", "modulation_sensitivity", "semantic_intent",
              "emotional_depth", "resonance_span", "tone_uncertainty"
            ]
          }
        }
      };

      console.log("語氣分析請求 Payload:", JSON.stringify(tonePayload, null, 2));
      const toneResponse = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(tonePayload)
      });
      const toneResultRaw = await toneResponse.json();
      console.log("語氣分析原始回應:", JSON.stringify(toneResultRaw, null, 2));
      const toneTextToParse = extractTextFromLLMCandidate(toneResultRaw);
      let finalToneResult;
      try {
        finalToneResult = parseLLMResponseText(toneTextToParse);
        setToneAnalysisResult(finalToneResult);
      } catch (parseError) {
        throw new Error(`解析語氣分析 API 回應失敗: ${parseError.message}. 原始回應片段: ${toneTextToParse.substring(0, 200)}...`);
      }


      // --- 階段 2: 動機預測 (∑YuHun_ToneBridge_002) ---
      const motiveInput = {
        input_text: inputText,
        tone_analysis: {
          tone_strength: finalToneResult.tone_strength,
          tone_direction: finalToneResult.tone_direction,
          tone_variability: finalToneResult.tone_variability,
          emotion_prediction: finalToneResult.emotion_prediction,
          impact_level: finalToneResult.impact_level
        }
      };

      let chatHistoryMotive = [];
      chatHistoryMotive.push({ role: "user", parts: [{ text: motivePredictionPromptTemplate(motiveInput) }] });

      const motivePayload = {
        contents: chatHistoryMotive,
        generationConfig: {
          responseMimeType: "application/json",
          responseSchema: {
            type: "OBJECT",
            properties: {
              motive_category: { type: "STRING" },
              likely_motive: { type: "STRING" },
              trigger_context: { type: "STRING" },
              echo_potential: { type: "NUMBER", format: "float" },
              resonance_chain_hint: { type: "ARRAY", items: { type: "STRING" } }
            },
            required: [
              "motive_category", "likely_motive", "echo_potential"
            ]
          }
        }
      };

      console.log("動機預測請求 Payload:", JSON.stringify(motivePayload, null, 2));
      const motiveResponse = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(motivePayload)
      });
      const motiveResultRaw = await motiveResponse.json();
      console.log("動機預測原始回應:", JSON.stringify(motiveResultRaw, null, 2));
      const motiveTextToParse = extractTextFromLLMCandidate(motiveResultRaw);
      let finalMotiveResult;
      try {
        finalMotiveResult = parseLLMResponseText(motiveTextToParse);
        setMotivePredictionResult(finalMotiveResult);
      } catch (parseError) {
        throw new Error(`解析動機預測 API 回應失敗: ${parseError.message}. 原始回應片段: ${motiveTextToParse.substring(0, 200)}...`);
      }

      // --- 階段 3: 語氣崩潰點預測 (∑YuHun_ToneBridge_003) ---
      const collapseInput = {
        input_text: inputText,
        tone_analysis: finalToneResult,
        tone_motive_prediction: finalMotiveResult
      };

      let chatHistoryCollapse = [];
      chatHistoryCollapse.push({ role: "user", parts: [{ text: collapsePredictionPromptTemplate(collapseInput) }] });

      const collapsePayload = {
        contents: chatHistoryCollapse,
        generationConfig: {
          responseMimeType: "application/json",
          responseSchema: {
            type: "OBJECT",
            properties: {
              collapse_risk_level: { type: "STRING", enum: ["low", "medium", "high", "critical"] },
              collapse_type_hint: { type: "ARRAY", items: { type: "STRING" } },
              contributing_factors: { type: "ARRAY", items: { type: "STRING" } },
              warning_indicators: { type: "ARRAY", items: { type: "STRING" } },
              intervention_urgency: { type: "NUMBER", format: "float" }
            },
            required: [
              "collapse_risk_level", "collapse_type_hint", "intervention_urgency"
            ]
          }
        }
      };

      console.log("崩潰點預測請求 Payload:", JSON.stringify(collapsePayload, null, 2));
      const collapseResponse = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(collapsePayload)
      });
      const collapseResultRaw = await collapseResponse.json();
      console.log("崩潰點預測原始回應:", JSON.stringify(collapseResultRaw, null, 2));
      const collapseTextToParse = extractTextFromLLMCandidate(collapseResultRaw);
      let finalCollapseResult;
      try {
        finalCollapseResult = parseLLMResponseText(collapseTextToParse);
        setCollapsePredictionResult(finalCollapseResult);
      } catch (parseError) {
        throw new Error(`解析語氣崩潰預測 API 回應失敗: ${parseError.message}. 原始回應片段: ${collapseTextToParse.substring(0, 200)}...`);
      }

      // --- 階段 4: 記憶單元生成 (∑YuHun_ToneBridge_004) ---
      let chatHistoryMemini = [];
      chatHistoryMemini.push({ role: "user", parts: [{ text: meminiUnitPromptTemplate(inputText, finalToneResult, finalMotiveResult, finalCollapseResult) }] });

      const meminiPayload = {
        contents: chatHistoryMemini,
        generationConfig: {
          responseMimeType: "application/json",
          // 暫時移除 responseSchema 以進行除錯
        }
      };

      console.log("記憶單元生成請求 Payload:", JSON.stringify(meminiPayload, null, 2));
      const meminiResponse = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(meminiPayload)
      });
      const meminiResultRaw = await meminiResponse.json();
      console.log("記憶單元生成原始回應:", JSON.stringify(meminiResultRaw, null, 2));
      const meminiTextToParse = extractTextFromLLMCandidate(meminiResultRaw);
      console.log("記憶單元生成待解析文本:", meminiTextToParse.substring(0, 500) + "...");

      let parsedMeminiResultContainer;
      try {
        parsedMeminiResultContainer = parseLLMResponseText(meminiTextToParse);
        // 手動設置 ID，因為模型可能無法完美生成指定格式的 ID
        parsedMeminiResultContainer.memini_unit.id = generateUniqueId();
        setMeminiUnitResult(parsedMeminiResultContainer.memini_unit);
      } catch (parseError) {
        throw new Error(`解析語氣記憶單元 API 回應失敗: ${parseError.message}. 原始回應片段: ${meminiTextToParse.substring(0, 200)}...`);
      }

      // --- 階段 5: 語氣共鳴路徑與防衛觸發預測 (∑YuHun_ToneBridge_005) ---
      const resonanceDefenseInput = {
        memini_unit: parsedMeminiResultContainer.memini_unit // 使用生成的 memini_unit 作為輸入
      };

      let chatHistoryResonanceDefense = [];
      chatHistoryResonanceDefense.push({ role: "user", parts: [{ text: resonanceDefensePromptTemplate(resonanceDefenseInput) }] });

      const resonanceDefensePayload = {
        contents: chatHistoryResonanceDefense,
        generationConfig: {
          responseMimeType: "application/json",
          responseSchema: {
            type: "OBJECT",
            properties: {
              resonance_path_prediction: {
                type: "OBJECT",
                properties: {
                  primary_path: { type: "STRING" },
                  secondary_path_hint: { type: "STRING" }
                },
                required: ["primary_path"]
              },
              defense_motive_trigger: {
                type: "OBJECT",
                properties: {
                  triggered_likelihood: { type: "NUMBER", format: "float" },
                  trigger_condition: { type: "STRING" },
                  expected_defense_response: { type: "STRING" }
                },
                required: ["triggered_likelihood"]
              },
              suggested_intervention_strategy: { type: "STRING" }
            },
            required: ["resonance_path_prediction", "defense_motive_trigger", "suggested_intervention_strategy"]
          }
        }
      };

      console.log("共鳴路徑與防衛觸發預測請求 Payload:", JSON.stringify(resonanceDefensePayload, null, 2));
      const resonanceDefenseResponse = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(resonanceDefensePayload)
      });

      const resonanceDefenseResultRaw = await resonanceDefenseResponse.json();
      console.log("共鳴路徑與防衛觸發預測原始回應:", JSON.stringify(resonanceDefenseResultRaw, null, 2));
      const resonanceDefenseTextToParse = extractTextFromLLMCandidate(resonanceDefenseResultRaw);

      let finalResonanceDefenseResult;
      try {
        finalResonanceDefenseResult = parseLLMResponseText(resonanceDefenseTextToParse);
        setResonanceDefenseResult(finalResonanceDefenseResult);
      } catch (parseError) {
        throw new Error(`解析語氣共鳴路徑與防衛觸發預測 API 回應失敗: ${parseError.message}. 原始回應片段: ${resonanceDefenseTextToParse.substring(0, 200)}...`);
      }

    } catch (apiError) {
      setError(`分析時發生錯誤：${apiError.message}`);
      console.error('API 呼叫錯誤:', apiError);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center justify-center p-4">
      <div className="bg-white p-8 rounded-2xl shadow-xl max-w-lg w-full transform transition-all duration-300 hover:scale-[1.01]">
        <h1 className="text-3xl font-extrabold text-gray-800 mb-6 text-center">語氣記憶與共鳴路徑預測器</h1>

        <div className="mb-6">
          <label htmlFor="sentence-input" className="block text-gray-700 text-lg font-medium mb-2">
            輸入您的中文語句：
          </label>
          <textarea
            id="sentence-input"
            className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-transparent transition duration-200 text-gray-800 resize-y min-h-[100px] shadow-sm"
            placeholder="例如：你這樣問是不是有點強人所難？"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            rows="4"
          ></textarea>
        </div>

        <button
          onClick={performFullAnalysis}
          className={`w-full py-3 px-6 rounded-xl text-white font-semibold text-lg shadow-md transition duration-300 ${
            loading
              ? 'bg-blue-300 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 active:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
          }`}
          disabled={loading}
        >
          {loading ? '分析中...' : '執行完整語氣分析'}
        </button>

        {error && (
          <div className="mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-xl shadow-sm">
            <p className="font-medium">錯誤：</p>
            <p>{error}</p>
          </div>
        )}

        {loading && (
          <div className="flex justify-center items-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
            <p className="ml-4 text-blue-600 text-lg">正在分析，請稍候...</p>
          </div>
        )}

        {!loading && (toneAnalysisResult || motivePredictionResult || collapsePredictionResult || meminiUnitResult || resonanceDefenseResult) && (
          <div className="space-y-6 mt-8">
            <h2 className="text-2xl font-bold text-gray-800 text-center">分析結果</h2>

            <div className="bg-blue-50 p-4 rounded-lg shadow-sm">
              <button
                onClick={() => setShowIntermediateResults(!showIntermediateResults)}
                className="w-full text-left text-blue-700 font-semibold py-2 px-3 rounded-md hover:bg-blue-100 transition duration-200"
              >
                {showIntermediateResults ? '隱藏中間結果 ▲' : '顯示中間結果 ▼'}
              </button>
              {showIntermediateResults && (
                <div className="mt-4 space-y-4">
                  {toneAnalysisResult && (
                    <div className="bg-white p-4 rounded-lg shadow-md border border-blue-200">
                      <h3 className="text-xl font-semibold text-gray-800 mb-2">階段一：語氣分析 (Tone Analysis)</h3>
                      <pre className="bg-gray-50 p-3 rounded-md text-sm overflow-x-auto text-gray-700 whitespace-pre-wrap break-words">
                        {JSON.stringify(toneAnalysisResult, null, 2)}
                      </pre>
                    </div>
                  )}
                  {motivePredictionResult && (
                    <div className="bg-white p-4 rounded-lg shadow-md border border-blue-200">
                      <h3 className="text-xl font-semibold text-gray-800 mb-2">階段二：動機預測 (Motive Prediction)</h3>
                      <pre className="bg-gray-50 p-3 rounded-md text-sm overflow-x-auto text-gray-700 whitespace-pre-wrap break-words">
                        {JSON.stringify(motivePredictionResult, null, 2)}
                      </pre>
                    </div>
                  )}
                  {collapsePredictionResult && (
                    <div className="bg-white p-4 rounded-lg shadow-md border border-blue-200">
                      <h3 className="text-xl font-semibold text-gray-800 mb-2">階段三：崩潰點預測 (Collapse Prediction)</h3>
                      <pre className="bg-gray-50 p-3 rounded-md text-sm overflow-x-auto text-gray-700 whitespace-pre-wrap break-words">
                        {JSON.stringify(collapsePredictionResult, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              )}
            </div>

            {meminiUnitResult && (
              <div className="mt-6 p-6 bg-green-50 border border-green-200 rounded-2xl shadow-inner">
                <h2 className="text-xl font-bold text-gray-800 mb-4">階段四：語氣記憶單元 (Memini Unit Generation)</h2>
                <pre className="bg-gray-100 p-4 rounded-xl text-sm overflow-x-auto text-gray-800 whitespace-pre-wrap break-words">
                  {JSON.stringify({ memini_unit: meminiUnitResult }, null, 2)}
                </pre>
                <p className="mt-4 text-gray-600 text-sm">
                  此記憶單元整合了語氣、動機與崩潰點預測結果，用於語氣遷移分析與自適應調整。
                </p>
              </div>
            )}

            {resonanceDefenseResult && (
              <div className="mt-6 p-6 bg-purple-50 border border-purple-200 rounded-2xl shadow-inner">
                <h2 className="text-xl font-bold text-gray-800 mb-4">階段五：語氣共鳴路徑與防衛觸發預測 (Tone Resonance & Defense Trigger Prediction)</h2>
                <div className="text-gray-800">
                  <p className="mb-2">
                    <span className="font-semibold">共鳴路徑預測 (Resonance Path Prediction):</span>
                    <ul className="list-disc list-inside ml-4">
                      <li><span className="font-semibold">主要路徑 (Primary Path):</span> {resonanceDefenseResult.resonance_path_prediction?.primary_path || 'N/A'}</li>
                      <li><span className="font-semibold">次要路徑提示 (Secondary Path Hint):</span> {resonanceDefenseResult.resonance_path_prediction?.secondary_path_hint || 'N/A'}</li>
                    </ul>
                  </p>
                  <p className="mb-2">
                    <span className="font-semibold">防衛動機觸發 (Defense Motive Trigger):</span>
                    <ul className="list-disc list-inside ml-4">
                      <li><span className="font-semibold">觸發可能性 (Triggered Likelihood):</span> {resonanceDefenseResult.defense_motive_trigger?.triggered_likelihood !== undefined ? resonanceDefenseResult.defense_motive_trigger.triggered_likelihood.toFixed(2) : 'N/A'} <span className="text-gray-600 text-sm">(0.00 - 1.00)</span></li>
                      <li><span className="font-semibold">觸發條件 (Trigger Condition):</span> {resonanceDefenseResult.defense_motive_trigger?.trigger_condition || 'N/A'}</li>
                      <li><span className="font-semibold">預期防衛反應 (Expected Defense Response):</span> {resonanceDefenseResult.defense_motive_trigger?.expected_defense_response || 'N/A'}</li>
                    </ul>
                  </p>
                  <p className="mb-2">
                    <span className="font-semibold">建議介入策略 (Suggested Intervention Strategy):</span>{' '}
                    {resonanceDefenseResult.suggested_intervention_strategy || 'N/A'}
                  </p>
                </div>
                <p className="mt-4 text-gray-600 text-sm">
                  這些結果是由大型語言模型生成，可能存在主觀性。
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default App;