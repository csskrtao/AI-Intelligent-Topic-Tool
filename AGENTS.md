# Repository Guidelines

## Project Structure & Module Organization
`backend_api.py` hosts the FastAPI service and coordinates file handling, OCR, and exporting by calling the Python modules inside `src/*.py`. React/Vite renderer files live alongside them in `src/components`, `src/gui`, `App.jsx`, and `main.jsx`; they are bundled and consumed by `electron/main.js` plus `electron/preload.js`. User artifacts flow through `temp_uploads/` (ingest), `exports/` (final payloads), and `issues/` (debug assets). Keep build-only assets such as icons inside `electron/assets` so electron-builder picks them up automatically.

## Build, Test, and Development Commands
Run `pip install -r requirements.txt` and `npm install` after cloning. Use `python backend_api.py` (or `npm run backend`) to start the API, `npm run dev` to boot the Vite server on `5173`, and `npm run electron:dev` for the desktop shell; `npm run start` launches both in parallel via `concurrently`. For releases, run `npm run build` followed by `npm run electron:build` to produce installers in `dist-electron/`.

## Coding Style & Naming Conventions
Python code sticks to 4-space indentation, snake_case functions, and module-level constants in SCREAMING_SNAKE_CASE; place shared dataclasses in `models.py` and keep utilities pure so they stay reusable inside tests. React components should be PascalCase files under `src/components/` exporting default functions, hooks/utilities stay camelCase, and CSS lives in `App.css` or collocated modules. Keep imports relative to `src/` root and prefer descriptive filenames such as `question_splitter.py` or `UploadPanel.jsx`.

## Testing Guidelines
Regression scripts follow the `test_*.py` convention (`test_ocr_full.py`, `test_bounding_box_api.py`, etc.); run `python test_ocr_full.py` for high-level OCR checks and `python test_ocr_parser.py` when working on parsing. Backend smoke tests are documented in `TESTING.md`, including `curl http://localhost:8000/health` once the API is up. For UI changes, run `npm run dev`, upload `test.png`, and validate split/merge/export flows while inspecting `exports/` for new files. Record tricky scenarios inside `issues/<ticket>/` together with the command you used.

## Commit & Pull Request Guidelines
Keep commits short and imperative, mirroring the existing log (`整理项目：修复正则表达式问题`). Reference issues in the body (`Refs #42`) and note the test files you executed. A pull request should contain: a concise summary, reproduction/setup steps, screenshots or GIFs for UI updates, and a checklist covering backend, renderer, and packaging impact. Tag both backend and frontend reviewers when touching shared logic, and update `.env.example` plus documentation whenever you introduce new configuration.

## Environment & Security Notes
Never commit `.env`; copy from `.env.example` locally and load secrets through `python-dotenv`. Uploaded files in `temp_uploads/` are trusted only during the current session, so purge sensitive data before committing fixtures. When sharing logs, redact OCR payloads and API keys, and avoid attaching proprietary exam content unless you have clearance.
