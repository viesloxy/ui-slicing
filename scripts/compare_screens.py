#!/usr/bin/env python3
"""Compare a rebuilt page screenshot against the reference image.

Usage:
  python compare_screens.py <reference.png> <output.png> [--outdir DIR] [--bands N]

Produces:
  side.png   reference (left) and output (right) side by side, height-normalized
  diff.png   absolute-pixel difference heatmap
Prints a table of mean difference per horizontal band so the worst sections
can be fixed first.

Requires: Pillow
"""
from __future__ import annotations

import argparse
import json
import os
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("reference")
    ap.add_argument("output")
    ap.add_argument("--outdir", default="compare")
    ap.add_argument("--bands", type=int, default=10, help="number of horizontal bands to score (default 10)")
    args = ap.parse_args()

    try:
        from PIL import Image, ImageChops

        Image.MAX_IMAGE_PIXELS = None
    except ImportError:
        print(json.dumps({"error": "Pillow not installed. Run: pip install Pillow"}))
        sys.exit(1)

    ref = Image.open(args.reference).convert("RGB")
    out = Image.open(args.output).convert("RGB")

    os.makedirs(args.outdir, exist_ok=True)

    # --- side-by-side, height-normalized ---
    H = 1200
    def scaled(im):
        w = max(1, round(im.width * H / im.height))
        return im.resize((w, H))

    rs, os_ = scaled(ref), scaled(out)
    side = Image.new("RGB", (rs.width + os_.width + 24, H), (40, 40, 40))
    side.paste(rs, (0, 0))
    side.paste(os_, (rs.width + 24, 0))
    side_path = os.path.join(args.outdir, "side.png")
    side.save(side_path)

    # --- diff heatmap + per-band score (output resized to reference dims) ---
    out_r = out.resize(ref.size)
    diff = ImageChops.difference(ref, out_r).convert("L")
    diff_path = os.path.join(args.outdir, "diff.png")
    diff.save(diff_path)

    px = diff.load()
    W, Hh = diff.size
    band_h = Hh // args.bands
    scores = []
    for i in range(args.bands):
        y0, y1 = i * band_h, (Hh if i == args.bands - 1 else (i + 1) * band_h)
        total = n = 0
        for y in range(y0, y1, 2):  # sample every 2px for speed
            for x in range(0, W, 2):
                total += px[x, y]
                n += 1
        scores.append({"band": i, "y0": y0, "y1": y1, "mean_diff": round(total / n, 1)})

    overall = round(sum(s["mean_diff"] for s in scores) / len(scores), 1)
    print(json.dumps(
        {
            "side_by_side": os.path.abspath(side_path),
            "diff_heatmap": os.path.abspath(diff_path),
            "overall_mean_diff": overall,
            "note": "0 = identical, 255 = completely different. Fix highest bands first.",
            "bands": scores,
        },
        indent=2,
    ))


if __name__ == "__main__":
    main()
