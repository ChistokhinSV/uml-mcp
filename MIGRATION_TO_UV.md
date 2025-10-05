# Migration to UV Package Manager

This document summarizes the migration from pip/poetry to UV package manager.

## What Changed

### ✅ Completed

1. **Removed pip-based dependency files:**
   - ❌ Deleted `requirements.txt`
   - ❌ Deleted `requirements-dev.txt`

2. **Updated pyproject.toml:**
   - ✅ Converted to modern PEP 621 format
   - ✅ Added all dependencies with version constraints
   - ✅ Added platform-specific uvloop for Linux/Mac: `uvloop>=0.17.0; sys_platform != "win32"`
   - ✅ Changed build system to `hatchling`
   - ✅ Added project URLs pointing to https://github.com/ChistokhinSV/uml-mcp

3. **Updated Documentation:**
   - ✅ README.md - All pip references replaced with UV
   - ✅ CLAUDE.md - Updated for UV-only workflow
   - ✅ UV_SETUP.md - Comprehensive UV guide
   - ✅ docs/installation.md - UV installation instructions
   - ✅ Makefile - UV-only commands with setup helper

4. **Updated GitHub Actions:**
   - ✅ `.github/workflows/ci.yml` - Removed requirements.txt reference
   - ✅ `.github/workflows/test.yml` - Replaced Poetry with UV
   - ✅ `.github/workflows/build.yml` - Replaced Poetry with UV
   - ✅ `.github/workflows/publish.yml` - Complete UV migration:
     - Install UV instead of Poetry
     - Build with `python -m build`
     - Publish with `twine`
     - Custom version bumping script (no Poetry needed)

5. **Updated Docker & Deployment:**
   - ✅ Dockerfile - Installs UV and uses `uv pip install`
   - ✅ vercel.json - Uses UV for builds

6. **Updated GitHub URLs:**
   - ✅ All references changed from placeholder to https://github.com/ChistokhinSV/uml-mcp

## New Installation Flow

### For Users

```bash
# Install UV
winget install --id=astral-sh.uv -e  # Windows
# or
curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/Mac

# Clone and install
git clone https://github.com/ChistokhinSV/uml-mcp.git
cd uml-mcp
uv pip install -e .

# For development
uv pip install -e ".[dev]"
```

### Using Makefile

```bash
make setup-uv      # Shows UV installation instructions
make install       # Install production dependencies
make install-dev   # Install development dependencies
```

## Benefits

1. **🚀 Speed**: 10-100x faster than pip/poetry
2. **🔧 Better dependency resolution**: Faster conflict detection
3. **🔄 Platform-aware**: Automatically installs uvloop only on Linux/Mac
4. **💾 Smaller footprint**: No lock files, uses pyproject.toml
5. **🦀 Rust-powered**: Built by Astral (makers of ruff)

## Breaking Changes

⚠️ **Users must install UV before installing dependencies:**

Old way:
```bash
pip install -r requirements.txt
```

New way:
```bash
# First time only: install UV
winget install --id=astral-sh.uv -e

# Then install project
uv pip install -e .
```

## CI/CD Changes

All GitHub Actions workflows now:
1. Install UV instead of Poetry
2. Use `uv pip install --system -e ".[dev]"`
3. Build with `python -m build` (via UV)
4. Publish with `twine` (installed via UV)

## Platform-Specific Behavior

**Windows:**
- Uses default asyncio event loop
- No uvloop installed (not compatible)

**Linux/Mac:**
- Automatically installs uvloop via environment markers
- Uses uvloop for better async performance
- Fallback to asyncio if uvloop import fails

## Files Modified

### Deleted
- requirements.txt
- requirements-dev.txt
- poetry.lock (if exists)

### Created
- UV_SETUP.md
- MIGRATION_TO_UV.md (this file)
- uv.toml (optional alternative config)

### Modified
- pyproject.toml (complete rewrite)
- README.md
- CLAUDE.md
- Makefile
- Dockerfile
- vercel.json
- docs/installation.md
- .github/workflows/*.yml (all workflows)

## Rollback Plan

If you need to rollback to pip/poetry:

1. Checkout the commit before migration
2. Restore requirements.txt files from git history
3. Revert pyproject.toml changes

```bash
git log --oneline  # Find commit before migration
git checkout <commit-hash> requirements.txt requirements-dev.txt
git checkout <commit-hash> pyproject.toml
```

## Support

For UV-related issues:
- [UV Documentation](https://github.com/astral-sh/uv)
- [UV Installation Guide](https://astral.sh/uv/)
- [Project Issues](https://github.com/ChistokhinSV/uml-mcp/issues)
