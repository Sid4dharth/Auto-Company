# Cloudflare Platform Overview

Cloudflare Developer Platform: comprehensive edge computing ecosystem for full-stack applications on global network across 300+ cities.

## Core Concepts

### Edge Computing Model

**Global Network:**
- Code runs on servers in 300+ cities globally
- Requests execute from nearest location
- Ultra-low latency (<50ms typical)
- Automatic failover and redundancy

**V8 Isolates:**
- Lightweight execution environments (faster than containers)
- Millisecond cold starts
- Zero infrastructure management
- Automatic scaling
- Pay-per-request pricing

### Key Components

**Workers** - Serverless functions on edge
- HTTP/scheduled/queue/email handlers
- JavaScript/TypeScript/Python/Rust support
- Max 50ms CPU (free), 30s (paid)
- 128MB memory limit

**D1** - SQLite database with global read replication
- Standard SQLite syntax
- Single-writer consistency
- Global read replication
- 25GB database size limit
- Batch operations for transactions

**KV** - Distributed key-value store
- Sub-millisecond reads (edge-cached)
- Eventual consistency (~60s globally)
- 25MB value size limit
- Automatic TTL expiration
- Best for: cache, sessions, feature flags

**R2** - Object storage (S3-compatible)
- Zero egress fees (huge cost advantage)
- Unlimited storage
- 5TB object size limit
- S3-compatible API
- Multipart upload support

**Durable Objects** - Stateful compute with WebSockets
- Single-instance coordination (strong consistency)
- Persistent storage (1GB limit paid)
- WebSocket support
- Automatic hibernation

**Queues** - Message queue system
- At-least-once delivery
- Automatic retries (exponential backoff)
- Dead-letter queue support
- Batch processing

**Pages** - Static site hosting + serverless functions
- Git integration (auto-deploy)
- Directory-based routing
- Framework support (Next.js, Remix, Astro, SvelteKit)
- Built-in preview deployments

**Workers AI** - Run AI models on edge
- LLMs (Llama 3, Mistral, Gemma, Qwen)
- Image generation (Stable Diffusion, DALL-E)
- Embeddings (BGE, GTE)
- Speech recognition (Whisper)
- No GPU management required

**Browser Rendering** - Headless browser automation
- Puppeteer/Playwright support
- Screenshots, PDFs, web scraping
- Session reuse for cost optimization
- MCP server support for AI agents

## Architecture Patterns

### Full-Stack Application

```
┌─────────────────────────────────────────┐
│    Cloudflare Pages (Frontend)          │
│    Next.js / Remix / Astro               │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│    Workers (API Layer)                   │
│    - Routing                             │
│    - Authentication                      │
│    - Business logic                      │
└─┬──────┬──────┬──────┬──────┬───────────┘
  │      │      │      │      │
  ▼      ▼      ▼      ▼      ▼
┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────────────┐
│ D1 │ │ KV │ │ R2 │ │ DO │ │ Workers AI │
└────┘ └────┘ └────┘ └────┘ └────────────┘
```

### Polyglot Storage Pattern

```typescript
export default {
  async fetch(request: Request, env: Env) {
    // KV: Fast cache
    const cached = await env.KV.get(key);
    if (cached) return new Response(cached);

    // D1: Structured data
    const user = await env.DB.prepare(
      "SELECT * FROM users WHERE id = ?"
    ).bind(userId).first();

    // R2: Media files
    const avatar = await env.R2_BUCKET.get(`avatars/${user.id}.jpg`);

    // Durable Objects: Real-time
    const chat = env.CHAT_ROOM.get(env.CHAT_ROOM.idFromName(roomId));

    // Queue: Async processing
    await env.EMAIL_QUEUE.send({ to: user.email, template: 'welcome' });

    return new Response(JSON.stringify({ user }));
  }
};
```

## Wrangler CLI Essentials

### Installation
```bash
