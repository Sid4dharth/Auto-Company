"""
Tests for docker-optimize.py

Run with: pytest test_docker_optimize.py -v
"""

import pytest
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from docker_optimize import DockerfileAnalyzer


@pytest.fixture
def temp_dockerfile(tmp_path):
    """Create temporary Dockerfile"""
    dockerfile = tmp_path / "Dockerfile"
    return dockerfile


def write_dockerfile(filepath, content):
    """Helper to write Dockerfile content"""
    with open(filepath, 'w') as f:
        f.write(content)


class TestDockerfileAnalyzerInit:
    """Test DockerfileAnalyzer initialization"""

    def test_init(self, temp_dockerfile):
        write_dockerfile(temp_dockerfile, "FROM node:20\n")
        analyzer = DockerfileAnalyzer(temp_dockerfile)

        assert analyzer.dockerfile_path == temp_dockerfile
        assert analyzer.verbose is False
        assert analyzer.lines == []
        assert analyzer.issues == []
        assert analyzer.suggestions == []


class TestLoadDockerfile:
    """Test Dockerfile loading"""

    def test_load_success(self, temp_dockerfile):
        content = "FROM node:20\nWORKDIR /app\n"
        write_dockerfile(temp_dockerfile, content)

        analyzer = DockerfileAnalyzer(temp_dockerfile)
        result = analyzer.load_dockerfile()

        assert result is True
        assert len(analyzer.lines) == 2

    def test_load_nonexistent(self, tmp_path):
        analyzer = DockerfileAnalyzer(tmp_path / "nonexistent")

        with pytest.raises(FileNotFoundError):
            analyzer.load_dockerfile()


class TestAnalyzeBaseImage:
    """Test base image analysis"""

    def test_latest_tag(self, temp_dockerfile):
        write_dockerfile(temp_dockerfile, "FROM node:latest\n")
        analyzer = DockerfileAnalyzer(temp_dockerfile)
        analyzer.load_dockerfile()
        analyzer.analyze_base_image()

        assert len(analyzer.issues) == 1
        assert analyzer.issues[0]['category'] == 'base_image'
        assert 'latest' in analyzer.issues[0]['message']

    def test_no_tag(self, temp_dockerfile):
        write_dockerfile(temp_dockerfile, "FROM node\n")
        analyzer = DockerfileAnalyzer(temp_dockerfile)
        analyzer.load_dockerfile()
        analyzer.analyze_base_image()

        assert len(analyzer.issues) == 1
        assert 'no tag' in analyzer.issues[0]['message']

    def test_specific_tag(self, temp_dockerfile):
        write_dockerfile(temp_dockerfile, "FROM node:20-alpine\n")
        analyzer = DockerfileAnalyzer(temp_dockerfile)
        analyzer.load_dockerfile()
        analyzer.analyze_base_image()

        # Should have no issues with specific tag
        base_image_issues = [i for i in analyzer.issues if i['category'] == 'base_image']
        assert len(base_image_issues) == 0

    def test_non_alpine_suggestion(self, temp_dockerfile):
        write_dockerfile(temp_dockerfile, "FROM node:20\n")
        analyzer = DockerfileAnalyzer(temp_dockerfile)
        analyzer.load_dockerfile()
        analyzer.analyze_base_image()

        assert len(analyzer.suggestions) >= 1
        assert any('Alpine' in s['message'] for s in analyzer.suggestions)


class TestAnalyzeMultiStage:
    """Test multi-stage build analysis"""

    def test_single_stage_with_build_tools(self, temp_dockerfile):
        content = """
FROM node:20
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
CMD ["node", "server.js"]
"""
        write_dockerfile(temp_dockerfile, content)
        analyzer = DockerfileAnalyzer(temp_dockerfile)
        analyzer.load_dockerfile()
        analyzer.analyze_multi_stage()

        assert len(analyzer.issues) == 1
        assert analyzer.issues[0]['category'] == 'optimization'
        assert 'multi-stage' in analyzer.issues[0]['message'].lower()

    def test_multi_stage_no_issues(self, temp_dockerfile):
        content = """
FROM node:20 AS build
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=build /app/dist ./dist
CMD ["node", "dist/server.js"]
"""
        write_dockerfile(temp_dockerfile, content)
        analyzer = DockerfileAnalyzer(temp_dockerfile)
        analyzer.load_dockerfile()
        analyzer.analyze_multi_stage()

        multi_stage_issues = [i for i in analyzer.issues if i['category'] == 'optimization']
        assert len(multi_stage_issues) == 0


class TestAnalyzeLayerCaching:
    """Test layer caching analysis"""

    def test_source_before_dependencies(self, temp_dockerfile):
        content = """
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
"""
        write_dockerfile(temp_dockerfile, content)
        analyzer = DockerfileAnalyzer(temp_dockerfile)
        analyzer.load_dockerfile()
        analyzer.analyze_layer_caching()

        assert len(analyzer.issues) == 1
        assert analyzer.issues[0]['category'] == 'caching'

    def test_correct_order(self, temp_dockerfile):
        content = """
FROM node:20
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
"""
        write_dockerfile(temp_dockerfile, content)
        analyzer = DockerfileAnalyzer(temp_dockerfile)
        analyzer.load_dockerfile()
        analyzer.analyze_layer_caching()

        caching_issues = [i for i in analyzer.issues if i['category'] == 'caching']
        assert len(caching_issues) == 0


class TestAnalyzeSecurity:
    """Test security analysis"""

    def test_no_user_instruction(self, temp_dockerfile):
        content = """
FROM node:20
WORKDIR /app
COPY . .
CMD ["node", "server.js"]
"""
        write_dockerfile(temp_dockerfile, content)
        analyzer = DockerfileAnalyzer(temp_dockerfile)
        analyzer.load_dockerfile()
        analyzer.analyze_security()

        assert len(analyzer.issues) >= 1
        security_issues = [i for i in analyzer.issues if i['category'] == 'security']
        assert any('root' in i['message'] for i in security_issues)

    def test_with_user_instruction(self, temp_dockerfile):
        content = """
FROM node:20
WORKDIR /app
COPY . .
USER node
CMD ["node", "server.js"]
"""
        write_dockerfile(temp_dockerfile, content)
        analyzer = DockerfileAnalyzer(temp_dockerfile)
        analyzer.load_dockerfile()
        analyzer.analyze_security()

        # Should not have root user issue
        root_issues = [i for i in analyzer.issues
                      if i['category'] == 'security' and 'root' in i['message']]
        assert len(root_issues) == 0

    def test_detect_secrets(self, temp_dockerfile):
        content = """
FROM node:20
ENV API_KEY=secret123
ENV PASSWORD=mypassword
"""
        write_dockerfile(temp_dockerfile, content)
        analyzer = DockerfileAnalyzer(temp_dockerfile)
        analyzer.load_dockerfile()
        analyzer.analyze_security()

        secret_issues = [i for i in analyzer.issues
                        if i['category'] == 'security' and 'secret' in i['message'].lower()]
        assert len(secret_issues) >= 1


class TestAnalyzeAptCache:
    """Test apt cache cleanup analysis"""

    def test_apt_without_cleanup(self, temp_dockerfile):
        content = """
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y curl
"""
        write_dockerfile(temp_dockerfile, content)
        analyzer = DockerfileAnalyzer(temp_dockerfile)
        analyzer.load_dockerfile()
        analyzer.analyze_apt_cache()

        assert len(analyzer.suggestions) >= 1
        assert any('apt cache' in s['message'] for s in analyzer.suggestions)

    def test_apt_with_cleanup(self, temp_dockerfile):
        content = """
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
"""
        write_dockerfile(temp_dockerfile, content)
        analyzer = DockerfileAnalyzer(temp_dockerfile)
        analyzer.load_dockerfile()
        analyzer.analyze_apt_cache()

        apt_suggestions = [s for s in analyzer.suggestions if 'apt cache' in s['message']]
        assert len(apt_suggestions) == 0


class TestAnalyzeCombineRun:
    """Test RUN command combination analysis"""

    def test_consecutive_runs(self, temp_dockerfile):
        content = """
FROM node:20
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean
"""
        write_dockerfile(temp_dockerfile, content)
        analyzer = DockerfileAnalyzer(temp_dockerfile)
        analyzer.load_dockerfile()
        analyzer.analyze_combine_run()

        assert len(analyzer.suggestions) >= 1
        assert any('consecutive' in s['message'] for s in analyzer.suggestions)

    def test_non_consecutive_runs(self, temp_dockerfile):
        content = """
FROM node:20
RUN apt-get update
COPY package.json .
