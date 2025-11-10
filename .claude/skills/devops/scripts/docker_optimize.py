#!/usr/bin/env python3
"""
Dockerfile Optimization Analyzer

Analyzes Dockerfiles for optimization opportunities including multi-stage builds,
security issues, size reduction, and best practices.

Usage:
    python docker-optimize.py Dockerfile
    python docker-optimize.py --json Dockerfile
    python docker-optimize.py --verbose Dockerfile
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Windows UTF-8 compatibility (works for both local and global installs)
CLAUDE_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(CLAUDE_ROOT / 'scripts'))
try:
    from win_compat import ensure_utf8_stdout
    ensure_utf8_stdout()
except ImportError:
    if sys.platform == 'win32':
        import io
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class DockerfileAnalyzer:
    """Analyze Dockerfile for optimization opportunities."""

    def __init__(self, dockerfile_path: Path, verbose: bool = False):
        """
        Initialize analyzer.

        Args:
            dockerfile_path: Path to Dockerfile
            verbose: Enable verbose output
        """
        self.dockerfile_path = Path(dockerfile_path)
        self.verbose = verbose
        self.lines = []
        self.issues = []
        self.suggestions = []

    def load_dockerfile(self) -> bool:
        """
        Load and parse Dockerfile.

        Returns:
            True if loaded successfully

        Raises:
            FileNotFoundError: If Dockerfile doesn't exist
        """
        if not self.dockerfile_path.exists():
            raise FileNotFoundError(f"Dockerfile not found: {self.dockerfile_path}")

        with open(self.dockerfile_path, 'r') as f:
            self.lines = f.readlines()

        return True

    def analyze_base_image(self) -> None:
        """Check base image for optimization opportunities."""
        for i, line in enumerate(self.lines, 1):
            line = line.strip()
            if line.startswith('FROM'):
                # Check for 'latest' tag
                if ':latest' in line or (': ' not in line and 'AS' not in line and '@' not in line):
                    self.issues.append({
                        'line': i,
                        'severity': 'warning',
                        'category': 'base_image',
                        'message': 'Base image uses :latest or no tag',
                        'suggestion': 'Use specific version tags for reproducibility'
                    })

                # Check for non-alpine/slim variants
                if 'node' in line.lower() and 'alpine' not in line.lower():
                    self.suggestions.append({
                        'line': i,
                        'category': 'size',
                        'message': 'Consider using Alpine variant',
                        'suggestion': 'node:20-alpine is ~10x smaller than node:20'
                    })

    def analyze_multi_stage(self) -> None:
        """Check if multi-stage build is used."""
        from_count = sum(1 for line in self.lines if line.strip().startswith('FROM'))

        if from_count == 1:
            # Check if build tools are installed
            has_build_tools = any(
                any(tool in line.lower() for tool in ['gcc', 'make', 'build-essential', 'npm install', 'pip install'])
                for line in self.lines
            )

            if has_build_tools:
                self.issues.append({
                    'line': 0,
                    'severity': 'warning',
                    'category': 'optimization',
                    'message': 'Single-stage build with build tools',
                    'suggestion': 'Use multi-stage build to exclude build dependencies from final image'
                })

    def analyze_layer_caching(self) -> None:
        """Check for optimal layer caching order."""
        copy_lines = []
        run_lines = []

        for i, line in enumerate(self.lines, 1):
            stripped = line.strip()
            if stripped.startswith('COPY'):
                copy_lines.append((i, stripped))
            elif stripped.startswith('RUN'):
                run_lines.append((i, stripped))

        # Check if dependency files copied before source
        has_package_copy = any('package.json' in line or 'requirements.txt' in line or 'go.mod' in line
                               for _, line in copy_lines)
        has_source_copy = any('COPY . .' in line or 'COPY ./' in line
                              for _, line in copy_lines)

        if has_source_copy and not has_package_copy:
            self.issues.append({
                'line': 0,
                'severity': 'warning',
                'category': 'caching',
                'message': 'Source copied before dependencies',
                'suggestion': 'Copy dependency files first (package.json, requirements.txt) then run install, then copy source'
            })

    def analyze_security(self) -> None:
        """Check for security issues."""
        has_user = any(line.strip().startswith('USER') and 'root' not in line.lower()
                      for line in self.lines)

        if not has_user:
            self.issues.append({
                'line': 0,
                'severity': 'error',
                'category': 'security',
                'message': 'Container runs as root',
                'suggestion': 'Create and use non-root user with USER instruction'
            })

        # Check for secrets in build
        for i, line in enumerate(self.lines, 1):
            if any(secret in line.upper() for secret in ['PASSWORD', 'SECRET', 'TOKEN', 'API_KEY']):
                if 'ENV' in line or 'ARG' in line:
                    self.issues.append({
                        'line': i,
                        'severity': 'error',
                        'category': 'security',
                        'message': 'Potential secret in Dockerfile',
                        'suggestion': 'Use build-time arguments or runtime environment variables'
                    })

    def analyze_apt_cache(self) -> None:
        """Check for apt cache cleanup."""
        for i, line in enumerate(self.lines, 1):
            if 'apt-get install' in line.lower() or 'apt install' in line.lower():
                # Check if same RUN command cleans cache
                if 'rm -rf /var/lib/apt/lists/*' not in line:
                    self.suggestions.append({
                        'line': i,
                        'category': 'size',
                        'message': 'apt cache not cleaned in same layer',
                        'suggestion': 'Add && rm -rf /var/lib/apt/lists/* to reduce image size'
                    })

    def analyze_combine_run(self) -> None:
        """Check for multiple consecutive RUN commands."""
        consecutive_runs = 0
        first_run_line = 0

        for i, line in enumerate(self.lines, 1):
            if line.strip().startswith('RUN'):
                if consecutive_runs == 0:
                    first_run_line = i
                consecutive_runs += 1
            else:
                if consecutive_runs > 1:
                    self.suggestions.append({
                        'line': first_run_line,
                        'category': 'layers',
                        'message': f'{consecutive_runs} consecutive RUN commands',
                        'suggestion': 'Combine related RUN commands with && to reduce layers'
                    })
                consecutive_runs = 0

    def analyze_workdir(self) -> None:
        """Check for WORKDIR usage."""
        has_workdir = any(line.strip().startswith('WORKDIR') for line in self.lines)

        if not has_workdir:
            self.suggestions.append({
                'line': 0,
                'category': 'best_practice',
                'message': 'No WORKDIR specified',
                'suggestion': 'Use WORKDIR to set working directory instead of cd commands'
            })

    def analyze(self) -> Dict:
        """
        Run all analyses.

        Returns:
            Analysis results dictionary
        """
        self.load_dockerfile()

        self.analyze_base_image()
        self.analyze_multi_stage()
        self.analyze_layer_caching()
