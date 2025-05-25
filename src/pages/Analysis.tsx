
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Loader2, Sparkles, Download, Share2, Leaf, Droplets, Activity, Sun, TrendingUp, BarChart3 } from 'lucide-react';
import ImageUpload from '@/components/ImageUpload';
import MetricsDisplay from '@/components/MetricsDisplay';
import GrowthChart from '@/components/GrowthChart';
import { useToast } from '@/hooks/use-toast';

const Analysis = () => {
  const [images, setImages] = useState<{ before: File | null; after: File | null }>({
    before: null,
    after: null,
  });
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResults, setAnalysisResults] = useState<any>(null);
  const { toast } = useToast();

  const mockAnalyze = async () => {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    return {
      growthScore: 78.5,
      metrics: [
        {
          name: 'Leaf Count',
          value: 24,
          previousValue: 18,
          unit: 'leaves',
          icon: Leaf,
          color: 'bg-plant-gradient',
          description: 'Number of visible leaves detected in the plant'
        },
        {
          name: 'Green Pixel Ratio',
          value: 0.67,
          previousValue: 0.52,
          unit: 'ratio',
          icon: Droplets,
          color: 'bg-sky-gradient',
          description: 'Proportion of green pixels indicating plant health'
        },
        {
          name: 'Plant Size',
          value: 1250,
          previousValue: 950,
          unit: 'px²',
          icon: Activity,
          color: 'bg-earth-gradient',
          description: 'Total area covered by the plant in the image'
        },
        {
          name: 'Color Health Index',
          value: 0.82,
          previousValue: 0.75,
          unit: 'index',
          icon: Sun,
          color: 'bg-gradient-to-r from-yellow-400 to-orange-500',
          description: 'Overall health score based on color analysis'
        },
        {
          name: 'Growth Rate',
          value: 15.8,
          previousValue: 12.3,
          unit: '%/week',
          icon: TrendingUp,
          color: 'bg-gradient-to-r from-green-400 to-blue-500',
          description: 'Estimated weekly growth rate percentage'
        },
        {
          name: 'Symmetry Score',
          value: 0.88,
          previousValue: 0.81,
          unit: 'score',
          icon: BarChart3,
          color: 'bg-gradient-to-r from-purple-400 to-pink-500',
          description: 'Plant symmetry and structural balance'
        }
      ],
      chartData: [
        { date: '2024-01-01', growthScore: 65, leafCount: 15, greenPixelRatio: 0.45, boundingBoxArea: 800, colorHealthIndex: 0.68 },
        { date: '2024-01-15', growthScore: 72, leafCount: 18, greenPixelRatio: 0.52, boundingBoxArea: 950, colorHealthIndex: 0.75 },
        { date: '2024-02-01', growthScore: 78.5, leafCount: 24, greenPixelRatio: 0.67, boundingBoxArea: 1250, colorHealthIndex: 0.82 },
      ]
    };
  };

  const handleAnalyze = async () => {
    if (!images.before || !images.after) {
      toast({
        title: "Missing Images",
        description: "Please upload both before and after images to proceed with analysis.",
        variant: "destructive",
      });
      return;
    }

    setIsAnalyzing(true);
    try {
      const results = await mockAnalyze();
      setAnalysisResults(results);
      toast({
        title: "Analysis Complete!",
        description: "Your plant growth analysis has been completed successfully.",
      });
    } catch (error) {
      toast({
        title: "Analysis Failed",
        description: "There was an error analyzing your images. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleDownloadReport = () => {
    toast({
      title: "Report Downloaded",
      description: "Your growth analysis report has been downloaded as PDF.",
    });
  };

  const handleShareResults = () => {
    toast({
      title: "Results Shared",
      description: "Analysis results have been copied to clipboard.",
    });
  };

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="text-center bg-white rounded-2xl p-8 shadow-lg">
        <div className="mb-6">
          <h1 className="text-4xl font-bold bg-nature-gradient bg-clip-text text-transparent mb-3">
            Plant Growth Analysis
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Upload two images of your plant taken at different times and get detailed growth insights with AI-powered analysis
          </p>
        </div>
        
        <div className="flex justify-center space-x-2 text-sm text-gray-500">
          <span className="bg-plant-100 text-plant-700 px-3 py-1 rounded-full">🌱 Leaf Analysis</span>
          <span className="bg-sky-100 text-sky-700 px-3 py-1 rounded-full">📊 Growth Metrics</span>
          <span className="bg-earth-100 text-earth-700 px-3 py-1 rounded-full">📈 Progress Tracking</span>
        </div>
      </div>

      {/* Upload Section */}
      <div className="bg-white rounded-2xl p-8 shadow-lg">
        <ImageUpload onImagesSelected={setImages} isAnalyzing={isAnalyzing} />
        
        {images.before && images.after && (
          <div className="mt-8 flex justify-center">
            <Button
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              size="lg"
              className="bg-plant-gradient hover:bg-plant-700 text-white px-8 py-3 text-lg font-semibold shadow-lg transition-all duration-200 hover:shadow-xl"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  Analyzing Growth...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5 mr-2" />
                  Analyze Growth
                </>
              )}
            </Button>
          </div>
        )}
      </div>

      {/* Analysis Progress */}
      {isAnalyzing && (
        <div className="bg-white rounded-2xl p-8 shadow-lg animate-pulse-gentle">
          <div className="text-center space-y-4">
            <div className="w-16 h-16 bg-plant-gradient rounded-full mx-auto flex items-center justify-center">
              <Loader2 className="w-8 h-8 text-white animate-spin" />
            </div>
            <h3 className="text-xl font-semibold text-gray-800">Processing Your Plant Images</h3>
            <div className="max-w-md mx-auto space-y-2 text-sm text-gray-600">
              <div className="flex justify-between">
                <span>Extracting features...</span>
                <span>✓</span>
              </div>
              <div className="flex justify-between">
                <span>Analyzing growth patterns...</span>
                <span>⏳</span>
              </div>
              <div className="flex justify-between opacity-50">
                <span>Calculating metrics...</span>
                <span>○</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Results Section */}
      {analysisResults && (
        <div className="space-y-8">
          {/* Action Buttons */}
          <div className="flex justify-center space-x-4">
            <Button onClick={handleDownloadReport} variant="outline" className="flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>Download Report</span>
            </Button>
            <Button onClick={handleShareResults} variant="outline" className="flex items-center space-x-2">
              <Share2 className="w-4 h-4" />
              <span>Share Results</span>
            </Button>
          </div>

          {/* Metrics Display */}
          <div className="bg-white rounded-2xl p-8 shadow-lg">
            <MetricsDisplay 
              metrics={analysisResults.metrics} 
              growthScore={analysisResults.growthScore}
            />
          </div>

          {/* Growth Chart */}
          <div className="bg-white rounded-2xl p-8 shadow-lg">
            <GrowthChart 
              data={analysisResults.chartData}
              currentMetrics={{
                leafCount: analysisResults.metrics[0],
                greenPixelRatio: analysisResults.metrics[1],
                boundingBoxArea: analysisResults.metrics[2],
                colorHealthIndex: analysisResults.metrics[3],
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default Analysis;
