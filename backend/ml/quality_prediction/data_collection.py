"""
Data collection module for the ML quality prediction system.
Extracts and processes data from multiple sources for model training.
"""

import os
import json
import datetime
import logging
import subprocess
import requests
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple

from config import CONFIG, DATA_DIR

# Set up logging
logging.basicConfig(
    level=getattr(logging, CONFIG["logging"]["level"]),
    format=CONFIG["logging"]["format"],
    handlers=[
        logging.FileHandler(CONFIG["logging"]["file"]),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("data_collection")


class DataCollector:
    """Base class for data collectors."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize with configuration."""
        self.config = config
        self.output_dir = Path(CONFIG["data_collection"]["output_path"])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def collect(self) -> pd.DataFrame:
        """Collect data and return as DataFrame."""
        raise NotImplementedError("Subclasses must implement collect()")
    
    def save_data(self, data: pd.DataFrame, source_name: str) -> Path:
        """Save collected data to the output directory."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{source_name}_{timestamp}.parquet"
        output_path = self.output_dir / filename
        
        data.to_parquet(output_path, index=False)
        logger.info(f"Saved {len(data)} records to {output_path}")
        
        return output_path


class GithubIssuesCollector(DataCollector):
    """Collector for GitHub issues data."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize GitHub issues collector."""
        super().__init__(config)
        self.repositories = config["params"]["repositories"]
        self.issue_types = config["params"]["issue_types"]
        self.max_issues = config["params"]["max_issues"]
        self.include_closed = config["params"]["include_closed"]
        self.api_token = os.environ.get("GITHUB_API_TOKEN", "")
        
    def collect(self) -> pd.DataFrame:
        """Collect GitHub issues data."""
        logger.info("Collecting GitHub issues data...")
        all_issues = []
        
        for repo in self.repositories:
            logger.info(f"Processing repository: {repo}")
            repo_issues = self._get_repo_issues(repo)
            all_issues.extend(repo_issues)
            
        if not all_issues:
            logger.warning("No GitHub issues collected")
            return pd.DataFrame()
        
        df = pd.DataFrame(all_issues)
        df["collection_date"] = datetime.datetime.now()
        
        logger.info(f"Collected {len(df)} GitHub issues")
        return df
    
    def _get_repo_issues(self, repo: str) -> List[Dict[str, Any]]:
        """Get issues for a specific repository."""
        issues = []
        page = 1
        per_page = 100
        state = "all" if self.include_closed else "open"
        
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"token {self.api_token}"
        
        while len(issues) < self.max_issues:
            url = f"https://api.github.com/repos/{repo}/issues"
            params = {
                "state": state,
                "per_page": per_page,
                "page": page
            }
            
            try:
                response = requests.get(url, params=params, headers=headers)
                response.raise_for_status()
                
                page_issues = response.json()
                if not page_issues:
                    break  # No more issues to retrieve
                
                # Filter issues by type if labels are set
                filtered_issues = []
                for issue in page_issues:
                    # Skip pull requests
                    if "pull_request" in issue:
                        continue
                    
                    # Check if issue has any of the specified types in labels
                    issue_labels = [label["name"].lower() for label in issue.get("labels", [])]
                    if any(issue_type in issue_labels for issue_type in self.issue_types):
                        # Extract relevant fields
                        processed_issue = {
                            "id": issue["id"],
                            "number": issue["number"],
                            "title": issue["title"],
                            "body": issue["body"],
                            "state": issue["state"],
                            "created_at": issue["created_at"],
                            "updated_at": issue["updated_at"],
                            "closed_at": issue["closed_at"],
                            "labels": [label["name"] for label in issue["labels"]],
                            "repository": repo,
                            "url": issue["html_url"]
                        }
                        filtered_issues.append(processed_issue)
                
                issues.extend(filtered_issues)
                page += 1
                
            except requests.RequestException as e:
                logger.error(f"Error fetching GitHub issues for {repo}: {e}")
                break
        
        return issues[:self.max_issues]


class SonarQubeCollector(DataCollector):
    """Collector for SonarQube metrics."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize SonarQube collector."""
        super().__init__(config)
        self.url = config["params"]["url"]
        self.token = config["params"]["token"]
        self.projects = config["params"]["projects"]
        self.metrics = config["params"]["metrics"]
        
    def collect(self) -> pd.DataFrame:
        """Collect SonarQube metrics."""
        logger.info("Collecting SonarQube metrics...")
        all_metrics = []
        
        for project in self.projects:
            logger.info(f"Processing project: {project}")
            project_metrics = self._get_project_metrics(project)
            if project_metrics:
                all_metrics.append(project_metrics)
        
        if not all_metrics:
            logger.warning("No SonarQube metrics collected")
            return pd.DataFrame()
        
        df = pd.DataFrame(all_metrics)
        df["collection_date"] = datetime.datetime.now()
        
        logger.info(f"Collected SonarQube metrics for {len(df)} projects")
        return df
    
    def _get_project_metrics(self, project: str) -> Dict[str, Any]:
        """Get metrics for a specific project."""
        auth = (self.token, "") if self.token else None
        metrics_param = ",".join(self.metrics)
        
        try:
            # Get overall project metrics
            url = f"{self.url}/api/measures/component"
            params = {
                "component": project,
                "metricKeys": metrics_param
            }
            
            response = requests.get(url, params=params, auth=auth)
            response.raise_for_status()
            data = response.json()
            
            # Process project metrics
            metrics = {"project": project}
            for measure in data["component"]["measures"]:
                metric_key = measure["metric"]
                metric_value = measure.get("value") or measure.get("period", {}).get("value")
                metrics[metric_key] = metric_value
            
            # Get files with issues
            files_with_issues = self._get_files_with_issues(project, auth)
            metrics["files_with_issues"] = files_with_issues
            
            return metrics
            
        except requests.RequestException as e:
            logger.error(f"Error fetching SonarQube metrics for {project}: {e}")
            return {}
    
    def _get_files_with_issues(self, project: str, auth: Optional[Tuple[str, str]]) -> List[Dict[str, Any]]:
        """Get files with issues for a specific project."""
        url = f"{self.url}/api/issues/search"
        params = {
            "componentKeys": project,
            "resolved": "false",
            "ps": 500  # Page size
        }
        
        try:
            response = requests.get(url, params=params, auth=auth)
            response.raise_for_status()
            data = response.json()
            
            files_with_issues = {}
            for issue in data.get("issues", []):
                component = issue.get("component")
                if component and component != project:  # Skip project-level issues
                    severity = issue.get("severity", "unknown")
                    if component not in files_with_issues:
                        files_with_issues[component] = {
                            "file": component,
                            "issue_count": 0,
                            "severities": {
                                "blocker": 0,
                                "critical": 0,
                                "major": 0,
                                "minor": 0,
                                "info": 0
                            }
                        }
                    
                    files_with_issues[component]["issue_count"] += 1
                    files_with_issues[component]["severities"][severity.lower()] += 1
            
            return list(files_with_issues.values())
            
        except requests.RequestException as e:
            logger.error(f"Error fetching files with issues for {project}: {e}")
            return []


class GitHistoryCollector(DataCollector):
    """Collector for Git repository metrics."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Git history collector."""
        super().__init__(config)
        self.repositories = config["params"]["repositories"]
        self.metrics = config["params"]["metrics"]
        self.timeframe_days = config["params"]["timeframe_days"]
        
    def collect(self) -> pd.DataFrame:
        """Collect Git history metrics."""
        logger.info("Collecting Git history metrics...")
        all_metrics = []
        
        for repo in self.repositories:
            logger.info(f"Processing repository: {repo}")
            repo_path = self._get_repo_path(repo)
            if not os.path.exists(repo_path):
                logger.warning(f"Repository path does not exist: {repo_path}")
                continue
                
            # Collect repository-level metrics
            repo_metrics = self._get_repo_metrics(repo_path)
            repo_metrics["repository"] = repo
            
            # Collect file-level metrics
            file_metrics = self._get_file_metrics(repo_path)
            for file_metric in file_metrics:
                file_metric["repository"] = repo
                all_metrics.append({**repo_metrics, **file_metric})
        
        if not all_metrics:
            logger.warning("No Git history metrics collected")
            return pd.DataFrame()
        
        df = pd.DataFrame(all_metrics)
        df["collection_date"] = datetime.datetime.now()
        
        logger.info(f"Collected Git metrics for {len(df)} files")
        return df
    
    def _get_repo_path(self, repo: str) -> str:
        """Get the local path for a repository."""
        # This assumes repositories are in the project root
        return os.path.join(os.getcwd(), repo)
    
    def _get_repo_metrics(self, repo_path: str) -> Dict[str, Any]:
        """Get repository-level metrics."""
        metrics = {}
        
        # Get commit frequency
        if "commit_frequency" in self.metrics:
            since_date = (datetime.datetime.now() - datetime.timedelta(days=self.timeframe_days)).strftime("%Y-%m-%d")
            cmd = f"git -C {repo_path} log --since={since_date} --format=%ad --date=short | sort | uniq -c"
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
                daily_commits = [line.strip().split() for line in result.stdout.strip().split("\n") if line.strip()]
                if daily_commits:
                    commit_counts = [int(count) for count, date in daily_commits]
                    metrics["commit_frequency_mean"] = np.mean(commit_counts)
                    metrics["commit_frequency_median"] = np.median(commit_counts)
                    metrics["commit_frequency_max"] = np.max(commit_counts)
                    metrics["total_commits"] = sum(commit_counts)
                else:
                    metrics["commit_frequency_mean"] = 0
                    metrics["commit_frequency_median"] = 0
                    metrics["commit_frequency_max"] = 0
                    metrics["total_commits"] = 0
            except subprocess.SubprocessError as e:
                logger.error(f"Error getting commit frequency: {e}")
        
        # Get contributor count
        if "contributor_count" in self.metrics:
            since_date = (datetime.datetime.now() - datetime.timedelta(days=self.timeframe_days)).strftime("%Y-%m-%d")
            cmd = f"git -C {repo_path} log --since={since_date} --format=%an | sort | uniq | wc -l"
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
                contributor_count = int(result.stdout.strip())
                metrics["contributor_count"] = contributor_count
            except (subprocess.SubprocessError, ValueError) as e:
                logger.error(f"Error getting contributor count: {e}")
                metrics["contributor_count"] = 0
        
        return metrics
    
    def _get_file_metrics(self, repo_path: str) -> List[Dict[str, Any]]:
        """Get file-level metrics."""
        file_metrics = []
        since_date = (datetime.datetime.now() - datetime.timedelta(days=self.timeframe_days)).strftime("%Y-%m-%d")
        
        # Get list of files in repository
        try:
            cmd = f"git -C {repo_path} ls-files | grep -E '\\.(py|js|ts|jsx|tsx|html|css|scss)$'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
            files = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        except subprocess.SubprocessError as e:
            logger.error(f"Error listing files: {e}")
            return []
        
        for file_path in files:
            file_metric = {"file_path": file_path}
            
            # Get file change frequency
            if "file_change_frequency" in self.metrics:
                cmd = f"git -C {repo_path} log --since={since_date} --format=%h -- {file_path} | wc -l"
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
                    change_count = int(result.stdout.strip())
                    file_metric["change_frequency"] = change_count
                except (subprocess.SubprocessError, ValueError) as e:
                    logger.error(f"Error getting change frequency for {file_path}: {e}")
                    file_metric["change_frequency"] = 0
            
            # Get code churn
            if "code_churn" in self.metrics:
                cmd = f"git -C {repo_path} log --since={since_date} --numstat --format='%H' -- {file_path}"
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
                    lines = result.stdout.strip().split("\n")
                    total_added = 0
                    total_deleted = 0
                    
                    for i in range(len(lines)):
                        if lines[i].strip() and i + 1 < len(lines) and not lines[i+1].startswith(" "):
                            parts = lines[i+1].strip().split("\t")
                            if len(parts) >= 2 and parts[0] != "-" and parts[1] != "-":
                                try:
                                    added = int(parts[0])
                                    deleted = int(parts[1])
                                    total_added += added
                                    total_deleted += deleted
                                except ValueError:
                                    pass
                    
                    file_metric["lines_added"] = total_added
                    file_metric["lines_deleted"] = total_deleted
                    file_metric["code_churn"] = total_added + total_deleted
                except subprocess.SubprocessError as e:
                    logger.error(f"Error getting code churn for {file_path}: {e}")
                    file_metric["lines_added"] = 0
                    file_metric["lines_deleted"] = 0
                    file_metric["code_churn"] = 0
            
            # Get file age
            if "file_age" in self.metrics:
                cmd = f"git -C {repo_path} log --format=%ad --date=short --reverse -- {file_path} | head -1"
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
                    creation_date_str = result.stdout.strip()
                    if creation_date_str:
                        creation_date = datetime.datetime.strptime(creation_date_str, "%Y-%m-%d")
                        age_days = (datetime.datetime.now() - creation_date).days
                        file_metric["file_age_days"] = age_days
                    else:
                        file_metric["file_age_days"] = 0
                except (subprocess.SubprocessError, ValueError) as e:
                    logger.error(f"Error getting file age for {file_path}: {e}")
                    file_metric["file_age_days"] = 0
            
            file_metrics.append(file_metric)
        
        return file_metrics


class TestResultsCollector(DataCollector):
    """Collector for test results data."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize test results collector."""
        super().__init__(config)
        self.include_unit_tests = config["params"]["include_unit_tests"]
        self.include_integration_tests = config["params"]["include_integration_tests"]
        self.include_e2e_tests = config["params"]["include_e2e_tests"]
        self.metrics = config["params"]["metrics"]
        
    def collect(self) -> pd.DataFrame:
        """Collect test results data."""
        logger.info("Collecting test results data...")
        all_test_results = []
        
        # Collect unit test results
        if self.include_unit_tests:
            unit_test_results = self._get_unit_test_results()
            for result in unit_test_results:
                result["test_type"] = "unit"
                all_test_results.append(result)
        
        # Collect integration test results
        if self.include_integration_tests:
            integration_test_results = self._get_integration_test_results()
            for result in integration_test_results:
                result["test_type"] = "integration"
                all_test_results.append(result)
        
        # Collect E2E test results
        if self.include_e2e_tests:
            e2e_test_results = self._get_e2e_test_results()
            for result in e2e_test_results:
                result["test_type"] = "e2e"
                all_test_results.append(result)
        
        if not all_test_results:
            logger.warning("No test results collected")
            return pd.DataFrame()
        
        df = pd.DataFrame(all_test_results)
        df["collection_date"] = datetime.datetime.now()
        
        logger.info(f"Collected {len(df)} test results")
        return df
    
    def _get_unit_test_results(self) -> List[Dict[str, Any]]:
        """Get unit test results."""
        logger.info("Collecting unit test results...")
        results = []
        
        # Look for pytest results in both backend and frontend
        for component in ["backend", "frontend"]:
            test_results_path = os.path.join(os.getcwd(), component, ".test_results")
            if not os.path.exists(test_results_path):
                logger.warning(f"No test results directory found for {component}")
                continue
            
            # Find the most recent results file
            results_files = [f for f in os.listdir(test_results_path) if f.endswith(".json")]
            if not results_files:
                logger.warning(f"No test results files found for {component}")
                continue
            
            latest_file = max(results_files, key=lambda f: os.path.getmtime(os.path.join(test_results_path, f)))
            results_path = os.path.join(test_results_path, latest_file)
            
            try:
                with open(results_path, "r") as f:
                    data = json.load(f)
                
                # Process test results based on format
                # This assumes pytest-json format but can be adapted for other formats
                for test_name, test_data in data.get("tests", {}).items():
                    test_result = {
                        "component": component,
                        "test_name": test_name,
                        "result": test_data.get("outcome", "unknown"),
                        "duration": test_data.get("duration", 0),
                        "file_path": test_data.get("file_path", ""),
                        "line_number": test_data.get("line_number", 0)
                    }
                    
                    if "failure_message" in test_data:
                        test_result["failure_message"] = test_data["failure_message"]
                    
                    results.append(test_result)
                
                # Add summary metrics
                if "summary" in data:
                    summary = data["summary"]
                    failed = summary.get("failed", 0)
                    total = summary.get("total", 0)
                    skipped = summary.get("skipped", 0)
                    duration = summary.get("duration", 0)
                    
                    if total > 0:
                        results.append({
                            "component": component,
                            "test_name": "summary",
                            "result": "summary",
                            "duration": duration,
                            "file_path": "",
                            "line_number": 0,
                            "total_tests": total,
                            "failed_tests": failed,
                            "skipped_tests": skipped,
                            "failure_rate": failed / total if total > 0 else 0
                        })
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Error parsing test results file {results_path}: {e}")
        
        return results
    
    def _get_integration_test_results(self) -> List[Dict[str, Any]]:
        """Get integration test results."""
        logger.info("Collecting integration test results...")
        # Implementation similar to unit tests but for integration tests
        return []  # Placeholder
    
    def _get_e2e_test_results(self) -> List[Dict[str, Any]]:
        """Get end-to-end test results."""
        logger.info("Collecting E2E test results...")
        # Implementation similar to unit tests but for E2E tests
        return []  # Placeholder


class DataCollectionManager:
    """Manager for orchestrating data collection from multiple sources."""
    
    def __init__(self):
        """Initialize the data collection manager."""
        self.config = CONFIG["data_collection"]
        self.collectors = {}
        self._initialize_collectors()
    
    def _initialize_collectors(self):
        """Initialize all enabled data collectors."""
        for source_config in self.config["sources"]:
            if source_config["enabled"]:
                collector_name = source_config["name"]
                logger.info(f"Initializing collector: {collector_name}")
                
                try:
                    if collector_name == "github_issues":
                        collector = GithubIssuesCollector(source_config)
                    elif collector_name == "sonarqube_reports":
                        collector = SonarQubeCollector(source_config)
                    elif collector_name == "git_history":
                        collector = GitHistoryCollector(source_config)
                    elif collector_name == "test_results":
                        collector = TestResultsCollector(source_config)
                    else:
                        logger.warning(f"Unknown collector type: {collector_name}")
                        continue
                    
                    self.collectors[collector_name] = collector
                except Exception as e:
                    logger.error(f"Error initializing collector {collector_name}: {e}")
    
    def collect_all(self) -> Dict[str, Path]:
        """Collect data from all enabled sources."""
        logger.info("Starting data collection from all sources...")
        results = {}
        
        for collector_name, collector in self.collectors.items():
            logger.info(f"Collecting data from {collector_name}...")
            try:
                data = collector.collect()
                if not data.empty:
                    output_path = collector.save_data(data, collector_name)
                    results[collector_name] = output_path
            except Exception as e:
                logger.error(f"Error collecting data from {collector_name}: {e}")
        
        logger.info("Data collection completed")
        return results


def main():
    """Main function to run data collection."""
    logger.info("Starting data collection process...")
    manager = DataCollectionManager()
    results = manager.collect_all()
    
    logger.info(f"Collected data from {len(results)} sources")
    for source, path in results.items():
        logger.info(f"  - {source}: {path}")


if __name__ == "__main__":
    main() 