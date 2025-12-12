const express = require('express');

const app = express();

app.get('/hello', async (req, res) => {
  try {
    console.log('=== 開始執行 /hello ===');
    
    // 測試 SoulTracer 是否能正確載入
    const { SoulTracer } = require('./src/soul/tracer');
    console.log('✅ SoulTracer 載入成功');
    
    const tracer = new SoulTracer('hello-api-v0.2');
    console.log('✅ tracer 實例化成功');
    
    // 測試 makeReflection 方法
    const reflection = tracer.makeReflection();
    console.log('✅ makeReflection 成功:', reflection);
    
    res.json({ status: 'debug success', reflection });
  } catch (error) {
    console.error('❌ 錯誤:', error);
    res.status(500).json({ error: error.message, stack: error.stack });
  }
});

app.listen(3001, () => {
  console.log('Debug server running on port 3001');
});