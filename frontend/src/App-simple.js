import React from 'react';
import './index.css';

function App() {
  return (
    <div className="container mx-auto px-4 py-8">
      <header className="bg-white shadow rounded-lg p-6 mb-8">
        <h1 className="text-3xl font-bold text-blue-600">Smart Rent Platform</h1>
        <p className="text-gray-600">A decentralized rental platform powered by blockchain</p>
      </header>
      
      <main>
        <section className="bg-white shadow rounded-lg p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Welcome to Smart Rent</h2>
          <p className="text-gray-600 mb-4">
            This is a simplified version of the application to test that React is working properly.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
            <div className="bg-blue-50 p-4 rounded-lg shadow">
              <h3 className="text-xl font-semibold text-blue-800 mb-2">Secure Rental Agreements</h3>
              <p className="text-gray-600">Use smart contracts for transparent and secure rental agreements</p>
            </div>
            
            <div className="bg-blue-50 p-4 rounded-lg shadow">
              <h3 className="text-xl font-semibold text-blue-800 mb-2">No Middlemen</h3>
              <p className="text-gray-600">Direct transactions between landlords and tenants</p>
            </div>
            
            <div className="bg-blue-50 p-4 rounded-lg shadow">
              <h3 className="text-xl font-semibold text-blue-800 mb-2">Blockchain Powered</h3>
              <p className="text-gray-600">Ethereum blockchain ensures transparency and security</p>
            </div>
          </div>
        </section>
        
        <section className="bg-white shadow rounded-lg p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Getting Started</h2>
          <p className="text-gray-600 mb-4">
            Follow these steps to start using the Smart Rent platform:
          </p>
          
          <ol className="list-decimal list-inside space-y-2 text-gray-700">
            <li>Create an account</li>
            <li>Connect your Ethereum wallet</li>
            <li>Browse available properties</li>
            <li>Sign rental agreements securely</li>
            <li>Make payments directly through the platform</li>
          </ol>
        </section>
      </main>
      
      <footer className="mt-12 text-center text-gray-500 text-sm">
        <p>Smart Rent Platform &copy; 2023 - A decentralized rental solution</p>
      </footer>
    </div>
  );
}

export default App; 