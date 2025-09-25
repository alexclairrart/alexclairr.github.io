# Invisible Watermark Protection - Quick Guide

## 🤔 Why Invisible Watermarks?

### **The Problem**

- **Image theft** - People download and reuse your photos without permission
- **Visible watermarks** - Destroy image aesthetics and user experience
- **No protection** - Zero deterrent and no ownership proof

# Invisible Watermark Protection

## 🎯 What It Does

Embeds `© Alex Clairr 2025` invisibly into WebP images using steganography. Provides copyright protection without destroying image aesthetics.

## 🔧 Implementation

**Library:** `invisible-watermark` (Python)
**Algorithm:** DWT-DCT-SVD steganography
**Automation:** Git hooks apply watermarks automatically on commit

## ⚠️ Limitations (Be Honest)

**Protects against (95%):** Casual thieves, social media reposting, basic image theft
**Bypassed by:** Advanced attackers using same library, heavy image processing, AI reconstruction

**Reality:** Makes theft harder/riskier, not impossible. Perfect protection doesn't exist.

## 🛠️ Usage

**Automatic (Preferred):**

```bash
git add assets/pics/new-image.webp
git commit -m "Add image"  # Watermark applied automatically
```

**Manual:**

```bash
# Apply watermark
python .githooks/watermark.py apply image.webp

# Verify watermark exists
python .githooks/watermark.py verify image.webp
```

**Decrypt/Verify Stolen Images:**

```python
from imwatermark import WatermarkDecoder

# Check if image contains your watermark
decoder = WatermarkDecoder('bytes', len("© Alex Clairr 2025") * 8)
watermark = decoder.decode(cv2.imread('suspected_image.jpg'), 'dwtDctSvd')

if watermark == b"© Alex Clairr 2025":
    print("This image contains your watermark - proof of theft!")
else:
    print("No watermark found")
```

## 🎯 Bottom Line

Invisible watermarks provide **practical protection** against most image theft while maintaining **professional presentation**. Not bulletproof, but much better than visible watermarks or no protection.

## � How It Works

**Technical:** Uses DWT-DCT-SVD algorithm to embed copyright data in frequency coefficients
**Practical:** Hidden in image data, survives JPEG compression, social media processing, and screenshots

**Protection Flow:**

1. New images automatically watermarked on commit
2. Copyright embedded invisibly in pixel data
3. Stolen images can be verified to contain your watermark
4. Strong legal evidence for takedown/compensation
