// src/utils/mapEmbeddingToToneVector.ts

import { ToneVector } from '../core/toneVector';

/**
 * @function mapEmbeddingToToneVector
 * @description 概念性的函式，將語義嵌入向量映射為語氣向量 (ToneVector)。
 * 這是「反向解碼模型」的初版實作，基於簡單的規則和模擬值。
 * 未來可替換為：
 * 1. 一個訓練過的微模型，將嵌入向量映射到 ΔT, ΔS, ΔR 值。
 * 2. 基於向量相似度的查詢表，將 embedding 區域對應到 tone region。
 * @param {number[]} embedding - 文本的語義嵌入向量。
 * @returns {ToneVector} - 映射出的語氣向量。
 */
export function mapEmbeddingToToneVector(embedding: number[]): ToneVector {
  // ⚠️ 這是模擬實現。實際需要更複雜的邏輯或模型。
  // 我們假設 embedding 向量的各維度與 ToneVector 的各維度有簡單的關聯
  // 這裡僅用一個固定的模擬映射來展示其概念

  // 假設 embedding 向量長度為 3，且各維度分別對應 ΔT, ΔS, ΔR
  // 這是高度簡化的，實際嵌入向量維度會非常高
  if (embedding.length === 3) {
    return {
      ΔT: Math.min(Math.max(embedding[0], 0), 1),
      ΔS: Math.min(Math.max(embedding[1], 0), 1),
      ΔR: Math.min(Math.max(embedding[2], 0), 1),
    };
  }

  // 為了示範，我們根據模擬 embedding 的值，給出不同的 ToneVector
  // 模擬直率性（ΔT 高）的 embedding [0.9, 0.8, 0.7] -> ΔT: 0.9, ΔS: 0.8, ΔR: 0.7
  // 模擬迴避性（ΔT 低）的 embedding [0.1, 0.2, 0.3] -> ΔT: 0.1, ΔS: 0.2, ΔR: 0.3
  // 模擬負責性（ΔR 高）的 embedding [0.7, 0.7, 0.9] -> ΔT: 0.7, ΔS: 0.7, ΔR: 0.9
  // 預設中立的 embedding [0.5, 0.5, 0.5] -> ΔT: 0.5, ΔS: 0.5, ΔR: 0.5

  const delta = {
    t: (embedding[0] || 0) + (embedding[1] || 0) + (embedding[2] || 0),
    s: (embedding[3] || 0) + (embedding[4] || 0) + (embedding[5] || 0),
    r: (embedding[6] || 0) + (embedding[7] || 0) + (embedding[8] || 0),
  };

  // 這裡的邏輯是為了讓 ToneVector 的值更具隨機性，但又基於 embedding 的概念
  return {
    ΔT: parseFloat((0.5 + Math.tanh(delta.t - 1) / 2).toFixed(2)),
    ΔS: parseFloat((0.5 + Math.tanh(delta.s - 1) / 2).toFixed(2)),
    ΔR: parseFloat((0.5 + Math.tanh(delta.r - 1) / 2).toFixed(2)),
  };
}
