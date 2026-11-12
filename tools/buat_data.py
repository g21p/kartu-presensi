"""Buat data/siswa.json dan salin QR ke qr/<ID>.png.

Pemakaian:
  python tools/buat_data.py Data_Siswa.xlsx folder_qr

- Excel: kolom 'No Induk', 'NAMA SISWA', 'KELAS' (baris 1 = judul kolom).
- Folder QR: berisi file PNG bernama '<ID>_<Nama>.png' (boleh di subfolder),
  dengan ID = No Induk tanpa titik (2627.1.001 -> 26271001).
Butuh: pip install openpyxl
"""
import json, os, re, shutil, sys
import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main(xlsx, qr_dir):
    ws = openpyxl.load_workbook(xlsx, data_only=True).active
    head = [str(c or '').strip().upper() for c in next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]
    i_id, i_nama, i_kelas = head.index('NO INDUK'), head.index('NAMA SISWA'), head.index('KELAS')
    qr = {}
    for d, _, files in os.walk(qr_dir):
        for f in files:
            if f.lower().endswith('.png') and '_' in f:
                qr[f.split('_', 1)[0]] = os.path.join(d, f)
    out_qr = os.path.join(ROOT, 'qr')
    shutil.rmtree(out_qr, ignore_errors=True); os.makedirs(out_qr)
    siswa, tanpa_qr = [], []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[i_nama]:
            continue
        nid = str(r[i_id]).strip()
        key = re.sub(r'\D', '', nid)
        nama = re.sub(r'\s+', ' ', str(r[i_nama])).strip()
        kelas = str(r[i_kelas]).strip()
        if key not in qr:
            tanpa_qr.append(f'{nid} {nama} ({kelas})'); continue
        shutil.copy(qr[key], os.path.join(out_qr, key + '.png'))
        siswa.append({'id': nid, 'qr': key, 'nama': nama, 'kelas': kelas})
    siswa.sort(key=lambda s: (s['kelas'], s['nama']))
    with open(os.path.join(ROOT, 'data', 'siswa.json'), 'w', encoding='utf-8') as f:
        json.dump(siswa, f, ensure_ascii=False, separators=(',', ':'))
    print(f'{len(siswa)} siswa disimpan.')
    if tanpa_qr:
        print('Tidak ada QR untuk:', *tanpa_qr, sep='\n  ')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
