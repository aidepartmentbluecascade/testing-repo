# TableOS System Design — Complete Study Guide

**Source:** TableOS — System Design (as built), **v0.36.0**, dated **19 November 2026**. This guide reorganizes the user's nine-page PDF into 16 study modules. As-built facts refer to the dated snapshot. All practical scenarios and examples are learning illustrations unless specifically stated otherwise.

**Animated learning lab:** [Follow TableOS request flows](/tableos-architecture) — record editing, private attachments and HubSpot field sync with 21 guided steps, concept explanations and quizzes.

**Interactive study hub:** https://arslan-learning-studio.onrender.com/tableos

**Coverage:** 16 source sections, 205 individual terms including all 31 documented field types, 48 explained interview questions.

## Recommended study method

For every section: (1) say each **Term: Definition** aloud, (2) connect it to the example and backend use, (3) explain the working flow in your own words, (4) rehearse the worked example, (5) attempt one question at a time in the interactive portal, (6) review mistakes before advancing. The portal includes topic skipping, progress saving and a searchable glossary.

## Contents

1. 1. What TableOS Is (source p. 3)
2. 2. Deployment Topology (source p. 3)
3. 3. Code Structure and Libraries (source p. 4)
4. 4. Data Model and Record Storage (source p. 5)
5. 5. A Change, End to End (source p. 5)
6. 6. Realtime and Presence (source p. 6)
7. 7. Background Work and Event Bus (source p. 6)
8. 8. Fields, Formulas and Compute (source p. 7)
9. 9. Query Engine and Grid Rendering (source p. 7)
10. 10. Attachment Storage and Signed Links (source p. 7)
11. 11. Sync and External Integrations (source p. 8)
12. 12. Automations, Interfaces and Sharing (source p. 8)
13. 13. Security, Roles and Access (source p. 8)
14. 14. History, Undo, Trash and Audit (source p. 9)
15. 15. Operations, Releases and Limits (source p. 9)
16. 16. Further Reading and Full-System Review (source p. 9)

---

## 1. What TableOS Is

**Source page:** 3

Understand the product and its hierarchy before diving into infrastructure. This section describes the source's deployed v0.36.0 snapshot, not a promise about later releases.

### Definitions, examples, backend use

**TableOS:** A team-oriented, Airtable-style relational database platform.

**Example:** A sales team manages Leads and Deals in tables.

**Backend use:** Lets teams configure data and processes without changing backend schemas.

**Organization:** Top-level tenant containing members and workspaces.

**Example:** Blue Cascade is the tenant; teams work inside it.

**Backend use:** Defines membership and account-level security.

**Workspace:** Container grouping related bases inside an organization.

**Example:** Sales workspace has CRM and Reporting bases.

**Backend use:** Organizes access and collaboration.

**Base:** A database-like project containing tables, views and automations.

**Example:** CRM base contains Leads and Deals.

**Backend use:** Unit of data changes and realtime subscriptions.

**Table:** Collection of records with fields.

**Example:** Leads table.

**Backend use:** Stores one category of structured business data.

**Record:** A row containing field values.

**Example:** Lead record for a company.

**Backend use:** CRUD target in the REST API.

**Field:** Typed column describing a record attribute.

**Example:** Email or Deal Value.

**Backend use:** Validation, filtering, formatting and compute.

**View:** Saved presentation/query of a table.

**Example:** Kanban grouped by status or calendar by date.

**Backend use:** Different UIs over the same underlying records.

**Interface:** A page-based app assembled over data from a base.

**Example:** Manager's pipeline dashboard.

**Backend use:** Task-specific frontend without exposing the raw grid.

**Automation:** A trigger followed by actions.

**Example:** When a new lead is created, send a message.

**Backend use:** Event-based workflow execution.

**Synced table:** A table populated by another data source.

**Example:** HubSpot contacts copied into a TableOS table.

**Backend use:** Connect external CRM or another base.

**Public API:** Token-authenticated REST access to platform resources.

**Example:** Integration script creates a record.

**Backend use:** Third-party automation.

### How the subsystem works

1. Organization contains workspaces.
2. Workspace contains one or more bases.
3. Base contains tables; tables contain fields and records.
4. Views present those records in grid, gallery, kanban, calendar, timeline, list, Gantt or form.
5. Automations, interfaces, comments, syncs, attachments and sharing operate around that data.

### Worked example

Learning example: A support organization creates a Support workspace → Tickets base → Tickets table → Status and Priority fields → Kanban view. This illustrates the documented hierarchy; the PDF does not assert that this specific base exists.

### Remember

Remember: TableOS is a data platform with a hierarchy plus workflows and integrations—not just a spreadsheet.

### Interview practice (with answer explanations)

**Question 1 — Basic:** What is the correct TableOS hierarchy?

- A. Organization → Workspace → Base → Table → Record
- B. Record → Base → Organization → Workspace
- C. Workspace → Organization → Field → Base
- D. Organization → Table → Workspace → Record

**Answer: A.** An organization groups workspaces; workspaces group bases; bases contain tables and records.

**Question 2 — Medium:** Which feature changes how records appear without creating another table?

- A. View
- B. API token
- C. Migration
- D. Relay

**Answer: A.** Views display the same table in different layouts and with saved filtering/grouping.

**Question 3 — Advanced:** An application needs to create records from an external script. Which interface is intended?

- A. Only a screenshot
- B. Public REST API with access token
- C. Browser CSS
- D. Grafana dashboard

**Answer: B.** The document explicitly lists a public REST API accessed with tokens.


---

## 2. Deployment Topology

**Source page:** 3

Trace each service in the deployed architecture. The source specifies Render Singapore for compute/database/cache and Google Cloud Storage for objects.

### Definitions, examples, backend use

**API service:** The Fastify-backed service handling HTTP requests and several schedulers.

**Example:** PATCH updates a record.

**Backend use:** Validation, sessions, permissions and writes.

**Realtime service:** WebSocket gateway transmitting changes and presence.

**Example:** A colleague sees a cell update.

**Backend use:** Low-latency collaboration.

**Worker service:** Background process consuming BullMQ jobs and domain events.

**Example:** Index a changed record.

**Backend use:** Long-running and asynchronous tasks.

**Relay service:** Process polling database outbox rows and publishing events.

**Example:** Publish a committed record-change event.

**Backend use:** Reliable event handoff.

**PostgreSQL:** Relational system storing core, data and audit tables.

**Example:** Store records and revisions.

**Backend use:** Durable source of truth.

**Valkey / Redis-compatible store:** In-memory datastore used for queues, event bus, locks and realtime fan-out.

**Example:** Publish a base change to subscribers.

**Backend use:** Low-latency communication and job coordination.

**Google Cloud Storage (GCS):** Object storage for private attachments and thumbnails.

**Example:** Store an uploaded PDF.

**Backend use:** Large binary objects outside PostgreSQL.

**Static web app:** Built React application delivered as static assets.

**Example:** Interactive grid in the browser.

**Backend use:** Logged-in frontend.

**Public app:** Separate app serving shared views, forms and interfaces.

**Example:** Anyone with a valid share link submits a form.

**Backend use:** Limited no-account experiences.

**Grafana Cloud:** Observability platform for dashboards and monitoring.

**Example:** Track p95 request latency.

**Backend use:** Operations and troubleshooting.

**Migration:** Versioned database schema change.

**Example:** Create a new metadata table.

**Backend use:** Keep deployed schema compatible with app code.

### How the subsystem works

1. Browser uses HTTPS to communicate with the API and WSS to the realtime gateway.
2. API validates permissions and writes to Postgres.
3. Worker processes queued and event-triggered work, with Redis/Valkey assisting coordination.
4. Relay moves committed outbox events to the event bus.
5. Attachments live in private GCS; authorized clients access short-lived links.
6. Grafana and structured logs provide operational visibility.

### Worked example

As built (19 Nov 2026): API web service 2 CPU/4 GB; realtime 1 CPU/2 GB; worker 1 CPU/2 GB; relay 0.5 CPU/512 MB. A single Postgres 18 database and Valkey 8 instance are shared; the original sharded/Kafka-style target design is not deployed.

### Remember

Remember: API, realtime, worker and relay are separate runtime responsibilities around a single Postgres and Redis-compatible store.

### Interview practice (with answer explanations)

**Question 1 — Basic:** Which component polls outbox_events and publishes to the Redis event bus?

- A. Web app
- B. Relay
- C. Public app
- D. GCS

**Answer: B.** The relay bridges committed PostgreSQL outbox records to the Redis event bus.

**Question 2 — Medium:** Why store attachments in GCS instead of in the relational records table?

- A. To make every file public
- B. To separate large binary objects from structured data
- C. Because Postgres cannot store JSON
- D. To eliminate access checks

**Answer: B.** Object storage handles large files; PostgreSQL stores the structured metadata.

**Question 3 — Advanced:** Does the deployed design already use the original sharded data plane and Kafka-style log?

- A. Yes, both are live
- B. No; the document says those belong to the target design
- C. Only on mobile
- D. Only for HubSpot

**Answer: B.** The PDF explicitly distinguishes as-built single Postgres/Redis deployment from original target architecture.


---

## 3. Code Structure and Libraries

**Source page:** 4

Follow the TypeScript monorepo. The same server codebase has separate entrypoints; shared packages provide reusable domain logic.

### Definitions, examples, backend use

**Monorepo:** Repository containing multiple apps and shared packages.

**Example:** apps/server and apps/web in one repo.

**Backend use:** Coordinate types and contracts.

**pnpm:** JavaScript package manager supporting monorepo workspaces.

**Example:** Install workspace dependencies.

**Backend use:** Dependency management.

**Turborepo:** Build orchestration tool for monorepos.

**Example:** Run changed package builds.

**Backend use:** Efficient CI and builds.

**Entrypoint:** Program start target for a given runtime role.

**Example:** api, realtime, worker, relay.

**Backend use:** Run distinct services from one codebase.

**Fastify 5:** Node.js HTTP framework used by server code.

**Example:** Register REST routes.

**Backend use:** API request handling.

**Kysely:** Type-safe TypeScript SQL query builder.

**Example:** Build parameterized queries.

**Backend use:** Database access.

**pg:** PostgreSQL client for Node.js.

**Example:** Execute Kysely-generated SQL.

**Backend use:** Database connections.

**BullMQ:** Redis-backed Node.js job queue library.

**Example:** Process email queue.

**Backend use:** Background jobs.

**ioredis:** Redis/Valkey client for Node.js.

**Example:** Subscribe to a change channel.

**Backend use:** Realtime and queues.

**Zod:** Runtime schema parsing and validation library.

**Example:** Validate record update body.

**Backend use:** Reject malformed input.

**React / Vite:** Frontend component library and build tool.

**Example:** Build records grid.

**Backend use:** Interactive web app.

**TanStack Query:** Client-side management for server state.

**Example:** Cache table query results.

**Backend use:** Fetch and reconcile API data.

**Zustand:** Small client state store.

**Example:** Track presence display.

**Backend use:** Local UI state.

### How the subsystem works

1. apps/server contains API, realtime, worker and relay code; scheduler is listed as a stub entrypoint.
2. apps/web builds authenticated React SPA; apps/public builds no-account shared-view and form app.
3. packages/fields defines codecs and validation; formula and compute packages handle calculated values.
4. packages/db supplies migrations and typed SQL; packages/auth and permissions enforce access.
5. packages/events/jobs/realtime-protocol/connectors share contracts across services.

### Worked example

Learning example: A new Currency field involves a codec in packages/fields, a cell editor in packages/field-ui, query handling in packages/query, and API validation in apps/server. This example follows the documented boundaries; it is not an asserted change log entry.

### Remember

Remember: different apps and services share types, but each running process has a separate responsibility.

### Interview practice (with answer explanations)

**Question 1 — Basic:** Where does the PDF locate shared field-type codecs?

- A. apps/public
- B. packages/fields
- C. Grafana
- D. Render dashboard

**Answer: B.** The source names packages/fields for 31 field types, codecs and validation.

**Question 2 — Medium:** What advantage comes from separate api and worker entrypoints in one codebase?

- A. All jobs must share one process
- B. Shared domain code with independently deployed runtime roles
- C. No need for TypeScript
- D. No network errors

**Answer: B.** One codebase can reuse contracts while runtime roles are started separately.

**Question 3 — Advanced:** Why must API input still be validated with Zod even if TypeScript types exist?

- A. Types run on untrusted JSON automatically
- B. TypeScript types do not enforce runtime input shapes
- C. Because Kysely is not SQL
- D. Because React changes tokens

**Answer: B.** Types disappear at runtime; parsing/validation protects API boundaries.


---

## 4. Data Model and Record Storage

**Source page:** 5

Understand the three PostgreSQL schemas and why adding fields does not require new SQL columns.

### Definitions, examples, backend use

**core schema:** PostgreSQL namespace for identity, tenancy, access and integrations.

**Example:** core.users and core.access_grants.

**Backend use:** Membership and access control.

**data schema:** Namespace for bases, tables, records, history, syncs and automations.

**Example:** data.records and data.fields.

**Backend use:** Business data.

**audit schema:** Namespace for security-relevant activity events.

**Example:** audit.audit_events.

**Backend use:** Trace security actions.

**JSONB:** PostgreSQL binary JSON representation with query operators.

**Example:** records.cells stores field values.

**Backend use:** Dynamic row schema.

**Stable field slot:** Internal immutable key identifying a field's stored value.

**Example:** cells keyed by slot, not display label.

**Backend use:** Rename fields without changing data keys.

**Computed values:** Derived values stored separately from user-edited cells.

**Example:** records.computed formula result.

**Backend use:** Fast reads of formulas/rollups.

**record_links:** Table storing relationships between records.

**Example:** Deal linked to Company.

**Backend use:** Relational links.

**Typed sidecar index:** Auxiliary rows indexing typed values from flexible JSONB records.

**Example:** record_index_num or record_index_time.

**Backend use:** Efficient filtering and sorting.

**DDL:** Database definition changes such as ALTER TABLE.

**Example:** Adding an SQL column.

**Backend use:** Avoided for normal user field edits.

**Prefixed public ID:** Identifier with a type-specific prefix.

**Example:** org_, bas_, tbl_, fld_, tos_.

**Backend use:** Distinguish resource types.

**Change sequence:** Per-base ordered counter for data changes.

**Example:** base_runtime.change_seq.

**Backend use:** Realtime ordering and replay.

**Revision:** Saved snapshot/change record for history.

**Example:** record_revisions.

**Backend use:** Activity, undo and audit context.

### How the subsystem works

1. Metadata about table fields is saved in data.fields.
2. Editable cell values are keyed by stable slots in data.records.cells JSONB.
3. Computed formula/lookup/rollup results are persisted in data.records.computed.
4. Linked-record relationships live in data.record_links.
5. Large tables can use numeric/text/time sidecars for indexed sorts and filters.
6. Adding/deleting a user field changes metadata rather than altering database table columns.

### Worked example

Illustrative storage: {cells:{'slot_a':'Ali','slot_b':1200},computed:{'slot_total':2400}}. Slots are invented for teaching, not real TableOS slot IDs. The source records 79 PostgreSQL tables across core, data and audit.

### Remember

Remember: meta schema is stable; flexible user-defined fields live in JSONB and sidecar indexes.

### Interview practice (with answer explanations)

**Question 1 — Basic:** Where do ordinary record values reside?

- A. data.records.cells JSONB keyed by stable slots
- B. One SQL column per user field
- C. Only Redis
- D. A CSV file

**Answer: A.** The source explicitly places editable values under stable slot keys in JSONB.

**Question 2 — Medium:** Why can a user add a field without a SQL ALTER TABLE?

- A. No data is persisted
- B. Field metadata and JSONB slots represent dynamic fields
- C. Migrations are forbidden
- D. Everything is in GCS

**Answer: B.** Dynamic field definitions avoid modifying the physical schema for every user column.

**Question 3 — Advanced:** How are numeric/date filters accelerated on large flexible tables?

- A. Only full JSON scans
- B. Typed sidecar indexes
- C. Only browser sorting
- D. By turning off filters

**Answer: B.** The source describes record_index_num/text/time sidecars.


---

## 5. A Change, End to End

**Source page:** 5

Follow the core system-design interview story: one authenticated record update becomes a durable transaction, a realtime frame and downstream event.

### Definitions, examples, backend use

**Authentication hook:** Request middleware verifying a session or API token.

**Example:** Validate PATCH request.

**Backend use:** Identify caller.

**Permission snapshot:** Compiled effective actions for a user and base.

**Example:** compileForUser.

**Backend use:** Fast consistent permission checks.

**assertCan:** Permission check for a specific action.

**Example:** assertCan(snapshot,'record.update').

**Backend use:** Authorization boundary.

**withBaseTx:** TableOS transaction wrapper around one base mutation.

**Example:** Update a cell and its revision.

**Backend use:** Atomic writes and event records.

**change_seq:** Monotonic per-base sequence of changes.

**Example:** 104 then 105.

**Backend use:** Order realtime mutations.

**Transactional outbox:** Event rows written in the same DB transaction as business changes.

**Example:** data.outbox_events.

**Backend use:** Avoid losing events after commits.

**base_changes:** Persisted per-base change frames.

**Example:** data.base_changes.

**Backend use:** Realtime replay.

**After-commit callback:** Logic executed only once transaction succeeds.

**Example:** Publish frame to Redis.

**Backend use:** Avoid notifying for rolled-back changes.

**FOR UPDATE SKIP LOCKED:** SQL locking option letting concurrent workers claim distinct rows.

**Example:** Relay batch claims.

**Backend use:** Avoid double claiming.

**Domain event:** Fact indicating a meaningful change.

**Example:** RecordUpdated.

**Backend use:** Trigger search indexing/notifications.

**Optimistic UI:** Browser displays an edit before server confirmation.

**Example:** Cell changes immediately.

**Backend use:** Responsive collaboration.

### How the subsystem works

1. 1. Browser sends PATCH/POST with session cookie or bearer token.
2. 2. Auth hook applies MFA/device conditions; compileForUser computes access; assertCan checks action and field rules.
3. 3. withBaseTx increments change_seq, writes cells and revisions, runs dependent compute and queues sync pushes.
4. 4. In the SAME transaction, append data.base_changes and data.outbox_events.
5. 5. Commit succeeds. Only then publish realtime frame to a base Redis channel; other tabs patch caches.
6. 6. Relay reads outbox with locking and publishes domain events; workers update search, send notifications and trigger syncs/automations.

### Worked example

Learning trace: A user edits Ticket Status from Open to Resolved. The database update, revision, sequence increment and outbox event either all commit together or all roll back. The UI publishes the new status only after commit. Exact schema identifiers and example field names are illustrative.

### Remember

Remember this 6-step explanation; it is the most important TableOS system-design interview flow.

### Interview practice (with answer explanations)

**Question 1 — Basic:** What must be in the same transaction as a record update?

- A. Only browser animations
- B. Revision, base change and outbox event
- C. External email delivery
- D. Frontend cache

**Answer: B.** The source's one-transaction design atomically stores mutation, revision, base_changes and outbox.

**Question 2 — Medium:** Why publish realtime updates only after COMMIT?

- A. To make Redis persistent
- B. To avoid announcing a change that might roll back
- C. To bypass authorization
- D. To simplify CSS

**Answer: B.** Clients should not observe a change that was not durably committed.

**Question 3 — Advanced:** What failure does the transactional outbox help prevent?

- A. Invalid CSS
- B. Committed DB change with no downstream event publication
- C. Browser tab closure
- D. Missing JWT issuer

**Answer: B.** Persist the event with the business change; relay can publish later.


---

## 6. Realtime and Presence

**Source page:** 6

Understand collaboration, synchronization after gaps and why WebSocket tickets are separate from normal API sessions.

### Definitions, examples, backend use

**WebSocket:** Persistent bidirectional browser-server connection.

**Example:** Realtime cell updates.

**Backend use:** Collaboration.

**WS ticket:** Short-lived proof allowing an authenticated client to connect.

**Example:** POST /v1/auth/ws-ticket.

**Backend use:** Secure realtime handshake.

**Subprotocol:** Named application protocol on top of WebSocket.

**Example:** tableos.v1.

**Backend use:** Compatible frame negotiation.

**Base subscription:** Gateway subscription to events for one base.

**Example:** Subscribe to bas_x.

**Backend use:** Scope changes to viewers.

**Presence heartbeat:** Periodic signal describing active user location.

**Example:** Selected cell and view.

**Backend use:** Show collaborators.

**Sequence replay:** Resend ordered changes after a client's last known number.

**Example:** Replay changes 203-208.

**Backend use:** Recover missed frames.

**resync_required:** Signal asking a client to refetch when a gap cannot be replayed.

**Example:** Reconnect after long outage.

**Backend use:** Restore consistency.

**Mutation ID:** Client identifier for a particular optimistic edit.

**Example:** Client ignores matching echo.

**Backend use:** Prevent duplicate local patch.

**Access signal:** Immediate authorization change broadcast.

**Example:** Removed user loses base access.

**Backend use:** Revocation.

**Redis pub/sub fan-out:** Distribution of base changes across realtime gateways.

**Example:** One gateway forwards to connected users.

**Backend use:** Scale realtime subscribers.

### How the subsystem works

1. 1. Authenticated client requests a short-lived WebSocket ticket.
2. 2. Browser connects using tableos.v1 and subscribes to a base, optionally supplying last sequence.
3. 3. Gateway delivers change frames and presence lists, with Redis subscription per base.
4. 4. Collaborators see avatars and selected cells; clients send presence heartbeats.
5. 5. If a sequence gap is recoverable, replay; otherwise emit resync_required.
6. 6. Removed access is signaled immediately so connected tabs disconnect from the base.

### Worked example

Learning scenario: Editor A updates a cell while Editor B is viewing it. B receives a frame and patches the cached row without requesting the entire grid. A ignores the matching own-mutation frame. This follows the documented browser behavior.

### Remember

Remember: WebSocket sends changes, sequence numbers preserve order, presence is ephemeral, and DB remains source of truth.

### Interview practice (with answer explanations)

**Question 1 — Basic:** What does a realtime client request before opening the TableOS WebSocket?

- A. A public API key pasted in UI
- B. A short-lived WS ticket
- C. A new database migration
- D. An S3 upload

**Answer: B.** The source states POST /v1/auth/ws-ticket precedes connection.

**Question 2 — Medium:** What should a client do when the server sends resync_required?

- A. Ignore it
- B. Refetch authoritative state
- C. Delete its own record
- D. Disable presence

**Answer: B.** It signals a gap that cannot be safely replayed.

**Question 3 — Advanced:** Why does a browser ignore a frame with its own client mutation ID?

- A. To disable access checks
- B. To avoid reapplying an optimistic local edit
- C. To skip audit logging
- D. To preserve offline files

**Answer: B.** The sender has already applied its optimistic change and can suppress duplicate presentation.


---

## 7. Background Work and Event Bus

**Source page:** 6

Separate queued jobs, domain events, relay and scheduled jobs—four concepts interviewers often mix up.

### Definitions, examples, backend use

**BullMQ queue:** Named Redis-backed work list consumed by workers.

**Example:** file-process queue.

**Backend use:** Durable background execution.

**Queue producer:** Code adding jobs for later execution.

**Example:** API enqueues export.

**Backend use:** Decouple request latency.

**Queue consumer:** Worker processing a job.

**Example:** Build an export file.

**Backend use:** Async work.

**Domain event consumer:** Subscriber handling committed platform facts.

**Example:** Search indexer handles change.

**Backend use:** Event-driven side effects.

**Outbox relay:** Worker claiming unpublished DB events and forwarding to bus.

**Example:** Read batches of 50.

**Backend use:** Reliable asynchronous publication.

**Poll interval:** Time between relay checks.

**Example:** About 0.5 seconds in source.

**Backend use:** Event propagation latency.

**Scheduled task:** Task initiated at configured times.

**Example:** Trash purge.

**Backend use:** Periodic maintenance.

**Database lock:** Mutual exclusion coordination across worker processes.

**Example:** One sync run at a time.

**Backend use:** Prevent duplicated work.

**Search indexer:** Worker maintaining searchable text.

**Example:** Update search_documents.

**Backend use:** Full-text search.

**Automation engine:** Runner for triggers, schedules and steps.

**Example:** On record update, send email.

**Backend use:** Workflow orchestration.

### How the subsystem works

1. API transaction writes outbox_events; it does not synchronously execute every downstream effect.
2. Relay polls roughly every 0.5 s and claims batches of 50 using database row locks.
3. Redis event bus delivers events to consumers such as search-indexer, collaboration notifications and table-sync.
4. BullMQ worker processes compute, automation-trigger/step, webhook-out, email, notification, search-index, file-scan/process, import/export, AI, sync, snapshot, purge and maintenance queues.
5. API schedulers also run sync sweeps, HubSpot push/mapping, retention, trash purge and time formulas.
6. Database locks protect scheduled syncs from simultaneous API/worker execution.

### Worked example

Learning example: An uploaded CSV creates an import job. The HTTP request can return quickly, a worker imports rows later, and events trigger search indexing. The exact queue and table names follow the source; the example sequence is illustrative.

### Remember

Remember: jobs are work requests; events describe things that happened; schedulers start work by time.

### Interview practice (with answer explanations)

**Question 1 — Basic:** Which library backs TableOS background queues?

- A. BullMQ on Redis
- B. Only browser localStorage
- C. React Router
- D. Sharp

**Answer: A.** The source lists BullMQ on Redis/Valkey for many job types.

**Question 2 — Medium:** Why use FOR UPDATE SKIP LOCKED when claiming outbox events?

- A. Allow several relays to claim distinct rows
- B. Delete all events
- C. Make SQL read-only
- D. Generate signed URLs

**Answer: A.** Skip locked rows prevents concurrent claimers waiting on already claimed rows.

**Question 3 — Advanced:** Two schedulers try to sync the same source. What mechanism is documented?

- A. CSS selector
- B. Database lock
- C. Higher LLM temperature
- D. Gallery view

**Answer: B.** A DB lock guards scheduler runs to avoid concurrent duplicate sync operations.


---

## 8. Fields, Formulas and Compute

**Source page:** 7

Learn the field engine: typed validation, dependency tracking, calculated values and sensitive-data policies. The complete 31-field-type glossary is included below, reflecting the exact field-type family listed in the document.

### Definitions, examples, backend use

**Field type:** Kind of value and available operations.

**Example:** Currency, Date, Attachment.

**Backend use:** Validate and render cells.

**Codec:** Rules for parsing, serializing and converting a type.

**Example:** Parse number text.

**Backend use:** Reliable field transformations.

**Formula:** Expression computed from record data.

**Example:** Quantity * Price.

**Backend use:** Derived values.

**Formula parser:** Converts formula text into a structured typed representation.

**Example:** Parse A+B.

**Backend use:** Safe evaluation.

**Typed tree:** Tree of expression nodes annotated with types.

**Example:** Add(Number,Number).

**Backend use:** Validation and execution.

**Lookup:** Read a field through a linked record.

**Example:** Company name for a deal.

**Backend use:** Cross-table computed values.

**Rollup:** Aggregate linked records.

**Example:** Sum linked invoice values.

**Backend use:** Calculated summaries.

**Count field:** Computed number of related records.

**Example:** Number of tickets for a customer.

**Backend use:** Relationship summary.

**Dependency graph:** Map of fields that depend on other fields.

**Example:** Total depends on Quantity and Price.

**Backend use:** Incremental recalculation.

**Incremental compute:** Recalculate only affected derived values.

**Example:** Edit Quantity; recompute Total.

**Backend use:** Performance.

**NOW()/TODAY():** Time-dependent formula functions refreshed by a scheduler.

**Example:** Days until due date.

**Backend use:** Time-aware values.

**Sensitive field masking:** Hiding protected values unless reveal policy permits access.

**Example:** Masked phone number.

**Backend use:** Privacy and audit.

**Reveal list:** Allowed people who may reveal selected sensitive fields.

**Example:** Authorized support lead.

**Backend use:** Controlled unmasking.

**Text field:** Stores a short string value.

**Example:** Lead name = Ali.

**Backend use:** Names, labels and titles.

**Long text field:** Stores longer multi-line text.

**Example:** Issue description paragraph.

**Backend use:** Notes and free-form text.

**Checkbox field:** Stores a checked/unchecked choice.

**Example:** Approved = true.

**Backend use:** Binary states.

**Single select field:** Stores one value from configured options.

**Example:** Status = Open.

**Backend use:** Consistent categorization.

**Multiple select field:** Stores several selected options.

**Example:** Tags = Urgent, VIP.

**Backend use:** Multi-label classification.

**User field:** References or identifies a team member.

**Example:** Assigned to = Support Agent.

**Backend use:** Responsibility and ownership.

**Date field:** Stores a calendar date.

**Example:** Due date = 2026-12-01.

**Backend use:** Scheduling.

**Date and time field:** Stores a point in time with time component.

**Example:** Meeting = 15:30.

**Backend use:** Timestamped workflow.

**Phone field:** Stores a phone value subject to type rules and masking.

**Example:** +92… contact number.

**Backend use:** Communication and privacy controls.

**Email field:** Stores an email value subject to type rules and masking.

**Example:** support@example.com.

**Backend use:** Contact and sensitive-data control.

**URL field:** Stores a web address.

**Example:** https://example.com.

**Backend use:** External links.

**Number field:** Stores a numeric value.

**Example:** Quantity = 12.

**Backend use:** Arithmetic, filtering and sorting.

**Currency field:** Stores a money-formatted numeric amount.

**Example:** Revenue = 12,500 PKR.

**Backend use:** Financial data.

**Percent field:** Stores/displays a percentage-type value.

**Example:** Completion = 75%.

**Backend use:** Progress and rates.

**Duration field:** Stores a span of time.

**Example:** Task duration = 90 minutes.

**Backend use:** Time tracking.

**Rating field:** Stores a bounded rating-like value.

**Example:** Priority score = 4/5.

**Backend use:** Scoring.

**Attachment field:** Associates files with a record.

**Example:** Contract PDF.

**Backend use:** Document storage.

**Link-to-record field:** Connects one record to records in another table.

**Example:** Deal → Company.

**Backend use:** Relationships.

**Barcode field:** Holds a barcode-oriented identifier.

**Example:** SKU barcode.

**Backend use:** Inventory workflows.

**Button field:** Represents a record-level action control.

**Example:** Run automation.

**Backend use:** Interactive actions.

**JSON field:** Stores structured JSON content.

**Example:** {source:'crm'}.

**Backend use:** Nested integration metadata.

**Formula field:** Evaluates an expression based on other values.

**Example:** Quantity * Price.

**Backend use:** Derived numeric/text values.

**Lookup field:** Reads related-record values.

**Example:** Company industry via link.

**Backend use:** Cross-table display.

**Rollup field:** Aggregates values from linked records.

**Example:** SUM(invoice amounts).

**Backend use:** Aggregated metrics.

**Count field:** Counts related or matching records.

**Example:** Number of linked tickets.

**Backend use:** Relationship totals.

**Autonumber field:** Assigns an automatically increasing record number.

**Example:** Ticket #1205.

**Backend use:** Human-friendly sequence.

**TOS Record ID field:** Exposes a record's stable prefixed public identifier.

**Example:** tos_…

**Backend use:** Integrations and identity.

**Created time field:** Displays when the record was created.

**Example:** Created on 19 Nov.

**Backend use:** Record metadata.

**Modified time field:** Displays when the record last changed.

**Example:** Edited at 14:20.

**Backend use:** Change tracking.

**Created by field:** Displays which user created a record.

**Example:** Created by Alice.

**Backend use:** Accountability.

**Modified by field:** Displays which user last updated a record.

**Example:** Updated by Bob.

**Backend use:** Edit provenance.

### How the subsystem works

1. User creates a typed field; field package supplies codec, validation, filtering, sorting and conversions.
2. When a formula is saved, parser/evaluator identifies dependencies.
3. A changed input cell causes server runCompute to refresh affected formulas, lookups, rollups or counts.
4. Time-dependent expressions refresh on schedule because time can change without edits.
5. Email, Phone and Sensitive-marked fields are masked unless an authorized user reveals one cell with a logged reason.

### Worked example

Learning example: Line Item has Quantity 3, Unit Price 20; formula Total = Quantity * Unit Price yields 60. Change Quantity to 4; dependency graph triggers recompute to 80. Expression is illustrative; incremental computation is documented.

### Remember

Remember: a field is not just a column label; it has a codec, permissions, filter semantics and compute rules.

### Interview practice (with answer explanations)

**Question 1 — Basic:** What enables efficient recomputation after one input field changes?

- A. Field dependencies
- B. Delete every record
- C. Public share links
- D. WebSocket ticket

**Answer: A.** A dependency graph tells the system which calculated values depend on the input.

**Question 2 — Medium:** What makes NOW() and TODAY() different from ordinary formulas?

- A. They depend on time, so a scheduler refreshes them
- B. They cannot be saved
- C. They are API tokens
- D. They are SQL migrations

**Answer: A.** These formulas change without record edits.

**Question 3 — Advanced:** How does the PDF describe revealing sensitive cells?

- A. Always visible to all editors
- B. Allowlisted people reveal cells individually with logged reason
- C. Only browser CSS masks them
- D. Every external API bypasses audit

**Answer: B.** Field-level controls require explicit reveal permissions and log the action.


---

## 9. Query Engine and Grid Rendering

**Source page:** 7

Follow how a browser view becomes a database query and why the grid avoids fetching the full table.

### Definitions, examples, backend use

**Query compiler:** Logic translating view filters/sorts/search into SQL.

**Example:** POST …/records/query.

**Backend use:** Safe consistent data access.

**Cursor pagination:** Paging with a position marker rather than large offsets.

**Example:** Fetch after cursor X.

**Backend use:** Scalable scrolling.

**Projection:** Selecting only required columns/fields.

**Example:** Show Name and Status only.

**Backend use:** Reduce payload.

**Virtualized grid:** UI rendering only the visible subset of data.

**Example:** Render rows as user scrolls.

**Backend use:** Handle large tables.

**Typed sidecar:** Index-friendly typed representation of JSON values.

**Example:** Number/date index rows.

**Backend use:** Efficient filtering.

**Incremental patch:** Update cached result from an incoming frame.

**Example:** Patch one changed row.

**Backend use:** Avoid expensive refetches.

**Grouped view:** Display that groups records by a field.

**Example:** Kanban by Status.

**Backend use:** Different presentations.

**Attachment preview:** Lightweight metadata sent for attachment cells.

**Example:** First files and '+N'.

**Backend use:** Avoid large responses.

**Full-text search:** Text indexing/querying across supported fields.

**Example:** Search visible names.

**Backend use:** Locate records.

### How the subsystem works

1. Browser requests a table/view with filters, sorts, groupings and needed field IDs.
2. POST …/records/query compiles this into SQL over JSONB cells, typed sidecars and computed values.
3. Server returns cursor-paged records with only fields the grid needs.
4. Initial grid loads up to 1,200 rows, then requests more as user scrolls.
5. Attachment cells include initial files and count; long text shows 300-character preview.
6. Realtime frames patch existing rows; grid searches only fields visible in that view.

### Worked example

Learning example: Sales Kanban filters Status = Open and orders by Due Date; query compiler pushes conditions into SQL with sidecar support. Grid shows loaded cards, not every DB record at once. Specific SQL syntax is illustrative.

### Remember

Remember: SQL handles filtering, cursor pages bound work, and realtime patches keep the grid current.

### Interview practice (with answer explanations)

**Question 1 — Basic:** What operation does the grid use to query records?

- A. POST …/records/query
- B. Only Redis GET
- C. GCS upload
- D. TOTP verification

**Answer: A.** The documented API compiles filters, sorts and search into SQL.

**Question 2 — Medium:** Why request only visible/needed fields?

- A. To prevent user access entirely
- B. Reduce response size and rendering cost
- C. To disable computed columns
- D. To force DDL

**Answer: B.** Field projection reduces payload for wide tables.

**Question 3 — Advanced:** What prevents full refetch after every collaborator edit?

- A. Browser patches cached rows using realtime frames
- B. Reload entire application
- C. Delete grid state
- D. Longer signed links

**Answer: A.** The source describes realtime cache patching, not full refetch on every edit.


---

## 10. Attachment Storage and Signed Links

**Source page:** 7

Understand the private-bucket lifecycle from upload to authorized browser access.

### Definitions, examples, backend use

**Attachment:** File associated with a TableOS record.

**Example:** Customer agreement PDF.

**Backend use:** Record-linked content.

**Object storage:** Service for storing binary objects with object keys.

**Example:** Private GCS bucket.

**Backend use:** Files outside SQL.

**Object key:** Path-like name locating an object.

**Example:** attachments/<workspace>/<base>/…

**Backend use:** Organized storage.

**Private bucket:** Storage whose objects are not public by default.

**Example:** Access prevention on bucket.

**Backend use:** File confidentiality.

**Signed URL:** Time-limited cryptographically authorized object request.

**Example:** V4 signed file link.

**Backend use:** Temporary download access.

**V4 signature:** Google Cloud Storage signature proving allowed URL parameters.

**Example:** Authenticated download redirect.

**Backend use:** Prevent unauthorized path/expiry changes.

**Thumbnail:** Smaller preview derived from an attachment.

**Example:** Image preview generated by sharp.

**Backend use:** Fast grid rendering.

**sharp:** Node.js image processing library.

**Example:** Generate previews.

**Backend use:** Thumbnail pipeline.

**Server-side copy:** Storage provider copies objects without browser re-upload.

**Example:** Legacy bucket migration.

**Backend use:** Efficient data transfer.

### How the subsystem works

1. Client uploads through TableOS API; the system stores the object in private GCS.
2. The object key includes workspace/base/attachment/filename organization.
3. The API verifies the caller's access before redirecting to a signed V4 link.
4. The source says thumbnail links are valid around 1 hour and full file links 10 minutes, bounded by an at-most 2-hour issuance window.
5. GCS refuses changing signed object or extending signed expiry.
6. Sharp generates thumbnails; records reference attachments and variants.

### Worked example

Source note: On 19 Nov 2026, the former shared bucket's 319,341 objects were copied server-side; call recordings referenced from records remained in the older ai-calls/ path. These are historical operations in the PDF, not instructions for current migration.

### Remember

Remember: authorization at the API and cryptographic time-limited storage access are two separate controls.

### Interview practice (with answer explanations)

**Question 1 — Basic:** Are TableOS attachment files publicly readable without checks?

- A. Yes, all are public
- B. No, access is checked before a short signed URL
- C. Only through Slack
- D. Only if in JSONB

**Answer: B.** Objects are private; the API checks access and provides temporary signed links.

**Question 2 — Medium:** Why are signed URLs short-lived?

- A. So files become unencrypted
- B. To limit reuse after an authorized access decision
- C. Because URLs cannot contain filenames
- D. To make uploads slower

**Answer: B.** The expiry limits the duration of delegated access.

**Question 3 — Advanced:** Can an attacker alter the object key inside an existing signed URL and keep it valid?

- A. Yes, signatures don't cover objects
- B. No, the provider validates the signature against the signed request
- C. Only for thumbnails
- D. Only after refresh

**Answer: B.** Changing protected URL parameters invalidates its signature.


---

## 11. Sync and External Integrations

**Source page:** 8

Distinguish a copied synced table from ordinary-table HubSpot field mapping and understand conflict resolution.

### Definitions, examples, backend use

**Integration connection:** Stored credential/config for an external provider.

**Example:** HubSpot account connection.

**Backend use:** Shared external integrations.

**AES-256-GCM:** Authenticated symmetric encryption algorithm.

**Example:** Encrypt provider credentials.

**Backend use:** Protect secrets at rest.

**Synced table:** Read-only mirror from another system into TableOS.

**Example:** Airtable or Gmail data copied.

**Backend use:** Scheduled ingestion.

**Incremental pull:** Fetch changes since previous checkpoint.

**Example:** Recent HubSpot updates.

**Backend use:** Efficient refresh.

**Full resync:** Re-fetch complete source for reconciliation.

**Example:** Daily full read.

**Backend use:** Correct missed changes.

**Two-way sync:** Changes can flow in both directions.

**Example:** TableOS and HubSpot edit a deal.

**Backend use:** Bidirectional integration.

**Field mapping:** Associating a TableOS field with a provider property.

**Example:** Email ↔ hs_email.

**Backend use:** Schema correspondence.

**Match key:** Attribute used to pair records lacking stored IDs.

**Example:** Email.

**Backend use:** Cross-system identity resolution.

**Conflict resolution:** Choosing a value when both systems edited same field.

**Example:** Newer change wins.

**Backend use:** Deterministic sync.

**Sync checkpoint:** Last observed values/state saved for each side.

**Example:** hubspot_link_records.

**Backend use:** Detect changed fields.

**Push queue:** Buffered outbound updates to another system.

**Example:** table_sync_pushes.

**Backend use:** Retry external writes.

**OAuth PKCE:** Proof Key for Code Exchange strengthening OAuth authorization code flow.

**Example:** Gmail connection from browser.

**Backend use:** Reduce code interception risk.

**Property cache:** Locally stored provider field definitions.

**Example:** core.hubspot_properties.

**Backend use:** Efficient mapping UI.

### How the subsystem works

1. Owner configures encrypted organization-shared connection.
2. Synced table pulls another TableOS base, Airtable table, HubSpot object or Gmail inbox; it normally presents read-only copied data.
3. HubSpot field mapping instead links an ordinary table to provider object properties; each mapping has one of three directions.
4. Match records using stored HubSpot ID or configured match key; create unmatched records on the permitted side.
5. Compare saved per-side field values to see what changed; when both changed a two-way field, source says newer edit wins.
6. Run periodically (5–1,440 minutes), shortly after an edit, or manually; HubSpot properties refresh hourly. Source states deletes are not propagated.

### Worked example

Learning example: Map local Deals.Amount ↔ HubSpot Deals.amount. TableOS becomes 500, HubSpot becomes 600 later, both since last sync; the latest change wins according to the documented policy. Record IDs and values are illustrative. This is not a proof of conflict-safety in all clock scenarios.

### Remember

Remember: shared connection → select source → pair records → compare changed fields → apply direction → update/checkpoint.

### Interview practice (with answer explanations)

**Question 1 — Basic:** Who manages organization-shared integration connections in the PDF?

- A. Only Owners
- B. Every guest
- C. Only workers
- D. Anonymous visitors

**Answer: A.** Connections are owner-managed and stored encrypted.

**Question 2 — Medium:** What distinguishes a synced table from HubSpot field mapping?

- A. They are always identical
- B. Synced table copies a source into a read-only table; mapping syncs selected fields on an ordinary table
- C. Mapping uses no credentials
- D. Synced tables only store images

**Answer: B.** These are distinct integration features and workflows.

**Question 3 — Advanced:** What happens if both sides changed the same two-way mapped field?

- A. Delete both values
- B. Newer change wins under documented rule
- C. User must always choose manually
- D. Disable all records

**Answer: B.** The document says newer change wins after tracking last values on each side.


---

## 12. Automations, Interfaces and Sharing

**Source page:** 8

Learn how automation triggers and steps execute durably, and why public experiences have limited tokens.

### Definitions, examples, backend use

**Automation trigger:** Condition starting a workflow.

**Example:** Record created or form submitted.

**Backend use:** React to business events.

**Automation step:** Action within a workflow.

**Example:** Send email or update record.

**Backend use:** Execute business work.

**Durable run state:** Persisted workflow run/step progress.

**Example:** Postgres run tables.

**Backend use:** Resume and inspect failures.

**Idempotency:** Repeated execution gives the same intended effect.

**Example:** Deduplicate webhook delivery.

**Backend use:** Avoid duplicated effects.

**Loop guard:** Check preventing automation from retriggering itself forever.

**Example:** Update causing another update trigger.

**Backend use:** Protect system resources.

**Service session:** Short-lived identity for automation execution.

**Example:** Run as automation owner.

**Backend use:** Permission scoping and audit.

**Public interface:** Page-based app over selected base data.

**Example:** Customer issue submission page.

**Backend use:** Tailored no-account access.

**Share link:** Tokenized access to a limited public view or form.

**Example:** Public feedback form URL.

**Backend use:** Controlled sharing.

**Rate limit:** Bound on actions/requests in time.

**Example:** Max form submissions/minute.

**Backend use:** Abuse prevention.

**Webhook trigger:** Incoming HTTP event that starts an automation.

**Example:** CRM sends event.

**Backend use:** External orchestration.

### How the subsystem works

1. Create automation trigger (record created/updated/matches, form, schedule, webhook or button).
2. Configure ordered actions (create/update records, email, Slack, webhook, script).
3. Store run/step state in Postgres and execute steps via BullMQ.
4. Guard against duplicate execution and loops; run in the owner's permission context.
5. Short-lived service session may access masked values for authorized operations; such reveal access is logged.
6. Public views/forms/interfaces use distinct share tokens and rate limits in the separate public app.

### Worked example

Learning example: Ticket created → automation triggers → worker creates run record → sends Slack notification → marks step completed. If worker retries, idempotency should prevent duplicate notifications; exact implementation specifics beyond described guarantees are not given.

### Remember

Remember: trigger → durable run → queued steps → owner-scoped execution → idempotent completion.

### Interview practice (with answer explanations)

**Question 1 — Basic:** Which can trigger a TableOS automation?

- A. Record update
- B. Only GCS deletion
- C. Only database migration
- D. Only an admin's browser refresh

**Answer: A.** The PDF lists record changes, form submissions, schedules, webhooks and buttons.

**Question 2 — Medium:** Why store automation run and step state in PostgreSQL?

- A. To improve CSS
- B. To make execution durable and inspectable
- C. To replace authentication
- D. To store audio

**Answer: B.** Persisted states survive worker interruptions and support retries.

**Question 3 — Advanced:** An automation updates the same field that triggers itself repeatedly. What guards against runaway execution?

- A. Loop guard
- B. CORS
- C. Signed URL
- D. Sidecar index

**Answer: A.** Loop guards are explicitly documented for automation safety.


---

## 13. Security, Roles and Access

**Source page:** 8

Understand layered authentication and authorization without confusing organization account type, base role and field visibility.

### Definitions, examples, backend use

**Account type:** Organization-wide level: Owner, Admin or Member.

**Example:** Owner can manage connectors.

**Backend use:** High-level governance.

**Workspace/base role:** Resource-scoped permissions: Owner, Creator, Editor, Commenter, Read only, Interface only or No access.

**Example:** Editor in Sales base.

**Backend use:** Least-privilege access.

**Session token:** Credential representing signed-in browser session.

**Example:** Hashed token in core.sessions.

**Backend use:** Authentication.

**Bearer API token:** Credential sent in Authorization header.

**Example:** tos_-prefixed token.

**Backend use:** Programmatic access.

**Token hash:** One-way digest used instead of storing raw bearer token.

**Example:** Hash stored for API token.

**Backend use:** Limit exposure if DB leaked.

**Token scope:** Set of allowed operations/resources.

**Example:** Read/write/delete; chosen bases.

**Backend use:** Fine-grained API privileges.

**TOTP:** Time-based one-time password factor.

**Example:** Authenticator code.

**Backend use:** MFA protection.

**Device approval:** Owner approval for a browser device to access an organization.

**Example:** Approve a new laptop.

**Backend use:** Account/device governance.

**Field-level permission:** Fine-grained control of field editing/reveal.

**Example:** Only finance edits Salary.

**Backend use:** Protect sensitive columns.

**Sensitive-field masking:** Return obscured values until authorized reveal.

**Example:** ******** for phone.

**Backend use:** Controlled disclosure.

**Master token:** Owner-only high-privilege API token reaching all bases and sensitive fields.

**Example:** Owner maintenance script.

**Backend use:** Special privileged API use.

**Invitation token:** Time-limited join link stored protected.

**Example:** 7-day invite.

**Backend use:** Safe onboarding.

**Audit event:** Recorded security-relevant action.

**Example:** Token usage or unmask.

**Backend use:** Accountability.

### How the subsystem works

1. Request authenticates using browser session or bearer API token.
2. MFA, forced password change and approved device policy are enforced at authentication boundary.
3. Account type plus workspace/base roles and grants produce compiled access snapshot.
4. Route checks a specific action; field edit and sensitive reveal rules add finer checks.
5. Owner alone manages Members & access and Connectors; Admin has operational powers but not those settings.
6. API tokens have scopes, base restrictions, expiry and rate limits; logged calls and revocation are documented.

### Worked example

Example (illustrative): a Member has Editor role in the Support base but No access to Finance. The compiled snapshot allows record.update in Support only. The document also describes owner-only master-token behavior including unmask, and that such tokens stop when the creator loses Owner status.

### Remember

Remember: identity → organization account type → workspace/base role → specific action → field-level rules.

### Interview practice (with answer explanations)

**Question 1 — Basic:** Who can manage organization connectors according to the PDF?

- A. Owner
- B. Admin and Member automatically
- C. Any base commenter
- D. Unauthenticated users

**Answer: A.** Owner alone manages connections and connector settings.

**Question 2 — Medium:** Does having organization Admin status automatically grant access to every base?

- A. Yes
- B. No, Admin opens only bases it has been granted
- C. Only via WebSocket
- D. Only with a signed URL

**Answer: B.** The table says Owners have all; Admins and Members have 'given' base access.

**Question 3 — Advanced:** What happens to an owner's master token after its creator is no longer an Owner?

- A. It remains universally valid
- B. It stops working
- C. It becomes a public share link
- D. It changes to a TOTP code

**Answer: B.** The source explicitly states master token rights depend on the creator retaining Owner status.


---

## 14. History, Undo, Trash and Audit

**Source page:** 9

Distinguish ordinary record history from recoverable deletion and organization-wide security audit.

### Definitions, examples, backend use

**Record revision:** Persisted record-change version.

**Example:** Status changed from Open to Done.

**Backend use:** Activity/history.

**Undo/redo:** Ability to reverse or reapply prior edits.

**Example:** Undo accidental status edit.

**Backend use:** User experience recovery.

**Deletion batch:** Saved group of deleted items for restoration.

**Example:** data.deletion_batches.

**Backend use:** Trash recovery.

**Trash purge:** Scheduled permanent removal of expired trash items.

**Example:** Retention job.

**Backend use:** Storage and lifecycle.

**Retention:** Policy defining how long history or trash is kept.

**Example:** Purge after policy window.

**Backend use:** Data lifecycle.

**Audit trail:** Security event log for accountability.

**Example:** Sign-in or token change.

**Backend use:** Incident review.

**audit_events:** PostgreSQL table of security-relevant actions.

**Example:** Device approval recorded.

**Backend use:** Compliance/operations.

**Record activity:** Per-record list of changes.

**Example:** Who edited the field.

**Backend use:** Collaboration context.

### How the subsystem works

1. Each record edit writes a record_revisions entry.
2. Users can view record activity and use per-base undo/redo, including after page reload.
3. Deleted records are tracked in deletion_batches so they can be restored from trash.
4. Schedulers enforce retention and purge eligible trash.
5. Security-relevant actions write to audit.audit_events rather than being mixed with ordinary row history.

### Worked example

Learning scenario: An editor deletes a customer record, then restores it from Trash. The record's ordinary changes belong in record_revisions; a security-setting change belongs in audit.audit_events. Which exact data is retained depends on platform retention policy not enumerated in the source.

### Remember

Remember: revisions = data history; deletion batches = trash; audit_events = security activity.

### Interview practice (with answer explanations)

**Question 1 — Basic:** Which table records ordinary record revisions?

- A. record_revisions
- B. audit_events only
- C. core.sessions
- D. table_sync_pushes

**Answer: A.** Record history lives in data.record_revisions.

**Question 2 — Medium:** Where are deleted records tracked for restoration?

- A. deletion_batches
- B. Redis locks only
- C. Frontend CSS
- D. GCS signature

**Answer: A.** Deletion batches represent recoverable trash.

**Question 3 — Advanced:** How do record history and security audit differ?

- A. They are identical
- B. Revisions describe record edits; audit_events describe security-relevant actions
- C. Audit is only in browser
- D. History never persists

**Answer: B.** They serve separate accountability needs.


---

## 15. Operations, Releases and Limits

**Source page:** 9

Know how TableOS is tested, released, deployed and monitored, and distinguish deployed limits from planned scaling.

### Definitions, examples, backend use

**Release branch:** Branch holding a prepared version release.

**Example:** release/v0.36.0.

**Backend use:** Controlled delivery.

**Type check:** Static TypeScript validation.

**Example:** tsc --noEmit.

**Backend use:** Catch type errors.

**Regression test:** Test that old behavior still works after changes.

**Example:** Record editing still updates search.

**Backend use:** Prevent breakage.

**Playwright:** Browser automation framework.

**Example:** Check editing workflow with screenshots.

**Backend use:** End-to-end QA.

**Migration on startup:** API applies outstanding schema migrations when launched.

**Example:** New table migration.

**Backend use:** Database compatibility.

**Structured logs:** Machine-readable request/event logs.

**Example:** pino JSON.

**Backend use:** Troubleshooting.

**p95 latency:** Latency below which 95% of measured requests fall.

**Example:** 95% of API calls under target.

**Backend use:** Tail performance.

**Grafana dashboard:** Operational charts for metrics.

**Example:** CPU, memory, latency and DB health.

**Backend use:** Monitoring.

**Capacity limit:** Documented product/infrastructure bound.

**Example:** 50,000 records per synced table.

**Backend use:** Product planning.

**Sharding:** Partitioning data across multiple database instances.

**Example:** Target architecture, not deployed.

**Backend use:** Potential future scale.

**Release approval:** Human sign-off before merging a release.

**Example:** Merge to master only after approval.

**Backend use:** Production governance.

### How the subsystem works

1. Develop changes on a feature branch and test locally with dummy data.
2. Run type checks, server build, regression scripts and Playwright UI check with screenshots.
3. Bump version; push release/vX.Y.Z to complete remote.
4. Merge approved release to master; Render deploys master.
5. API applies missing migrations on startup; deployment restarts API, realtime, worker and relay.
6. Observe Grafana metrics and Render pino JSON logs; investigate incidents using request status and timing.

### Worked example

As built limits (19 Nov 2026): one PostgreSQL and one Redis/Valkey instance for all tenants; each synced table up to 50,000 records; incremental HubSpot search capped at 10,000 changes before a full read; HubSpot field mapping does not propagate deletes. These are source-dated statements.

### Remember

Remember: describe the actual deployment, release branch policy and known limits—never present the target architecture as deployed.

### Interview practice (with answer explanations)

**Question 1 — Basic:** Which branch does the PDF say Render deploys for TableOS?

- A. master
- B. Any arbitrary developer branch
- C. Only gh-pages
- D. The original architecture folder

**Answer: A.** It describes approved releases merged into master, which Render deploys. Note: this is TableOS, not the Learning Studio repo.

**Question 2 — Medium:** What quality checks precede a TableOS release?

- A. Type checks, server build, regression scripts and Playwright
- B. Only unit test count
- C. No tests ever
- D. Only database dump

**Answer: A.** The documented release workflow explicitly lists those checks.

**Question 3 — Advanced:** Which scalability feature is a target design rather than deployed?

- A. Single shared Postgres
- B. Sharded data plane with Kafka-style log
- C. BullMQ worker queues
- D. Private object storage

**Answer: B.** The PDF says the sharded/Kafka-style original design is not built.


---

## 16. Further Reading and Full-System Review

**Source page:** 9

Turn the whole design into one interview-ready explanation; the PDF names references you can open in the real TableOS source repository.

### Definitions, examples, backend use

**As-built design:** Documentation of the currently implemented/deployed system at a dated snapshot.

**Example:** SYSTEM-DESIGN.md v0.36.0.

**Backend use:** Accurate architecture discussions.

**Target architecture:** Design planned before implementation.

**Example:** architecture/ sharded data plane.

**Backend use:** Future-state direction.

**ADR:** Architecture Decision Record explaining a choice and trade-off.

**Example:** Decision to use JSONB slots.

**Backend use:** Rationale and constraints.

**CHANGELOG.md:** Version-by-version record of changes.

**Example:** Read changes since v0.36.0.

**Backend use:** Release tracking.

**Work log:** Chronological implementation/verification notes.

**Example:** docs/TABLEOS-WORK-LOG.md.

**Backend use:** Understand build history.

**API reference:** Endpoint contracts and examples for integrators.

**Example:** Help → API reference.

**Backend use:** Developer onboarding.

**System diagram:** Visual explanation of components and interactions.

**Example:** Browser → API → Postgres → Redis.

**Backend use:** Architecture communication.

**Trade-off:** Cost accepted to gain a benefit.

**Example:** JSONB flexibility vs typed index sidecars.

**Backend use:** Design justification.

**Failure mode:** Way a component can become unavailable or inconsistent.

**Example:** Relay temporarily down.

**Backend use:** Resilience planning.

### How the subsystem works

1. Start explanation at organization → workspace → base → table → record.
2. Name API, realtime, worker and relay around PostgreSQL/Redis and private GCS.
3. Describe one record change, emphasizing a single DB transaction and outbox.
4. Describe websocket sequence replay, compute dependencies and typed index sidecars.
5. Explain automation, synced tables, HubSpot mapping and access layers.
6. Conclude with limits, monitoring, release process and next architectural improvements.

### Worked example

Interview script: 'TableOS is a multi-tenant relational workspace product with flexible JSONB record storage. Fastify handles authenticated requests; changes commit with revisions, base changes and an outbox. Redis/Valkey distributes realtime and jobs; a relay publishes durable events; workers handle search, automation and sync. Private GCS stores files. The current deployment uses a single Postgres/Redis; sharding is a future target.'

### Remember

Remember: always distinguish PDF source facts from learning examples, and current implementation from target architecture.

### Interview practice (with answer explanations)

**Question 1 — Basic:** Which document describes what TableOS actually ran on 19 Nov 2026?

- A. System Design — as built v0.36.0
- B. Only the original ADRs
- C. Only UI CSS
- D. Only the future sharded design

**Answer: A.** The uploaded PDF is explicitly the current-state companion to the earlier architecture target.

**Question 2 — Medium:** Where should an engineer inspect why architecture decisions were chosen?

- A. architecture/ ADRs
- B. Only public share links
- C. A table view color
- D. GCS thumbnails

**Answer: A.** ADRs capture design rationale; work log and change log explain implementation.

**Question 3 — Advanced:** What is the strongest concise TableOS system-design explanation?

- A. It's only a React spreadsheet
- B. It uses flexible record storage, atomic changes/outbox, realtime gateway, jobs, permissions and private file storage
- C. It already uses Kafka shards in production
- D. It has no permissions

**Answer: B.** This answer connects the major as-built subsystems and avoids conflating them with target architecture.


---

## Provenance and limits

The source is the user's *TableOS — System Design (as built), v0.36.0, 19 November 2026*. It describes the deployed system at that time. Its original sharded data plane and Kafka-style logging were *target architecture*, not described as deployed. Original referenced sources include `docs/SYSTEM-DESIGN.md`, `docs/TABLEOS-WORK-LOG.md`, `CHANGELOG.md`, `docs/VERSIONING.md`, `architecture/` and Help → API reference. These files are referenced, not claimed as present in this learning repository. Examples are illustrative and no access credentials are provided.
