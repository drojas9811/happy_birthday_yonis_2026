#!/usr/bin/env python3
"""Actualiza únicamente la lista de recuerdos; no modifica los textos ni el diseño."""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import quote

IMAGES = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'}
VIDEOS = {'.mp4', '.webm', '.mov'}
START = '<script id="media-data" type="application/json">'
END = '</script>'

def natural_key(path):
    return tuple((0, int(part)) if part.isdigit() else (1, part.casefold())
                 for part in re.split(r'(\d+)', path.as_posix()))

def collect(root):
    folder = root / 'media'
    folder.mkdir(exist_ok=True)
    result, warnings = [], []
    files = sorted(folder.rglob('*'), key=lambda p: (natural_key(p.relative_to(folder)), p.as_posix()))
    for file in files:
        relative = file.relative_to(root)
        if not file.is_file() or file.is_symlink() or any(part.startswith('.') for part in relative.parts):
            continue
        if any((root / parent).is_symlink() for parent in relative.parents if str(parent) != '.'):
            continue
        suffix = file.suffix.lower()
        if suffix in {'.heic', '.heif'}:
            warnings.append(f'Convertir a JPG antes de publicar: {relative}')
            continue
        if suffix not in IMAGES | VIDEOS:
            continue
        path = relative.as_posix()
        result.append({'path': path, 'url': quote(path, safe='/'),
                       'type': 'video' if suffix in VIDEOS else 'image'})
    if any(item['type'] == 'video' for item in result):
        warnings.append('La extensión no garantiza compatibilidad. Para videos, se recomienda MP4 con H.264 y audio AAC. Prueba su reproducción; no renombres extensiones ni sobrescribas originales.')
    return result, warnings

def generate(root):
    html_path = root / 'index.html'
    html = html_path.read_text(encoding='utf-8')
    if html.count(START) != 1:
        raise ValueError('No se encontró un único bloque media-data en index.html.')
    start = html.index(START) + len(START)
    end = html.index(END, start)
    items, warnings = collect(root)
    payload = json.dumps(items, ensure_ascii=True, indent=2).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    html_path.write_text(html[:start] + '\n' + payload + '\n' + html[end:], encoding='utf-8')
    for warning in warnings:
        print('AVISO:', warning)
    print(f"Galería lista: {sum(i['type']=='image' for i in items)} fotos y {sum(i['type']=='video' for i in items)} videos.")
    return items

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    generate(parser.parse_args().root.resolve())
