#!/usr/bin/env python
"""
Script to run performance benchmarks for the SmartRent API.
This will test various endpoints and generate a performance report.
"""

import argparse
import os
import sys
import json
from typing import Dict, Any, Optional
from benchmark import APIBenchmark


def run_comprehensive_benchmark(base_url: str, auth_token: Optional[str] = None, 
                              iterations: int = 50) -> None:
    """
    Run a comprehensive benchmark suite against all important API endpoints.
    
    Args:
        base_url: Base URL of the API
        auth_token: Authentication token for protected endpoints
        iterations: Number of requests to make per endpoint
    """
    print(f"Starting comprehensive benchmark against {base_url}")
    benchmark = APIBenchmark(base_url, auth_token)
    
    # User endpoints
    print("\n--- User API Endpoints ---")
    benchmark.benchmark_endpoint("/api/users", method="GET", iterations=iterations)
    benchmark.benchmark_endpoint("/api/users/statistics", method="GET", iterations=iterations)
    
    # Property endpoints
    print("\n--- Property API Endpoints ---")
    benchmark.benchmark_endpoint("/api/properties", method="GET", iterations=iterations)
    benchmark.benchmark_endpoint("/api/properties/statistics", method="GET", iterations=iterations)
    benchmark.benchmark_endpoint("/api/properties/search", method="GET", 
                               params={"q": "apartment"}, iterations=iterations)
    
    # Contract endpoints
    print("\n--- Contract API Endpoints ---")
    benchmark.benchmark_endpoint("/api/contracts", method="GET", iterations=iterations)
    benchmark.benchmark_endpoint("/api/contracts/statistics", method="GET", iterations=iterations)
    
    # Proposal endpoints
    print("\n--- Proposal API Endpoints ---")
    benchmark.benchmark_endpoint("/api/proposals", method="GET", iterations=iterations)
    benchmark.benchmark_endpoint("/api/proposals/statistics", method="GET", iterations=iterations)
    
    # Document endpoints
    print("\n--- Document API Endpoints ---")
    benchmark.benchmark_endpoint("/api/documents", method="GET", iterations=iterations)
    benchmark.benchmark_endpoint("/api/documents/statistics", method="GET", iterations=iterations)
    
    # Save results and generate report
    results_file = benchmark.save_results()
    report_file = benchmark.generate_report(results_file)
    
    print(f"\nComprehensive benchmark completed!")
    print(f"Raw results saved to: {results_file}")
    print(f"HTML report available at: {report_file}")


def run_focused_benchmark(base_url: str, focus_area: str, auth_token: Optional[str] = None,
                        iterations: int = 100) -> None:
    """
    Run a focused benchmark on a specific area of the API.
    
    Args:
        base_url: Base URL of the API
        focus_area: Area to focus on (users, properties, contracts, proposals, documents)
        auth_token: Authentication token for protected endpoints
        iterations: Number of requests to make per endpoint
    """
    print(f"Starting focused benchmark on {focus_area} API against {base_url}")
    benchmark = APIBenchmark(base_url, auth_token)
    
    if focus_area == "users":
        benchmark.benchmark_endpoint("/api/users", method="GET", iterations=iterations)
        benchmark.benchmark_endpoint("/api/users/statistics", method="GET", iterations=iterations)
        
        # Test user retrieval with specific IDs
        with open('sample_ids.json', 'r') as f:
            sample_ids = json.load(f)
        
        if "user_id" in sample_ids:
            benchmark.benchmark_endpoint(f"/api/users/{sample_ids['user_id']}", 
                                      method="GET", iterations=iterations)
    
    elif focus_area == "properties":
        benchmark.benchmark_endpoint("/api/properties", method="GET", iterations=iterations)
        benchmark.benchmark_endpoint("/api/properties/statistics", method="GET", iterations=iterations)
        benchmark.benchmark_endpoint("/api/properties/search", method="GET", 
                                  params={"q": "apartment"}, iterations=iterations)
        benchmark.benchmark_endpoint("/api/properties/search", method="GET", 
                                  params={"q": "house"}, iterations=iterations)
        benchmark.benchmark_endpoint("/api/properties", method="GET", 
                                  params={"status": "available"}, iterations=iterations)
        benchmark.benchmark_endpoint("/api/properties", method="GET", 
                                  params={"min_price": 1000, "max_price": 2000}, iterations=iterations)
    
    elif focus_area == "contracts":
        benchmark.benchmark_endpoint("/api/contracts", method="GET", iterations=iterations)
        benchmark.benchmark_endpoint("/api/contracts/statistics", method="GET", iterations=iterations)
        benchmark.benchmark_endpoint("/api/contracts", method="GET", 
                                  params={"status": "active"}, iterations=iterations)
    
    elif focus_area == "proposals":
        benchmark.benchmark_endpoint("/api/proposals", method="GET", iterations=iterations)
        benchmark.benchmark_endpoint("/api/proposals/statistics", method="GET", iterations=iterations)
        benchmark.benchmark_endpoint("/api/proposals", method="GET", 
                                  params={"status": "pending"}, iterations=iterations)
    
    elif focus_area == "documents":
        benchmark.benchmark_endpoint("/api/documents", method="GET", iterations=iterations)
        benchmark.benchmark_endpoint("/api/documents/statistics", method="GET", iterations=iterations)
        benchmark.benchmark_endpoint("/api/documents", method="GET", 
                                  params={"document_type": "lease"}, iterations=iterations)
    
    else:
        print(f"Unknown focus area: {focus_area}")
        print("Available focus areas: users, properties, contracts, proposals, documents")
        return
    
    # Save results and generate report
    results_file = benchmark.save_results(f"benchmark_{focus_area}.json")
    report_file = benchmark.generate_report(results_file)
    
    print(f"\nFocused benchmark on {focus_area} completed!")
    print(f"Raw results saved to: {results_file}")
    print(f"HTML report available at: {report_file}")


def compare_environments(prod_url: str, staging_url: str, auth_token: Optional[str] = None,
                       iterations: int = 50) -> None:
    """
    Compare performance between two environments (e.g., production vs staging).
    
    Args:
        prod_url: Production API base URL
        staging_url: Staging API base URL
        auth_token: Authentication token for protected endpoints
        iterations: Number of requests to make per endpoint
    """
    print(f"Starting environment comparison benchmark")
    print(f"Production: {prod_url}")
    print(f"Staging: {staging_url}")
    
    # Run benchmarks on production
    print("\n=== PRODUCTION ENVIRONMENT ===")
    prod_benchmark = APIBenchmark(prod_url, auth_token)
    
    # Core endpoints
    prod_benchmark.benchmark_endpoint("/api/users", method="GET", iterations=iterations)
    prod_benchmark.benchmark_endpoint("/api/properties", method="GET", iterations=iterations)
    prod_benchmark.benchmark_endpoint("/api/properties/search", method="GET", 
                                   params={"q": "apartment"}, iterations=iterations)
    
    prod_results_file = prod_benchmark.save_results("benchmark_production.json")
    
    # Run benchmarks on staging
    print("\n=== STAGING ENVIRONMENT ===")
    staging_benchmark = APIBenchmark(staging_url, auth_token)
    
    # Same endpoints as production
    staging_benchmark.benchmark_endpoint("/api/users", method="GET", iterations=iterations)
    staging_benchmark.benchmark_endpoint("/api/properties", method="GET", iterations=iterations)
    staging_benchmark.benchmark_endpoint("/api/properties/search", method="GET", 
                                      params={"q": "apartment"}, iterations=iterations)
    
    staging_results_file = staging_benchmark.save_results("benchmark_staging.json")
    
    # Generate comparison report
    generate_comparison_report(prod_results_file, staging_results_file)


def generate_comparison_report(prod_file: str, staging_file: str) -> None:
    """
    Generate a comparison report between production and staging environments.
    
    Args:
        prod_file: Path to production benchmark results file
        staging_file: Path to staging benchmark results file
    """
    # Load results
    with open(prod_file, 'r') as f:
        prod_data = json.load(f)
    
    with open(staging_file, 'r') as f:
        staging_data = json.load(f)
    
    # Prepare output directory
    output_dir = os.path.dirname(prod_file)
    comparison_file = os.path.join(output_dir, "environment_comparison.html")
    
    # Create comparison HTML report
    with open(comparison_file, 'w') as f:
        f.write(f"""
        <html>
        <head>
            <title>SmartRent API Environment Comparison</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .endpoint {{ margin-bottom: 30px; border: 1px solid #ddd; padding: 20px; border-radius: 5px; }}
                .metric {{ margin-bottom: 15px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .better {{ color: green; font-weight: bold; }}
                .worse {{ color: red; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>SmartRent API Environment Comparison</h1>
            <p>Production: {prod_data.get('base_url')}</p>
            <p>Staging: {staging_data.get('base_url')}</p>
            <p>Generated: {prod_data.get('timestamp')}</p>
        """)
        
        # Process each endpoint that exists in both environments
        for key in prod_data.get("endpoints", {}):
            if key in staging_data.get("endpoints", {}):
                prod_endpoint = prod_data["endpoints"][key]
                staging_endpoint = staging_data["endpoints"][key]
                
                f.write(f"""
                <div class="endpoint">
                    <h2>{prod_endpoint.get('method')} {prod_endpoint.get('endpoint')}</h2>
                    
                    <div class="metric">
                        <h3>Response Time Comparison (ms)</h3>
                        <table>
                            <tr>
                                <th>Environment</th>
                                <th>Min</th>
                                <th>Max</th>
                                <th>Average</th>
                                <th>Median</th>
                                <th>95th Percentile</th>
                            </tr>
                """)
                
                # Production row
                prod_times = prod_endpoint.get("metrics", {}).get("response_time", {})
                f.write(f"""
                    <tr>
                        <td>Production</td>
                        <td>{prod_times.get('min', 'N/A'):.2f}</td>
                        <td>{prod_times.get('max', 'N/A'):.2f}</td>
                        <td>{prod_times.get('avg', 'N/A'):.2f}</td>
                        <td>{prod_times.get('median', 'N/A'):.2f}</td>
                        <td>{prod_times.get('p95', 'N/A') or 'N/A'}</td>
                    </tr>
                """)
                
                # Staging row
                staging_times = staging_endpoint.get("metrics", {}).get("response_time", {})
                f.write(f"""
                    <tr>
                        <td>Staging</td>
                        <td>{staging_times.get('min', 'N/A'):.2f}</td>
                        <td>{staging_times.get('max', 'N/A'):.2f}</td>
                        <td>{staging_times.get('avg', 'N/A'):.2f}</td>
                        <td>{staging_times.get('median', 'N/A'):.2f}</td>
                        <td>{staging_times.get('p95', 'N/A') or 'N/A'}</td>
                    </tr>
                """)
                
                # Difference row (staging - production)
                if prod_times and staging_times:
                    avg_diff = staging_times.get('avg', 0) - prod_times.get('avg', 0)
                    avg_diff_class = "worse" if avg_diff > 0 else "better"
                    
                    median_diff = staging_times.get('median', 0) - prod_times.get('median', 0)
                    median_diff_class = "worse" if median_diff > 0 else "better"
                    
                    f.write(f"""
                    <tr>
                        <td>Difference</td>
                        <td>-</td>
                        <td>-</td>
                        <td class="{avg_diff_class}">{avg_diff:+.2f}</td>
                        <td class="{median_diff_class}">{median_diff:+.2f}</td>
                        <td>-</td>
                    </tr>
                    """)
                
                f.write("""
                        </table>
                    </div>
                </div>
                """)
        
        f.write("""
        </body>
        </html>
        """)
    
    print(f"Environment comparison report generated at {comparison_file}")


def main():
    """Parse arguments and run the appropriate benchmark."""
    parser = argparse.ArgumentParser(description="Run performance benchmarks for SmartRent API")
    
    # Add arguments
    parser.add_argument('--url', default="http://localhost:8000",
                      help='Base URL of the API to benchmark')
    parser.add_argument('--token', help='Authentication token for protected endpoints')
    parser.add_argument('--iterations', type=int, default=50,
                      help='Number of requests to make per endpoint')
    parser.add_argument('--type', choices=['comprehensive', 'focused', 'compare'],
                      default='comprehensive', help='Type of benchmark to run')
    parser.add_argument('--focus', choices=['users', 'properties', 'contracts', 'proposals', 'documents'],
                      help='API area to focus on for focused benchmark')
    parser.add_argument('--staging-url', help='Staging URL for environment comparison')
    
    args = parser.parse_args()
    
    # Run the appropriate benchmark
    if args.type == 'comprehensive':
        run_comprehensive_benchmark(args.url, args.token, args.iterations)
    
    elif args.type == 'focused':
        if not args.focus:
            print("Error: --focus argument is required for focused benchmark")
            parser.print_help()
            sys.exit(1)
        run_focused_benchmark(args.url, args.focus, args.token, args.iterations)
    
    elif args.type == 'compare':
        if not args.staging_url:
            print("Error: --staging-url argument is required for environment comparison")
            parser.print_help()
            sys.exit(1)
        compare_environments(args.url, args.staging_url, args.token, args.iterations)


if __name__ == "__main__":
    main() 