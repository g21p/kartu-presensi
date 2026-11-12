"""Siapkan template: SVG Canva -> PDF vektor yang dipakai web saat membuat PDF.

Pemakaian (butuh rsvg-convert / librsvg, Pillow, numpy):
  python tools/siapkan_template.py template/kartu-1.svg   (bisa beberapa file sekaligus)
Hasil: template/kartu-1.pdf di folder yang sama.
Mask logo pada SVG Canva diubah menjadi gambar transparan biasa supaya tetap tajam di PDF.
"""
import re, sys, base64, io, os, subprocess
import numpy as np
from PIL import Image

POLA_MASK = r'<mask maskUnits="userSpaceOnUse" id="(\w+)"><g filter="url\(#\w+\)"><g filter="url\(#\w+\)" transform="([^"]+)"><image x="0" y="0" width="(\d+)" xlink:href="data:image/png;base64,([A-Za-z0-9+/=]+)" height="(\d+)"[^>]*/></g></g></mask>'
POLA_PAKAI = r'<g mask="url\(#(\w+)\)"><g transform="([^"]+)"><image x="0" y="0" width="(\d+)" xlink:href="data:image/png;base64,([A-Za-z0-9+/=]+)" height="(\d+)"([^>]*)/></g></g>'

def gabung(b64, mask_b64):
    img = np.array(Image.open(io.BytesIO(base64.b64decode(b64))).convert('RGBA')).astype(float)
    mk = np.array(Image.open(io.BytesIO(base64.b64decode(mask_b64))).convert('RGBA')).astype(float)
    lum = (0.2126 * mk[..., 0] + 0.7152 * mk[..., 1] + 0.0722 * mk[..., 2]) * (mk[..., 3] / 255)
    img[..., 3] = img[..., 3] * lum / 255
    bio = io.BytesIO(); Image.fromarray(img.clip(0, 255).astype('uint8'), 'RGBA').save(bio, 'PNG', optimize=True)
    return base64.b64encode(bio.getvalue()).decode()

def proses(svg):
    s = open(svg, encoding='utf-8').read()
    masks = {m.group(1): m.group(4) for m in re.finditer(POLA_MASK, s)}
    def ganti(m):
        mid, tr, w, b64, h, sisa = m.groups()
        return f'<g transform="{tr}"><image x="0" y="0" width="{w}" xlink:href="data:image/png;base64,{gabung(b64, masks[mid])}" height="{h}"{sisa}/></g>'
    s = re.sub(POLA_PAKAI, ganti, s)
    tmp = svg[:-4] + '.tmp.svg'
    open(tmp, 'w', encoding='utf-8').write(s)
    pdf = svg[:-4] + '.pdf'
    subprocess.run(['rsvg-convert', '-f', 'pdf', tmp, '-o', pdf], check=True)
    os.remove(tmp)
    print('OK', pdf)

if __name__ == '__main__':
    for f in sys.argv[1:]:
        proses(f)
