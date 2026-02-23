# Jetson Orin Nano — Edge Deployment Evidence

## Files to provide
- runtime_logs.csv — per-frame agent metrics (timestamp_iso, frame_id, inference_ms, img_latency_ms, loop_hz)
- tegrastats_raw.txt — raw tegrastats (with ISO timestamps prefixed)
- tegrastats.csv — parsed tegrastats (generated)
- combined_edge_logs.csv — merged per-frame + tegrastats (generated)
- nvpmodel.txt — output of `sudo nvpmodel -q`
- jetson_clocks.txt — output of `sudo jetson_clocks --show`

## How to collect
```bash
# 1) Record power mode and clocks
sudo nvpmodel -q | tee nvpmodel.txt
sudo jetson_clocks --show | tee jetson_clocks.txt

# 2) Start tegrastats (CTRL+C to stop)
cd ../Jetson_Common
sudo ./collect_tegrastats.sh ../Jetson_Orin_Nano/tegrastats_raw.txt 1000

# 3) In another shell, log runtime metrics (or integrate edge_runtime_logger.py in your app)
python edge_runtime_logger.py --out ../Jetson_Orin_Nano/runtime_logs.csv --simulate 100 --hz 5

# 4) Parse tegrastats to CSV
python parse_tegrastats.py ../Jetson_Orin_Nano/tegrastats_raw.txt ../Jetson_Orin_Nano/tegrastats.csv

# 5) Merge logs by nearest timestamp (1s tolerance)
python combine_edge_logs.py \
  --runtime ../Jetson_Orin_Nano/runtime_logs.csv \
  --tegra   ../Jetson_Orin_Nano/tegrastats.csv \
  --out     ../Jetson_Orin_Nano/combined_edge_logs.csv \
  --tolerance_s 1.0
````

## Tips
- Run with `sudo` only where needed (tegrastats, jetson_clocks).
- If `awk` time prefixing fails, you can run tegrastats and prefix timestamps in Python when parsing.
- Keep the same timezone between devices and the logs to simplify merges.
