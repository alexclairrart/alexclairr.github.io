# Image Validation System Documentation

This repository uses a comprehensive multi-layer image validation system to ensure all artwork is properly protected and free from sensitive metadata before publication.

## 🎯 Overview

The system provides **three layers of protection**:

1. **Pre-commit hooks** - Local validation before commits
2. **GitHub Actions** - Remote validation before deployment
3. **Local testing** - Test GitHub workflows locally

## 🏗️ System Architecture

```
Developer Workflow:
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Local Work    │───▶│   Pre-commit     │───▶│   GitHub Actions    │
│                 │    │   Validation     │    │   Validation        │
│ • Add images    │    │ • EXIF cleanup   │    │ • EXIF verification │
│ • Modify files  │    │ • Watermarking   │    │ • Watermark check   │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                              │                           │
                              ▼                           ▼
                       ✅ Commit allowed         ✅ Deployment allowed
                       ❌ Commit blocked         ❌ Deployment blocked
```

## 📋 Components

### 1. Pre-commit Hook (`.githooks/pre-commit`)

**What it does:**

- Automatically processes new/modified images during commits
- Applies invisible watermarks to protect artwork
- Strips sensitive EXIF metadata (GPS, camera info, dates)
- Adds copyright information to EXIF data

**Key features:**

- Converts JPEG to PNG to preserve watermarks
- Validates ALL images in repository for compliance
- Skips specific files (e.g., `assets/pics/lelem.png`)
- Blocks commits if validation fails

**Dependencies:**

- Python 3 with `invisible-watermark` and `opencv-python`
- `exiftool` for metadata management

### 2. GitHub Actions Workflows

#### 🔍 EXIF Guard (`.github/workflows/exif-guard.yml`)

**Triggers:** Push to main, Pull requests
**Purpose:** Verify no images contain sensitive metadata

**What it checks:**

- GPS coordinates
- Camera make/model/serial numbers
- Technical shooting data (ISO, exposure, focal length)
- Software/processing information
- User comments and descriptions
- Timestamps and modification dates

**Allowed metadata:**

- Basic file format information
- Image dimensions and color profiles
- Copyright fields (Artist, Creator, Copyright)

#### 🖼️ Watermark Check (`.github/workflows/check-watermark.yml`)

**Triggers:** Push to main, Pull requests
**Purpose:** Ensure all images have invisible watermarks

**What it does:**

- Scans all images for invisible watermark presence
- Uses the same watermarking script as pre-commit hook
- Respects skip lists for excluded files
- Fails if any image is missing a watermark

### 3. Local Testing Script (`test-github-workflows.sh`)

**Purpose:** Test GitHub Actions workflows locally before pushing

**Usage:**

```bash
# Interactive mode
./test-github-workflows.sh

# Test specific workflows
./test-github-workflows.sh 1   # EXIF only
./test-github-workflows.sh 2   # Watermark only
./test-github-workflows.sh 3   # Both workflows
```

**Requirements:**

- Docker installed and running
- `act` tool: `brew install act`

## 🔧 Setup Instructions

### Initial Setup

1. **Install dependencies:**

   ```bash
   # Python dependencies
   pip install -r requirements.txt

   # System tools
   brew install exiftool act
   ```

2. **Configure Git hooks:**

   ```bash
   git config core.hooksPath .githooks
   chmod +x .githooks/pre-commit
   ```

3. **Make test scripts executable:**
   ```bash
   chmod +x test-github-workflows.sh
   chmod +x test-*.sh
   ```

### Workflow Integration

The system is designed to work seamlessly:

1. **Developer adds/modifies images** → Pre-commit automatically processes them
2. **Developer pushes changes** → GitHub Actions verify compliance
3. **All checks pass** → Changes are deployed
4. **Any check fails** → Deployment is blocked until fixed

## 🛠️ Usage

### Adding New Images

When you add new images to the repository:

1. **Add the image file normally:**

   ```bash
   git add assets/pics/new-artwork.jpg
   ```

2. **Commit triggers pre-commit processing:**

   ```bash
   git commit -m "Add new artwork"
   # Pre-commit automatically:
   # - Applies invisible watermark
   # - Converts JPEG to PNG if needed
   # - Strips sensitive EXIF data
   # - Adds copyright information
   # - Re-stages processed files
   ```

3. **Push triggers GitHub validation:**
   ```bash
   git push
   # GitHub Actions verify:
   # - No sensitive metadata present
   # - All images have watermarks
   ```

### Testing Locally

Before pushing, you can test the exact GitHub workflows:

```bash
# Test both workflows (recommended)
./test-github-workflows.sh 3

# Or test individually
./test-exif-local.sh      # Simple EXIF check
./test-watermark-local.sh # Simple watermark check
```

## 🔒 Security Features

### Watermark Protection

- **Invisible watermarks** using steganography
- **Copyright text:** `© Alex Clairr 2025` embedded in image data
- **Format conversion:** JPEG → PNG to preserve watermarks
- **Verification:** All images checked for watermark presence

### EXIF Privacy Protection

- **Strips sensitive data:** GPS, camera info, timestamps
- **Preserves copyright:** Artist, Creator, Copyright fields maintained
- **Comprehensive scanning:** Checks all tracked images
- **Skip list support:** Excludes specific files when needed

### Multi-layer Validation

- **Pre-commit:** Prevents bad commits locally
- **GitHub Actions:** Prevents bad deployments remotely
- **Consistent logic:** Same validation rules across all layers

## 📁 File Structure

```
alexclairr.github.io/
├── .github/workflows/
│   ├── exif-guard.yml           # EXIF validation workflow
│   └── check-watermark.yml      # Watermark validation workflow
├── .githooks/
│   ├── pre-commit              # Main pre-commit hook
│   └── watermark.py            # Watermarking script
├── assets/pics/                 # Image gallery
│   ├── 001.jpg → 001.png       # Auto-converted by pre-commit
│   ├── 002.png                 # Processed images
│   └── lelem.png               # Skip-listed file
├── docu/
│   └── image-validation.md     # This documentation
├── requirements.txt            # Python dependencies
├── test-github-workflows.sh    # Local GitHub Actions testing
├── test-exif-local.sh         # Simple EXIF test
└── test-watermark-local.sh    # Simple watermark test
```

## 🚨 Troubleshooting

### Common Issues

**Pre-commit fails:**

```bash
# Check Python dependencies
pip install -r requirements.txt

# Verify exiftool installation
brew install exiftool

# Check hook permissions
chmod +x .githooks/pre-commit
```

**GitHub Actions fail:**

- Check the Actions tab in your GitHub repository
- Verify all images pass local tests first
- Ensure no sensitive metadata was accidentally introduced

**Local testing issues:**

```bash
# Install act if missing
brew install act

# Check Docker is running
docker ps

# Use correct architecture for M1 Macs
act --container-architecture linux/amd64
```

### Skip Lists

To exclude specific files from validation, update the skip lists:

**Pre-commit hook:** Edit `SKIP_FILES` in `.githooks/watermark.py`
**GitHub workflows:** Edit the skip conditions in workflow YAML files

Example:

```bash
if [ "$f" = "assets/pics/lelem.png" ]; then
    echo "⏭ Skipping EXIF check for: $f"
    continue
fi
```

## 🔄 Maintenance

### Regular Tasks

1. **Update dependencies** periodically:

   ```bash
   pip install -r requirements.txt --upgrade
   brew upgrade exiftool act
   ```

2. **Test workflows** before major releases:

   ```bash
   ./test-github-workflows.sh 3
   ```

3. **Monitor GitHub Actions** for any failures and address promptly

### Adding New Image Formats

To support additional image formats:

1. Update the file pattern in all validation scripts:

   ```bash
   # Change this pattern:
   grep -Ei '\.(jpe?g|png|webp)$'

   # To include new formats:
   grep -Ei '\.(jpe?g|png|webp|avif|tiff)$'
   ```

2. Test with the new format to ensure compatibility

## 📊 Validation Results

When everything works correctly, you'll see output like:

**Pre-commit:**

```
✓ Watermark applied: assets/pics/new-image.jpg
🔄 Converted to PNG: assets/pics/new-image.png
✓ EXIF processed and re-staged: assets/pics/new-image.png
```

**GitHub Actions:**

```
✓ EXIF verified: assets/pics/001.png
✓ EXIF verified: assets/pics/002.png
⏭ Skipping EXIF check for: assets/pics/lelem.png
✓ Watermark verified: assets/pics/001.png
✓ Watermark verified: assets/pics/002.png
```

This comprehensive system ensures your artwork is always protected and compliant! 🎨✨
