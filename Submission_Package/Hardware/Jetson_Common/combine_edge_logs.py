#!/usr/bin/env python3
# combine_edge_logs.py
"""Join runtime_logs.csv with tegrastats.csv by nearest timestamp (within a tolerance).
Outputs combined_edge_logs.csv with columns from both.
"""
import pandas as pd
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('--runtime', default='runtime_logs.csv')
ap.add_argument('--tegra', default='tegrastats.csv')
ap.add_argument('--out', default='combined_edge_logs.csv')
ap.add_argument('--tolerance_s', type=float, default=1.0)
args = ap.parse_args()

rt = pd.read_csv(args.runtime, parse_dates=['timestamp_iso'])
ts = pd.read_csv(args.tegra, parse_dates=['timestamp_iso'])

rt = rt.sort_values('timestamp_iso').reset_index(drop=True)
ts = ts.sort_values('timestamp_iso').reset_index(drop=True)

merged = pd.merge_asof(rt.sort_values('timestamp_iso'),
                       ts.sort_values('timestamp_iso'),
                       on='timestamp_iso',
                       direction='nearest',
                       tolerance=pd.Timedelta(seconds=args.tolerance_s))
merged.to_csv(args.out, index=False)
print(f'Wrote {args.out}')
