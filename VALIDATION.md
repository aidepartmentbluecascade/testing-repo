# Validation - Definitions & Examples Edition

## Automated content and server checks

53 checks passed. The detailed check names are in `CONTENT_VALIDATION.json`.

- All 38 lessons remain in their original order.
- All 228 original questions and their explanations are unchanged.
- All 114 original exercise/answer pairs, original reading/source passages and 153 CV coverage entries are unchanged.
- The embedded original PDF is unchanged.
- 883 definition entries have unique stable IDs and nonempty term, definition, example and clarification fields.
- Every lesson has expanded definitions.
- Tutor context includes the current term and the lesson's expanded entries, clearly separated from original source claims.
- Invalid cross-lesson definition IDs are rejected.
- An unconfigured AI tutor fails explicitly rather than inventing a reply.
- A mocked Responses request returns output, carries the requested formatting instructions and preserves `store: false`.
- No API credential is included in the model's textual lesson context.

## Browser checks

29 interaction checks passed in headless Chromium with Playwright. They cover the dashboard, individual Software/Application/System entries, examples, next/skip controls, definition ratings, recall, review queues, search, filtering, cross-lesson helper lookup, quizzes, exercise answers, export generation, legacy-backup import, note preservation and a 390-pixel mobile viewport.

Desktop lesson, glossary, quiz and mobile screenshots were inspected for readable layout and horizontal overflow. No uncaught browser JavaScript errors were observed in these tests.

The container's Chromium navigation policy blocked local-file and HTTP page navigation. Browser UI tests therefore loaded the bundled HTML into an in-memory document. Browser storage and health-check responses were simulated; the export Blob was inspected rather than downloaded through a real user browser. Legacy JSON imports were exercised through the actual application import handler. These checks do not constitute a test on the user's actual Windows browser, filesystem origin, storage settings or download permissions.

The local Python server health endpoint was exercised separately. Python syntax compilation and JavaScript syntax validation passed. Existing server restrictions were retained; this update is not a penetration test or certification for public hosting.

## Untested boundaries

No paid model-provider request was made. Actual API credentials, account quota, model availability and generated answer quality must be verified with the user's account. The prompt requests the new definition/example style but cannot guarantee that every model response will obey it.

The offline helper is deterministic lookup over prepared material, not a general conversational model. It may return a nearby concept or no match for ambiguous wording.

Self-ratings and quiz scores describe practice only. Written exercises are not automatically graded. Source claims about CV achievements and project metrics were preserved, not independently verified.

Use Export/Import when moving between files or origins. Import replaces the current progress rather than merging it. No cloud synchronization is provided.
