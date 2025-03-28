import React from 'react';

const IllustrationSimple = () => {
  return (
    <div className="main-illustration-container relative w-full max-w-2xl mx-auto">
      <svg 
        viewBox="0 0 800 600" 
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-auto"
      >
        {/* Gradient Background */}
        <defs>
          <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#1E3A8A" />
            <stop offset="100%" stopColor="#1E40AF" />
          </linearGradient>
          <linearGradient id="houseGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#38BDF8" />
            <stop offset="100%" stopColor="#0EA5E9" />
          </linearGradient>
          <linearGradient id="personGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#F59E0B" />
            <stop offset="100%" stopColor="#D97706" />
          </linearGradient>
          <linearGradient id="keyGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#F59E0B" />
            <stop offset="100%" stopColor="#FBBF24" />
          </linearGradient>
          <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="5" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>

        {/* Background */}
        <rect width="800" height="600" fill="url(#bgGradient)" />
        
        {/* Soft Light Effect */}
        <circle cx="400" cy="250" r="300" fill="white" opacity="0.05" />
        
        {/* Blockchain Chain - Simplified */}
        <g transform="translate(400, 300)">
          {[-150, -100, -50, 0, 50, 100, 150].map((x, i) => (
            <g key={i} transform={`translate(${x}, 0)`}>
              <circle cx="0" cy="0" r="18" fill="white" opacity="0.1" />
              <circle cx="0" cy="0" r="15" fill="white" opacity="0.15" stroke="#60A5FA" strokeWidth="1" />
            </g>
          ))}
          <path d="M-150,0 L150,0" stroke="#60A5FA" strokeWidth="2" strokeDasharray="5,5" opacity="0.7" />
        </g>

        {/* House */}
        <g transform="translate(280, 200)">
          {/* House base */}
          <rect x="0" y="50" width="160" height="120" fill="url(#houseGradient)" rx="2" ry="2" />
          
          {/* House roof */}
          <polygon points="0,50 80,-20 160,50" fill="#0369A1" />
          
          {/* House door */}
          <rect x="65" y="110" width="35" height="60" fill="#0C4A6E" rx="2" ry="2" />
          <circle cx="90" cy="140" r="3" fill="#FBBF24" />
          
          {/* House windows */}
          <rect x="25" y="70" width="30" height="30" fill="#DBEAFE" stroke="#0C4A6E" strokeWidth="1" rx="2" ry="2" />
          <rect x="105" y="70" width="30" height="30" fill="#DBEAFE" stroke="#0C4A6E" strokeWidth="1" rx="2" ry="2" />
        </g>

        {/* Person */}
        <g transform="translate(520, 310)">
          {/* Body */}
          <rect x="-25" y="-60" width="50" height="60" rx="25" ry="30" fill="url(#personGradient)" />
          
          {/* Head */}
          <circle cx="0" cy="-85" r="25" fill="#F59E0B" />
          
          {/* Arms */}
          <line x1="-25" y1="-45" x2="-50" y2="-20" stroke="#F59E0B" strokeWidth="10" strokeLinecap="round" />
          <line x1="25" y1="-45" x2="50" y2="-60" stroke="#F59E0B" strokeWidth="10" strokeLinecap="round" />
          
          {/* Legs */}
          <line x1="-15" y1="0" x2="-20" y2="50" stroke="#F59E0B" strokeWidth="10" strokeLinecap="round" />
          <line x1="15" y1="0" x2="20" y2="50" stroke="#F59E0B" strokeWidth="10" strokeLinecap="round" />
          
          {/* Face - simple smile */}
          <circle cx="-8" cy="-90" r="3" fill="#0C4A6E" />
          <circle cx="8" cy="-90" r="3" fill="#0C4A6E" />
          <path d="M-10,-80 C-5,-75 5,-75 10,-80" stroke="#0C4A6E" strokeWidth="2" fill="none" />
        </g>

        {/* Digital Key with Heart */}
        <g transform="translate(480, 220)">
          {/* Key head */}
          <circle cx="0" cy="0" r="20" fill="url(#keyGradient)" filter="url(#glow)" />
          
          {/* Key teeth */}
          <rect x="-5" y="20" width="10" height="40" fill="url(#keyGradient)" filter="url(#glow)" />
          <rect x="-15" y="30" width="10" height="10" fill="url(#keyGradient)" filter="url(#glow)" />
          <rect x="-15" y="50" width="10" height="10" fill="url(#keyGradient)" filter="url(#glow)" />
          
          {/* Digital circuit pattern in key */}
          <path d="M-10,0 H10 M0,-10 V10" stroke="white" strokeWidth="1.5" opacity="0.8" />
          
          {/* Heart in key */}
          <path d="M0,-2 C0,-6 -4,-8 -6,-8 C-10,-8 -12,-4 -12,-2 C-12,2 -6,6 0,10 C6,6 12,2 12,-2 C12,-4 10,-8 6,-8 C4,-8 0,-6 0,-2 Z" 
                fill="#EF4444" transform="scale(0.6)" />
        </g>

        {/* Connection Lines (simplified) */}
        <path d="M360,220 Q400,150 480,220" stroke="white" strokeWidth="1.5" strokeDasharray="3,3" opacity="0.6" />
        <path d="M450,310 Q400,350 360,310" stroke="white" strokeWidth="1.5" strokeDasharray="3,3" opacity="0.6" />

        {/* Small Blockchain Icons */}
        {[1, 2, 3].map((_, i) => {
          const x = 220 + i * 180;
          const y = 450;
          return (
            <g key={i} transform={`translate(${x}, ${y})`}>
              <rect x="-15" y="-15" width="30" height="30" rx="5" fill="#DBEAFE" opacity="0.9" stroke="#60A5FA" strokeWidth="1" />
              <path d="M-5,-5 H5 M-5,0 H5 M-5,5 H5" stroke="#0369A1" strokeWidth="1.5" />
            </g>
          );
        })}

        {/* Title and Subtitle */}
        <text x="400" y="520" textAnchor="middle" fill="white" fontSize="32" fontWeight="bold" fontFamily="sans-serif">Home is where your key is</text>
        <text x="400" y="550" textAnchor="middle" fill="white" fontSize="16" opacity="0.8" fontFamily="sans-serif">Secure • Simple • Human</text>
      </svg>
    </div>
  );
};

export default IllustrationSimple; 