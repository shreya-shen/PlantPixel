
import React, { useState, useCallback } from 'react';
import { Upload, X, Camera, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface ImageUploadProps {
  onImagesSelected: (images: { before: File | null; after: File | null }) => void;
  isAnalyzing?: boolean;
}

const ImageUpload = ({ onImagesSelected, isAnalyzing = false }: ImageUploadProps) => {
  const [beforeImage, setBeforeImage] = useState<File | null>(null);
  const [afterImage, setAfterImage] = useState<File | null>(null);
  const [beforePreview, setBeforePreview] = useState<string | null>(null);
  const [afterPreview, setAfterPreview] = useState<string | null>(null);

  const handleFileSelect = useCallback((file: File, type: 'before' | 'after') => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const preview = e.target?.result as string;
      if (type === 'before') {
        setBeforeImage(file);
        setBeforePreview(preview);
      } else {
        setAfterImage(file);
        setAfterPreview(preview);
      }
    };
    reader.readAsDataURL(file);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent, type: 'before' | 'after') => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files);
    const file = files[0];
    if (file && file.type.startsWith('image/')) {
      handleFileSelect(file, type);
    }
  }, [handleFileSelect]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>, type: 'before' | 'after') => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file, type);
    }
  }, [handleFileSelect]);

  const removeImage = (type: 'before' | 'after') => {
    if (type === 'before') {
      setBeforeImage(null);
      setBeforePreview(null);
    } else {
      setAfterImage(null);
      setAfterPreview(null);
    }
  };

  React.useEffect(() => {
    onImagesSelected({ before: beforeImage, after: afterImage });
  }, [beforeImage, afterImage, onImagesSelected]);

  const UploadArea = ({ type, image, preview }: { type: 'before' | 'after'; image: File | null; preview: string | null }) => (
    <div
      className={`relative border-2 border-dashed rounded-xl p-6 transition-all duration-200 ${
        image
          ? 'border-plant-300 bg-plant-50'
          : 'border-gray-300 bg-white hover:border-plant-400 hover:bg-plant-50'
      }`}
      onDrop={(e) => handleDrop(e, type)}
      onDragOver={(e) => e.preventDefault()}
    >
      {preview ? (
        <div className="relative">
          <img
            src={preview}
            alt={`${type} plant`}
            className="w-full h-48 object-cover rounded-lg"
          />
          <div className="absolute top-2 right-2 flex space-x-2">
            <div className="bg-plant-500 text-white px-2 py-1 rounded-md text-xs font-medium flex items-center space-x-1">
              <CheckCircle className="w-3 h-3" />
              <span>Ready</span>
            </div>
            <button
              onClick={() => removeImage(type)}
              className="bg-red-500 text-white p-1 rounded-md hover:bg-red-600 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          <div className="absolute bottom-2 left-2 bg-black/70 text-white px-2 py-1 rounded text-xs">
            {image?.name}
          </div>
        </div>
      ) : (
        <div className="text-center">
          <Camera className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <div className="space-y-2">
            <p className="text-lg font-semibold text-gray-700">
              {type === 'before' ? 'Before Growth' : 'After Growth'}
            </p>
            <p className="text-sm text-gray-500">
              Drag and drop your plant image here, or click to browse
            </p>
          </div>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => handleFileInput(e, type)}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />
          <Button variant="outline" className="mt-4 pointer-events-none">
            <Upload className="w-4 h-4 mr-2" />
            Choose Image
          </Button>
        </div>
      )}
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Upload Plant Images</h2>
        <p className="text-gray-600">
          Upload two images of the same plant taken at different times to analyze growth
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <UploadArea type="before" image={beforeImage} preview={beforePreview} />
        <UploadArea type="after" image={afterImage} preview={afterPreview} />
      </div>

      {beforeImage && afterImage && (
        <div className="text-center">
          <div className="inline-flex items-center space-x-2 bg-plant-100 text-plant-700 px-4 py-2 rounded-lg">
            <CheckCircle className="w-5 h-5" />
            <span className="font-medium">Both images ready for analysis!</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
