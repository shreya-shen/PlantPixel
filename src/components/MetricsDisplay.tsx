
import React from 'react';
import { TrendingUp, TrendingDown, Activity, Sun, Droplets, Leaf } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface MetricData {
  name: string;
  value: number;
  previousValue: number;
  unit: string;
  icon: React.ElementType;
  color: string;
  description: string;
}

interface MetricsDisplayProps {
  metrics: MetricData[];
  growthScore: number;
}

const MetricsDisplay = ({ metrics, growthScore }: MetricsDisplayProps) => {
  const getChangePercent = (current: number, previous: number) => {
    if (previous === 0) return 0;
    return ((current - previous) / previous) * 100;
  };

  const formatChange = (change: number) => {
    const isPositive = change > 0;
    const TrendIcon = isPositive ? TrendingUp : TrendingDown;
    const color = isPositive ? 'text-plant-600' : 'text-red-500';
    
    return (
      <div className={`flex items-center space-x-1 ${color}`}>
        <TrendIcon className="w-4 h-4" />
        <span className="text-sm font-medium">{Math.abs(change).toFixed(1)}%</span>
      </div>
    );
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-plant-600';
    if (score >= 60) return 'text-earth-600';
    return 'text-red-500';
  };

  const getScoreBg = (score: number) => {
    if (score >= 80) return 'bg-plant-gradient';
    if (score >= 60) return 'bg-earth-gradient';
    return 'bg-gradient-to-r from-red-400 to-red-600';
  };

  return (
    <div className="space-y-6">
      {/* Growth Score Card */}
      <Card className="overflow-hidden">
        <CardHeader className={`text-white ${getScoreBg(growthScore)}`}>
          <CardTitle className="flex items-center justify-between">
            <span>Overall Growth Score</span>
            <Activity className="w-6 h-6" />
          </CardTitle>
        </CardHeader>
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <div className={`text-4xl font-bold ${getScoreColor(growthScore)} mb-2`}>
                {growthScore.toFixed(1)}
              </div>
              <p className="text-gray-600">
                {growthScore >= 80 ? 'Excellent Growth' : 
                 growthScore >= 60 ? 'Good Growth' : 'Needs Attention'}
              </p>
            </div>
            <div className="w-24 h-24 relative">
              <svg className="w-24 h-24 transform -rotate-90" viewBox="0 0 100 100">
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke="currentColor"
                  strokeWidth="8"
                  fill="transparent"
                  className="text-gray-200"
                />
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke="currentColor"
                  strokeWidth="8"
                  fill="transparent"
                  strokeDasharray={`${(growthScore / 100) * 251.2} 251.2`}
                  className={getScoreColor(growthScore)}
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className={`text-xl font-bold ${getScoreColor(growthScore)}`}>
                  {Math.round(growthScore)}%
                </span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {metrics.map((metric, index) => {
          const Icon = metric.icon;
          const change = getChangePercent(metric.value, metric.previousValue);
          
          return (
            <Card key={index} className="hover:shadow-lg transition-all duration-200 animate-fade-in">
              <CardHeader className="pb-3">
                <CardTitle className="flex items-center justify-between text-sm">
                  <span className="text-gray-700">{metric.name}</span>
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${metric.color}`}>
                    <Icon className="w-4 h-4 text-white" />
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-0">
                <div className="space-y-3">
                  <div className="flex items-end justify-between">
                    <div>
                      <div className="text-2xl font-bold text-gray-800">
                        {metric.value.toFixed(1)}
                      </div>
                      <div className="text-xs text-gray-500">{metric.unit}</div>
                    </div>
                    {formatChange(change)}
                  </div>
                  
                  <div className="text-xs text-gray-600 leading-relaxed">
                    {metric.description}
                  </div>
                  
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>Previous: {metric.previousValue.toFixed(1)}</span>
                    <span>Current: {metric.value.toFixed(1)}</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
};

export default MetricsDisplay;
