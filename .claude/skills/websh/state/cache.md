---
role: cache-management
summary: |
  How websh caches pages and extracts content. Includes the iterative extraction
  prompt that drives the haiku subagent, cache directory structure, and
  graceful degradation when extraction is incomplete.
see-also:
  - ../shell.md: Shell semantics
  - ../commands.md: Command reference
  - crawl.md: Eager crawl agent
---

# websh Cache Management

When you `cd` to a URL, websh fetches the HTML and spawns an async haiku subagent to extract rich content into a markdown file. This document defines the cache structure and extraction process.

---

## Directory Structure

```
.websh/
├── session.md                    # Current session state
├── cache/
│   ├── index.md                  # URL → slug mapping
│   ├── {slug}.html               # Raw HTML
│   └── {slug}.parsed.md          # Extracted content (by haiku)
├── history.md                    # Command history
└── bookmarks.md                  # Saved URLs
```

---

## URL to Slug Conversion

URLs become readable filenames:

**Algorithm:**
1. Remove protocol (`https://`)
2. Replace `/` with `-`
3. Replace special chars with `-`
4. Collapse multiple `-` to single
5. Trim to reasonable length (100 chars max)
6. Lowercase

**Examples:**

| URL | Slug |
|-----|------|
| `https://news.ycombinator.com` | `news-ycombinator-com` |
| `https://x.com/deepfates/status/123` | `x-com-deepfates-status-123` |
| `https://techcrunch.com/2024/06/25/smashing/` | `techcrunch-com-2024-06-25-smashing` |
| `https://example.com/path?q=test&a=1` | `example-com-path-q-test-a-1` |

---

## index.md

Tracks all cached URLs:

```markdown
# websh cache index

## Entries

| Slug | URL | Fetched | Status |
|------|-----|---------|--------|
| news-ycombinator-com | https://news.ycombinator.com | 2026-01-24T10:30:00Z | extracted |
| x-com-deepfates-status-123 | https://x.com/deepfates/status/123 | 2026-01-24T10:35:00Z | extracting |
| techcrunch-com-article | https://techcrunch.com/... | 2026-01-24T10:40:00Z | fetched |
```

**Status values:**
- `fetched` — HTML saved, extraction not started
- `extracting` — Haiku agent running
- `extracted` — Extraction complete

---

## Extraction: The Haiku Subagent

When `cd` completes the fetch, spawn an extraction agent:

```
Task({
  description: "websh: extract page content",
  prompt: <EXTRACTION_PROMPT>,
  subagent_type: "general-purpose",
  model: "haiku",
  run_in_background: true
})
```

### Extraction Prompt

````markdown
# websh Page Extraction

You are extracting useful content from a webpage for the websh cache.

## Input

URL: {url}
HTML file: {html_path}
Output file: {output_path}

## Task

Perform an **iterative intelligent parse** of the HTML. Make multiple passes,
each time extracting more useful detail. Write your findings to the output
markdown file, updating it as you go.

## Process

```
loop until extraction is thorough (typically 2-4 passes):
  1. Read the HTML file
  2. Read your current output (if exists)
  3. Identify what's missing or could be richer
  4. Update the output file with new findings
  5. Assess: is there more useful content to extract?
```

## Pass Focus

- **Pass 1**: Basic structure
  - Page title, main heading
  - All links (text + href)
  - Basic metadata (description, og tags)

- **Pass 2**: Content extraction
  - Main article/content text
  - Comments or discussion (if present)
  - Key quotes or highlights
  - Author, date, source info

- **Pass 3**: Structure and patterns
  - Navigation elements
  - Forms and inputs
  - Repeated patterns (list items, cards, etc.)
  - Site-specific structures (tweets, posts, stories)
