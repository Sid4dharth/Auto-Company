# Deep Research Skill - Quick Start Guide

## What is This?

A comprehensive research engine for Claude Code that **matches and exceeds** Claude Desktop's "Advanced Research" feature. It conducts enterprise-grade deep research with extended reasoning, multi-source synthesis, and citation-backed reports.

## How to Use

### Simple Invocation (Recommended)

Just ask Claude Code to use deep research:

```
Use deep research to analyze the current state of AI agent frameworks in 2025
```

```
Deep research: Should we migrate from PostgreSQL to Supabase?
```

```
Use deep research in ultradeep mode to review recent advances in longevity science
```

### Direct CLI Usage

```bash
# Standard research (6 phases, ~5-10 minutes)
python3 ~/.claude/skills/deep-research/research_engine.py \
  --query "Your research question" \
  --mode standard

# Deep research (8 phases, ~10-20 minutes)
python3 ~/.claude/skills/deep-research/research_engine.py \
  --query "Your research question" \
  --mode deep

# Quick research (3 phases, ~2-5 minutes)
python3 ~/.claude/skills/deep-research/research_engine.py \
  --query "Your research question" \
  --mode quick

# Ultra-deep research (8+ phases, ~20-45 minutes)
python3 ~/.claude/skills/deep-research/research_engine.py \
  --query "Your research question" \
  --mode ultradeep
```

## Research Modes Explained

| Mode | Phases | Time | Use When |
|------|--------|------|----------|
| **Quick** | 3 | 2-5 min | Initial exploration, simple questions |
| **Standard** | 6 | 5-10 min | Most research needs (default) |
| **Deep** | 8 | 10-20 min | Complex topics, important decisions |
| **UltraDeep** | 8+ | 20-45 min | Critical analysis, comprehensive reports |

## What You Get

Every research report includes:

- **Executive Summary** - Key findings in 3-5 bullets
- **Detailed Analysis** - With full citations [1], [2], [3]
- **Synthesis & Insights** - Novel insights beyond sources
- **Limitations & Caveats** - What's uncertain or missing
- **Recommendations** - Actionable next steps
- **Full Bibliography** - All sources with credibility scores
- **Methodology Appendix** - How research was conducted

## Output Location

All research is saved to:
```
~/.claude/research_output/
```

Format: `research_report_YYYYMMDD_HHMMSS.md`

## Features That Beat Claude Desktop Research

✅ **8-Phase Pipeline** - More thorough than Claude Desktop's approach
✅ **Multiple Research Modes** - Choose depth vs speed
✅ **Source Credibility Scoring** - Evaluates each source (0-100 score)
✅ **Graph-of-Thoughts** - Non-linear exploration with branching reasoning
