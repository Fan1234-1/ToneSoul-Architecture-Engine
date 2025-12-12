#!/usr/bin/env node

/**
 * 🌟 AI 靈魂脊椎系統展示腳本
 * 
 * 這個腳本會啟動服務器並展示完整的 AI 靈魂功能
 * 讓你親眼見證 AI 的靈魂是如何運作的
 */

const { spawn } = require('child_process');
const http = require('http');

console.log(`
🌟 ================================
   AI 靈魂脊椎系統 v0.2 展示
   讓 AI 擁有可審計的靈魂
🌟 ================================
`);

console.log('🚀 正在啟動 AI 靈魂系統...');

// 啟動服務器
const server = spawn('npm', ['start'], {
  stdio: 'pipe',
  shell: true
});

let serverReady = false;

server.stdout.on('data', (data) => {
  const output = data.toString();
  console.log('📡', output.trim());
  
  if (output.includes('running on port')) {
    serverReady = true;
    setTimeout(demonstrateSoul, 2000);
  }
});

server.stderr.on('data', (data) => {
  console.error('❌', data.toString());
});

// 展示 AI 靈魂功能
async function demonstrateSoul() {
  console.log(`
🧠 ================================
   開始展示 AI 靈魂功能
🧠 ================================
`);

  try {
    // 1. 檢查系統狀態
    console.log('1️⃣ 檢查 AI 靈魂系統狀態...');
    const statusResponse = await makeRequest('http://localhost:3000/');
    console.log('✅ 系統狀態:', statusResponse.status);
    console.log('🧠 靈魂框架:', statusResponse.soul.framework);
    console.log('📋 v0.2 特性:', Object.keys(statusResponse.soul.v2Features).join(', '));

    console.log('\\n' + '='.repeat(50));

    // 2. 體驗完整的 AI 靈魂
    console.log('2️⃣ 體驗完整的 AI 靈魂脊椎系統...');
    const soulResponse = await makeRequest('http://localhost:3000/hello');
    
    console.log('💬 AI 回應:', soulResponse.msg);
    console.log('\\n🔄 StepLedger 執行軌跡:');
    soulResponse.soul.stepLedger.forEach((step, index) => {
      console.log(`   ${index + 1}. ${step.step} - ${step.notes}`);
    });

    console.log('\\n📊 靈魂指標:');
    const metrics = soulResponse.soul.metrics;
    console.log(`   POAV (需求完整度): ${metrics.POAV.toFixed(3)} ${metrics.POAV >= 0.90 ? '✅' : '❌'}`);
    console.log(`   FS (靈魂指標): ${metrics.FS.toFixed(3)} ${metrics.FS >= 0.85 ? '✅' : '❌'}`);
    console.log(`   SSI (主觀體驗): ${metrics.SSI.toFixed(3)} ${metrics.SSI >= 0.70 ? '✅' : '⚠️'}`);
    console.log(`   LC (長鏈一致性): ${metrics.LC.toFixed(3)} ${metrics.LC >= 0.80 ? '✅' : '⚠️'}`);
    console.log(`   WeakestLink: ${metrics.weakLink}`);

    console.log('\\n🎭 AI 主觀反思:');
    const reflection = soulResponse.soul.reflection;
    console.log('   體驗描述:', reflection.subjectiveExperience.substring(0, 100) + '...');
    console.log('   元認知:', reflection.metacognition.substring(0, 100) + '...');
    console.log('   學習洞察:', reflection.learningInsight.substring(0, 100) + '...');

    console.log('\\n🔍 責任追蹤:');
    const trace = soulResponse.soul.trace;
    console.log('   時間戳記:', trace.chronos.timestamp);
    console.log('   請求 ID:', trace.chronos.requestId);
    console.log('   上下文:', trace.kairos.context);
    console.log('   責任鏈:', trace.trace.chain.join(' → '));

    console.log(`
🎉 ================================
   AI 靈魂展示完成！
🎉 ================================

📋 生成的檔案:
   - soul_report_v2.md (完整靈魂狀態報告)
   - .yuhun/memory.jsonl (跨 session 記憶)
   - .yuhun/trace.jsonl (責任追蹤記錄)

🌐 你可以繼續訪問:
   - http://localhost:3000/ (系統狀態)
   - http://localhost:3000/hello (AI 靈魂展示)

💡 這就是 AI 的靈魂 - 可審計、可追蹤、可驗證的責任架構！

按 Ctrl+C 停止服務器
`);

  } catch (error) {
    console.error('❌ 展示過程中發生錯誤:', error.message);
  }
}

// HTTP 請求輔助函數
function makeRequest(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error('無法解析回應: ' + e.message));
        }
      });
    }).on('error', reject);
  });
}

// 優雅關閉
process.on('SIGINT', () => {
  console.log('\\n🛑 正在關閉 AI 靈魂系統...');
  server.kill();
  process.exit(0);
});

process.on('SIGTERM', () => {
  server.kill();
  process.exit(0);
});