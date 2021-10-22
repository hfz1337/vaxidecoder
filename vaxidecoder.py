#!/usr/bin/python3
from pyzbar import pyzbar
from PIL import Image
import zlib
import sys
import re
from base64 import b64decode


def fix_b64_padding(s):
    return s + "=" * (4 - len(s) % 4)


def b64_url_decode(s):
    return s.replace("-", "+").replace("_", "/")


if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <qr_image>")
    exit(0)

shc = pyzbar.decode(Image.open(sys.argv[1]))[0].data.decode()
payload = zlib.decompress(
    b64decode(
        fix_b64_padding(
            b64_url_decode(
                "".join(
                    chr(int(i) + 45) for i in re.findall("..", shc.split("/")[1])
                ).split(".")[1]
            )
        )
    ),
    -zlib.MAX_WBITS,
).decode()

print(payload)
