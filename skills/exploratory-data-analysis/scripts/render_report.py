# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow>=10"]
# ///
"""Render a report with headless Chrome or Edge and cut the page into readable crops.

CLI: uv run render_report.py REPORT.html [--browser PATH] [--out-dir DIR]

Captures the whole page at a fixed width, growing the window until the page ends in
background padding, then writes numbered crops covering the page from top to bottom.
Prints each crop's path; read every one. Exits 1 when no browser is found or the page
cannot be captured completely.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

WIDTH = 1280
FIRST_HEIGHT = 8_000
MAX_HEIGHT = 64_000
# The template's main element ends with 80px of bottom padding; a complete capture
# shows at least this much background below the last content.
BOTTOM_PADDING = 60
CROP_HEIGHT = 1_400
# Pixel difference from the page background that counts as content.
TOLERANCE = 8


def find_browser() -> str | None:
    """Chrome or Edge from the usual install locations, then the PATH."""
    candidates = []
    for root in (os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)"), os.environ.get("LOCALAPPDATA")):
        if root:
            candidates += [Path(root, "Google/Chrome/Application/chrome.exe"),
                           Path(root, "Microsoft/Edge/Application/msedge.exe")]
    candidates += [Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
                   Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge")]
    for path in candidates:
        if path.is_file():
            return str(path)
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "chrome", "msedge"):
        if found := shutil.which(name):
            return found
    return None


def capture(browser: str, report: Path, height: int, png: Path, profile: Path) -> Image.Image:
    png.unlink(missing_ok=True)
    subprocess.run(
        [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={profile}",
         f"--window-size={WIDTH},{height}", f"--screenshot={png}", report.as_uri()],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180, check=False,
    )
    if not png.is_file():
        raise RuntimeError(f"The browser wrote no screenshot at height {height}.")
    with Image.open(png) as image:
        return image.convert("RGB")


def content_bottom(image: Image.Image) -> int:
    """One past the last row that differs from the background at the bottom of the page."""
    background = Image.new("RGB", image.size, image.getpixel((image.width // 2, image.height - 1)))
    mask = ImageChops.difference(image, background).convert("L").point(lambda value: 255 if value > TOLERANCE else 0)
    box = mask.getbbox()
    return box[3] if box else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("report", help="The report's .html file")
    parser.add_argument("--browser", help="Path to a Chrome or Edge executable (default: search)")
    parser.add_argument("--out-dir", help="Directory for the crops (default: a new temporary directory)")
    args = parser.parse_args(argv)

    report = Path(args.report).resolve()
    if not report.is_file():
        parser.error(f"No report at {report}")
    browser = args.browser or find_browser()
    if not browser:
        print("No Chrome or Edge found; visual verification remains outstanding.", file=sys.stderr)
        return 1
    out_dir = Path(args.out_dir).resolve() if args.out_dir else Path(tempfile.mkdtemp(prefix="eda-render-"))
    out_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="eda-browser-") as profile:
        height = FIRST_HEIGHT
        while True:
            image = capture(browser, report, height, out_dir / "page.png", Path(profile))
            bottom = content_bottom(image)
            if height - bottom >= BOTTOM_PADDING:
                break
            if height >= MAX_HEIGHT:
                print(f"The page is taller than {MAX_HEIGHT}px; the capture is incomplete.", file=sys.stderr)
                return 1
            height = min(height * 2, MAX_HEIGHT)

    page_end = min(bottom + BOTTOM_PADDING, image.height)
    crops = []
    for number, top in enumerate(range(0, page_end, CROP_HEIGHT), start=1):
        path = out_dir / f"crop-{number:02d}.png"
        image.crop((0, top, WIDTH, min(top + CROP_HEIGHT, page_end))).save(path)
        crops.append(path)
    (out_dir / "page.png").unlink()
    print(f"Complete page captured: content ends at {bottom}px, followed by background padding.")
    for path in crops:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
