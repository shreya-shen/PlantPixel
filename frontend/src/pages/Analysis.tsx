import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import { Leaf, Circle, Square, Heart, Sun } from 'lucide-react';
import { toast } from 'sonner';
import ImageUpload from '@/components/ImageUpload';
import MetricsDisplay from '@/components/MetricsDisplay';
import GrowthChart from '@/components/GrowthChart';

const Analysis = () => {
  const [images, setImages] = useState<{ before: File | null; after: File | null }>({
    before: null,
    after: null
  });
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const fileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = error => reject(error);
    });
  };

  const handleAnalyze = async () => {
    if (!images.before || !images.after) {
      toast.error('Please upload both images before analyzing');
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    try {
      // Convert images to base64
      const beforeBase64 = await fileToBase64(images.before);
      const afterBase64 = await fileToBase64(images.after);

      // Call backend API
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          beforeImage: beforeBase64,
          afterImage: afterBase64,
          species: 'unknown'
        }),
      });

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`);
      }

      const result = await response.json();
      setAnalysisResult(result);
      
      toast.success('Analysis completed successfully!');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Analysis failed';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const formatMetricsForDisplay = (metrics: any) => {
    return [
      {
        name: 'Leaf Count',
        value: metrics.leafCount.value,
        previousValue: metrics.leafCount.previousValue,
        unit: metrics.leafCount.unit,
        icon: Leaf,
        color: 'bg-plant-500',
        description: metrics.leafCount.description
      },
      {
        name: 'Green Pixel Ratio',
        value: metrics.greenPixelRatio.value,
        previousValue: metrics.greenPixelRatio.previousValue,
        unit: metrics.greenPixelRatio.unit,
        icon: Circle,
        color: 'bg-green-500',
        description: metrics.greenPixelRatio.description
      },
      {
        name: 'Plant Size',
        value: metrics.boundingBoxArea.value,
        previousValue: metrics.boundingBoxArea.previousValue,
        unit: metrics.boundingBoxArea.unit,
        icon: Square,
        color: 'bg-blue-500',
        description: metrics.boundingBoxArea.description
      },
      {
        name: 'Health Index',
        value: metrics.colorHealthIndex.value,
        previousValue: metrics.colorHealthIndex.previousValue,
        unit: metrics.colorHealthIndex.unit,
        icon: Heart,
        color: 'bg-red-500',
        description: metrics.colorHealthIndex.description
      },
      {
        name: 'Sunlight Exposure',
        value: metrics.sunlightProxy.value,
        previousValue: metrics.sunlightProxy.previousValue,
        unit: metrics.sunlightProxy.unit,
        icon: Sun,
        color: 'bg-yellow-500',
        description: metrics.sunlightProxy.description
      }
    ];
  };

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold bg-plant-gradient bg-clip-text text-transparent mb-4">
          Plant Growth Analysis
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Upload two images of your plant taken at different times to analyze growth patterns,
          health metrics, and receive personalized care recommendations.
        </p>
      </div>

      <ImageUpload onImagesSelected={setImages} isAnalyzing={isAnalyzing} />

      {images.before && images.after && !analysisResult && (
        <Card className="mx-auto max-w-2xl">
          <CardContent className="pt-6">
            <div className="text-center space-y-4">
              <CheckCircle className="w-16 h-16 text-plant-500 mx-auto" />
              <h3 className="text-xl font-semibold">Ready for Analysis</h3>
              <p className="text-gray-600">
                Both images have been uploaded successfully. Click analyze to start processing.
              </p>
              <Button
                onClick={handleAnalyze}
                disabled={isAnalyzing}
                size="lg"
                className="bg-plant-gradient hover:opacity-90"
              >
                {isAnalyzing ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Analyzing Growth...
                  </>
                ) : (
                  'Analyze Growth'
                )}
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {analysisResult && (
        <div className="space-y-8">
          <Card>
            <CardHeader>
              <CardTitle className="text-center text-2xl text-gray-800">
                Analysis Complete!
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center space-y-4">
                <div className="text-sm text-gray-600">{analysisResult.suggestion}</div>
                <div className="text-xs text-gray-500">
                  Analysis completed on {new Date(analysisResult.timestamp).toLocaleString()}
                </div>
              </div>
            </CardContent>
          </Card>

          <MetricsDisplay
            metrics={formatMetricsForDisplay(analysisResult.metrics)}
            growthScore={analysisResult.growth_score}
          />

          <GrowthChart
            data={analysisResult.chart_data}
            currentMetrics={analysisResult.metrics}
          />
        </div>
      )}
    </div>
  );
};

export default Analysis;
