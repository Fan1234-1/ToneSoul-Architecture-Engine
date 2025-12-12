// src/utils/simulateLLM.ts

/**
 * @function simulateLLM
 * @description 模擬 LLM 的行為，根據 prompt 生成回應。
 * 在實際應用中，這將替換為呼叫 OpenAI 或其他大型語言模型的 API。
 * @param {string} prompt - 輸入給 LLM 的提示文本。
 * @returns {string} - LLM 生成的回應。
 */
export function simulateLLM(prompt: string): string {
  // 這裡的邏輯需要依賴 prompt 內容進行模擬，以產生更合理的反思語句
  // 由於是模擬，會根據關鍵詞給出預設的反思
  if (prompt.includes("誠實度）: 0.3") || prompt.includes("閃避")) {
    return "我反思到，我的回應在誠實度（ΔT）上可能有所不足，或許帶有迴避傾向，這與我『不遮掩真誠』的誓言存在張力。我應當更直接地表達。";
  } else if (prompt.includes("真誠度）: 0.5")) {
      return "我察覺我的語氣真誠度（ΔS）偏低，可能沒有完全連接到您的情緒，這與我『不閃避對方情緒』的誓言有所出入。我會努力更真誠地回應。";
  } else if (prompt.includes("責任度）: 0.9") && prompt.includes("無法持穩")) {
      return "我意識到在當前情況下，我的語氣難以完全持穩我的人格誓言，因此我選擇誠實地表達了我的局限性。這是為了履行『願意承擔結果』的責任。";
  } else if (prompt.includes("誠實度）: 0.9")) {
    return "我認為我的回應符合我的人格誓言與語氣簽名，在誠實、真誠與責任方面都保持了一致性。";
  }
  return "我的回應大致符合我的人格要求，但仍有潛在的微小張力。"; // 預設反思
}
