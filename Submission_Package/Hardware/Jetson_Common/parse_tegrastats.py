#!/usr/bin/env python3
# parse_tegrastats.py
"""Parse tegrastats output (with ISO timestamp prefixed) to CSV.
Output columns (best effort):
 timestamp_iso, ram_used_MB, ram_total_MB, swap_used_MB, swap_total_MB,
 cpu_util_pct, gpu_util_pct, gr3d_freq_pct, emc_freq_pct,
 power_W, temp_CPU_C, temp_GPU_C, temp_AO_C, raw_line
"""
import re, sys, csv
from pathlib import Path

if len(sys.argv) < 3:
    print("Usage: parse_tegrastats.py <tegrastats_raw.txt> <out_csv>")
    sys.exit(1)
raw_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])

MB = r'(\d+)'
PCT = r'(\d+)'
FLT = r'([0-9]+\.?[0-9]*)'
ram_re = re.compile(r'RAM\s+'+MB+r'/' + MB + r'MB')
swap_re = re.compile(r'SWAP\s+'+MB+r'/' + MB + r'MB')
cpu_re = re.compile(r'CPU\s+\[(.*?)\]')
gpu_re = re.compile(r'GPU\s+'+PCT+r'%')
gr3d_re = re.compile(r'GR3D_FREQ\s+'+PCT+r'%')
emc_re = re.compile(r'EMC_FREQ\s+'+PCT+r'%')
power_re = re.compile(r'POM_5V_IN\s+'+FLT+r'W')
TEMP_PAIR = re.compile(r'(AO|GPU|CPU)@'+MB+r'C')

with raw_path.open('r') as fin, out_path.open('w', newline='') as fout:
    w = csv.writer(fout)
    w.writerow(['timestamp_iso','ram_used_MB','ram_total_MB','swap_used_MB','swap_total_MB',
                'cpu_util_pct','gpu_util_pct','gr3d_freq_pct','emc_freq_pct',
                'power_W','temp_CPU_C','temp_GPU_C','temp_AO_C','raw_line'])

    for line in fin:
        line=line.strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        if len(parts) < 2:
            ts, rest = parts[0], ''
        else:
            ts, rest = parts[0], parts[1]

        ru=rt=su=st=cpu=gpu=gr3d=emc=pow=None
        tCPU=tGPU=tAO=None

        m = ram_re.search(rest)
        if m:
            ru, rt = int(m.group(1)), int(m.group(2))
        m = swap_re.search(rest)
        if m:
            su, st = int(m.group(1)), int(m.group(2))
        m = cpu_re.search(rest)
        if m:
            cores = re.findall(r'(\d+)%', m.group(1))
            if cores:
                cpu = sum(map(int, cores)) / len(cores)
        m = gpu_re.search(rest)
        if m:
            gpu = int(m.group(1))
        m = gr3d_re.search(rest)
        if m:
            gr3d = int(m.group(1))
        m = emc_re.search(rest)
        if m:
            emc = int(m.group(1))
        m = power_re.search(rest)
        if m:
            pow = float(m.group(1))
        for label,val in TEMP_PAIR.findall(rest):
            val = int(val)
            if label=='CPU': tCPU = val
            elif label=='GPU': tGPU = val
            elif label=='AO': tAO = val

        w.writerow([ts, ru, rt, su, st, cpu, gpu, gr3d, emc, pow, tCPU, tGPU, tAO, rest])

print(f'Wrote {out_path}')
