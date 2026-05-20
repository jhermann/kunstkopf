# kunstkopf — Agent Guidelines

**Project**: Python CLI toolkit for audio metadata handling and hi-fi gear control.
Entry point: `kunstkopf` CLI → `src/kunstkopf/__main__.py:cli`

## Build and Test

```sh
uv sync --all-extras
uv run pytest
uv run pylint src
```

## Architecture

- Source layout: `src/kunstkopf/` (PEP 517, `setuptools` backend)
- CLI built with **Click** — commands are subcommands of the `cli` group in `__main__.py`
- Audio metadata parsing via **mutagen**; terminal color output via **colorama**
- Standalone scripts in `bin/` (not part of the installed package)

## Conventions

- Python 3.10+ required
- PEP 8 style; spaces, never TABs
- Linting: `pylint` with project config at [pylint.cfg](pylint.cfg)
- Every source file should carry the GPLv3 copyright header (see existing files for the pattern)
- New CLI commands: add a `@cli.command()` function in `__main__.py`; keep `CONTEXT_SETTINGS` applied to the group

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow (branching, PR guidelines, etc.).
