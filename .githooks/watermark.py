#!/usr/bin/env python3
"""
Invisible watermarking script for Alex Clairr photography portfolio
Handles watermarking and verification of images
"""

import cv2
import sys
import os
from pathlib import Path
from imwatermark import WatermarkEncoder, WatermarkDecoder

WATERMARK_TEXT = b"\xc2\xa9 Alex Clairr 2025"  # © Alex Clairr 2025 in UTF-8
ALGORITHM = "dwtDctSvd"

# Images to skip from watermarking and verification
SKIP_FILES = {"assets/pics/lelem.png"}


class ImageWatermarker:
    def __init__(self):
        self.encoder = WatermarkEncoder()
        self.encoder.set_watermark("bytes", WATERMARK_TEXT)
        self.decoder = WatermarkDecoder("bytes", len(WATERMARK_TEXT) * 8)

    def apply_watermark(self, image_path):
        """Apply invisible watermark to an image"""
        # Check if file should be skipped
        if str(image_path) in SKIP_FILES:
            return True, f"Skipped (in skip list): {image_path}"

        # First check if watermark already exists (skip the skip-file check)
        has_watermark, _ = self.verify_watermark(image_path, skip_check=False)
        if has_watermark:
            return True, f"Already watermarked: {image_path}"

        try:
            img = cv2.imread(str(image_path))
            if img is None:
                return False, f"Could not read image: {image_path}"

            # Apply watermark
            watermarked = self.encoder.encode(img, ALGORITHM)

            # Convert JPEG to PNG to preserve watermark (JPEG compression destroys it)
            if str(image_path).lower().endswith((".jpg", ".jpeg")):
                # Convert to PNG
                png_path = str(image_path).rsplit(".", 1)[0] + ".png"
                success = cv2.imwrite(png_path, watermarked)
                if success:
                    # Remove original JPEG
                    os.remove(image_path)
                    return True, f"Converted to PNG and watermarked: {png_path}"
            else:
                success = cv2.imwrite(str(image_path), watermarked)

            return success, None
        except Exception as e:
            return False, str(e)

    def verify_watermark(self, image_path, skip_check=True):
        """Check if image contains the watermark"""
        # Check if file should be skipped (unless called internally)
        if skip_check and str(image_path) in SKIP_FILES:
            return True, f"Skipped (in skip list): {image_path}"

        try:
            img = cv2.imread(str(image_path))
            if img is None:
                return False, f"Could not read image: {image_path}"

            # Try to decode watermark
            decoded = self.decoder.decode(img, ALGORITHM)

            # Check if it matches our expected watermark
            return decoded == WATERMARK_TEXT, None
        except Exception as e:
            return False, str(e)


def main():
    if len(sys.argv) < 2:
        print("Usage: python watermark.py <command> [file1] [file2] ...")
        print("Commands:")
        print("  apply <files...>   - Apply watermark to files")
        print("  verify <files...>  - Verify watermark exists in files")
        sys.exit(1)

    command = sys.argv[1]
    files = sys.argv[2:]

    watermarker = ImageWatermarker()

    if command == "apply":
        for file_path in files:
            success, message = watermarker.apply_watermark(file_path)
            if success:
                if "Skipped" in str(message):
                    print(f"⏭ {message}")
                elif "Already watermarked" in str(message):
                    print(f"✓ {message}")
                elif "Converted to PNG" in str(message):
                    print(f"🔄 {message}")
                else:
                    print(f"✓ Watermarked: {file_path}")
            else:
                print(f"✗ Failed to watermark {file_path}: {message}")
                sys.exit(1)

    elif command == "verify":
        all_good = True
        for file_path in files:
            has_watermark, message = watermarker.verify_watermark(file_path)
            if has_watermark:
                if "Skipped" in str(message):
                    print(f"⏭ {message}")
                else:
                    print(f"✓ Watermark verified: {file_path}")
            else:
                print(f"✗ Missing watermark: {file_path}")
                if message:
                    print(f"  Error: {message}")
                all_good = False

        if not all_good:
            sys.exit(1)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
