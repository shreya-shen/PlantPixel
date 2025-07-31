# 🧪 PlantPixel Testing Suite

This directory contains all testing and validation scripts for the PlantPixel plant analysis system.

## 📁 Directory Structure

```
tests/
├── README.md                    # This file
├── test_images/                 # Real plant images for testing
│   ├── basil_plant.jpg         # Basil plant test image
│   ├── herb_garden.jpg         # Herb garden test image
│   ├── lettuce_mature.jpg      # Mature lettuce test image
│   ├── pepper_plant.jpg        # Pepper plant test image
│   └── tomato_seedling.jpg     # Tomato seedling test image
├── run_benchmarks.py           # Comprehensive performance benchmarking
├── test_performance.py         # Basic performance testing
└── test_real_validation.py     # Real image validation testing
```

## 🚀 Running Tests

### Prerequisites
Ensure you have the required dependencies installed:
```bash
cd ../backend
pip install -r requirements.txt
```

### Performance Benchmarking
Run comprehensive performance analysis with resume-ready statistics:
```bash
cd tests
python run_benchmarks.py
```

### Basic Performance Testing
Run basic performance validation:
```bash
cd tests
python test_performance.py
```

### Real Image Validation
Test computer vision algorithms with actual plant images:
```bash
cd tests
python test_real_validation.py
```

## 📊 Test Data

The `test_images/` directory contains 5 real plant photographs used for validation:
- **basil_plant.jpg**: Complex basil plant with multiple leaves
- **herb_garden.jpg**: Multi-plant herb garden scene
- **lettuce_mature.jpg**: Mature lettuce head
- **pepper_plant.jpg**: Pepper plant with visible fruits
- **tomato_seedling.jpg**: Young tomato seedling

## 🎯 Test Coverage

The testing suite validates:
- ✅ Processing speed and performance metrics
- ✅ Computer vision algorithm accuracy
- ✅ Real-world image processing capabilities
- ✅ System reliability and error handling
- ✅ Resume-ready performance statistics

## 📈 Output

Tests generate comprehensive reports including:
- Performance metrics and timing data
- Algorithm accuracy scores
- System reliability measurements
- Resume-ready achievement summaries
- Detailed JSON reports for analysis

Run any test script to see detailed output and performance validation results.
