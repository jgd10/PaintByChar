# Release checklist

Use this checklist before publishing a new release to PyPI.

## Pre-release

- [ ] Confirm the package version in `src/paintbychar.py` matches the intended release
- [ ] Update README examples if the public API changed
- [ ] Run the full test suite: `pytest`
- [ ] Confirm package metadata in `pyproject.toml` is correct
- [ ] Review `CONTRIBUTING.md` and docs for accuracy

## Build

- [ ] Build the package locally: `python -m build`
- [ ] Check the built artifacts in `dist/`
- [ ] Verify import works in a clean virtual environment

## Publish

- [ ] Create a GitHub release with a changelog summary
- [ ] Confirm the PyPI token is configured in GitHub Actions secrets
- [ ] Trigger the `Publish to PyPI` workflow
- [ ] Verify the package appears on PyPI and install works

## Post-release

- [ ] Announce the release in the project documentation or changelog
- [ ] Review issue tracker for follow-up fixes
- [ ] Add any notes for the next release cycle
