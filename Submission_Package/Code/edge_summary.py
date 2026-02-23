#!/usr/bin/env python3
import os, argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def ensure_combined(runtime_csv, tegra_csv, combined_csv):
    if os.path.exists(combined_csv):
        return pd.read_csv(combined_csv, parse_dates=['timestamp_iso'])
    rt = pd.read_csv(runtime_csv, parse_dates=['timestamp_iso'])
    ts = pd.read_csv(tegra_csv, parse_dates=['timestamp_iso'])
    rt = rt.sort_values('timestamp_iso').reset_index(drop=True)
    ts = ts.sort_values('timestamp_iso').reset_index(drop=True)
    merged = pd.merge_asof(rt, ts, on='timestamp_iso', direction='nearest', tolerance=pd.Timedelta(seconds=1))
    return merged

def pct(series, p):
    s = pd.to_numeric(series, errors='coerce').dropna()
    return float(np.nanpercentile(s.to_numpy(), p)) if len(s) else np.nan

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runtime', default='Hardware/Jetson_Orin_Nano/runtime_logs.csv')
    ap.add_argument('--tegra',   default='Hardware/Jetson_Orin_Nano/tegrastats.csv')
    ap.add_argument('--combined', default='Hardware/Jetson_Orin_Nano/combined_edge_logs.csv')
    ap.add_argument('--outdir', default='outputs/edge_summary')
    ap.add_argument('--device_name', default='Jetson Orin Nano')
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    df = ensure_combined(args.runtime, args.tegra, args.combined)

    metrics = {}
    for col in ['inference_ms','img_latency_ms','loop_hz']:
        if col in df.columns:
            s = pd.to_numeric(df[col], errors='coerce')
            metrics[col] = {'count': int(s.count()), 'mean': float(s.mean()), 'std': float(s.std()),
                            'p50': pct(s,50), 'p90': pct(s,90), 'p99': pct(s,99)}
    for col in ['power_W','temp_CPU_C','temp_GPU_C','temp_AO_C','gpu_util_pct','cpu_util_pct']:
        if col in df.columns:
            s = pd.to_numeric(df[col], errors='coerce')
            metrics[col] = {'count': int(s.count()), 'mean': float(s.mean()), 'std': float(s.std()),
                            'min': float(s.min()), 'max': float(s.max())}

    # CSV
    import csv
    with open(os.path.join(args.outdir,'edge_summary.csv'),'w',newline='') as f:
        w=csv.writer(f); w.writerow(['metric','count','mean','std','p50','p90','p99','min','max'])
        for k,v in metrics.items():
            w.writerow([k, v.get('count'), v.get('mean'), v.get('std'), v.get('p50'), v.get('p90'), v.get('p99'), v.get('min'), v.get('max')])

    # TXT
    txt_file = os.path.join(args.outdir,'edge_summary.txt')
    with open(txt_file,'w') as ftxt:
        ftxt.write('Edge Summary - {}
'.format(args.device_name))
        ftxt.write('='*64+'

')
        if 'inference_ms' in metrics:
            m=metrics['inference_ms']
            ftxt.write('Inference (ms): mean={:.2f}  p50={:.2f}  p90={:.2f}  p99={:.2f}
'.format(m['mean'],m['p50'],m['p90'],m['p99']))
        if 'img_latency_ms' in metrics:
            m=metrics['img_latency_ms']
            ftxt.write('Image Latency (ms): mean={:.2f}  p50={:.2f}  p90={:.2f}  p99={:.2f}
'.format(m['mean'],m['p50'],m['p90'],m['p99']))
        if 'loop_hz' in metrics:
            m=metrics['loop_hz']
            ftxt.write('Loop Rate (Hz): mean={:.2f}  p50={:.2f}  p90={:.2f}  p99={:.2f}
'.format(m['mean'],m['p50'],m['p90'],m['p99']))
        if 'power_W' in metrics:
            m=metrics['power_W']
            ftxt.write('Power (W): mean={:.2f}  min={:.2f}  max={:.2f}
'.format(m['mean'],m['min'],m['max']))
        for tcol in ['temp_CPU_C','temp_GPU_C','temp_AO_C']:
            if tcol in metrics:
                m=metrics[tcol]
                ftxt.write('{}: mean={:.1f}C  min={:.1f}C  max={:.1f}C
'.format(tcol.replace('_',' '), m['mean'],m['min'],m['max']))

    # FIG

    fig, axes = plt.subplots(3,1,figsize=(10,10))
    if 'inference_ms' in df.columns:
        s = pd.to_numeric(df['inference_ms'], errors='coerce').dropna()
        axes[0].hist(s, bins=20, color='#2c7be5', alpha=0.75)
        axes[0].set_title('Inference time (ms)'); axes[0].set_xlabel('ms'); axes[0].set_ylabel('count')
    if 'timestamp_iso' in df.columns:
        t = pd.to_datetime(df['timestamp_iso'])
        if 'loop_hz' in df.columns:
            axes[1].plot(t, pd.to_numeric(df['loop_hz'], errors='coerce'), color='#2ca02c', label='Loop Hz')
            axes[1].set_ylabel('Hz', color='#2ca02c'); axes[1].tick_params(axis='y', labelcolor='#2ca02c')
        ax2 = axes[1].twinx()
        if 'power_W' in df.columns:
            ax2.plot(t, pd.to_numeric(df['power_W'], errors='coerce'), color='#d62728', label='Power (W)')
            ax2.set_ylabel('W', color='#d62728'); ax2.tick_params(axis='y', labelcolor='#d62728')
        axes[1].set_title('Timeseries: Loop Hz & Power (W)'); axes[1].set_xlabel('Time')
    if 'loop_hz' in df.columns and 'power_W' in df.columns:
        x = pd.to_numeric(df['power_W'], errors='coerce'); y = pd.to_numeric(df['loop_hz'], errors='coerce')
        m = (~x.isna() & ~y.isna()); x,y=x[m],y[m]
        axes[2].scatter(x,y,s=12,alpha=0.7,color='#9467bd')
        if len(x)>2:
            coeff = np.polyfit(x, y, 1)
            xx = np.linspace(x.min(), x.max(), 100); yy = coeff[0]*xx+coeff[1]
            axes[2].plot(xx,yy,color='#111111',linewidth=1.5,label='y={:.2f}x+{:.2f}'.format(coeff[0],coeff[1]))
            axes[2].legend()
        axes[2].set_title('Power (W) vs Loop Hz'); axes[2].set_xlabel('Power (W)'); axes[2].set_ylabel('Loop Hz')
    fig.tight_layout(); plt.savefig(os.path.join(args.outdir,'edge_summary.png'), dpi=180); plt.close(fig)

if __name__=='__main__':
    main()
