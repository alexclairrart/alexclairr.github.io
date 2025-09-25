#!/usr/bin/env python3
"""
Image to WebP Converter (Lossless Only)

This script converts all JPG and PNG images in the assets/pics/ directory
to lossless WebP format while preserving the original files.

Features:
- Converts JPG and PNG images to lossless WebP format
- No quality loss - identical to original image quality
- Preserves original images (creates .webp alongside originals)
- Provides compression statistics
- Handles errors gracefully

Usage:
    python scripts/convert_to_webp.py [--overwrite] [--input-dir DIR]

Options:
    --overwrite         Overwrite existing WebP files
    --input-dir DIR     Input directory (default: assets/pics)
"""

import os
import argparse
from pathlib import Path
from PIL import Image
import sys


def convert_image_to_webp(input_path, output_path):
    """
    Convert an image to lossless WebP format.

    Args:
        input_path (Path): Path to the input image
        output_path (Path): Path to the output WebP file

    Returns:
        tuple: (success: bool, original_size: int, webp_size: int, error: str)
    """
    try:
        # Open and convert image
        with Image.open(input_path) as img:
            # WebP lossless supports RGB and RGBA
            if img.mode in ("RGBA", "LA", "P"):
                if img.mode == "P":
                    img = img.convert("RGBA")
                # Keep RGBA for lossless
            elif img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")

            # Save as lossless WebP
            img.save(output_path, "WebP", lossless=True, quality=100, optimize=True)

        # Get file sizes for comparison
        original_size = input_path.stat().st_size
        webp_size = output_path.stat().st_size

        return True, original_size, webp_size, None

    except Exception as e:
        return False, 0, 0, str(e)


def format_bytes(bytes_value):
    """Convert bytes to human readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} TB"


def main():
    parser = argparse.ArgumentParser(
        description="Convert images to lossless WebP format"
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing WebP files"
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        default="assets/pics",
        help="Input directory (default: assets/pics)",
    )

    args = parser.parse_args()

    # Define paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    input_dir = project_root / args.input_dir

    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' does not exist")
        return 1

    # Supported image formats
    supported_formats = {".jpg", ".jpeg", ".png"}

    # Find all images
    image_files = []
    for ext in supported_formats:
        image_files.extend(input_dir.glob(f"*{ext}"))
        image_files.extend(input_dir.glob(f"*{ext.upper()}"))

    if not image_files:
        print(f"No supported image files found in '{input_dir}'")
        print(f"Supported formats: {', '.join(supported_formats)}")
        return 0

    print(f"Found {len(image_files)} image(s) to convert")
    print("Compression mode: Lossless (no quality loss)")
    print(f"Input directory: {input_dir}")
    print("-" * 60)

    # Conversion statistics
    converted_count = 0
    skipped_count = 0
    error_count = 0
    total_original_size = 0
    total_webp_size = 0

    # Convert each image
    for img_path in sorted(image_files):
        webp_path = img_path.with_suffix(".webp")

        # Check if WebP already exists
        if webp_path.exists() and not args.overwrite:
            print(f"SKIP: {img_path.name} -> WebP already exists")
            skipped_count += 1
            continue

        print(f"Converting: {img_path.name} -> {webp_path.name}")

        success, orig_size, webp_size, error = convert_image_to_webp(
            img_path, webp_path
        )

        if success:
            converted_count += 1
            total_original_size += orig_size
            total_webp_size += webp_size

            compression_ratio = (1 - webp_size / orig_size) * 100
            print(
                f"  ✓ {format_bytes(orig_size)} -> {format_bytes(webp_size)} "
                f"({compression_ratio:.1f}% smaller)"
            )
        else:
            error_count += 1
            print(f"  ✗ Error: {error}")

    # Print summary
    print("-" * 60)
    print("CONVERSION SUMMARY:")
    print(f"  Converted: {converted_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Errors: {error_count}")

    if total_original_size > 0:
        total_savings = (1 - total_webp_size / total_original_size) * 100
        print(f"  Original total size: {format_bytes(total_original_size)}")
        print(f"  WebP total size: {format_bytes(total_webp_size)}")
        print(
            f"  Total space saved: {format_bytes(total_original_size - total_webp_size)} "
            f"({total_savings:.1f}%)"
        )

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
