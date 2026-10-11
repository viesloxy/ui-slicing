#!/usr/bin/env python3
"""Analyze and slice a UI reference image.

Usage:
  python slice_reference.py <image> [--outdir DIR] [--bands] [--grid N]
                            [--crop x,y,w,h] [--out FILE] [--zoom Z]
                            [--colors N] [--threshold T]

Analyzes the image (dimensions, dominant palette, section boundaries) and
prints a JSON report to stdout. Optionally saves crops for close inspection:
  --bands        one crop per detected section (recommended first step)
  --grid N       N equal horizontal slices instead
  --crop x,y,w,h manual crop at ORIGINAL pixel coordinates (+ --out, --zoom)

Requires: Pillow
"""
from __future__ import annotations

import argparse
import json
import os
import sys


def hexc(rgb) -> str:
    return "#%02X%02X%02X" % tuple(rgb[:3])


def get_palette(img, n: int):
    im = img.convert("RGB")
    w = 200
    h = max(1, round(w * im.height / im.width))
    small = im.resize((w, h))
    q = small.quantize(colors=n)
    pal = q.getpalette() or []
    total = w * h
    counts = sorted(q.getcolors(total) or [], reverse=True)
    out = []
    for cnt, idx in counts[:n]:
        rgb = tuple(pal[idx * 3 : idx * 3 + 3])
        out.append({"hex": hexc(rgb), "pct": round(100 * cnt / total, 1)})
    return out


def detect_sections(img, threshold: float):
    """Detect horizontal section boundaries via per-row mean-color deltas."""
    im = img.convert("RGB")
    w = 100
    h = max(2, round(w * im.height / im.width))
    small = im.resize((w, h))
    px = small.load()
    rows = []
    for y in range(h):
        r = g = b = 0
        for x in range(w):
            p = px[x, y]
            r += p[0]
            g += p[1]
            b += p[2]
        rows.append((r / w, g / w, b / w))

    cuts = [0]
    for y in range(1, h):
        d = sum(abs(rows[y][i] - rows[y - 1][i]) for i in range(3))
        if d >= threshold and y - cuts[-1] > 2:
            cuts.append(y)
    if cuts[-1] != h:
        cuts.append(h)

    scale = im.height / h
    bands = []
    for i in range(len(cuts) - 1):
        y0, y1 = round(cuts[i] * scale), round(cuts[i + 1] * scale)
        if y1 - y0 < 4:
            continue
        bands.append({"index": len(bands), "y0": y0, "y1": y1, "height": y1 - y0})
    return bands


def save_crop(img, box, path, zoom: float):
    crop = img.convert("RGB").crop(box)
    if zoom and zoom != 1.0:
        crop = crop.resize((round(crop.width * zoom), round(crop.height * zoom)))
    crop.save(path)
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image")
    ap.add_argument("--outdir", default="slices", help="output directory for crops")
    ap.add_argument("--bands", action="store_true", help="save one crop per detected section")
    ap.add_argument("--grid", type=int, metavar="N", help="save N equal horizontal slices")
    ap.add_argument("--crop", metavar="x,y,w,h", help="manual crop (original px coords)")
    ap.add_argument("--out", default=None, help="output filename for --crop")
    ap.add_argument("--zoom", type=float, default=2.0, help="zoom factor for saved crops (default 2)")
    ap.add_argument("--colors", type=int, default=10, help="palette size (default 10)")
    ap.add_argument("--threshold", type=float, default=12.0, help="section detection sensitivity (default 12; lower = more sections)")
    args = ap.parse_args()

    try:
        from PIL import Image

        Image.MAX_IMAGE_PIXELS = None
    except ImportError:
        print(json.dumps({"error": "Pillow not installed. Run: pip install Pillow"}))
        sys.exit(1)

    try:
        img = Image.open(args.image)
        img.load()
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"error": f"cannot open image: {e}"}))
        sys.exit(1)

    report = {
        "image": os.path.abspath(args.image),
        "width": img.width,
        "height": img.height,
        "aspect": round(img.width / img.height, 3),
        "likely_dpr": 2 if (img.width >= 2000 and img.height >= 2000) else 1,
        "palette": get_palette(img, args.colors),
        "sections": detect_sections(img, args.threshold),
    }

    saved = []
    os.makedirs(args.outdir, exist_ok=True)

    if args.bands:
        for band in report["sections"]:
            name = f"band{band['index']:02d}_y{band['y0']}-{band['y1']}.png"
            path = os.path.join(args.outdir, name)
            zoom = args.zoom if img.width < 1600 * args.zoom else 1.0
            save_crop(img, (0, band["y0"], img.width, band["y1"]), path, zoom)
            band["crop"] = path
            saved.append(path)

    if args.grid:
        step = img.height // args.grid
        for i in range(args.grid):
            y0, y1 = i * step, (img.height if i == args.grid - 1 else (i + 1) * step)
            path = os.path.join(args.outdir, f"grid{i:02d}_y{y0}-{y1}.png")
            save_crop(img, (0, y0, img.width, y1), path, args.zoom)
            saved.append(path)

    if args.crop:
        try:
            x, y, w, h = (int(v) for v in args.crop.split(","))
        except ValueError:
            print(json.dumps({"error": "--crop must be x,y,w,h integers"}))
            sys.exit(1)
        path = args.out or os.path.join(args.outdir, f"crop_{x}_{y}_{w}x{h}.png")
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        save_crop(img, (x, y, x + w, y + h), path, args.zoom)
        saved.append(path)

    report["saved_crops"] = saved
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
