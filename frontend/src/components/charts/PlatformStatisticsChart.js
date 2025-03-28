import React, { useMemo } from 'react';

/**
 * Simple statistics chart component for the admin dashboard
 * In a production app, this would use a proper charting library like Chart.js, Recharts, or D3
 */
const PlatformStatisticsChart = () => {
  // Mock data for the chart
  const chartData = useMemo(() => {
    return {
      months: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      users: [12, 19, 30, 45, 62, 78],
      properties: [5, 8, 13, 17, 22, 28],
      transactions: [3, 7, 15, 22, 30, 41]
    };
  }, []);

  // Calculate maximum value for scaling
  const maxValue = useMemo(() => {
    return Math.max(
      ...chartData.users,
      ...chartData.properties,
      ...chartData.transactions
    );
  }, [chartData]);

  // Calculate bar heights as percentage of max value
  const getBarHeight = (value) => {
    return (value / maxValue) * 150; // 150px is max bar height
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <div className="mb-4">
        <div className="flex items-center space-x-4">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-blue-500 rounded-full mr-2"></div>
            <span className="text-sm text-gray-600">Users</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
            <span className="text-sm text-gray-600">Properties</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-purple-500 rounded-full mr-2"></div>
            <span className="text-sm text-gray-600">Transactions</span>
          </div>
        </div>
      </div>

      <div className="flex items-end h-[200px] mt-6 space-x-6 border-b border-l border-gray-300">
        {chartData.months.map((month, index) => (
          <div key={month} className="flex-1 flex items-end justify-center space-x-1">
            <div 
              className="w-3 bg-blue-500 rounded-t" 
              style={{ height: `${getBarHeight(chartData.users[index])}px` }}
            ></div>
            <div 
              className="w-3 bg-green-500 rounded-t" 
              style={{ height: `${getBarHeight(chartData.properties[index])}px` }}
            ></div>
            <div 
              className="w-3 bg-purple-500 rounded-t" 
              style={{ height: `${getBarHeight(chartData.transactions[index])}px` }}
            ></div>
            <div className="absolute mt-2 text-xs text-gray-600">{month}</div>
          </div>
        ))}
      </div>

      <div className="mt-8">
        <h3 className="text-sm font-medium text-gray-700">Platform Growth</h3>
        <p className="text-xs text-gray-500 mt-1">
          Tracking user registrations, property listings, and transactions over time.
        </p>
      </div>
    </div>
  );
};

export default React.memo(PlatformStatisticsChart); 