const { spawn } = require('child_process');

console.log('啟動 server...');

const server = spawn('npx', ['tsx', 'src/api/server.ts'], {
  stdio: 'inherit',
  shell: true
});

server.on('error', (error) => {
  console.error('Server 錯誤:', error);
});

server.on('exit', (code) => {
  console.log('Server 退出，代碼:', code);
});

// 等待 2 秒後測試
setTimeout(async () => {
  console.log('測試 API...');
  
  try {
    const http = require('http');
    
    const options = {
      hostname: 'localhost',
      port: 3000,
      path: '/hello',
      method: 'GET'
    };

    const req = http.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        console.log('Status:', res.statusCode);
        console.log('Response:', JSON.stringify(JSON.parse(data), null, 2));
        process.exit(0);
      });
    });

    req.on('error', (error) => {
      console.error('請求錯誤:', error);
      process.exit(1);
    });

    req.end();
  } catch (error) {
    console.error('測試錯誤:', error);
    process.exit(1);
  }
}, 2000);