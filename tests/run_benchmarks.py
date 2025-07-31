#!/usr/bin/env python3
"""
PlantPixel Performance Benchmarking Suite
Run this script to generate comprehensive performance metrics
"""

import sys
import os
import json
from datetime import datetime

# Add backend directory to path (moved to tests/ subdirectory)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))

def main():
    print("🌱 PlantPixel Performance Benchmarking Suite")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🖥️  Starting comprehensive performance analysis...")
    print()
    
    try:
        # Import and run performance analyzer
        from backend.utils.performance_analyzer import run_full_performance_analysis
        
        # Run comprehensive analysis
        report = run_full_performance_analysis()
        
        print("\n✅ Performance analysis completed successfully!")
        
        # Generate summary statistics for resume
        generate_resume_statistics(report)
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure you're running this from the project root directory")
        print("and all dependencies are installed (pip install -r backend/requirements.txt)")
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return False
    
    return True

def generate_resume_statistics(report):
    """Generate statistics suitable for resume inclusion"""
    print("\n" + "="*60)
    print("📋 RESUME-READY PERFORMANCE STATISTICS")
    print("="*60)
    
    if not report or "key_performance_indicators" in report:
        kpis = report.get("key_performance_indicators", {})
        
        print("\n🚀 SYSTEM PERFORMANCE METRICS:")
        print("   • Analysis Speed:", kpis.get("average_analysis_time", "N/A"))
        print("   • Speed Compliance:", kpis.get("sub_3s_compliance", "N/A"), "of analyses under 3 seconds")
        print("   • System Accuracy:", kpis.get("system_accuracy", "N/A"))
        print("   • System Reliability:", kpis.get("system_reliability", "N/A"))
        print("   • Overall Grade:", kpis.get("system_grade", "N/A"))
        
        # Calculate additional metrics for resume
        speed_ok = kpis.get("meets_speed_target", False)
        accuracy_ok = kpis.get("meets_accuracy_target", False) 
        reliability_ok = kpis.get("meets_reliability_target", False)
        
        print("\n📊 RESUME BULLET POINTS:")
        print("   • Developed AI-powered plant analysis system with", end=" ")
        if speed_ok:
            print(f"sub-3-second processing ({kpis.get('average_analysis_time', 'N/A')} average)")
        else:
            print(f"{kpis.get('average_analysis_time', 'N/A')} average processing time")
            
        if accuracy_ok:
            print(f"   • Achieved {kpis.get('system_accuracy', 'N/A')} accuracy in automated plant growth assessment")
        else:
            print(f"   • Implemented computer vision system with {kpis.get('system_accuracy', 'N/A')} baseline accuracy")
            
        if reliability_ok:
            print(f"   • Delivered {kpis.get('system_reliability', 'N/A')} system reliability through robust algorithm design")
        else:
            print(f"   • Built analysis system with {kpis.get('system_reliability', 'N/A')} consistency rating")
    
    # Generate additional context
    print("\n🎯 TECHNICAL ACHIEVEMENTS:")
    print("   • Implemented 5 distinct computer vision metrics with weighted scoring")
    print("   • Utilized watershed segmentation for leaf counting with morphological operations")
    print("   • Developed HSV color space analysis for plant health assessment")
    print("   • Created dynamic thresholding algorithms for varying lighting conditions")
    print("   • Built full-stack solution with React/TypeScript frontend and Flask/Python backend")
    
    print("\n💡 RECOMMENDED RESUME LANGUAGE:")
    print('   "Engineered an AI-driven plant growth analysis platform using advanced')
    print('    computer vision techniques including watershed segmentation, HSV color')
    print('    analysis, and dynamic thresholding, achieving measurable performance')
    print('    improvements in agricultural monitoring applications."')
    
    print("\n📁 Report files generated in project directory for detailed metrics.")

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
