"""Render a compact overview of Xiaoba's nine animation rows."""

from pathlib import Path
import sys

from PIL import Image, ImageDraw


ROWS = (
    ("idle", 6),
    ("running-right", 8),
    ("running-left", 8),
    ("waving", 4),
    ("jumping", 5),
    ("failed", 8),
    ("waiting", 6),
    ("running", 6),
    ("review", 6),
)
CELL_WIDTH, CELL_HEIGHT = 192, 208
PREVIEW_WIDTH, PREVIEW_HEIGHT = 96, 104
HEADER_HEIGHT = 22


def render(atlas_path: Path, output_path: Path) -> None:
    with Image.open(atlas_path) as source:
        atlas = source.convert("RGBA")
    if atlas.size != (1536, 2288):
        raise ValueError(f"Unexpected atlas dimensions: {atlas.size}")

    row_height = HEADER_HEIGHT + PREVIEW_HEIGHT
    sheet = Image.new("RGB", (8 * PREVIEW_WIDTH, len(ROWS) * row_height), "#080d13")
    draw = ImageDraw.Draw(sheet)
    for row, (state, frame_count) in enumerate(ROWS):
        top = row * row_height
        draw.text((4, top + 3), f"row {row}: {state}", fill="white")
        draw.text((8 * PREVIEW_WIDTH - 62, top + 3), f"{frame_count} frames", fill="white")
        for column in range(8):
            left = column * PREVIEW_WIDTH
            preview_top = top + HEADER_HEIGHT
            for y in range(0, PREVIEW_HEIGHT, 12):
                for x in range(0, PREVIEW_WIDTH, 12):
                    shade = "#ffffff" if ((x + y) // 12) % 2 == 0 else "#e8e8e8"
                    draw.rectangle(
                        (left + x, preview_top + y, left + min(x + 11, 95), preview_top + min(y + 11, 103)),
                        fill=shade,
                    )
            if column < frame_count:
                frame = atlas.crop(
                    (
                        column * CELL_WIDTH,
                        row * CELL_HEIGHT,
                        (column + 1) * CELL_WIDTH,
                        (row + 1) * CELL_HEIGHT,
                    )
                ).resize((PREVIEW_WIDTH, PREVIEW_HEIGHT), Image.Resampling.LANCZOS)
                sheet.paste(frame, (left, preview_top), frame)
            outline = "#51b778" if column < frame_count else "#d97878"
            draw.rectangle((left, preview_top, left + 95, preview_top + 103), outline=outline)
            draw.text((left + 4, preview_top + 2), str(column), fill="black")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python render_xiaoba_contact.py ATLAS OUTPUT")
    render(Path(sys.argv[1]), Path(sys.argv[2]))
