# Arslan's Learning Studio - Definitions & Examples Edition

A personal learning portal built from **Understand your CV: A foundations-first learning workbook**. It follows your original 38-lesson order, from basic definitions through applications and engineering trade-offs.

## Updating from the previous portal

Read **UPDATE_GUIDE.md** first. Export a backup from the old portal before moving or replacing files, then import it through **Setup & backups** in this edition. Old-format backups are supported. Browser storage may differ between filenames, folders, browsers and server addresses.

The updated lessons contain **883 separate definition-and-example entries**. Every entry follows **Term: definition**, **Example:**, and **Remember:**. Use the searchable **Definitions & examples** library or learn one term at a time. Your original source passages and embedded PDF are preserved separately.

## Start immediately: no installation

Open **index.html** in a modern desktop browser. The separate `Arslan_Interactive_Learning_Portal.html` download is the same self-contained application.

Click **Start with the basics**. Choose A, B, C or D, then **Check answer**. Read the explanation before moving to the next question. All topics and difficulty levels remain unlocked.

The portal includes:

- **228 multiple-choice questions:** six per lesson, with two basic, two medium and two advanced questions. Answer positions are mixed; each question has a source-grounded explanation.
- **883 separate definition/example entries:** available through **Teach me first**, the searchable definition library and term recall. The 434 original source passages are preserved in the original lesson view.
- **114 original workbook exercises:** write an answer, reveal the original answer key, and mark whether you understand it. Written answers are self-assessed, not automatically graded.
- **Definition recall and original question cards:** explain a term and give an example before revealing the prepared answer. Mark terms as understood, review again or skipped.
- **153 CV coverage entries:** searchable checklist with links to the relevant lessons.
- **Review queues:** mistakes, skipped questions, skipped topics, bookmarks, recall cards and written exercises needing another pass.
- **Notes and discussions** attached to each question, exercise or lesson.
- **Three-day study route**, daily activity, first-try accuracy, and export/import backups.
- The **original 96-page PDF**, embedded in the HTML and available from source links.

Keyboard shortcuts: **1-4** selects an answer; **Enter** checks or advances; **Escape** closes a dialog. Shortcuts do not interrupt typing in a note or comment.

## Asking questions: two different modes

### Workbook helper: works immediately, offline

The side panel can provide the prepared explanation for your question, quote the original exercise answer, and retrieve separate definition/example entries. Each term is presented in its own block, with a concrete example and clarification.

This is a **local prepared-content lookup helper, not a live AI model**. It does not generate new conversational explanations. It explicitly says when it cannot find a supported passage. Your question and its reply remain attached to that item.

For a natural follow-up in this ChatGPT conversation, use **Ask in ChatGPT**. This copies your question, follow-up and relevant workbook context; paste it here. Nothing is sent automatically. The portal is not connected to your current ChatGPT session.

### Optional live AI tutor: natural follow-up conversation

The included local server enables real AI responses through your own OpenAI API account. This requires Python 3.10 or newer, an internet connection, an API key, and a Responses-compatible model available in your API account. No third-party Python packages are needed.

**API billing is separate from a ChatGPT subscription.** Requests can incur usage charges. No credentials are included in this package, and the live provider connection has not been tested with your account.

#### Windows setup

1. Extract this entire ZIP to a normal folder, such as `E:\Learning\ArslanStudio`.
2. Copy `.env.example` to a file named exactly `.env`, not `.env.txt`.
3. Edit the two lines in `.env`:

   ```text
   OPENAI_API_KEY=your_actual_api_key
   OPENAI_MODEL=a_responses_model_available_in_your_api_account
   ```

   The values above are placeholders. Choose a model your own API account can access; the portal does not assume that any historical model name is still available.

4. Double-click **Start-Portal.bat**. Alternatively, open a terminal in this folder and run:

   ```powershell
   python server.py
   ```

   Where the Python launcher is installed, `py -3 server.py` also works.

5. The local browser page opens at `http://127.0.0.1:8765`. Keep the terminal open while using the live tutor.
6. Select **Live AI** in the tutor panel and approve the context-sharing notice.
7. Send a question. Configuration detection is not a guarantee of model access or API credit; authentication, quota and connectivity errors appear clearly in the discussion.

For macOS/Linux, run `python3 server.py`, or `./start_portal.sh`.

If port 8765 is occupied, use `python server.py --port 8766`. To suppress browser launch, add `--no-browser`.

**Never put your API key into a quiz answer, comment, frontend code, or screenshot.** The server reads it from the environment or local `.env`, and does not send it to the browser. Restart the server after changing `.env`. Existing operating-system environment variables take precedence over `.env` values.

## What is saved, and what is sent?

**Offline:** answers, notes, discussions, reading positions and settings stay in your browser's local storage. No analytics or third-party scripts are loaded. No account or automatic synchronization is included.

**Live AI, only when you press Send:** the server sends your message, current lesson excerpts, question/exercise, selected or written answer, and a short recent discussion to OpenAI. A few relevant cross-lesson excerpts may be included. Do not enter confidential company records or secrets. Generated replies can be inaccurate; verify them against source pages.

The API request uses `store: false`. This does not override the provider's other retention or data-handling policies and is not a promise of zero retention. The local server does not log message bodies or API keys.

The server binds only to `127.0.0.1`, restricts hosts/origins, validates a session token, accepts bounded requests, caps concurrency and request rate, and serves only the portal and its API endpoints. It does not serve `.env` or directory listings. These measures are for a **personal local application**, not a production public hosting service. Do not expose it to the internet without appropriate authentication, HTTPS, operational controls and a security review.

## Save your progress

Open **Setup & backups -> Export backup** regularly. Import the resulting JSON to restore or move your progress.

Important details:

- The single-file HTML and the local-server address are different browser origins. Export from one and import into the other to move progress.
- Different browsers, private windows, browser cleanup, file renaming/moving, or a changed server port may use separate storage. Browser handling of local-file storage varies.
- A warning appears when saving is blocked; you can still practise in that session and export before closing.
- Imports replace, rather than merge, current progress. Invalid imports are rejected. Live AI is switched off after importing until you explicitly enable it again.
- Backups contain your notes and discussions. Keep them private.
- Skipping is not graded as a wrong answer. First-try accuracy and latest-result review are different measures. Help is available before answering, so a score is not a controlled examination result.
- Starting another practice round replaces only the active round. Overall attempts, notes, bookmarks and discussions remain saved.

## Source fidelity and limitations

All 38 original lessons, 114 original exercises/answers, and 153 coverage entries were taken from the supplied PDF. The MCQ wording, distractors, difficulty labels, and question explanations are learning adaptations grounded in that material. The 883 new definition/example entries expand those lessons for learning and are clearly distinguished from original source text and CV facts. They are not quotations. The source PDF remains the authority for its original content, while additional teaching examples are illustrative.

The questions sample the lessons rather than claim to test every possible fact. Use the coverage map and source cards for the smaller named tools. CV achievements are self-reported source claims, not independently verified measurements. Missing exact indexes, field-type lists, production dates, paper datasets/results, and similar details are not invented.

Extracted code and mathematical symbols may wrap or render differently from the PDF. When formatting matters, use **Original workbook** or a source-page link.

The workbook helper intentionally does not pretend to have general conversational intelligence. The optional AI tutor is designed to stay grounded in supplied context, but model responses still need checking.

## Files in this package

| File | Purpose |
| --- | --- |
| `index.html` | Complete offline-ready portal, embedded curriculum and PDF |
| `server.py` | Optional local server and server-side AI proxy |
| `.env.example` | Credential/model configuration template, no real keys |
| `Start-Portal.bat` | Windows launcher |
| `start_portal.sh` | macOS/Linux launcher |
| `course.json` | Structured original material, MCQ bank, and 883 expanded definition/example entries |
| `app.js`, `styles.css` | Readable frontend source |
| `build.py` | Rebuild the standalone HTML after source edits |
| `template.html` | HTML shell for rebuilding |
| `START_HERE.md` | This guide |
| `VALIDATION.md` | Checks performed and untested boundaries |
| `UPDATE_GUIDE.md` | New formatting, learning tools and safe progress migration |
| `CONTENT_VALIDATION.json` | Automated content-fidelity and tutor-context check results |

Editing `app.js`, `styles.css`, or `course.json` does not automatically modify `index.html`. Run `python build.py` to rebuild. The embedded original PDF is retained from the existing HTML unless you supply a new PDF using the build option.

## Official API references for optional integration

These references concern the optional API integration, not replacements for the workbook's teaching material:

- Responses API: https://developers.openai.com/api/reference/resources/responses/methods/create
- API key safety: https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety
- API data controls: https://platform.openai.com/docs/guides/your-data

No paid external API request was made while assembling this portal. UI and backend tests use local content and mocked provider responses.
