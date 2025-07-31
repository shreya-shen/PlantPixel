import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import os
from utils.performance_monitor import performance_monitor
from utils.validation_system import run_comprehensive_validation

class PerformanceAnalyzer:
    def __init__(self):
        self.results = {}
        
    def run_speed_benchmark(self, num_iterations=50):
        """Run speed benchmark for image analysis pipeline"""
        print(f"🏃‍♂️ Running Speed Benchmark ({num_iterations} iterations)...")
        
        # Import here to avoid circular imports
        from services.growth_analysis import extract_metrics
        
        # Generate test images of different sizes
        test_images = {
            "small": np.random.randint(0, 255, (150, 150, 3), dtype=np.uint8),
            "medium": np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8),
            "large": np.random.randint(0, 255, (600, 600, 3), dtype=np.uint8)
        }
        
        results = {}
        
        for size_name, test_image in test_images.items():
            print(f"  Testing {size_name} images ({test_image.shape[0]}x{test_image.shape[1]})...")
            times = []
            
            for i in range(num_iterations):
                start_time = time.time()
                try:
                    _ = extract_metrics(test_image)
                    execution_time = time.time() - start_time
                    times.append(execution_time)
                except Exception as e:
                    print(f"    Error in iteration {i}: {e}")
                    continue
            
            if times:
                results[size_name] = {
                    "mean_time": round(float(np.mean(times)), 3),
                    "std_time": round(float(np.std(times)), 3),
                    "min_time": round(float(np.min(times)), 3),
                    "max_time": round(float(np.max(times)), 3),
                    "successful_runs": len(times),
                    "image_size": f"{test_image.shape[0]}x{test_image.shape[1]}",
                    "sub_3s_rate": round(float(sum(1 for t in times if t < 3.0) / len(times) * 100), 1)
                }
        
        return results
    
    def run_accuracy_benchmark(self):
        """Run accuracy benchmark using real image validation"""
        print("🎯 Running Real Image Accuracy Benchmark...")
        
        # Import the real image validator
        from utils.real_image_validator import run_real_image_validation
        
        return run_real_image_validation()
    
    def run_reliability_test(self, num_runs=20):
        """Test system reliability and consistency"""
        print(f"🔄 Running Reliability Test ({num_runs} runs)...")
        
        from services.growth_analysis import extract_metrics, compare_and_score_growth
        
        # Create two test images
        before_image = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
        after_image = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
        
        growth_scores = []
        metric_consistency = {
            "bounding_box_area": [],
            "green_pixel_ratio": [],
            "leaf_count": [],
            "color_health_index": [],
            "sunlight_proxy": []
        }
        
        for i in range(num_runs):
            try:
                before_metrics = extract_metrics(before_image)
                after_metrics = extract_metrics(after_image)
                score, _ = compare_and_score_growth(before_metrics, after_metrics)
                growth_scores.append(score)
                
                # Track metric consistency
                for metric_name in metric_consistency.keys():
                    if metric_name in after_metrics:
                        metric_consistency[metric_name].append(after_metrics[metric_name])
                        
            except Exception as e:
                print(f"    Error in run {i}: {e}")
                continue
        
        # Calculate reliability metrics
        reliability_stats = {
            "growth_score_consistency": {
                "mean": round(float(np.mean(growth_scores)), 2),
                "std": round(float(np.std(growth_scores)), 2),
                "coefficient_of_variation": round(float(np.std(growth_scores) / np.mean(growth_scores) * 100), 2) if np.mean(growth_scores) > 0 else 0,
                "reliability_percentage": round(float(100 - (np.std(growth_scores) / np.mean(growth_scores) * 100)), 2) if np.mean(growth_scores) > 0 else 0
            },
            "metric_consistency": {}
        }
        
        for metric_name, values in metric_consistency.items():
            if values:
                mean_val = float(np.mean(values))
                std_val = float(np.std(values))
                cv = std_val / mean_val * 100 if mean_val > 0 else 0
                reliability_stats["metric_consistency"][metric_name] = {
                    "coefficient_of_variation": round(float(cv), 2),
                    "reliability_percentage": round(float(100 - cv), 2)
                }
        
        return reliability_stats
    
    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        print("📊 Generating Comprehensive Performance Report...")
        print("=" * 70)
        
        report = {
            "report_date": datetime.utcnow().isoformat(),
            "system_info": {
                "test_environment": "Development",
                "python_version": "3.x",
                "opencv_version": "4.x"
            }
        }
        
        # Run all benchmarks
        try:
            speed_results = self.run_speed_benchmark()
            report["speed_benchmark"] = speed_results
            
            accuracy_results = self.run_accuracy_benchmark()
            report["accuracy_benchmark"] = accuracy_results
            
            reliability_results = self.run_reliability_test()
            report["reliability_test"] = reliability_results
            
            # Calculate key performance indicators
            kpis = self.calculate_kpis(speed_results, accuracy_results, reliability_results)
            report["key_performance_indicators"] = kpis
            
        except Exception as e:
            print(f"❌ Error during benchmarking: {e}")
            report["error"] = str(e)
        
        # Save report
        report_filename = f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Display summary
        self.display_performance_summary(report)
        
        print(f"\n💾 Full report saved to: {report_filename}")
        return report
    
    def calculate_kpis(self, speed_results, accuracy_results, reliability_results):
        """Calculate key performance indicators"""
        kpis = {}
        
        # Speed KPIs
        if speed_results and "medium" in speed_results:
            medium_time = float(speed_results["medium"]["mean_time"])
            kpis["average_analysis_time"] = f"{medium_time}s"
            kpis["sub_3s_compliance"] = f"{speed_results['medium']['sub_3s_rate']}%"
            kpis["meets_speed_target"] = bool(medium_time < 3.0)
        
        # Accuracy KPIs (updated for real image validation)
        if accuracy_results:
            if "success_rate" in accuracy_results:
                # Real image validation format
                success_rate = float(accuracy_results["success_rate"])
                kpis["system_accuracy"] = f"{success_rate}%"
                kpis["meets_accuracy_target"] = bool(success_rate >= 85.0)
                kpis["real_image_testing"] = True
            elif "overall_performance" in accuracy_results:
                # Legacy synthetic validation format
                overall_accuracy = float(accuracy_results["overall_performance"]["system_accuracy"]["mean"])
                kpis["system_accuracy"] = f"{overall_accuracy}%"
                kpis["meets_accuracy_target"] = bool(overall_accuracy >= 85.0)
                kpis["real_image_testing"] = False
        
        # Reliability KPIs
        if reliability_results and "growth_score_consistency" in reliability_results:
            reliability = float(reliability_results["growth_score_consistency"]["reliability_percentage"])
            kpis["system_reliability"] = f"{reliability}%"
            kpis["meets_reliability_target"] = bool(reliability >= 90.0)
        
        # Overall system rating
        targets_met = sum([
            kpis.get("meets_speed_target", False),
            kpis.get("meets_accuracy_target", False), 
            kpis.get("meets_reliability_target", False)
        ])
        
        kpis["overall_system_rating"] = f"{targets_met}/3 targets met"
        kpis["system_grade"] = ["Needs Improvement", "Good", "Very Good", "Excellent"][targets_met]
        
        return kpis
    
    def display_performance_summary(self, report):
        """Display performance summary in a readable format"""
        print("\n🎯 PERFORMANCE SUMMARY")
        print("=" * 50)
        
        if "key_performance_indicators" in report:
            kpis = report["key_performance_indicators"]
            
            print(f"⚡ Speed Performance:")
            print(f"   Average Analysis Time: {kpis.get('average_analysis_time', 'N/A')}")
            print(f"   Sub-3s Compliance: {kpis.get('sub_3s_compliance', 'N/A')}")
            print(f"   Speed Target Met: {'✅' if kpis.get('meets_speed_target') else '❌'}")
            
            print(f"\n🎯 Accuracy Performance:")
            print(f"   System Accuracy: {kpis.get('system_accuracy', 'N/A')}")
            print(f"   Accuracy Target Met: {'✅' if kpis.get('meets_accuracy_target') else '❌'}")
            
            print(f"\n🔄 Reliability Performance:")
            print(f"   System Reliability: {kpis.get('system_reliability', 'N/A')}")
            print(f"   Reliability Target Met: {'✅' if kpis.get('meets_reliability_target') else '❌'}")
            
            print(f"\n🏆 Overall Rating: {kpis.get('system_grade', 'Unknown')} ({kpis.get('overall_system_rating', 'N/A')})")
        
        if "speed_benchmark" in report:
            print(f"\n📊 Detailed Speed Results:")
            for size, results in report["speed_benchmark"].items():
                print(f"   {size.capitalize()} images: {results['mean_time']}s (±{results['std_time']}s)")
        
        if "accuracy_benchmark" in report:
            print(f"\n📈 Detailed Accuracy Results:")
            acc_data = report["accuracy_benchmark"]
            
            if "success_rate" in acc_data:
                # Real image validation format
                print(f"   Real Image Success Rate: {acc_data['success_rate']}%")
                print(f"   Images Tested: {acc_data.get('images_tested', 0)}")
                print(f"   Average Processing: {acc_data.get('average_processing_time', 0)}s")
                
                if "metric_statistics" in acc_data and acc_data["metric_statistics"]:
                    print(f"   Real CV Metrics Measured:")
                    for metric, stats in acc_data["metric_statistics"].items():
                        consistency = "High" if stats.get('coefficient_of_variation', 100) < 20 else "Medium"
                        print(f"     {metric}: {stats.get('mean', 0)} (consistency: {consistency})")
            
            elif "overall_performance" in acc_data:
                # Legacy synthetic validation format  
                perf_data = acc_data["overall_performance"]
                print(f"   Overall: {perf_data['system_accuracy']['mean']}% (±{perf_data['system_accuracy']['std']}%)")
                
                if "metric_specific_accuracy" in perf_data:
                    for metric, stats in perf_data["metric_specific_accuracy"].items():
                        print(f"   {metric}: {stats['mean']}%")

def run_full_performance_analysis():
    """Main function to run complete performance analysis"""
    analyzer = PerformanceAnalyzer()
    return analyzer.generate_performance_report()

if __name__ == "__main__":
    run_full_performance_analysis()
