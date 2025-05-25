
import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Calendar, TrendingUp, TrendingDown, Eye } from 'lucide-react';
import { toast } from 'sonner';

interface AnalysisRecord {
  analysis_id: string;
  growth_score: number;
  timestamp: string;
  suggestion: string;
  metrics: any;
}

const History = () => {
  const [analyses, setAnalyses] = useState<AnalysisRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedAnalysis, setSelectedAnalysis] = useState<AnalysisRecord | null>(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/history');
      if (response.ok) {
        const data = await response.json();
        setAnalyses(data.analyses || []);
      } else {
        toast.error('Failed to fetch analysis history');
      }
    } catch (error) {
      toast.error('Error connecting to server');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBadge = (score: number) => {
    if (score >= 80) return 'bg-green-100 text-green-800';
    if (score >= 60) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-plant-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold bg-plant-gradient bg-clip-text text-transparent mb-4">
          Analysis History
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Review your previous plant growth analyses and track progress over time.
        </p>
      </div>

      {analyses.length === 0 ? (
        <Card className="mx-auto max-w-2xl">
          <CardContent className="pt-6">
            <div className="text-center space-y-4">
              <Calendar className="w-16 h-16 text-gray-400 mx-auto" />
              <h3 className="text-xl font-semibold text-gray-600">No Analysis History</h3>
              <p className="text-gray-500">
                You haven't performed any plant growth analyses yet. Start by uploading some images!
              </p>
              <Button className="bg-plant-gradient hover:opacity-90">
                Start First Analysis
              </Button>
            </div>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6">
          {analyses.map((analysis) => (
            <Card key={analysis.analysis_id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="flex items-center space-x-3">
                      <span>Growth Analysis</span>
                      <Badge className={getScoreBadge(analysis.growth_score)}>
                        Score: {analysis.growth_score.toFixed(1)}
                      </Badge>
                    </CardTitle>
                    <div className="flex items-center space-x-2 text-sm text-gray-500 mt-2">
                      <Calendar className="w-4 h-4" />
                      <span>{new Date(analysis.timestamp).toLocaleString()}</span>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`text-3xl font-bold ${getScoreColor(analysis.growth_score)}`}>
                      {analysis.growth_score.toFixed(1)}
                    </div>
                    <div className="text-sm text-gray-500">Growth Score</div>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <p className="text-gray-700">{analysis.suggestion}</p>
                  
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                    {Object.entries(analysis.metrics).map(([key, metric]: [string, any]) => {
                      const change = metric.previousValue > 0 
                        ? ((metric.value - metric.previousValue) / metric.previousValue) * 100 
                        : 0;
                      const isPositive = change > 0;
                      
                      return (
                        <div key={key} className="text-center">
                          <div className="text-sm font-medium text-gray-600 mb-1">
                            {key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                          </div>
                          <div className="text-lg font-bold">{metric.value.toFixed(1)}</div>
                          <div className={`flex items-center justify-center text-xs ${
                            isPositive ? 'text-green-600' : 'text-red-500'
                          }`}>
                            {isPositive ? <TrendingUp className="w-3 h-3 mr-1" /> : <TrendingDown className="w-3 h-3 mr-1" />}
                            {Math.abs(change).toFixed(1)}%
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  <div className="flex justify-end">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setSelectedAnalysis(analysis)}
                    >
                      <Eye className="w-4 h-4 mr-2" />
                      View Details
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default History;
