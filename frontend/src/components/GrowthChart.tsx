
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Legend, Area, AreaChart } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { TrendingUp, BarChart3, Activity } from 'lucide-react';

interface ChartDataPoint {
  date: string;
  growthScore: number;
  leafCount: number;
  greenPixelRatio: number;
  boundingBoxArea: number;
  colorHealthIndex: number;
}

interface GrowthChartProps {
  data: ChartDataPoint[];
  currentMetrics: any;
}

const GrowthChart = ({ data, currentMetrics }: GrowthChartProps) => {
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-800">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} style={{ color: entry.color }} className="text-sm">
              {entry.name}: {entry.value.toFixed(1)}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const metricComparisonData = [
    {
      metric: 'Leaf Count',
      before: currentMetrics?.leafCount?.previousValue || 0,
      after: currentMetrics?.leafCount?.value || 0,
    },
    {
      metric: 'Green Pixels',
      before: currentMetrics?.greenPixelRatio?.previousValue || 0,
      after: currentMetrics?.greenPixelRatio?.value || 0,
    },
    {
      metric: 'Plant Size',
      before: currentMetrics?.boundingBoxArea?.previousValue || 0,
      after: currentMetrics?.boundingBoxArea?.value || 0,
    },
    {
      metric: 'Health Index',
      before: currentMetrics?.colorHealthIndex?.previousValue || 0,
      after: currentMetrics?.colorHealthIndex?.value || 0,
    },
  ];

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Activity className="w-5 h-5 text-plant-600" />
            <span>Growth Analysis Charts</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="timeline" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="timeline" className="flex items-center space-x-2">
                <TrendingUp className="w-4 h-4" />
                <span>Timeline</span>
              </TabsTrigger>
              <TabsTrigger value="comparison" className="flex items-center space-x-2">
                <BarChart3 className="w-4 h-4" />
                <span>Before vs After</span>
              </TabsTrigger>
              <TabsTrigger value="detailed" className="flex items-center space-x-2">
                <Activity className="w-4 h-4" />
                <span>Detailed View</span>
              </TabsTrigger>
            </TabsList>

            <TabsContent value="timeline" className="mt-6">
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={data}>
                    <defs>
                      <linearGradient id="growthGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#22c55e" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis 
                      dataKey="date" 
                      stroke="#6b7280"
                      fontSize={12}
                    />
                    <YAxis 
                      stroke="#6b7280"
                      fontSize={12}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Area
                      type="monotone"
                      dataKey="growthScore"
                      stroke="#22c55e"
                      strokeWidth={3}
                      fill="url(#growthGradient)"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </TabsContent>

            <TabsContent value="comparison" className="mt-6">
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={metricComparisonData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis 
                      dataKey="metric" 
                      stroke="#6b7280"
                      fontSize={12}
                    />
                    <YAxis 
                      stroke="#6b7280"
                      fontSize={12}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend />
                    <Bar 
                      dataKey="before" 
                      fill="#94a3b8" 
                      name="Before"
                      radius={[4, 4, 0, 0]}
                    />
                    <Bar 
                      dataKey="after" 
                      fill="#22c55e" 
                      name="After"
                      radius={[4, 4, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </TabsContent>

            <TabsContent value="detailed" className="mt-6">
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis 
                      dataKey="date" 
                      stroke="#6b7280"
                      fontSize={12}
                    />
                    <YAxis 
                      stroke="#6b7280"
                      fontSize={12}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="leafCount" 
                      stroke="#22c55e" 
                      strokeWidth={2}
                      name="Leaf Count"
                      dot={{ fill: '#22c55e', strokeWidth: 2, r: 4 }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="greenPixelRatio" 
                      stroke="#0ea5e9" 
                      strokeWidth={2}
                      name="Green Pixel Ratio"
                      dot={{ fill: '#0ea5e9', strokeWidth: 2, r: 4 }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="colorHealthIndex" 
                      stroke="#f59e0b" 
                      strokeWidth={2}
                      name="Health Index"
                      dot={{ fill: '#f59e0b', strokeWidth: 2, r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};

export default GrowthChart;
