# GitHub Actions Safety Analysis

## ✅ SAFE to Enable (Test-Only Workflows)

### 1. `.github/workflows/test.yml` - **100% SAFE**
**Triggers:**
- Push to `main` branch
- Pull requests

**What it does:**
- ✅ Installs dependencies with UV
- ✅ Runs tests with pytest
- ✅ Uploads coverage reports
- ❌ **NO publishing**
- ❌ **NO deployments**

**Verdict:** ✅ **SAFE TO ENABLE**

---

### 2. `.github/workflows/build.yml` - **100% SAFE**
**Triggers:**
- Push to `main` branch
- Pull requests
- Manual workflow_dispatch

**What it does:**
- ✅ Builds package for Python 3.10, 3.11, 3.12
- ✅ Uploads build artifacts to GitHub (stored for 5 days)
- ❌ **NO publishing to PyPI**
- ❌ **NO deployments**

**Verdict:** ✅ **SAFE TO ENABLE**

---

### 3. `.github/workflows/ci.yml` - **100% SAFE**
**Triggers:**
- Push to `main` branch
- Pull requests

**What it does:**
- ✅ Calls test.yml workflow
- ✅ Calls build.yml workflow
- ❌ **NO publishing**
- ❌ **NO deployments**

**Verdict:** ✅ **SAFE TO ENABLE**

---

## ⚠️ DANGEROUS - Contains Auto-Publishing

### 4. `.github/workflows/publish.yml` - **⚠️ CONTAINS AUTO-PUBLISHING**

**Triggers:**
- Push to `main` → Runs tests & build only (SAFE)
- Pull requests → Runs tests & build only (SAFE)
- **⚠️ Release created → AUTO-PUBLISHES TO PYPI**
- Manual workflow_dispatch → Only publishes if you check the box

**Jobs Breakdown:**

#### `test-and-build` job - ✅ SAFE
- Runs on: push, PR, release, workflow_dispatch
- Just tests and builds
- No publishing

#### `bump-version` job - ✅ SAFE (requires manual trigger)
- Only runs if: `workflow_dispatch` AND `publish_to_pypi == true`
- Bumps version in pyproject.toml
- Commits and tags

#### `publish-to-pypi` job - ⚠️ **DANGEROUS**
**Auto-triggers when:**
1. ❌ **GitHub Release is created** (automatic!)
2. ✅ Manual workflow_dispatch with `publish_to_pypi == true` checkbox

**What it does:**
- Builds package
- **Publishes to PyPI** using `PYPI_API_TOKEN` secret
- Requires `secrets.PYPI_API_TOKEN` to be set

#### `build-and-deploy-docker` job - ⚠️ **RUNS ON PUSH**
- Runs on: push to main OR manual dispatch
- Deploys Docker image (if Smithery is configured)

**Verdict:** ⚠️ **DISABLE OR MODIFY**

---

## Recommendations

### Option 1: Enable Only Safe Workflows (Recommended)
Keep these workflows active:
```bash
✅ test.yml    # Tests only
✅ build.yml   # Builds only (no publish)
✅ ci.yml      # Orchestrates test + build
```

**Disable this workflow:**
```bash
❌ publish.yml  # Contains auto-publishing on release
```

**How to disable:**
1. Rename `.github/workflows/publish.yml` to `.github/workflows/publish.yml.disabled`
2. Or delete it entirely
3. Or move it to a different folder

---

### Option 2: Make publish.yml Safer (Manual-Only)

Modify `publish.yml` to remove auto-publishing on release:

```yaml
# Current (DANGEROUS):
on:
  release:
    types: [created]  # ← This auto-publishes!

# Change to (SAFE):
on:
  workflow_dispatch:  # Manual trigger only
    inputs:
      publish_to_pypi:
        type: boolean
        default: false
```

Remove the `release` trigger and the `build-and-deploy-docker` job.

---

## What Happens When You Enable Actions?

### On Push to `main`:
1. ✅ `ci.yml` runs → calls `test.yml` + `build.yml`
2. ✅ `test.yml` runs → tests pass/fail
3. ✅ `build.yml` runs → builds package
4. ⚠️ `publish.yml` runs **test-and-build** job (safe)
5. ⚠️ `publish.yml` runs **build-and-deploy-docker** (if enabled)

### On Pull Request:
1. ✅ All workflows run tests and builds
2. ❌ No publishing (safe)

### On Release Creation:
1. ⚠️ **AUTO-PUBLISHES TO PYPI** (if publish.yml is enabled)

---

## My Recommendation

**For test-only usage:**

```bash
# Disable the publish workflow
mv .github/workflows/publish.yml .github/workflows/publish.yml.disabled

# Keep these enabled:
# ✅ test.yml
# ✅ build.yml
# ✅ ci.yml
```

This ensures:
- ✅ Tests run automatically on push/PR
- ✅ Builds are validated
- ❌ Nothing ever publishes automatically
- ✅ You control when/if to publish manually

---

## Current Status Check

**Required Secrets:**
- `PYPI_API_TOKEN` - Only needed if you enable publish.yml
- `GITHUB_TOKEN` - Automatically provided by GitHub

**If `PYPI_API_TOKEN` is not set:**
- ✅ Safe workflows will work fine
- ⚠️ `publish-to-pypi` job will fail (but won't run unless release is created)
