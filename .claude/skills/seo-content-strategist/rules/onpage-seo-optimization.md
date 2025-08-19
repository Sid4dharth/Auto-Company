---
title: On-Page SEO Optimization
impact: CRITICAL
tags: on-page, meta-tags, titles, headers, content-optimization, keywords
---

## On-Page SEO Optimization

**Impact: CRITICAL**

On-page SEO is where content meets technical optimization. Perfect on-page can't save bad content, but bad on-page can sink great content. Every element should serve both users and search engines.

### On-Page Elements Hierarchy

| Element | Impact | User-Facing | Search-Facing |
|---------|--------|-------------|---------------|
| **Title Tag** | Very High | Browser tab, SERP | Primary ranking signal |
| **H1** | High | Page headline | Content topic signal |
| **Meta Description** | Medium | SERP snippet | Click-through rate |
| **URL** | Medium | Address bar | Topic signal |
| **H2-H6** | Medium | Content structure | Subtopic signals |
| **Body Content** | High | Main content | Topical relevance |
| **Images** | Medium | Visual content | Alt text, file names |
| **Internal Links** | High | Navigation | PageRank flow |
| **Schema** | Medium | Rich snippets | Structured data |

### Title Tag Best Practices

| Rule | Guideline |
|------|-----------|
| **Length** | 50-60 characters (avoid truncation) |
| **Keyword placement** | Primary keyword near the front |
| **Uniqueness** | Every page needs unique title |
| **Brand** | Include brand name (usually at end) |
| **Readability** | Must make sense to humans |

### Good Title Tags

```
✓ "Kubernetes Secrets Management: Complete Guide (2024) | Infisical"
  └── Keyword first, year for freshness, brand at end
  └── 62 chars (slight truncation OK)

✓ "HashiCorp Vault vs AWS Secrets Manager: Full Comparison"
  └── Comparison keyword pattern, clear intent

✓ "How to Rotate API Keys Automatically | Step-by-Step Guide"
  └── How-to format, action-oriented
```

### Bad Title Tags

```
✗ "Home"
  └── No keyword, no value, no differentiation

✗ "Secrets Management | Secret Management | Manage Secrets | Infisical"
  └── Keyword stuffing, unreadable

✗ "The Ultimate Comprehensive Complete Guide to Everything You Need to Know About Secrets Management in 2024"
  └── Way too long, will truncate badly

✗ "Infisical - Secrets Management"
  └── Brand first (wastes prime keyword space)
```

### Meta Description Guidelines

| Rule | Guideline |
|------|-----------|
| **Length** | 150-160 characters |
| **Purpose** | Sell the click, not the product |
| **Keywords** | Include naturally (bolded in SERP) |
| **CTA** | Soft call-to-action when appropriate |
| **Unique** | Every page needs unique description |

### Good Meta Descriptions

```
✓ "Learn how to manage secrets in Kubernetes with encryption,
   rotation, and access controls. Step-by-step guide with
   code examples for production environments."

   └── Keywords included naturally
   └── Clear value proposition
   └── Specific (mentions what they'll learn)

✓ "Compare HashiCorp Vault and AWS Secrets Manager side-by-side.
   Features, pricing, security models, and which to choose for
   your infrastructure."

   └── Addresses search intent directly
   └── Lists what comparison covers
```

### Bad Meta Descriptions

```
✗ "Welcome to our website. We provide secrets management
   solutions for businesses of all sizes."

   └── Generic, no value, doesn't match search intent

✗ "secrets management kubernetes docker secrets vault aws
   secrets manager api keys environment variables .env"

   └── Keyword stuffing, unreadable

✗ [No meta description]
   └── Google will pull random text, likely poor
```

### URL Structure

| Element | Best Practice |
|---------|---------------|
| **Length** | Keep short (3-5 words after domain) |
| **Keywords** | Include primary keyword |
| **Separators** | Use hyphens, not underscores |
| **Case** | Lowercase only |
| **Parameters** | Avoid when possible |

### Good URLs

```
✓ /guides/kubernetes-secrets-management
✓ /blog/vault-vs-aws-secrets-manager
✓ /docs/api-key-rotation
✓ /integrations/github-actions
```

### Bad URLs

```
✗ /page?id=12345&category=secrets
✗ /blog/2024/01/15/the-complete-ultimate-guide-to-secrets-management-for-developers
✗ /Blog/Kubernetes_Secrets
✗ /content/article/secrets/management/guide/overview/index.html
```

### Header Structure (H1-H6)

```
