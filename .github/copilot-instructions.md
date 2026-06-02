# Copilot / AI agent instructions for PythonTemplate (Fenrir)

Purpose
- Help an AI dev agent become productive quickly in this repo.

Quick summary
- Layout: source code lives under `src/` (flat modules: `src/core.py`, `src/main.py`, `src/data/...`).
- High-level flow: `AppCore` -> `Downloader` -> `BaseSource` implementations (e.g. `YahooSource`) -> external downloader (`yfinance`).

How to run locally
- Create and activate venv: `. setupVirtualEnv.sh` (recommended) or `python3 -m venv myVirtualEnv && source myVirtualEnv/bin/activate`.
- Install the package in editable mode so imports resolve: `pip install -e .` or `pip install -e ".[dev]"` to also get test/dev deps.
- Run app: `PYTHONPATH=src python src/main.py` (or after editable install simply `python -m src.main`).

Tests and CI
- Tests are configured via `pyproject.toml` (`[tool.pytest.ini_options]`).
- Run tests: `pytest` (prefer after `pip install -e ".[dev]"`).
- Coverage is enabled in `pyproject.toml` and collects from `src`.

Project-specific patterns and conventions
- src-layout: code is located inside `src/` (not a nested package folder). Many modules use top-level imports like `from data.sources.yahoo_source import YahooSource`. To avoid import errors, run with `PYTHONPATH=src` or install editable.
- Dependency injection for testability: `YahooSource.__init__` accepts a `downloader` callable so tests can inject a fake downloader (see `tests/data/test_yahoo_source.py`). Prefer this pattern when adding new sources.
- Small coordinator core: `AppCore` in `src/core.py` wires together sources and `Downloader` and returns an exit code (0 on success). Keep side effects (prints, IO) localized to `main`/`core`.
- Minimal settings file exists at `src/config/settings.py` (currently empty). Use it for app-wide constants/config; tests do not rely on it yet.

Key files to inspect when coding
- Application entry: `src/main.py`
- Coordinator: `src/core.py` (creates `Downloader` and calls `.download`)
- Data fetcher: `src/data/downloader.py`
- Source implementations: `src/data/sources/*.py` (example: `yahoo_source.py`)
- Tests: `tests/` (see `tests/data/test_downloader.py`, `tests/data/test_yahoo_source.py`, `tests/test_core.py`) — these show the intended public API and mocking approach.

Integration points & external deps
- `yfinance` is used by `YahooSource` (injected as `downloader` by default). When adding network calls, follow the `downloader` injection pattern for testability.
- Data flow: user code -> `Downloader.download()` -> `Source.get_data()` -> returns a `pandas.DataFrame`.

What AI agents should do and avoid
- Do: prefer small, incremental changes; run unit tests locally after changes; use the injectable `downloader` to unit-test networking logic without hitting the network.
- Do: install the package editable or run with `PYTHONPATH=src` before executing modules or tests.
- Avoid: adding global side effects at import time. Keep I/O inside `main` or `AppCore.run()`.

Examples (commands)
```
. setupVirtualEnv.sh
pip install -e ".[dev]"
pytest
PYTHONPATH=src python src/main.py
```

Notes / TODOs discovered
- `src/config/settings.py` is empty — intended place for future configuration.
- Import style is inconsistent between modules/tests (some use `src.` imports, others top-level). Installing editable resolves this; consider harmonizing imports later.

If anything in this file is unclear, tell me which area (run/tests/imports/sources) and I'll expand examples or update the instructions.
