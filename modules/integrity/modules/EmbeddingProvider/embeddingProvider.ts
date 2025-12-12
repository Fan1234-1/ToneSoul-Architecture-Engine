// src/modules/EmbeddingProvider/embeddingProvider.ts

/**
 * @interface EmbeddingProvider
 * @description 定義一個語義嵌入提供者介面。
 * 實現此介面的類別將負責將文本轉換為數值向量 (embedding)。
 * 透過這個介面，我們可以輕鬆地替換不同的嵌入服務（例如 OpenAI, Cohere 等），
 * 而無需修改 SemanticVowMatcher 的核心邏輯。
 */
export interface EmbeddingProvider {
  /**
   * @method getEmbedding
   * @description 將給定文本轉換為語義向量。
   * @param {string} text - 要嵌入的文本。
   * @returns {Promise<number[]>} - 包含語義向量的 Promise。
   */
  getEmbedding(text: string): Promise<number[]>;

  /**
   * @method embed
   * @description 將給定文本轉換為語義向量（getEmbedding 的別名方法）。
   * @param {string} text - 要嵌入的文本。
   * @returns {Promise<number[]>} - 包含語義向量的 Promise。
   */
  embed(text: string): Promise<number[]>;
}

/**
 * @interface OpenAIErrorResponse
 * @description OpenAI API 錯誤回應的型別定義
 */
interface OpenAIErrorResponse {
  error: {
    message: string;
    type?: string;
    code?: string;
  };
}

/**
 * @interface OpenAIEmbeddingResponse
 * @description OpenAI API 嵌入回應的型別定義
 */
interface OpenAIEmbeddingResponse {
  data: Array<{
    embedding: number[];
    index: number;
  }>;
  model: string;
  usage: {
    prompt_tokens: number;
    total_tokens: number;
  };
}

/**
 * @class OpenAIEmbeddingProvider
 * @description 實現 EmbeddingProvider 介面，使用 OpenAI 的嵌入服務。
 * ⚠️ 在實際運行中，需要配置 API Key 和正確的 URL。
 */
export class OpenAIEmbeddingProvider implements EmbeddingProvider {
  private apiKey: string;
  private modelId: string;

  constructor(apiKey: string, modelId: string = "text-embedding-ada-002") {
    this.apiKey = apiKey;
    this.modelId = modelId;
  }

  async getEmbedding(text: string): Promise<number[]> {
    try {
      const response = await fetch("https://api.openai.com/v1/embeddings", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${this.apiKey}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          input: text,
          model: this.modelId
        })
      });

      if (!response.ok) {
        const errorData = await response.json() as OpenAIErrorResponse;
        throw new Error(`OpenAI API error: ${response.status} - ${errorData.error.message}`);
      }

      const json = await response.json() as OpenAIEmbeddingResponse;
      return json.data[0].embedding;
    } catch (error) {
      console.error("Error calling OpenAI Embedding API:", error);
      throw error;
    }
  }

  /**
   * @method embed
   * @description 別名方法，調用 getEmbedding。
   * @param {string} text - 要嵌入的文本。
   * @returns {Promise<number[]>} - 包含語義向量的 Promise。
   */
  async embed(text: string): Promise<number[]> {
    return this.getEmbedding(text);
  }
}

/**
 * @class MockEmbeddingProvider
 * @description 用於測試和開發的模擬嵌入提供者。
 * 將文字依字元碼的總和映射為向量，用於單元測試。
 */
export class MockEmbeddingProvider implements EmbeddingProvider {
  async getEmbedding(text: string): Promise<number[]> {
    const seed = text.split('').reduce((sum, char) => sum + char.charCodeAt(0), 0);
    return [seed / 100, (seed % 50) / 50, Math.sin(seed)];
  }

  /**
   * @method embed
   * @description 別名方法，調用 getEmbedding。
   * @param {string} text - 要嵌入的文本。
   * @returns {Promise<number[]>} - 包含語義向量的 Promise。
   */
  async embed(text: string): Promise<number[]> {
    return this.getEmbedding(text);
  }
}
