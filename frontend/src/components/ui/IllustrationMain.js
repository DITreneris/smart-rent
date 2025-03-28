import React from 'react';

const IllustrationMain = () => {
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
            <stop offset="0%" stopColor="#0f2235" />
            <stop offset="100%" stopColor="#1a365d" />
          </linearGradient>
          <linearGradient id="glowGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#4299e1" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#3182ce" stopOpacity="0.2" />
          </linearGradient>
          <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="8" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
          
          {/* Animations */}
          <animateTransform
            id="rotateBlockchain"
            attributeName="transform"
            attributeType="XML"
            type="rotate"
            from="0 400 300"
            to="360 400 300"
            dur="60s"
            repeatCount="indefinite"
          />
          <animate 
            id="pulseHouse" 
            attributeName="opacity" 
            values="0.8;1;0.8" 
            dur="3s" 
            repeatCount="indefinite" 
          />
          <animate
            id="moveCoin"
            attributeName="cy"
            values="0;-10;0"
            dur="2s"
            repeatCount="indefinite"
          />
        </defs>

        {/* Background */}
        <rect width="800" height="600" fill="url(#bgGradient)" />

        {/* Blockchain Circle */}
        <g>
          <circle cx="400" cy="300" r="200" fill="none" stroke="#4299e1" strokeWidth="2" strokeDasharray="10,5" opacity="0.5">
            <animateTransform
              attributeName="transform"
              attributeType="XML"
              type="rotate"
              from="0 400 300"
              to="360 400 300"
              dur="60s"
              repeatCount="indefinite"
            />
          </circle>
        </g>

        {/* Blockchain Nodes */}
        <g>
          {[0, 45, 90, 135, 180, 225, 270, 315].map((angle, i) => {
            const x = 400 + 200 * Math.cos(angle * Math.PI / 180);
            const y = 300 + 200 * Math.sin(angle * Math.PI / 180);
            return (
              <g key={i}>
                <rect x={x-20} y={y-20} width="40" height="40" rx="5" fill="#2C5282" stroke="#4299e1" strokeWidth="1">
                  <animate 
                    attributeName="opacity" 
                    values="0.7;1;0.7" 
                    dur={`${3 + i*0.5}s`} 
                    repeatCount="indefinite" 
                  />
                </rect>
                <text x={x} y={y+5} textAnchor="middle" fill="white" fontSize="12">BLOCK</text>
              </g>
            );
          })}
        </g>

        {/* Central House */}
        <g transform="translate(325, 225)">
          {/* House base */}
          <rect x="0" y="50" width="150" height="100" fill="#81E6D9" stroke="#4FD1C5" strokeWidth="2">
            <animate 
              attributeName="fill" 
              values="#81E6D9;#4FD1C5;#81E6D9" 
              dur="5s" 
              repeatCount="indefinite" 
            />
          </rect>
          
          {/* House roof */}
          <polygon points="0,50 75,-20 150,50" fill="#3182CE" stroke="#2B6CB0" strokeWidth="2" />
          
          {/* House door */}
          <rect x="60" y="100" width="30" height="50" fill="#2C5282" />
          
          {/* House windows */}
          <rect x="25" y="70" width="30" height="30" fill="#EBF8FF" stroke="#2B6CB0" strokeWidth="1">
            <animate 
              attributeName="fill" 
              values="#EBF8FF;#BEE3F8;#EBF8FF" 
              dur="4s" 
              repeatCount="indefinite" 
            />
          </rect>
          <rect x="95" y="70" width="30" height="30" fill="#EBF8FF" stroke="#2B6CB0" strokeWidth="1">
            <animate 
              attributeName="fill" 
              values="#EBF8FF;#BEE3F8;#EBF8FF" 
              dur="4s" 
              repeatCount="indefinite" 
              begin="2s"
            />
          </rect>
          
          {/* Digital circuit overlay */}
          <path d="M0,80 H150 M30,50 V150 M120,50 V150 M75,0 V150" stroke="#4FD1C5" strokeWidth="1" strokeDasharray="5,5" opacity="0.7">
            <animate 
              attributeName="stroke-dashoffset" 
              values="0;30" 
              dur="4s" 
              repeatCount="indefinite" 
            />
          </path>
        </g>

        {/* Users and Connections */}
        {/* User 1 - Top Right */}
        <g transform="translate(600, 150)">
          <circle cx="0" cy="0" r="25" fill="#F6AD55" />
          <rect x="-15" y="-10" width="30" height="50" rx="5" fill="#ED8936" />
          <circle cx="0" cy="-25" r="15" fill="#F6AD55" />
          <line x1="0" y1="25" x2="0" y2="40" stroke="#F6AD55" strokeWidth="2" />
          <path d="M-400,-50 Q-200,-150 -200,-25" stroke="#ED8936" strokeWidth="2" strokeDasharray="5,5" filter="url(#glow)">
            <animate 
              attributeName="stroke-dashoffset" 
              values="0;100" 
              dur="4s" 
              repeatCount="indefinite" 
            />
          </path>
        </g>

        {/* User 2 - Bottom Right */}
        <g transform="translate(600, 450)">
          <circle cx="0" cy="0" r="25" fill="#F6AD55" />
          <rect x="-15" y="-10" width="30" height="50" rx="5" fill="#ED8936" />
          <circle cx="0" cy="-25" r="15" fill="#F6AD55" />
          <line x1="0" y1="25" x2="0" y2="40" stroke="#F6AD55" strokeWidth="2" />
          <path d="M-400,50 Q-200,150 -200,25" stroke="#ED8936" strokeWidth="2" strokeDasharray="5,5" filter="url(#glow)">
            <animate 
              attributeName="stroke-dashoffset" 
              values="0;100" 
              dur="4s" 
              repeatCount="indefinite" 
              begin="1s"
            />
          </path>
        </g>

        {/* User 3 - Bottom Left */}
        <g transform="translate(200, 450)">
          <circle cx="0" cy="0" r="25" fill="#F6AD55" />
          <rect x="-15" y="-10" width="30" height="50" rx="5" fill="#ED8936" />
          <circle cx="0" cy="-25" r="15" fill="#F6AD55" />
          <line x1="0" y1="25" x2="0" y2="40" stroke="#F6AD55" strokeWidth="2" />
          <path d="M200,50 Q200,150 200,25" stroke="#ED8936" strokeWidth="2" strokeDasharray="5,5" filter="url(#glow)">
            <animate 
              attributeName="stroke-dashoffset" 
              values="0;100" 
              dur="4s" 
              repeatCount="indefinite" 
              begin="2s"
            />
          </path>
        </g>

        {/* Cryptocurrency Tokens */}
        {[1, 2, 3, 4, 5].map((_, i) => {
          const angle = i * 72 * Math.PI / 180;
          const radius = 150;
          const x = 400 + radius * Math.cos(angle);
          const y = 300 + radius * Math.sin(angle);
          return (
            <g key={i} transform={`translate(${x}, ${y})`}>
              <circle cx="0" cy="0" r="15" fill="#F6E05E" stroke="#D69E2E" strokeWidth="2">
                <animate 
                  attributeName="cy" 
                  values="-5;5;-5" 
                  dur={`${2 + i*0.4}s`} 
                  repeatCount="indefinite" 
                />
                <animate 
                  attributeName="fill" 
                  values="#F6E05E;#ECC94B;#F6E05E" 
                  dur={`${3 + i*0.4}s`} 
                  repeatCount="indefinite" 
                />
              </circle>
              <text x="0" y="5" textAnchor="middle" fill="#744210" fontSize="12" fontWeight="bold">$</text>
            </g>
          );
        })}

        {/* Smart Contract Icons */}
        <g transform="translate(535, 300)">
          <rect x="-20" y="-25" width="40" height="50" fill="white" stroke="#3182CE" strokeWidth="2" rx="5">
            <animate 
              attributeName="stroke" 
              values="#3182CE;#63B3ED;#3182CE" 
              dur="3s" 
              repeatCount="indefinite" 
            />
          </rect>
          <line x1="-10" y1="-10" x2="10" y2="-10" stroke="#3182CE" strokeWidth="2" />
          <line x1="-10" y1="0" x2="10" y2="0" stroke="#3182CE" strokeWidth="2" />
          <line x1="-10" y1="10" x2="0" y2="10" stroke="#3182CE" strokeWidth="2" />
          <path d="M5,15 L15,5" stroke="#48BB78" strokeWidth="2">
            <animate 
              attributeName="stroke-width" 
              values="2;3;2" 
              dur="2s" 
              repeatCount="indefinite" 
            />
          </path>
        </g>

        <g transform="translate(265, 300)">
          <rect x="-20" y="-25" width="40" height="50" fill="white" stroke="#3182CE" strokeWidth="2" rx="5">
            <animate 
              attributeName="stroke" 
              values="#3182CE;#63B3ED;#3182CE" 
              dur="3s" 
              repeatCount="indefinite" 
              begin="1.5s"
            />
          </rect>
          <line x1="-10" y1="-10" x2="10" y2="-10" stroke="#3182CE" strokeWidth="2" />
          <line x1="-10" y1="0" x2="10" y2="0" stroke="#3182CE" strokeWidth="2" />
          <line x1="-10" y1="10" x2="0" y2="10" stroke="#3182CE" strokeWidth="2" />
          <path d="M5,15 L15,5" stroke="#48BB78" strokeWidth="2">
            <animate 
              attributeName="stroke-width" 
              values="2;3;2" 
              dur="2s" 
              repeatCount="indefinite" 
              begin="0.5s"
            />
          </path>
        </g>

        {/* Platform Title */}
        <text x="400" y="550" textAnchor="middle" fill="white" fontSize="24" fontWeight="bold">Smart Rent Platform</text>
        <text x="400" y="580" textAnchor="middle" fill="#A0AEC0" fontSize="16">Secure • Transparent • Innovative</text>
      </svg>
    </div>
  );
};

export default IllustrationMain; 