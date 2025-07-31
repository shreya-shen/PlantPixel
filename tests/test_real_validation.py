import sys
import os

# Add the backend directory to Python path (moved to tests/ subdirectory)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend'))

try:
    from utils.real_image_validator import run_real_image_validation
    
    print("🌱 Running PlantPixel Real Image Validation...")
    print("=" * 60)
    print("🔬 Testing ACTUAL Computer Vision Algorithms with REAL Images")
    print("=" * 60)
    
    # Run the real image validation
    report = run_real_image_validation()
    
    print("\n✅ Real image validation complete!")
    print("\n📋 AUTHENTIC PERFORMANCE METRICS:")
    print(f"   🎯 Success Rate: {report.get('success_rate', 0)}%")
    print(f"   ⚡ Avg Processing: {report.get('average_processing_time', 0)}s")
    print(f"   🚀 Sub-3s Compliance: {report.get('sub_3s_compliance', 0)}%")
    print(f"   📊 Images Tested: {report.get('images_tested', 0)}")
    
    if report.get('metric_statistics'):
        print(f"\n🔬 Real CV Algorithm Measurements:")
        for metric, stats in report['metric_statistics'].items():
            print(f"   {metric}: {stats.get('mean', 0)} (range: {stats.get('range', 0)})")
    
    print(f"\n💾 Detailed report saved for analysis.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMake sure to install required dependencies:")
    print("pip install opencv-python numpy requests pillow")
