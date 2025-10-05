# GitHub Actions Workflows

## Active Workflows (Safe - Test Only)

### ✅ `ci.yml` - CI Pipeline
**Triggers:** Push to main, Pull requests
**What it does:**
- Runs test.yml workflow
- Runs build.yml workflow
- No publishing or deployments

### ✅ `test.yml` - Run Tests
**Triggers:** Push to main, Pull requests
**What it does:**
- Installs UV and dependencies
- Runs pytest with coverage
- Uploads coverage reports
- No publishing or deployments

### ✅ `build.yml` - Build Package
**Triggers:** Push to main, Pull requests, Manual
**What it does:**
- Builds package for Python 3.10, 3.11, 3.12
- Uploads build artifacts (kept for 5 days)
- No publishing to PyPI

---

## Disabled Workflows

### ⚠️ `publish.yml.disabled` - Publish & Deploy
**Status:** DISABLED for safety

**Why disabled:**
- Contains automatic PyPI publishing when GitHub releases are created
- Could accidentally publish if a release is created

**To re-enable:**
1. Review the triggers in the file
2. Ensure `PYPI_API_TOKEN` secret is set
3. Rename to `publish.yml` when ready to publish

**Manual publish process instead:**
```bash
# 1. Build the package
uv pip install build
python -m build

# 2. Publish manually (when ready)
uv pip install twine
twine upload dist/* --username __token__ --password YOUR_PYPI_TOKEN
```

---

## Safe to Enable

All currently active workflows are **100% safe** - they only:
- Run tests
- Build packages (stored as artifacts, not published)
- Generate coverage reports

**Nothing will be published to PyPI automatically.**

---

## When You're Ready to Publish

1. Review `publish.yml.disabled`
2. Set up `PYPI_API_TOKEN` secret in GitHub
3. Rename to `publish.yml`
4. Create a release or run manually via workflow_dispatch
