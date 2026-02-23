#!/usr/bin/env python3
# edge_runtime_logger.py
"""Template logger for edge inference loops.
Append one CSV row per frame with: timestamp_iso, frame_id, inference_ms, img_latency_ms, loop_hz
Example use (dummy simulation):
  python edge_runtime_logger.py --out runtime_logs.csv --simulate 100 --hz 5
Then run: parse_tegrastats.py and combine_edge_logs.py to correlate.
"""
import csv, time, argparse
from datetime import datetime

ap = argparse.ArgumentParser()
ap.add_argument('--out', default='runtime_logs.csv')
ap.add_argument('--simulate', type=int, default=0, help='if >0, run N dummy frames')
ap.add_argument('--hz', type=float, default=5.0)
args = ap.parse_args()

with open(args.out, 'a', newline='') as f:
    w = csv.writer(f)
    if f.tell()==0:
        w.writerow(['timestamp_iso','frame_id','inference_ms','img_latency_ms','loop_hz'])
    if args.simulate>0:
        dt = 1.0/args.hz
        for i in range(args.simulate):
            t0=time.perf_counter()
            # Simulated timings
            inf_ms = 18.0
            img_ms = 12.0
            time.sleep(dt)
            loop_hz = 1.0/(time.perf_counter()-t0)
            w.writerow([datetime.now().isoformat(), i, f'{inf_ms:.2f}', f'{img_ms:.2f}', f'{loop_hz:.2f}'])
            f.flush()
print(f'Appended to {args.out}')
