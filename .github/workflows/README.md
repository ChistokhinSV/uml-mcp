# GitHub Actions Workflows

## Active Workflows

### ✅ `test.yml` - Run Tests
**Triggers:** Push to main, Pull requests
**What it does:**
- Installs UV and dependencies
- Runs pytest with coverage
- Uploads coverage reports as artifacts

### ✅ `build.yml` - Build Package & Extension
**Triggers:** Push to main, Pull requests, Manual
**What it does:**
- Builds Python package (Windows & Linux)
- Builds Desktop Extension `.mcpb` (Linux only)
- Auto-commits extension to repo on main branch pushes
- No PyPI publishing

### ✅ `release.yml` - Create GitHub Release
**Triggers:** Manual workflow dispatch only
**Inputs:**
- `version` (required): Release version tag (e.g., v1.3.0)
- `release_notes` (optional): Custom release notes

**What it does:**
- Builds Desktop Extension on Linux runner
- Creates GitHub release with `.mcpb` file attached
- Never publishes to PyPI

### ✅ `claude-code-review.yml` - AI Code Review
**Triggers:** Pull requests, Manual
**What it does:**
- AI-powered code review using Claude Sonnet 4.5
- Reviews code quality, security, performance, testing
- Posts structured feedback directly on PR
- Skips draft PRs unless manually triggered

**Requirements:**
- GitHub Secret: `OPENROUTER_API_KEY` must be configured

---

## Disabled Workflows

### ⚠️ `ci.yml.disabled` - CI Pipeline
**Status:** DISABLED (redundant)
- Orchestrated test.yml and build.yml
- Redundant with direct workflow triggers

### ⚠️ `cd.yml.disabled` - CD Pipeline
**Status:** DISABLED (missing dependencies)
- Missing deploy.yml and related workflows
- Contains references to non-existent workflows

### ⚠️ `publish.yml.disabled` - PyPI Publishing
**Status:** DISABLED for safety

**Why disabled:**
- Contains automatic PyPI publishing on releases
- Could accidentally publish if a release is created

**To re-enable:**
1. Review the triggers in the file
2. Ensure `PYPI_API_TOKEN` secret is set
3. Rename to `publish.yml` when ready to publish

---

## Configuration

### Required Secrets

Add these secrets at **Settings → Secrets and variables → Actions**:

#### For Claude Code Review
```
Name: OPENROUTER_API_KEY
Value: <your-openrouter-api-key>
```

**How to add:**
1. Go to repository Settings
2. Navigate to Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `OPENROUTER_API_KEY`
5. Value: Your OpenRouter API key (starts with `sk-or-v1-...`)
6. Click "Add secret"

---

## Manual Workflow Triggers

**To manually trigger workflows:**
1. Go to **Actions** tab in GitHub
2. Select workflow from left sidebar
3. Click **"Run workflow"** button
4. Fill in required inputs (if any)
5. Click **"Run workflow"** to execute

---

## Workflow Safety

All active workflows are **safe** - they:
- ✅ Run tests and build packages
- ✅ Store artifacts (not published anywhere)
- ✅ Auto-commit extension to repo (tracked in git)
- ✅ AI code reviews (read-only + PR comments)
- ❌ Never publish to PyPI automatically
- ❌ Never deploy to production

---

## Cost Optimization

### Claude Code Review
- Limited to 3 conversation turns (`--max-turns 3`)
- Only runs on non-draft PRs
- Path filters for Python files only
- Uses y-router proxy for OpenRouter (cost-effective)

---

## Manual Publishing (When Ready)

```bash
# 1. Build the package
uv pip install build
python -m build

# 2. Publish to PyPI
uv pip install twine
twine upload dist/* --username __token__ --password YOUR_PYPI_TOKEN
```
