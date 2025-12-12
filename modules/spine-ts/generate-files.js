const { SoulTracer } = require('./dist/soul/tracer');

async function generateFiles() {
  const tracer = new SoulTracer('manual-test');
  
  tracer.record('Align', '手動生成檔案測試');
  tracer.record('Isolate', '生成 trace.jsonl 和 selfcheck.md');
  tracer.record('Borrow', '使用 SoulTracer 類別');
  tracer.record('Digitwise', '執行檔案寫入操作');
  tracer.record('Conclude', '完成檔案生成');
  
  await tracer.writeTrace();
  await tracer.writeSelfCheck();
  
  console.log('檔案生成完成');
}

generateFiles().catch(console.error);