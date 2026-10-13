from pathlib import Path
from PIL import Image, ImageOps

source = Path("images")
destination = Path("images_compressed")
destination.mkdir(exist_ok=True)

for path in source.iterdir():
    if path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        continue

    with Image.open(path) as original:
        image = ImageOps.exif_transpose(original)
        image.thumbnail((2000, 2000), Image.Resampling.LANCZOS)

        # JPEG doesn't support transparency.
        if image.mode == "RGBA":
            background = Image.new("RGB", image.size, "white")
            background.paste(image, mask=image.getchannel("A"))
            image = background
        else:
            image = image.convert("RGB")

        output = destination / f"{path.stem}.jpg"
        image.save(output, "JPEG", quality=85, optimize=True)

    before = path.stat().st_size / 1e6
    after = output.stat().st_size / 1e6
    print(f"{path.name}: {before:.2f} MB -> {after:.2f} MB")