import time
import json
import os
from datetime import datetime
from functools import wraps
import numpy as np
import psutil
import cv2

class PerformanceMonitor:
    def __init__(self, log_file="performance_logs.json"):
        self.log_file = log_file
        self.metrics = []
        
    def timing_decorator(self, operation_name):
        """Decorator to measure execution time of functions"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                
                try:
                    result = func(*args, **kwargs)
                    success = True
                    error = None
                except Exception as e:
                    result = None
                    success = False
                    error = str(e)
                
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                
                execution_time = end_time - start_time
                memory_usage = end_memory - start_memory
                
                metric = {
                    "operation": operation_name,
                    "function": func.__name__,
                    "execution_time": round(execution_time, 3),
                    "memory_usage_mb": round(memory_usage, 2),
                    "timestamp": datetime.utcnow().isoformat(),
                    "success": success,
                    "error": error
                }
                
                self.log_metric(metric)
                print(f"⏱️  {operation_name}: {execution_time:.3f}s | Memory: {memory_usage:.2f}MB")
                
                return result
            return wrapper
        return decorator
    
    def log_metric(self, metric):
        """Log performance metric to file"""
        self.metrics.append(metric)
        
        # Append to file
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []
        
        data.append(metric)
        
        with open(self.log_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_performance_stats(self, operation_name=None):
        """Get performance statistics for specific operation or all"""
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []
        
        if operation_name:
            data = [m for m in data if m.get('operation') == operation_name]
        
        if not data:
            return {"error": "No performance data found"}
        
        execution_times = [m['execution_time'] for m in data if m['success']]
        memory_usage = [m['memory_usage_mb'] for m in data if m['success']]
        success_rate = sum(1 for m in data if m['success']) / len(data) * 100
        
        stats = {
            "operation": operation_name or "all_operations",
            "total_runs": len(data),
            "success_rate": round(success_rate, 2),
            "execution_time": {
                "avg": round(np.mean(execution_times), 3) if execution_times else 0,
                "min": round(np.min(execution_times), 3) if execution_times else 0,
                "max": round(np.max(execution_times), 3) if execution_times else 0,
                "std": round(np.std(execution_times), 3) if execution_times else 0
            },
            "memory_usage": {
                "avg": round(np.mean(memory_usage), 2) if memory_usage else 0,
                "min": round(np.min(memory_usage), 2) if memory_usage else 0,
                "max": round(np.max(memory_usage), 2) if memory_usage else 0
            },
            "last_updated": datetime.utcnow().isoformat()
        }
        
        return stats

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

def measure_image_analysis_accuracy(ground_truth_data, analysis_results):
    """
    Measure accuracy of image analysis against ground truth data
    
    Args:
        ground_truth_data: Dict with expert measurements
        analysis_results: Dict with system measurements
    
    Returns:
        Dict with accuracy metrics
    """
    metrics = {}
    
    for metric_name in ground_truth_data.keys():
        if metric_name in analysis_results:
            gt_value = ground_truth_data[metric_name]
            pred_value = analysis_results[metric_name]
            
            # Calculate percentage error
            if gt_value != 0:
                error = abs(pred_value - gt_value) / gt_value * 100
                accuracy = max(0, 100 - error)
            else:
                accuracy = 100 if pred_value == 0 else 0
            
            metrics[metric_name] = {
                "ground_truth": float(gt_value),
                "predicted": float(pred_value),
                "accuracy": round(float(accuracy), 2),
                "absolute_error": float(abs(pred_value - gt_value))
            }
    
    overall_accuracy = float(np.mean([m["accuracy"] for m in metrics.values()]))
    
    return {
        "individual_metrics": metrics,
        "overall_accuracy": round(overall_accuracy, 2),
        "timestamp": datetime.utcnow().isoformat()
    }

def benchmark_system_performance():
    """Run comprehensive system performance benchmark"""
    print("🚀 Starting PlantPixel Performance Benchmark...")
    
    # Test image processing pipeline
    test_image = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
    
    benchmark_results = {
        "test_date": datetime.utcnow().isoformat(),
        "system_info": {
            "cpu_count": psutil.cpu_count(),
            "memory_total_gb": round(psutil.virtual_memory().total / 1024**3, 2),
            "python_version": psutil.__version__
        }
    }
    
    return benchmark_results
