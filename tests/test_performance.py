import sys
import os

# Add the backend directory to Python path (moved to tests/ subdirectory)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend'))

try:
    from utils.performance_analyzer import run_full_performance_analysis
    
    print("Running PlantPixel Performance Analysis...")
    print("=" * 50)
    
    # Run the analysis
    report = run_full_performance_analysis()
    
    print("\nAnalysis complete!")
    
except Exception as e:
    print(f"Error: {e}")
    print("\ninstall required dependencies:")
    print("pip install opencv-python numpy matplotlib seaborn psutil")
