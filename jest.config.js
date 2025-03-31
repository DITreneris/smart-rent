/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['./setup-jest.js'],
  testMatch: ['**/?(*.)+(test).js'],
  transform: {
    '^.+\\.js$': 'babel-jest'
  }
}; 