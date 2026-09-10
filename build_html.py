#!/usr/bin/env python3
"""Compress the five mood images + the couple portrait and inline them as base64 into index.html."""
import base64
import io

from PIL import Image

WIDTH = 600
QUALITY = 68
PORTRAIT_PATH = "uploads/4c539d7bb21580f965fa7b22f17171e3.jpg"

names = ["lagan", "haldi", "sangeet", "phere", "reception"]
total = 0
tpl = open("index.template.html").read()

# couple portrait for the header medallion
im = Image.open(PORTRAIT_PATH).convert("RGB")
w, h = im.size
im = im.resize((360, round(h * 360 / w)), Image.LANCZOS)
buf = io.BytesIO()
im.save(buf, "JPEG", quality=80, optimize=True, progressive=True)
b64 = base64.b64encode(buf.getvalue()).decode()
total += len(b64)
print(f"portrait: {len(buf.getvalue())//1024} KB raw, {len(b64)//1024} KB b64")
tpl = tpl.replace("__PORTRAIT_IMG__", b64)

for name in names:
    im = Image.open(f"assets/{name}.jpg").convert("RGB")
    w, h = im.size
    im = im.resize((WIDTH, round(h * WIDTH / w)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    total += len(b64)
    print(f"{name}: {len(buf.getvalue())//1024} KB raw, {len(b64)//1024} KB b64")
    tpl = tpl.replace(f"__{name.upper()}_IMG__", b64)

for name in names:
    assert f"__{name.upper()}_IMG__" not in tpl, f"placeholder left for {name}"
assert "__PORTRAIT_IMG__" not in tpl, "placeholder left for portrait"

open("index.html", "w").write(tpl)
print(f"index.html written, total b64 payload ~{total//1024} KB")
