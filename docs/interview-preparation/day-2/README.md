# Day 2 — Backend Engineering & Databases
## Associate Backend Engineer | Intensive Interview Preparation

**Duration:** 8 hours · **Difficulty:** Adaptive (basic → intermediate → advanced) · **Format:** Definitions, examples, backend use cases, interview scenarios and practice.

> Study one topic at a time. For every concept: explain the definition aloud, give a practical example, describe a production trade-off, and answer its interview question without notes.

## Learning dashboard

| Module | Topics | Time | Priority |
|---|---|---:|---|
| 1. Programming Fundamentals | Python, Node.js, TypeScript, async/await, event loop | 75 min | Critical |
| 2. Frameworks & APIs | FastAPI, Flask, Fastify, REST, OpenAPI, Pydantic | 65 min | Critical |
| 3. SQL & PostgreSQL | Joins, indexes, transactions, ACID, isolation | 85 min | Critical |
| 4. Redis & Caching | TTL, eviction, cache-aside, rate limiting | 45 min | High |
| 5. Authentication & Security | JWT, OAuth 2.0, RBAC, multi-tenancy | 65 min | Critical |
| 6. System Architecture | Monolith, microservices, events, WebSockets | 60 min | High |
| 7. Queues & Integrations | BullMQ, retries, DLQs, webhooks, n8n | 50 min | High |
| 8. System Design & Mock Interview | Scaling, observability, reliability | 35 min | Critical |

**Total:** 480 minutes (8 hours), excluding breaks. If pressed for time, prioritize modules 1, 2, 3, 5 and 8.

---

## Module 1 — Programming Fundamentals (75 min)

### Definitions and examples

**Python:** A general-purpose, dynamically typed language frequently used for backend APIs and AI services. **Example:** Build a FastAPI model-inference endpoint. **Backend use:** Data processing and services.

**Node.js:** A JavaScript runtime commonly used for network-oriented backend services. **Example:** A Fastify API calling PostgreSQL. **Backend use:** High-concurrency I/O.

**TypeScript:** JavaScript with static type checking before runtime. **Example:** Type a user response as `UserDTO`. **Backend use:** Maintain API contracts. **Caution:** TypeScript does not validate incoming JSON at runtime.

**Event loop:** Runtime mechanism that schedules callbacks and asynchronous continuations. **Example:** A Node.js server can handle another request while waiting for database I/O. **Backend use:** Efficient I/O concurrency.

**Promise:** JavaScript object representing eventual completion or rejection of an asynchronous operation. **Example:** `fetch(url)`. **Backend use:** HTTP and database calls.

**Async/await:** Syntax to suspend an async function until a promise or coroutine completes. **Example:** `await db.query(...)`. **Backend use:** Readable asynchronous workflows.

**Coroutine:** A suspendable Python function defined with `async def`. **Example:** `async def get_user(): return await repository.get()`. **Backend use:** Concurrent I/O with asyncio.

**Concurrency:** Multiple tasks making progress during overlapping periods. **Example:** Three HTTP requests in flight. **Backend use:** Reduce end-to-end latency.

**Parallelism:** Multiple operations executing simultaneously. **Example:** CPU work across worker processes. **Backend use:** Image processing and computation.

**CPU-bound:** Work limited mainly by computation speed. **Example:** Large image transformation. **Backend use:** Use workers or separate compute services.

**I/O-bound:** Work limited mainly by waiting for external operations. **Example:** PostgreSQL query. **Backend use:** Async I/O and connection pools.

**Generator:** Function producing items incrementally with `yield`. **Example:** Stream rows from a large dataset. **Backend use:** Memory-efficient processing.

**Decorator:** Python construct wrapping or registering callable behavior. **Example:** `@app.get("/users")`. **Backend use:** Routing and cross-cutting behavior.

### Code: concurrent independent I/O

```typescript
const [user, orders, settings] = await Promise.all([
  userService.get(userId),
  orderService.list(userId),
  settingsService.get(userId),
]);
```

Three independent calls can overlap. `Promise.all` rejects when one promise rejects, but does **not** automatically cancel the others. Bound concurrency and add timeouts for production dependencies.

```python
import asyncio

async def dashboard():
    user, orders = await asyncio.gather(get_user(), get_orders())
    return {"user": user, "orders": orders}
```

**Interview check:** Does `async` make CPU-heavy work faster? **Answer:** No. It improves overlapping waits; CPU-heavy work may require threads, processes, or dedicated workers.

**Practice:** Explain event loop vs threads; sequential await vs Promise.all; TypeScript types vs runtime validation; when Python asyncio is useful.

---

## Module 2 — Backend Frameworks & APIs (65 min)

**FastAPI:** Python ASGI framework with type-driven request parsing, validation and OpenAPI generation. **Example:** `POST /predict`. **Backend use:** Async APIs and AI services.

**Flask:** Lightweight Python web framework. **Example:** Internal admin endpoint. **Backend use:** Small APIs with chosen extensions.

**Fastify:** Node.js framework emphasizing efficient request handling, schema validation and plugins. **Example:** TypeScript SaaS REST API. **Backend use:** Validated API routes.

**REST:** Architectural style modeling resources using stateless HTTP interactions. **Example:** `GET /users/42`. **Backend use:** Predictable CRUD interfaces.

**OpenAPI:** Machine-readable HTTP API contract. **Example:** Describe `POST /tickets` request and response schemas. **Backend use:** Documentation, testing and client generation.

**Pydantic:** Python library for validating and parsing structured data. **Example:** Require a nonempty ticket title. **Backend use:** Runtime input validation.

**Middleware:** Code executed around request handling. **Example:** Add request IDs or enforce logging. **Backend use:** Consistent cross-cutting behavior.

**Dependency injection:** Supplying a component's dependencies rather than constructing them internally. **Example:** Inject a repository into a service. **Backend use:** Testing and modular design.

**Idempotency:** Repeating an operation has the same intended effect as doing it once. **Example:** Retry a payment request using the same idempotency key. **Backend use:** Safe network retries.

**Pagination:** Splitting large result sets into bounded pages. **Example:** Cursor-based listing of orders. **Backend use:** Avoid unbounded database queries.

### FastAPI endpoint

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class TicketInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)

@app.post("/tickets", status_code=201)
async def create_ticket(payload: TicketInput):
    return {"id": "t_123", "title": payload.title}
```

### HTTP interview essentials

- **200:** Success. **201:** Resource created. **202:** Accepted for asynchronous processing.
- **400:** Invalid request. **401:** Not authenticated. **403:** Not authorized. **404:** Not found.
- **409:** Conflict. **422:** Semantically invalid request content. **429:** Rate limit. **500/503:** Server/dependency failure.

**Interview scenario:** Design `POST /payments` for retry safety. Discuss unique idempotency keys, transaction boundaries, gateway reconciliation and returning the original result for duplicate requests.

---

## Module 3 — SQL & PostgreSQL (85 min)

**Relational database:** Tables connected through defined relationships. **Example:** Users and orders. **Backend use:** Structured transactional data.

**Primary key:** Column(s) uniquely identifying a row. **Example:** `users.id`. **Backend use:** Stable identity.

**Foreign key:** Constraint ensuring a reference points to a valid related row. **Example:** `orders.user_id`. **Backend use:** Referential integrity.

**JOIN:** Combining rows based on matching conditions. **Example:** Orders with customer emails. **Backend use:** Relational reporting.

**INNER JOIN:** Returns matching rows on both sides. **Example:** Orders with existing users. **Backend use:** Matching relationships.

**LEFT JOIN:** Retains all rows from the left side, with nulls for unmatched right rows. **Example:** Users with zero orders. **Backend use:** Inclusive reports.

**Index:** Data structure improving some queries at the expense of storage and write overhead. **Example:** B-tree on `orders(user_id, created_at)`. **Backend use:** Efficient filtering/sorting.

**Transaction:** Operations committed or rolled back as a unit. **Example:** Bank transfer. **Backend use:** Multi-statement consistency.

**ACID:** Atomicity, Consistency, Isolation, Durability. **Example:** Committed transfer survives a crash. **Backend use:** Reliable state changes.

**Isolation level:** Rules for visibility of concurrent transactions. **Example:** Read Committed or Serializable. **Backend use:** Prevent concurrency anomalies.

**MVCC:** Multi-version concurrency control using row versions for transaction visibility. **Example:** Readers can often proceed without blocking writers. **Backend use:** Concurrent workloads.

**Deadlock:** Cyclic waiting for locks. **Example:** Two transfers lock accounts in opposite order. **Backend use:** Retry aborted transactions and use consistent lock order.

**N+1 query:** One initial query followed by one query for each returned row. **Example:** Load each order's user separately. **Backend use:** Fix with joins or batching.

**Connection pool:** Shared collection of reusable database connections. **Example:** API with bounded PostgreSQL pool. **Backend use:** Control database load.

### SQL join and aggregation

```sql
SELECT u.id, u.email, COUNT(o.id) AS order_count
FROM users AS u
LEFT JOIN orders AS o ON o.user_id = u.id
GROUP BY u.id, u.email
ORDER BY order_count DESC
LIMIT 20;
```

`COUNT(o.id)` returns zero for users without orders. Explain why `COUNT(*)` behaves differently on a left join.

### Composite index

```sql
CREATE INDEX idx_orders_user_created
ON orders (user_id, created_at DESC);
```

Useful for queries filtering by `user_id` and sorting by `created_at`, depending on selectivity and the query planner. Diagnose slow queries with `EXPLAIN (ANALYZE, BUFFERS)`.

### Transactional transfer pattern

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100
WHERE id = 1 AND balance >= 100;
-- Application must verify exactly one row was updated; otherwise ROLLBACK.
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
-- Application must verify recipient exists; otherwise ROLLBACK.
COMMIT;
```

**Interview scenario:** Two users buy the last item simultaneously. Explain transactions, row locks, conditional updates and how to prevent overselling.

---

## Module 4 — Redis & Caching (45 min)

**Redis:** In-memory data store supporting key/value structures, counters, caches and queue infrastructure. **Example:** Cache product details. **Backend use:** Fast transient state.

**Cache:** Stored copy of expensive-to-retrieve data. **Example:** Product catalog. **Backend use:** Reduce DB latency/load.

**TTL:** Time-to-live after which a key expires. **Example:** 60-second cached profile. **Backend use:** Bound staleness.

**Cache-aside:** Read cache, load source on miss, populate cache. **Example:** `GET /products/:id`. **Backend use:** Read-heavy endpoints.

**Cache invalidation:** Updating or deleting cached entries when source data changes. **Example:** Delete product cache after update. **Backend use:** Freshness.

**Cache stampede:** Many concurrent misses for a popular expired key. **Example:** Thousands of users loading a homepage. **Backend use:** Single-flight locks or staggered TTLs.

**Eviction:** Removing cached entries under memory pressure. **Example:** LRU-like policies. **Backend use:** Manage memory.

**Rate limiting:** Restricting calls within a time budget. **Example:** 100 requests/minute per API key. **Backend use:** Abuse and load protection.

```typescript
const key = `tenant:${tenantId}:product:${productId}`;
const cached = await redis.get(key);
if (cached !== null) return JSON.parse(cached);
const product = await db.getProduct(tenantId, productId);
if (product) await redis.set(key, JSON.stringify(product), { EX: 60 });
return product;
```

**Interview scenario:** How do you cache authorization data safely? Consider short TTL, immediate invalidation after privilege changes, tenant-scoped keys, and source-of-truth checks for critical actions.

---

## Module 5 — Authentication & Security (65 min)

**Authentication:** Verifying the caller's identity. **Example:** Validate access token. **Backend use:** Identify requester.

**Authorization:** Deciding which actions an identity may perform. **Example:** Editor cannot delete billing account. **Backend use:** Resource protection.

**JWT:** Token format carrying claims with optional signing or encryption; signed JWTs are not inherently confidential. **Example:** Access token. **Backend use:** Carry identity/authorization claims.

**OAuth 2.0:** Framework for delegated authorization. **Example:** App accesses Google data with user approval. **Backend use:** Third-party integrations.

**OpenID Connect:** Identity protocol layered on OAuth 2.0. **Example:** Sign in with Google. **Backend use:** Authentication.

**RBAC:** Role-based access control. **Example:** Admin, editor, viewer. **Backend use:** Permission policies.

**Least privilege:** Grant only required permissions. **Example:** Read-only reporting service account. **Backend use:** Limit breach impact.

**Multi-tenant SaaS:** Shared application serving multiple organizations with isolated data. **Example:** One support platform for multiple companies. **Backend use:** Tenant-aware data access.

**CSRF:** Attack inducing an authenticated browser to submit an unintended request. **Example:** Malicious site triggering account change. **Backend use:** CSRF tokens and cookie defenses.

**CORS:** Browser policy controlling access to cross-origin responses; not a substitute for authorization. **Example:** Allow trusted frontend origin. **Backend use:** Browser integration.

**SQL injection:** Manipulation of SQL through unsafe concatenation of untrusted input. **Example:** Injected filter string. **Backend use:** Parameterized queries.

### Tenant-safe SQL

```sql
SELECT id, title FROM projects
WHERE tenant_id = $1 AND id = $2;
```

Derive the authorized tenant from verified server-side identity/membership, not an arbitrary client-supplied tenant ID.

### JWT verification checklist

Validate trusted signing algorithm/key, signature, issuer, audience, expiration and relevant claims; then perform **resource-level authorization**. JWT verification alone does not establish permission to access a specific record.

**Interview scenario:** User A changes a resource ID and reads Tenant B's data. Name the vulnerability: broken object-level authorization (BOLA/IDOR). Fix with tenant-scoped queries, policy checks and negative authorization tests.

---

## Module 6 — System Architecture (60 min)

**Monolith:** Application deployed as one logical unit. **Example:** Modular Fastify backend. **Backend use:** Simple operations and transactions.

**Microservice:** Independently deployable service owning a focused capability. **Example:** Billing service. **Backend use:** Team autonomy and independent scaling.

**Event-driven architecture:** Components communicate through events describing facts. **Example:** `OrderPlaced`. **Backend use:** Decoupled workflows.

**Message broker:** Infrastructure delivering messages to consumers. **Example:** RabbitMQ. **Backend use:** Asynchronous communication.

**WebSocket:** Persistent bidirectional connection. **Example:** Live order-status updates. **Backend use:** Real-time communication.

**Horizontal scaling:** Adding more service instances. **Example:** Three API replicas. **Backend use:** Capacity and resilience.

**Vertical scaling:** Increasing resources of one instance. **Example:** More RAM/CPU. **Backend use:** Immediate capacity increase.

**Load balancer:** Distributes requests among instances. **Example:** Route traffic to healthy replicas. **Backend use:** Availability.

**Circuit breaker:** Temporarily prevents calls to a failing dependency. **Example:** Stop hammering unavailable payment gateway. **Backend use:** Contain cascading failures.

**Observability:** Understanding system behavior through logs, metrics and traces. **Example:** Trace slow checkout request. **Backend use:** Debugging.

**SLO:** Measurable service reliability target. **Example:** 99.9% successful requests. **Backend use:** Operational priorities.

### Trade-off

Prefer a modular monolith when a small team needs fast delivery and simple transactions. Microservices add network failures, distributed consistency and deployment overhead; use them when clear ownership and scaling needs justify complexity.

**Interview scenario:** Design document processing: API upload → object storage → PostgreSQL job record → queue → worker → results store → polling/WebSocket status. Explain authentication, retries, deduplication and observability.

---

## Module 7 — Queues & Integrations (50 min)

**Queue:** Buffer of work awaiting asynchronous processing. **Example:** Email delivery. **Backend use:** Offload slow tasks.

**BullMQ:** Redis-backed job queue library for Node.js. **Example:** Background PDF parsing. **Backend use:** Scheduled/retried jobs.

**Producer:** Component enqueuing work. **Example:** Upload endpoint. **Backend use:** Request/job separation.

**Worker:** Component processing jobs. **Example:** Thumbnail generator. **Backend use:** Scale background work.

**Retry:** Reattempting failed work. **Example:** Transient email provider error. **Backend use:** Resilience.

**Exponential backoff:** Increasing delays between retries. **Example:** 1s, 2s, 4s. **Backend use:** Avoid overload.

**Dead-letter queue (DLQ):** Destination for messages that cannot be processed successfully. **Example:** Invalid invoice job. **Backend use:** Inspection and recovery.

**At-least-once delivery:** A message may be processed more than once. **Example:** Worker crashes after side effect but before acknowledgment. **Backend use:** Require idempotent handlers.

**Webhook:** HTTP callback triggered by an external event. **Example:** Payment succeeded. **Backend use:** Third-party event integration.

**Signature verification:** Cryptographically verifying the webhook source using the provider's scheme. **Example:** HMAC validation. **Backend use:** Reject forged events.

**n8n / Make / Zapier:** Workflow automation tools integrating APIs and actions. **Example:** New CRM contact triggers notification. **Backend use:** Low-code orchestration.

### BullMQ example

```typescript
import { Queue, Worker } from "bullmq";
const connection = { host: "localhost", port: 6379 };
const queue = new Queue("emails", { connection });

await queue.add("welcome", { userId: "u_1" }, {
  jobId: "welcome-u_1",
  attempts: 5,
  backoff: { type: "exponential", delay: 1000 },
});

const worker = new Worker("emails", async job => {
  await sendWelcomeEmail(job.data.userId);
}, { connection });
```

**Important:** Queue job IDs alone do not guarantee exactly-once external effects. Persist business-level deduplication state.

**Interview scenario:** A provider sends the same webhook five times. Verify signature, enforce a unique event ID, process atomically where possible and acknowledge safely.

---

## Module 8 — Backend System Design & Mock Interview (35 min)

### Design exercise: Multi-tenant AI support platform

1. **Frontend:** React interface authenticates users.
2. **API:** Fastify/FastAPI validates requests, enforces authorization and rate limits.
3. **PostgreSQL:** Stores tenants, users, tickets, job states and audit records.
4. **Redis:** Caches safe read models and rate-limit counters.
5. **BullMQ:** Runs long-running import, summarization and notification jobs.
6. **AI service:** Calls model providers with timeouts, bounded concurrency and output validation.
7. **Object storage:** Stores uploaded documents with access controls.
8. **Observability:** Structured logs, correlation IDs, metrics, distributed traces.
9. **Deployment:** Docker, CI/CD, secrets management, rollback.
10. **Security:** TLS, least privilege, tenant isolation, audit logs and dependency scanning.

### Answer structure for design interviews

**Clarify requirements → estimate traffic → API/data model → architecture/data flow → failure modes → security → monitoring → scaling trade-offs.**

### 15 mock interview questions

1. How does the Node.js event loop handle concurrent requests?
2. What blocks the event loop, and how would you fix it?
3. Compare FastAPI, Flask and Fastify.
4. Why does TypeScript need runtime input validation?
5. Design REST pagination for a million-row table.
6. Explain JOIN types and composite indexes.
7. What does ACID guarantee?
8. How do you handle PostgreSQL deadlocks and lost updates?
9. Design Redis cache invalidation.
10. JWT vs OAuth 2.0 vs OpenID Connect?
11. How do you prevent cross-tenant data leaks?
12. Explain at-least-once delivery and idempotent workers.
13. When would you choose microservices over a modular monolith?
14. How do you diagnose high p95 latency?
15. Design a secure document-processing backend with async workers.

### Interview readiness checklist

- [ ] Define important terms in one or two sentences.
- [ ] Explain async I/O and CPU-bound work accurately.
- [ ] Write a validated FastAPI or Fastify endpoint.
- [ ] Write a JOIN, choose an index and interpret a query plan.
- [ ] Explain transactions and concurrent updates.
- [ ] Implement cache-aside with tenant-safe keys.
- [ ] Distinguish authentication, authorization and OAuth.
- [ ] Explain idempotent jobs, retries and dead-letter handling.
- [ ] Defend a system architecture and its trade-offs.

---

## How to practice adaptively

For each module: **Basic:** Define terms. **Intermediate:** Explain a backend example. **Advanced:** Diagnose a production failure or design a resilient solution. Ask one multiple-choice or scenario question at a time; explain both the correct answer and why alternatives fail. Skip topics already mastered and revisit mistakes.

**Suggested daily target:** At least one architecture design, one SQL exercise and one security scenario completed without notes.
