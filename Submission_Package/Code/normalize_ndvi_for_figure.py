
# normalize_ndvi_for_figure.py
"""
Apply a common colormap and numeric scale to Sim and Real NDVI rasters so the
3×2 figure uses a consistent visual scale across both panels.

Usage (fixed scale, default):
  python Code/normalize_ndvi_for_figure.py     --sim_in Data_Samples/Sim/NDVI/sim_ndvi.png     --real_in Data_Samples/Real/NDVI/real_ndvi.png     --sim_out Data_Samples/Sim/NDVI/sim_ndvi.png     --real_out Data_Samples/Real/NDVI/real_ndvi.png     --fixed_vmin -0.2 --fixed_vmax 1.0 --cmap RdYlGn

Notes:
- This script expects grayscale NDVI rasters or single-band images. If inputs
  are already 3‑channel color maps, the script will warn and skip recoloring.
- If your grayscale is 0..255, use --in_min 0 --in_max 255 (maps to 0..1 then to NDVI scale).
- If your grayscale is -1..1 packed into 0..255 via (x+1)/2, use --input_is_ndvi_01.
"""
import os
import argparse
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def load_gray(path):
    im = Image.open(path)
    arr = np.array(im)
    if arr.ndim == 2:
        return arr.astype('float32'), 'L'
    if arr.ndim == 3 and arr.shape[2] == 1:
        return arr[...,0].astype('float32'), 'L'
    # 3‑channel; likely already colored
    return arr.astype('float32'), 'RGB'


def to_ndvi(arr, mode, in_min, in_max, input_is_ndvi_01):
    if input_is_ndvi_01:
        # assume arr in [0,1] but represents NDVI directly
        ndvi = arr
    else:
        # normalize raw to [0,1]
        if in_max <= in_min:
            raise ValueError('in_max must be > in_min')
        norm01 = (arr - in_min) / float(in_max - in_min)
        norm01 = np.clip(norm01, 0, 1)
        # map [0,1] → NDVI [-1,1]
        ndvi = norm01 * 2.0 - 1.0
    return ndvi


def colorize(ndvi, vmin, vmax, cmap_name='RdYlGn'):
    cmap = plt.get_cmap(cmap_name)
    clipped = np.clip(ndvi, vmin, vmax)
    normed = (clipped - vmin) / max(vmax - vmin, 1e-6)
    rgba = cmap(normed)
    rgb = (rgba[...,:3] * 255).astype('uint8')
    return rgb


def save_png(rgb, out_path, add_scale=False, vmin=-0.2, vmax=1.0, cmap_name='RdYlGn'):
    if add_scale:
        # create a small colorbar image on the right
        h, w, _ = rgb.shape
        fig, ax = plt.subplots(figsize=(w/100, h/100), dpi=100)
        ax.imshow(rgb)
        ax.axis('off')
        cax = fig.add_axes([0.92, 0.1, 0.02, 0.8])
        cmap = plt.get_cmap(cmap_name)
        cb = matplotlib.colorbar.ColorbarBase(cax, cmap=cmap, orientation='vertical')
        cb.set_label('NDVI')
        cb.set_ticks([vmin, (vmin+vmax)/2, vmax])
        cb.set_ticklabels([f'{vmin:.1f}', f'{(vmin+vmax)/2:.1f}', f'{vmax:.1f}'])
        plt.savefig(out_path, dpi=100, bbox_inches='tight')
        plt.close(fig)
    else:
        Image.fromarray(rgb).save(out_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sim_in', required=True)
    ap.add_argument('--real_in', required=True)
    ap.add_argument('--sim_out', required=True)
    ap.add_argument('--real_out', required=True)
    ap.add_argument('--fixed_vmin', type=float, default=-0.2)
    ap.add_argument('--fixed_vmax', type=float, default=1.0)
    ap.add_argument('--cmap', default='RdYlGn')
    ap.add_argument('--in_min', type=float, default=0.0)
    ap.add_argument('--in_max', type=float, default=255.0)
    ap.add_argument('--input_is_ndvi_01', action='store_true', help='inputs are already NDVI in [0,1]')
    ap.add_argument('--add_colorbar', action='store_true')
    args = ap.parse_args()

    sim_arr, sim_mode = load_gray(args.sim_in)
    real_arr, real_mode = load_gray(args.real_in)

    if sim_mode == 'RGB' or real_mode == 'RGB':
        print('WARNING: one or both NDVI inputs are already RGB; skipping recolor to avoid double mapping.')
        return 0

    sim_ndvi = to_ndvi(sim_arr, 'fixed', args.in_min, args.in_max, args.input_is_ndvi_01)
    real_ndvi = to_ndvi(real_arr, 'fixed', args.in_min, args.in_max, args.input_is_ndvi_01)

    # Apply the same fixed scale to both
    vmin, vmax = args.fixed_vmin, args.fixed_vmax
    sim_rgb = colorize(sim_ndvi, vmin, vmax, args.cmap)
    real_rgb = colorize(real_ndvi, vmin, vmax, args.cmap)

    save_png(sim_rgb, args.sim_out, add_scale=args.add_colorbar, vmin=vmin, vmax=vmax, cmap_name=args.cmap)
    save_png(real_rgb, args.real_out, add_scale=args.add_colorbar, vmin=vmin, vmax=vmax, cmap_name=args.cmap)
    print(f'Wrote common-scale NDVI to:
  {args.sim_out}
  {args.real_out}')

if __name__ == '__main__':
    main()
