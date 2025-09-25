# Image Validation System - Developer Guide

WebP-only photography portfolio with automated image protection and validation.

## 🚀 Quick Start (Developer Workflow)

### 1. Add Images (Any Format)

Drop your images into `assets/pics/` - JPG, PNG, whatever format:

```bash
cp ~/my-photos/*.jpg assets/pics/
```

### 2. Convert to WebP (Lossless)

Run the conversion script to get lossless WebP files:

```bash
python scripts/convert_to_webp.py --overwrite
```

### 3. Commit Changes

Git hooks handle watermarking, EXIF cleanup, and validation automatically:

```bash
git add .
git commit -m "Add new photography"
```

That's it! The system handles protection and validation automatically.

## ⚙️ Environment Setup

### Dependencies

Install required packages:

```bash
# Python packages
pip install -r requirements.txt

# System tools (macOS)
brew install exiftool

# System tools (Ubuntu/GitHub Actions)
sudo apt-get install exiftool
```

### Git Hooks Setup

```bash
# Enable git hooks
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit
```

### Local Testing Setup (Optional)

To test GitHub workflows locally before pushing:

```bash
# Install act (runs GitHub Actions locally)
brew install act

# Install Docker (required by act)
# Download from https://www.docker.com/products/docker-desktop/
# Or install via brew: brew install --cask docker

# Make test script executable
chmod +x scripts/test-github-workflows.sh
```

## 🔧 How It Works

### Pre-commit Hook (Automatic)

When you `git commit`, the hook automatically:

1. **Watermarks** new WebP images with invisible copyright
2. **Strips** sensitive EXIF data (GPS, camera info, dates)
3. **Adds** copyright info to remaining EXIF data
4. **Validates** image format compliance (WebP + ICO only)
5. **Increments** version number

### GitHub Workflows (Automatic)

#### `webp-exif-guard` - EXIF Validation

- Scans all WebP files for sensitive metadata
- Ensures no GPS, camera, or personal data leaked
- Runs on every push/PR

#### `check-webp-watermark` - Watermark Validation

- Verifies all WebP images contain invisible watermarks
- Protects against unauthorized image usage
- Runs on every push/PR

## 🧪 Testing

### Local Workflow Testing

Test GitHub Actions locally before pushing (requires Docker + act setup):

```bash
# Test both workflows multiple times to catch edge cases
./scripts/test-github-workflows.sh 3

# What this does:
# - Runs webp-exif-guard workflow locally using Docker
# - Runs check-webp-watermark workflow locally using Docker
# - Repeats 3 times to catch intermittent issues
# - Uses same Ubuntu environment as GitHub Actions
# - Validates your changes before pushing to GitHub
```

**First time setup requirements:**

1. Docker Desktop must be running
2. `act` tool installed (`brew install act`)
3. Script permissions set (`chmod +x scripts/test-github-workflows.sh`)

**Troubleshooting local tests:**

```bash
# If act fails on M1 Macs, specify architecture:
act --container-architecture linux/amd64

# Check Docker is running:
docker ps
```

### Manual Validation

```bash
# Check watermarks manually
python .githooks/watermark.py verify assets/pics/*.webp

# Check EXIF manually
exiftool assets/pics/*.webp
```

## 🚨 Troubleshooting

### Pre-commit Failures

```bash
# Convert images first
python scripts/convert_to_webp.py --overwrite

# Remove non-WebP files from assets
find assets -name "*.jpg" -o -name "*.png" | xargs rm

# Try commit again
git add . && git commit -m "Your message"
```

### Watermark Issues

```bash
# Re-apply watermarks
python .githooks/watermark.py apply assets/pics/*.webp
```

### EXIF Issues

```bash
# Strip all EXIF and re-add copyright
exiftool -all= -Artist="Alex Clairr" -Copyright="© 2025 Alex Clairr" assets/pics/*.webp
```

## 📁 File Structure

```
├── assets/pics/           # WebP images only
├── scripts/
│   ├── convert_to_webp.py # Lossless conversion script
│   └── test-github-workflows.sh
├── .githooks/
│   ├── pre-commit         # Main validation hook
│   └── watermark.py       # Watermarking script
└── .github/workflows/
    ├── webp-exif-guard.yml
    └── check-webp-watermark.yml
```

This system ensures your photography is always protected and web-optimized! 🎨
