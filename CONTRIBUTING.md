# Contributing to PaintByChar

Thanks for your interest in improving PaintByChar. Contributions of all kinds are welcome: bug fixes, examples, documentation, tests, and feature ideas.

## Project overview

PaintByChar turns a rectangular grid of characters into a colored image by mapping each character to a color and rendering it as a cell or text overlay.

Core code lives in `src/paintbychar.py` and tests live in `tests/`.

## Ways to contribute

- Report bugs or broken behavior
- Improve the documentation and examples
- Add tests for edge cases
- Propose or implement new features
- Improve compatibility with different fonts, Python versions, or file formats

## Before you start

- Make sure you have Python 3.12+ installed
- Use a virtual environment for local development
- Keep changes focused and easy to review

## Local development setup

Clone the repository:

```bash
git clone https://github.com/jgd10/PaintByChar.git
cd PaintByChar
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
python -m pip install --upgrade pip
python -m pip install -e .
```

Install test dependencies if needed:

```bash
python -m pip install pytest
```

## Running tests

Run the project test suite with:

```bash
pytest
```

If you are working on a specific change, you can also run a focused subset:

```bash
pytest tests/test_main.py
```

## Coding expectations

- Follow existing project style and keep changes readable
- Prefer small, targeted changes over broad refactors
- Add or update tests for logic changes
- Keep example scripts simple and runnable
- Preserve compatibility with the current public API unless the change is explicitly discussed

## Pull request process

1. Fork the repository and create a branch for your work.
2. Make your changes in a focused branch.
3. Run the relevant tests before opening a PR.
4. Update documentation or examples when behavior changes.
5. Open a pull request with a clear title and summary.

A good PR description should include:

- what problem the change solves
- how it was tested
- any important notes for reviewers

## Suggested workflow

```bash
git checkout -b fix/my-change
# make code changes
pytest
git add .
git commit -m "Fix issue in grid rendering"
git push origin fix/my-change
```

## Reporting issues

When opening an issue, include:

- a brief description of the bug or request
- steps to reproduce
- expected behavior
- actual behavior
- your environment (Python version, OS, package version)

## Example contributions

Examples for common use cases are especially welcome in `examples/`. Keep them:

- short
- easy to run
- realistic
- clearly labeled

## Code of conduct

Please be respectful and constructive in all discussions. We aim to keep this project welcoming and collaborative.

## Questions

If you are unsure whether a change is in scope, open an issue or ask before starting a large change.

Thank you for helping improve PaintByChar.
