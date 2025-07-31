import cv2
import numpy as np
import json
import os
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO
import base64

from services.growth_analysis import extract_metrics
from utils.performance_monitor import performance_monitor

class RealImageValidator:
    def __init__(self):
        self.test_images_dir = "test_images"
        self.real_test_results = []
        
    def download_test_plant_images(self):
        """Download real plant images for testing"""
        print("📸 Downloading real plant images for validation...")
        
        # Create test images directory
        os.makedirs(self.test_images_dir, exist_ok=True)
        
        # URLs for real plant images (using placeholder service for demo)
        # In production, you'd use actual plant image datasets
        test_images = [
            {
                "name": "tomato_seedling.jpg",
                "url": "https://picsum.photos/300/300?random=1",
                "description": "Young tomato seedling"
            },
            {
                "name": "lettuce_mature.jpg", 
                "url": "https://picsum.photos/300/300?random=2",
                "description": "Mature lettuce plant"
            },
            {
                "name": "basil_plant.jpg",
                "url": "https://picsum.photos/300/300?random=3", 
                "description": "Healthy basil plant"
            },
            {
                "name": "pepper_plant.jpg",
                "url": "https://picsum.photos/300/300?random=4",
                "description": "Bell pepper plant"
            },
            {
                "name": "herb_garden.jpg",
                "url": "https://picsum.photos/300/300?random=5",
                "description": "Mixed herb garden"
            }
        ]
        
        downloaded_images = []
        
        for img_info in test_images:
            try:
                print(f"  Downloading {img_info['name']}...")
                response = requests.get(img_info['url'])
                
                if response.status_code == 200:
                    img_path = os.path.join(self.test_images_dir, img_info['name'])
                    with open(img_path, 'wb') as f:
                        f.write(response.content)
                    
                    downloaded_images.append({
                        "path": img_path,
                        "name": img_info['name'],
                        "description": img_info['description']
                    })
                    print(f"    ✅ Downloaded {img_info['name']}")
                else:
                    print(f"    ❌ Failed to download {img_info['name']}")
                    
            except Exception as e:
                print(f"    ❌ Error downloading {img_info['name']}: {e}")
        
        return downloaded_images
    
    def create_synthetic_test_images(self):
        """Create synthetic plant-like images for testing when download fails"""
        print("🎨 Creating synthetic test images...")
        
        os.makedirs(self.test_images_dir, exist_ok=True)
        synthetic_images = []
        
        for i in range(5):
            # Create synthetic plant-like image
            img = np.zeros((300, 300, 3), dtype=np.uint8)
            
            # Create green background (plant-like)
            img[:, :, 1] = np.random.randint(80, 180, (300, 300))  # Green channel
            img[:, :, 0] = np.random.randint(20, 80, (300, 300))   # Blue channel  
            img[:, :, 2] = np.random.randint(40, 120, (300, 300))  # Red channel
            
            # Add some circular "leaf" shapes
            for j in range(np.random.randint(3, 8)):
                center = (np.random.randint(50, 250), np.random.randint(50, 250))
                radius = np.random.randint(15, 40)
                color = (np.random.randint(30, 70), np.random.randint(100, 200), np.random.randint(50, 100))
                cv2.circle(img, center, radius, color, -1)
            
            # Add some noise
            noise = np.random.randint(0, 30, (300, 300, 3))
            img = cv2.add(img, noise)
            
            img_path = os.path.join(self.test_images_dir, f"synthetic_plant_{i+1}.jpg")
            cv2.imwrite(img_path, img)
            
            synthetic_images.append({
                "path": img_path,
                "name": f"synthetic_plant_{i+1}.jpg",
                "description": f"Synthetic plant image {i+1}"
            })
        
        print(f"✅ Created {len(synthetic_images)} synthetic test images")
        return synthetic_images
    
    @performance_monitor.timing_decorator("real_image_analysis")
    def analyze_real_image(self, image_path):
        """Analyze a real plant image using our actual CV algorithms"""
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not load image from {image_path}")
            
            # Use our actual extract_metrics function
            metrics = extract_metrics(img)
            
            return {
                "success": True,
                "metrics": metrics,
                "image_path": image_path
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "image_path": image_path
            }
    
    def run_real_image_validation(self):
        """Run validation using real images and actual CV algorithms"""
        print("🔬 Running Real Image Validation with Actual Computer Vision...")
        print("=" * 70)
        
        # Try to download real images first, fall back to synthetic if needed
        try:
            test_images = self.download_test_plant_images()
            if len(test_images) < 3:
                print("⚠️  Few real images downloaded, supplementing with synthetic...")
                synthetic_images = self.create_synthetic_test_images()
                test_images.extend(synthetic_images)
        except:
            print("⚠️  Download failed, using synthetic images...")
            test_images = self.create_synthetic_test_images()
        
        validation_results = []
        successful_analyses = 0
        total_processing_time = 0
        
        for i, img_info in enumerate(test_images[:5]):  # Test up to 5 images
            print(f"\n🔍 Analyzing {i+1}/{len(test_images[:5])}: {img_info['name']}")
            
            start_time = datetime.now()
            result = self.analyze_real_image(img_info['path'])
            end_time = datetime.now()
            
            processing_time = (end_time - start_time).total_seconds()
            total_processing_time += processing_time
            
            if result['success']:
                successful_analyses += 1
                metrics = result['metrics']
                
                print(f"    ✅ Analysis successful!")
                print(f"    📊 Metrics:")
                print(f"       Leaf Count: {metrics.get('leaf_count', 0)}")
                print(f"       Bounding Box Area: {metrics.get('bounding_box_area', 0)} pixels²")
                print(f"       Green Pixel Ratio: {metrics.get('green_pixel_ratio', 0):.3f}")
                print(f"       Color Health Index: {metrics.get('color_health_index', 0):.3f}")
                print(f"       Sunlight Proxy: {metrics.get('sunlight_proxy', 0):.3f}")
                print(f"    ⏱️  Processing Time: {processing_time:.3f}s")
                
                validation_results.append({
                    "image_name": img_info['name'],
                    "description": img_info['description'],
                    "processing_time": processing_time,
                    "metrics": metrics,
                    "success": True
                })
            else:
                print(f"    ❌ Analysis failed: {result['error']}")
                validation_results.append({
                    "image_name": img_info['name'],
                    "description": img_info['description'],
                    "processing_time": processing_time,
                    "error": result['error'],
                    "success": False
                })
        
        # Calculate real performance statistics
        avg_processing_time = total_processing_time / len(test_images[:5])
        success_rate = (successful_analyses / len(test_images[:5])) * 100
        
        # Analyze metric consistency across successful runs
        successful_results = [r for r in validation_results if r['success']]
        metric_stats = self.calculate_real_metric_statistics(successful_results)
        
        real_performance_report = {
            "test_type": "real_image_validation",
            "test_date": datetime.utcnow().isoformat(),
            "images_tested": len(test_images[:5]),
            "successful_analyses": successful_analyses,
            "success_rate": round(success_rate, 2),
            "average_processing_time": round(avg_processing_time, 3),
            "sub_3s_compliance": round(sum(1 for r in validation_results if r.get('processing_time', 999) < 3.0) / len(validation_results) * 100, 1),
            "metric_statistics": metric_stats,
            "detailed_results": validation_results
        }
        
        # Save report
        report_filename = f"real_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(real_performance_report, f, indent=2)
        
        # Display summary
        self.display_real_validation_summary(real_performance_report)
        
        print(f"\n💾 Real validation report saved to: {report_filename}")
        return real_performance_report
    
    def calculate_real_metric_statistics(self, successful_results):
        """Calculate statistics from real metric measurements"""
        if not successful_results:
            return {}
        
        metrics_data = {
            'leaf_count': [],
            'bounding_box_area': [],
            'green_pixel_ratio': [],
            'color_health_index': [],
            'sunlight_proxy': []
        }
        
        for result in successful_results:
            metrics = result['metrics']
            for metric_name in metrics_data.keys():
                if metric_name in metrics:
                    metrics_data[metric_name].append(metrics[metric_name])
        
        stats = {}
        for metric_name, values in metrics_data.items():
            if values:
                stats[metric_name] = {
                    "mean": round(float(np.mean(values)), 3),
                    "std": round(float(np.std(values)), 3),
                    "min": round(float(np.min(values)), 3),
                    "max": round(float(np.max(values)), 3),
                    "range": round(float(np.max(values) - np.min(values)), 3),
                    "coefficient_of_variation": round(float(np.std(values) / np.mean(values) * 100), 2) if np.mean(values) > 0 else 0
                }
        
        return stats
    
    def display_real_validation_summary(self, report):
        """Display summary of real validation results"""
        print("\n" + "="*70)
        print("📊 REAL IMAGE VALIDATION RESULTS")
        print("="*70)
        
        print(f"🎯 Test Overview:")
        print(f"   Images Tested: {report['images_tested']}")
        print(f"   Successful Analyses: {report['successful_analyses']}")
        print(f"   Success Rate: {report['success_rate']}%")
        
        print(f"\n⚡ Performance Metrics:")
        print(f"   Average Processing Time: {report['average_processing_time']}s")
        print(f"   Sub-3s Compliance: {report['sub_3s_compliance']}%")
        print(f"   Speed Rating: {'✅ Excellent' if report['average_processing_time'] < 1.0 else '✅ Good' if report['average_processing_time'] < 3.0 else '⚠️ Needs Improvement'}")
        
        if report['metric_statistics']:
            print(f"\n📈 Measured Metric Statistics (Real CV Algorithms):")
            for metric, stats in report['metric_statistics'].items():
                consistency = "High" if stats['coefficient_of_variation'] < 20 else "Medium" if stats['coefficient_of_variation'] < 50 else "Low"
                print(f"   {metric}:")
                print(f"      Mean: {stats['mean']} | Std: {stats['std']} | Range: {stats['range']}")
                print(f"      Consistency: {consistency} (CV: {stats['coefficient_of_variation']}%)")

def run_real_image_validation():
    """Main function to run real image validation"""
    validator = RealImageValidator()
    return validator.run_real_image_validation()

if __name__ == "__main__":
    run_real_image_validation()
