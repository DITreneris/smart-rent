import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FaExclamationTriangle, FaHome } from 'react-icons/fa';

const NotFound = () => {
  // Add preload hints for faster navigation to commonly accessed pages
  useEffect(() => {
    // Preload the Home page component for faster navigation
    const link = document.createElement('link');
    link.rel = 'preload';
    link.as = 'script';
    link.href = '/static/js/main.chunk.js';
    document.head.appendChild(link);

    return () => {
      // Clean up preload link on unmount
      document.head.removeChild(link);
    };
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
      <FaExclamationTriangle className="text-yellow-500 text-6xl mb-6" />
      <h1 className="text-4xl font-bold text-gray-800 mb-4">404 - Page Not Found</h1>
      <p className="text-xl text-gray-600 mb-8 max-w-lg">
        The page you are looking for might have been removed, had its name changed, 
        or is temporarily unavailable.
      </p>
      <Link 
        to="/" 
        className="flex items-center bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
      >
        <FaHome className="mr-2" />
        Return to Home
      </Link>
    </div>
  );
};

export default React.memo(NotFound); 