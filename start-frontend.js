// Simple script to start the React application
const { spawn } = require('child_process');
const path = require('path');

console.log('Starting the Smart Rent Frontend...');

// Get the frontend directory path
const frontendDir = path.join(__dirname, 'frontend');

// Start the React application
const reactProcess = spawn('npx', ['react-scripts', 'start'], {
  cwd: frontendDir,
  stdio: 'inherit',
  shell: true
});

reactProcess.on('error', (error) => {
  console.error('Failed to start React application:', error);
});

console.log('React development server should be starting...');
console.log('Once started, you can access the application at: http://localhost:3000'); 