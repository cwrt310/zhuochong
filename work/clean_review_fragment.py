"""Remove the neighboring pose sliver in Xiaoba's review frame 1."""

from pathlib import Path
import sys

from PIL import Image


def clean(source: Path, destination: Path) -> None:
    with Image.open(source) as opened:
        atlas = opened.convert("RGBA")
    if atlas.size != (1536, 2288):
        raise ValueError(f"Unexpected atlas dimensions: {atlas.size}")

    left, top = 192, 8 * 208
    for y in range(117, 156):
        for x in range(29, 38):
            atlas.putpixel((left + x, top + y), (0, 0, 0, 0))

    destination.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(destination, format="WEBP", lossless=True, quality=100, method=6, exact=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python clean_review_fragment.py ATLAS OUTPUT_WEBP")
    clean(Path(sys.argv[1]), Path(sys.argv[2]))
