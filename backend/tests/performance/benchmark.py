"""
Performance benchmarking system for the SmartRent API.

This module contains tools for measuring and tracking performance metrics
of the SmartRent API endpoints, including response times and resource usage.
"""

import time
import json
import statistics
import os
import datetime
import requests
import matplotlib.pyplot as plt
import psutil
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Tuple


@dataclass
class BenchmarkResult:
    """Class to store benchmark results for a single endpoint."""
    endpoint: str
    method: str
    response_times: List[float]
    status_codes: List[int]
    cpu_usage: List[float]
    memory_usage: List[float]
    timestamp: datetime.datetime = datetime.datetime.now()

    def get_summary(self) -> Dict[str, Any]:
        """Return a summary of benchmark results."""
        if not self.response_times:
            return {
                "endpoint": self.endpoint,
                "method": self.method,
                "error": "No data collected"
            }
        
        return {
            "endpoint": self.endpoint,
            "method": self.method,
            "timestamp": self.timestamp.isoformat(),
            "metrics": {
                "response_time": {
                    "min": min(self.response_times),
                    "max": max(self.response_times),
                    "avg": statistics.mean(self.response_times),
                    "median": statistics.median(self.response_times),
                    "p95": statistics.quantiles(self.response_times, n=20)[18] if len(self.response_times) >= 20 else None,
                    "p99": statistics.quantiles(self.response_times, n=100)[98] if len(self.response_times) >= 100 else None
                },
                "status_codes": {
                    str(code): self.status_codes.count(code) for code in set(self.status_codes)
                },
                "cpu_usage": {
                    "min": min(self.cpu_usage),
                    "max": max(self.cpu_usage),
                    "avg": statistics.mean(self.cpu_usage)
                },
                "memory_usage": {
                    "min": min(self.memory_usage),
                    "max": max(self.memory_usage),
                    "avg": statistics.mean(self.memory_usage)
                }
            }
        }


class APIBenchmark:
    """Class to benchmark API endpoints."""
    
    def __init__(self, base_url: str, auth_token: Optional[str] = None):
        """Initialize the benchmark with API base URL and optional auth token."""
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
        self.results: Dict[str, BenchmarkResult] = {}
        self.output_dir = os.path.join(os.path.dirname(__file__), "results")
        os.makedirs(self.output_dir, exist_ok=True)

    def _get_resource_usage(self) -> Tuple[float, float]:
        """Get current CPU and memory usage."""
        process = psutil.Process(os.getpid())
        cpu_percent = process.cpu_percent(interval=0.1)
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / (1024 * 1024)  # Convert to MB
        return cpu_percent, memory_mb

    def benchmark_endpoint(self, endpoint: str, method: str = "GET", 
                          data: Optional[Dict[str, Any]] = None, 
                          params: Optional[Dict[str, Any]] = None,
                          iterations: int = 100) -> BenchmarkResult:
        """
        Benchmark a specific API endpoint.
        
        Args:
            endpoint: The API endpoint to benchmark (without base URL)
            method: HTTP method to use (GET, POST, PUT, PATCH, DELETE)
            data: JSON data to send in the request body
            params: Query parameters to include in the request
            iterations: Number of requests to make

        Returns:
            BenchmarkResult object with performance metrics
        """
        url = f"{self.base_url}{endpoint}"
        response_times = []
        status_codes = []
        cpu_usage = []
        memory_usage = []
        
        print(f"Benchmarking {method} {endpoint} with {iterations} iterations...")
        
        for i in range(iterations):
            cpu_percent, memory_mb = self._get_resource_usage()
            cpu_usage.append(cpu_percent)
            memory_usage.append(memory_mb)
            
            start_time = time.time()
            
            response = requests.request(
                method=method.upper(),
                url=url,
                json=data,
                params=params,
                headers=self.headers
            )
            
            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000  # Convert to ms
            
            response_times.append(elapsed_time)
            status_codes.append(response.status_code)
            
            # Add a small delay to avoid overwhelming the server
            time.sleep(0.05)
        
        result = BenchmarkResult(
            endpoint=endpoint,
            method=method,
            response_times=response_times,
            status_codes=status_codes,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage
        )
        
        key = f"{method}_{endpoint}"
        self.results[key] = result
        return result

    def save_results(self, filename: Optional[str] = None) -> str:
        """
        Save benchmark results to a JSON file.
        
        Args:
            filename: Name of the file to save results to. If None, a timestamp-based name is used.
            
        Returns:
            Path to the saved file
        """
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        results_summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "base_url": self.base_url,
            "endpoints": {}
        }
        
        for key, result in self.results.items():
            results_summary["endpoints"][key] = result.get_summary()
        
        with open(filepath, 'w') as f:
            json.dump(results_summary, f, indent=2)
            
        print(f"Benchmark results saved to {filepath}")
        return filepath

    def generate_report(self, filepath: Optional[str] = None) -> str:
        """
        Generate visual performance report from benchmark results.
        
        Args:
            filepath: Path to the JSON results file. If None, uses the latest results.
            
        Returns:
            Path to the generated report
        """
        if not filepath:
            # Use the current results
            results_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "base_url": self.base_url,
                "endpoints": {}
            }
            
            for key, result in self.results.items():
                results_data["endpoints"][key] = result.get_summary()
        else:
            # Load results from file
            with open(filepath, 'r') as f:
                results_data = json.load(f)
        
        # Create plots
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"performance_report_{timestamp}.html"
        report_path = os.path.join(self.output_dir, report_filename)
        
        # Create a simple HTML report
        with open(report_path, 'w') as f:
            f.write(f"""
            <html>
            <head>
                <title>SmartRent API Performance Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .endpoint {{ margin-bottom: 30px; border: 1px solid #ddd; padding: 20px; border-radius: 5px; }}
                    .metric {{ margin-bottom: 15px; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <h1>SmartRent API Performance Report</h1>
                <p>Generated: {results_data.get('timestamp')}</p>
                <p>Base URL: {results_data.get('base_url')}</p>
            """)
            
            for key, endpoint_data in results_data.get("endpoints", {}).items():
                metrics = endpoint_data.get("metrics", {})
                if not metrics:
                    continue
                    
                f.write(f"""
                <div class="endpoint">
                    <h2>{endpoint_data.get('method')} {endpoint_data.get('endpoint')}</h2>
                    
                    <div class="metric">
                        <h3>Response Time (ms)</h3>
                        <table>
                            <tr>
                                <th>Min</th>
                                <th>Max</th>
                                <th>Average</th>
                                <th>Median</th>
                                <th>95th Percentile</th>
                                <th>99th Percentile</th>
                            </tr>
                            <tr>
                                <td>{metrics.get('response_time', {}).get('min', 'N/A'):.2f}</td>
                                <td>{metrics.get('response_time', {}).get('max', 'N/A'):.2f}</td>
                                <td>{metrics.get('response_time', {}).get('avg', 'N/A'):.2f}</td>
                                <td>{metrics.get('response_time', {}).get('median', 'N/A'):.2f}</td>
                                <td>{metrics.get('response_time', {}).get('p95', 'N/A') or 'N/A'}</td>
                                <td>{metrics.get('response_time', {}).get('p99', 'N/A') or 'N/A'}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <div class="metric">
                        <h3>Status Codes</h3>
                        <table>
                            <tr>
                """)
                
                status_codes = metrics.get('status_codes', {})
                for code in status_codes:
                    f.write(f"<th>{code}</th>")
                
                f.write("</tr><tr>")
                
                for code, count in status_codes.items():
                    f.write(f"<td>{count}</td>")
                
                f.write(f"""
                            </tr>
                        </table>
                    </div>
                    
                    <div class="metric">
                        <h3>Resource Usage</h3>
                        <table>
                            <tr>
                                <th>Metric</th>
                                <th>Min</th>
                                <th>Max</th>
                                <th>Average</th>
                            </tr>
                            <tr>
                                <td>CPU Usage (%)</td>
                                <td>{metrics.get('cpu_usage', {}).get('min', 'N/A'):.2f}</td>
                                <td>{metrics.get('cpu_usage', {}).get('max', 'N/A'):.2f}</td>
                                <td>{metrics.get('cpu_usage', {}).get('avg', 'N/A'):.2f}</td>
                            </tr>
                            <tr>
                                <td>Memory Usage (MB)</td>
                                <td>{metrics.get('memory_usage', {}).get('min', 'N/A'):.2f}</td>
                                <td>{metrics.get('memory_usage', {}).get('max', 'N/A'):.2f}</td>
                                <td>{metrics.get('memory_usage', {}).get('avg', 'N/A'):.2f}</td>
                            </tr>
                        </table>
                    </div>
                </div>
                """)
            
            f.write("""
            </body>
            </html>
            """)
        
        print(f"Performance report generated at {report_path}")
        return report_path


def run_standard_benchmark(base_url: str = "http://localhost:8000", 
                          auth_token: Optional[str] = None,
                          iterations: int = 50) -> None:
    """
    Run a standard benchmark suite against common API endpoints.
    
    Args:
        base_url: Base URL of the API
        auth_token: Authentication token for protected endpoints
        iterations: Number of requests to make per endpoint
    """
    benchmark = APIBenchmark(base_url, auth_token)
    
    # Benchmark basic endpoints
    benchmark.benchmark_endpoint("/api/users", method="GET", iterations=iterations)
    benchmark.benchmark_endpoint("/api/properties", method="GET", iterations=iterations)
    benchmark.benchmark_endpoint("/api/properties/search", method="GET", 
                               params={"q": "apartment"}, iterations=iterations)
    
    # Save results and generate report
    results_file = benchmark.save_results()
    report_file = benchmark.generate_report(results_file)
    
    print(f"Standard benchmark completed. Report available at {report_file}")


if __name__ == "__main__":
    # Example usage
    run_standard_benchmark() 