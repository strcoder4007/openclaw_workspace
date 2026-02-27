---
name: nano-banana-pro
description: Generate or edit images via Gemini 3.1 Flash Image (Nano Banana 2).
metadata:
  {
    "openclaw": { "emoji": "🍌" }
  }
---

# Nano Banana 2 (Gemini 3.1 Flash Image)

High-quality image generation at mainstream price and low latency.

## New Features (v2)

- Resolutions: 0.5K, 1K (default), 2K, 4K
- Image Search Grounding
- Aspect ratios: 1:1, 1:4, 4:1, 1:8, 8:1
- Improved quality and text rendering

## Generate

```bash
cd /Users/str/.openclaw/workspace/skills/nano-banana-pro
uv run scripts/generate_image.py --prompt "your image description" --filename "output.png" --resolution 1K
```

## Edit (single image)

```bash
uv run scripts/generate_image.py --prompt "edit instructions" -i "/path/to/image.png" --filename "output.png"
```

## Multi-image composition (up to 14 images)

```bash
uv run scripts/generate_image.py --prompt "combine these" -i img1.png -i img2.png --filename "output.png"
```

## Notes

- Model: `gemini-3.1-flash-image-preview`
- Output saved to current directory (or specify full path)
- Use timestamps in filenames: `yyyy-mm-dd-hh-mm-ss-name.png`
