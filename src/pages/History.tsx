
import React, { useState } from 'react';
import { Calendar, Leaf, TrendingUp, Search, Filter, MoreHorizontal, Eye, Download, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';

interface AnalysisRecord {
  id: string;
  date: string;
  plantName: string;
  growthScore: number;
  leafCount: number;
  beforeImage: string;
  afterImage: string;
  status: 'completed' | 'processing' | 'failed';
}

const History = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<'date' | 'score' | 'name'>('date');

  // Mock data
  const analysisHistory: AnalysisRecord[] = [
    {
      id: '1',
      date: '2024-02-01',
      plantName: 'Monstera Deliciosa',
      growthScore: 78.5,
      leafCount: 24,
      beforeImage: 'https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=400&h=300&fit=crop',
      afterImage: 'https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=400&h=300&fit=crop',
      status: 'completed'
    },
    {
      id: '2',
      date: '2024-01-15',
      plantName: 'Fiddle Leaf Fig',
      growthScore: 85.2,
      leafCount: 18,
      beforeImage: 'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?w=400&h=300&fit=crop',
      afterImage: 'https://images.unsplash.com/photo-1465146344425-f00d5f5c8f07?w=400&h=300&fit=crop',
      status: 'completed'
    },
    {
      id: '3',
      date: '2024-01-01',
      plantName: 'Peace Lily',
      growthScore: 72.1,
      leafCount: 15,
      beforeImage: 'https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=400&h=300&fit=crop',
      afterImage: 'https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=400&h=300&fit=crop',
      status: 'completed'
    },
  ];

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'bg-plant-100 text-plant-700';
    if (score >= 60) return 'bg-earth-100 text-earth-700';
    return 'bg-red-100 text-red-700';
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return <Badge className="bg-plant-100 text-plant-700">Completed</Badge>;
      case 'processing':
        return <Badge className="bg-earth-100 text-earth-700">Processing</Badge>;
      case 'failed':
        return <Badge variant="destructive">Failed</Badge>;
      default:
        return null;
    }
  };

  const filteredHistory = analysisHistory.filter(record =>
    record.plantName.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-2xl p-8 shadow-lg">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold bg-plant-gradient bg-clip-text text-transparent mb-2">
              Analysis History
            </h1>
            <p className="text-gray-600">Track your plant growth journey over time</p>
          </div>
          
          <div className="flex items-center space-x-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <Input
                placeholder="Search plants..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 w-64"
              />
            </div>
            <Button variant="outline" size="icon">
              <Filter className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Total Analyses</CardTitle>
            <Calendar className="h-4 w-4 text-plant-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-800">{analysisHistory.length}</div>
            <p className="text-xs text-gray-500 mt-1">Completed this month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Average Score</CardTitle>
            <TrendingUp className="h-4 w-4 text-plant-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-800">
              {(analysisHistory.reduce((acc, record) => acc + record.growthScore, 0) / analysisHistory.length).toFixed(1)}
            </div>
            <p className="text-xs text-plant-600 mt-1">+12% from last month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Plants Tracked</CardTitle>
            <Leaf className="h-4 w-4 text-plant-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-800">
              {new Set(analysisHistory.map(record => record.plantName)).size}
            </div>
            <p className="text-xs text-gray-500 mt-1">Unique plants</p>
          </CardContent>
        </Card>
      </div>

      {/* Analysis Records */}
      <div className="space-y-4">
        {filteredHistory.map((record) => (
          <Card key={record.id} className="hover:shadow-lg transition-all duration-200">
            <CardContent className="p-6">
              <div className="flex flex-col lg:flex-row lg:items-center gap-6">
                {/* Images */}
                <div className="flex space-x-3">
                  <div className="relative">
                    <img
                      src={record.beforeImage}
                      alt="Before"
                      className="w-24 h-24 object-cover rounded-lg border-2 border-gray-200"
                    />
                    <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 bg-gray-700 text-white text-xs px-2 py-1 rounded">
                      Before
                    </div>
                  </div>
                  <div className="flex items-center">
                    <TrendingUp className="w-6 h-6 text-plant-500" />
                  </div>
                  <div className="relative">
                    <img
                      src={record.afterImage}
                      alt="After"
                      className="w-24 h-24 object-cover rounded-lg border-2 border-plant-200"
                    />
                    <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 bg-plant-700 text-white text-xs px-2 py-1 rounded">
                      After
                    </div>
                  </div>
                </div>

                {/* Details */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-800 mb-1">
                        {record.plantName}
                      </h3>
                      <p className="text-sm text-gray-500 mb-2">
                        Analyzed on {new Date(record.date).toLocaleDateString()}
                      </p>
                      <div className="flex items-center space-x-4 text-sm">
                        <div className="flex items-center space-x-1">
                          <Leaf className="w-4 h-4 text-plant-500" />
                          <span>{record.leafCount} leaves</span>
                        </div>
                        <Badge className={getScoreColor(record.growthScore)}>
                          Score: {record.growthScore.toFixed(1)}
                        </Badge>
                        {getStatusBadge(record.status)}
                      </div>
                    </div>

                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon">
                          <MoreHorizontal className="w-4 h-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem>
                          <Eye className="w-4 h-4 mr-2" />
                          View Details
                        </DropdownMenuItem>
                        <DropdownMenuItem>
                          <Download className="w-4 h-4 mr-2" />
                          Download Report
                        </DropdownMenuItem>
                        <DropdownMenuItem className="text-red-600">
                          <Trash2 className="w-4 h-4 mr-2" />
                          Delete
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>
                </div>

                {/* Score Circle */}
                <div className="flex-shrink-0">
                  <div className="w-20 h-20 relative">
                    <svg className="w-20 h-20 transform -rotate-90" viewBox="0 0 100 100">
                      <circle
                        cx="50"
                        cy="50"
                        r="35"
                        stroke="currentColor"
                        strokeWidth="6"
                        fill="transparent"
                        className="text-gray-200"
                      />
                      <circle
                        cx="50"
                        cy="50"
                        r="35"
                        stroke="currentColor"
                        strokeWidth="6"
                        fill="transparent"
                        strokeDasharray={`${(record.growthScore / 100) * 219.8} 219.8`}
                        className={record.growthScore >= 80 ? 'text-plant-500' : record.growthScore >= 60 ? 'text-earth-500' : 'text-red-500'}
                      />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <span className={`text-lg font-bold ${record.growthScore >= 80 ? 'text-plant-600' : record.growthScore >= 60 ? 'text-earth-600' : 'text-red-600'}`}>
                        {Math.round(record.growthScore)}
                      </span>
                      <span className="text-xs text-gray-500">score</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredHistory.length === 0 && (
        <div className="text-center py-12">
          <Leaf className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-600 mb-2">No analyses found</h3>
          <p className="text-gray-500">Start analyzing your plants to see their growth history here.</p>
        </div>
      )}
    </div>
  );
};

export default History;
