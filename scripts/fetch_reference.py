#!/usr/bin/env python3
"""Download a reference image from a URL (direct image, Pinterest/Dribbble/
Behance/blog page via og:image, etc.).

Usage:
  python fetch_reference.py <url> [--out DIR]

Strategy:
  1. If the URL returns image bytes, save directly.
  2. Otherwise parse the HTML for og:image / twitter:image / image_src /
     largest <img>, resolve relative URLs, download that.

Some sites (Pinterest walls, Dribbble behind CDN checks) block scripts.
If this fails, ask the user to save the image manually and pass the file path.

Requires: Pillow (validation), stdlib urllib.
"""
from __future__ import annotations

import argparse
import hashlib
import imghdr  # noqa: DEP051 - stdlib, fine for a helper script
import os
import re
import sys
import urllib.request

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".avif"}


def fetch(url: str, timeout: int = 30) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Content-Type", "")


def find_image_url(page_url: str, html: str) -> str | None:
    candidates: list[str] = []
    for pattern in (
        r'<meta[^>]+property=["\']og:image(?::secure_url)?["\'][^>]+content=["\']([^"\']+)',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
        r'<meta[^>]+name=["\']twitter:image(?::src)?["\'][^>]+content=["\']([^"\']+)',
        r'<link[^>]+rel=["\']image_src["\'][^>]+href=["\']([^"\']+)',
    ):
        candidates += re.findall(pattern, html, re.I)
    if not candidates:
        candidates = re.findall(r"<img[^>]+src=[\"']([^\"']+)[\"']", html, re.I)
    for c in candidates:
        url = c.replace("&amp;", "&")
        if url.startswith("//"):
            url = "https:" + url
        elif url.startswith("/"):
            m = re.match(r"(https?://[^/]+)", page_url)
            url = m.group(1) + url if m else None
        if url and url.lower().startswith("http"):
            return url
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--out", default="reference", help="output directory (default ./reference)")
    args = ap.parse_args()

    url = args.url
    try:
        data, ctype = fetch(url)
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: fetch failed: {e}", file=sys.stderr)
        sys.exit(1)

    looks_image = ctype.startswith("image/") or os.path.splitext(url.split("?")[0])[1].lower() in EXTS
    if not looks_image:
        try:
            html = data.decode("utf-8", "ignore")
        except Exception:  # noqa: BLE001
            html = ""
        found = find_image_url(url, html)
        if not found:
            print("ERROR: no image found in page (og:image / <img>). Save the image manually.", file=sys.stderr)
            sys.exit(2)
        url, data, ctype = found, *fetch(found)

    kind = imghdr.what(None, h=data)
    if kind is None and not looks_image:
        print("ERROR: downloaded file is not an image.", file=sys.stderr)
        sys.exit(3)

    os.makedirs(args.out, exist_ok=True)
    ext = "." + (kind or "png")
    if kind == "jpeg":
        ext = ".jpg"
    name = hashlib.sha1(url.encode()).hexdigest()[:12] + ext
    path = os.path.join(args.out, name)
    with open(path, "wb") as f:
        f.write(data)

    dims = ""
    try:
        from PIL import Image

        with Image.open(path) as im:
            dims = f"{im.width}x{im.height}"
    except Exception:  # noqa: BLE001
        pass

    print(path + ("\t" + dims if dims else ""))


if __name__ == "__main__":
    main()
