# make_manifest.py
"""Compute SHA-256 hashes for reproducibility.
Writes MANIFEST_SHA256.txt at repository root.
"""
import os, hashlib

ROOT = 'Submission_Package'
OUT = os.path.join(ROOT, 'MANIFEST_SHA256.txt')

EXCLUDE_DIRS = {'.git', '__pycache__'}

with open(OUT, 'w') as out:
    for folder, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fn in sorted(files):
            path = os.path.join(folder, fn)
            if os.path.abspath(path) == os.path.abspath(OUT):
                continue
            h = hashlib.sha256()
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(65536), b''):
                    h.update(chunk)
            rel = os.path.relpath(path, start=ROOT)
            out.write('{}  {}
'.format(h.hexdigest(), rel))
print('Wrote {}'.format(OUT))
