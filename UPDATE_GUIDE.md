# Learning Studio - Definitions & Examples Edition

## Open the updated portal

Open `index.html` in Chrome or Edge. The separately supplied `Arslan_Interactive_Learning_Portal_Updated.html` is the same self-contained portal.

The default learning view now uses **one term per entry**:

**Software:** It is a set of instructions that a computer executes to perform tasks.

**Example:** A Python script that totals completed calls is software.

**Remember:** Software is the instructions, not the physical computer running them.

Application, System, Frontend and every other entry follow the same separate format. Definitions are no longer bundled into a single learning paragraph.

## What changed

- **883 definition-and-example entries across all 38 lessons.** Each entry has its own term, explanation, concrete example and clarification. Some concepts are revisited in different project contexts; this is an entry count, not a count of unique technical terms.
- **Definitions & examples library:** search the term, meaning or example; filter by lesson or your understanding rating.
- **Lesson cards:** jump directly to any term; move forward or backward; mark I understand, Review again or Skip.
- **Definition recall:** explain the term and give an example before revealing the prepared entry. This is self-assessment, not automatic grading.
- **Quiz support:** expandable individual definitions and examples beside the existing questions.
- **Learning companion:** the offline helper retrieves prepared definition/example entries. It does not pretend to generate new open-ended responses.
- **Optional live tutor:** its instructions and lesson context now use separate Term, Example and Remember blocks. Provider-generated replies still need checking.
- **Term-specific notes and discussions:** questions and notes remain attached to the term being studied.

The original 228 quiz questions, 114 workbook exercises and answer keys, 153 CV-map entries, original source passages and embedded PDF are preserved. The PDF itself has not been rewritten.

## Bring over your existing progress

**Before replacing, moving or renaming the old portal file:**

1. Open the old portal in the browser where you studied.
2. Go to **Setup & backups -> Export backup** and save the JSON file.
3. Open the updated portal.
4. Go to **Setup & backups -> Import backup**, select that JSON file and confirm.

Old-format backups remain compatible. Quiz results, bookmarks, notes, written exercises, source reading positions and discussions retain their existing IDs. New definition ratings start empty when an old backup does not contain them.

Import replaces the current saved progress rather than merging it. Export the updated portal's progress first if you already used it. New-format backups include term notes, discussions and ratings. Do not rely on the old portal to preserve the new fields when importing an updated backup into it.

Browser handling of local-file storage varies. A new filename, folder, browser, private window, server address or port can use different storage. The safest migration route is Export/Import. No automatic account or cloud synchronization is provided.

## A useful learning loop

Open **All lessons -> Learn first**. Read one definition, follow the example, then explain the term without looking. Use **Recall definitions** to test yourself. Mark uncertain entries for review instead of reading all 883 at once.

Choose **See all terms** for the current lesson or **Definitions & examples** for a global search. All topics remain available; skipping never reduces your quiz accuracy.

The original walkthroughs, code and exercises remain available through **Original worked examples & lesson**, **Exercises**, and **Original workbook**.

## Asking a follow-up

In the side panel, try **Explain this**, **Show an example**, or a named term such as **What is an embedding?** The offline helper returns prepared entries and acknowledges when no match is found.

Use **Ask in ChatGPT** to copy the term, question and lesson context, then paste it into your ChatGPT conversation. This portal is not automatically connected to that conversation.

For live AI conversation inside the portal, use the included local server and configure your own credentials as described in `START_HERE.md`. Existing `.env` credentials should stay private. Do not put them in the HTML or send them in a question. No real provider credentials are included, and no paid provider request was made during this update.

## What is source-based and what is expanded

The lesson order, project claims, original questions, exercises and source passages come from the supplied workbook. The new entries are expanded teaching adaptations, not quotations. Their examples illustrate concepts unless explicitly marked as CV-reported facts.

A workbook page link identifies the original lesson topic; it does not claim the expanded wording appears verbatim on that page. Missing exact deployment details, benchmark conditions, research results and field-type lists are still identified as unknown rather than invented. Relevant official-documentation links appear under the lesson's **Source & teaching notes**.

## Running the optional local server

Extract the entire ZIP. Keep your `.env` configuration private and follow `START_HERE.md`. On Windows run `Start-Portal.bat`, or run `python server.py` in the extracted folder.

The original local-only safety restrictions remain. This is a personal application, not a public multi-user hosting service. Rebuild after editing `app.js`, `styles.css`, or `course.json` by running `python build.py`.
