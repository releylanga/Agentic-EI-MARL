
# Data_Samples

This folder holds the **paired simulation vs. real-world** images used to build the
3×2 Feature–Action Map and to accompany your 92% policy-consistency statement.

## Expected structure
```
Data_Samples/
  Sim/
    NDVI/       sim_ndvi.png
    Saliency/   sim_saliency.png
    Actions/    sim_vri_actions.png
  Real/
    NDVI/       real_ndvi.png
    Saliency/   real_saliency.png
    Actions/    real_vri_actions.png
```

> Place **your real outputs** over the placeholders with the exact filenames above.

## Assemble the 3×2 figure
Use the helper in `/Code`:

```bash
python Code/plot_and_assemble.py   --csv logs/training_metrics.csv   --sim_ndvi Data_Samples/Sim/NDVI/sim_ndvi.png   --real_ndvi Data_Samples/Real/NDVI/real_ndvi.png   --sim_act  Data_Samples/Sim/Saliency/sim_saliency.png   --real_act Data_Samples/Real/Saliency/real_saliency.png   --sim_vri  Data_Samples/Sim/Actions/sim_vri_actions.png   --real_vri Data_Samples/Real/Actions/real_vri_actions.png   --consistency 0.92
```

The script will produce:
- `outputs/ndvi_ndre_training.png` (NDVI/NDRE curves)
- `outputs/feature_action_map_3x2.png` (final composite)

## Tips
- Keep **NDVI** maps visually comparable (same colormap/range) across Sim/Real.
- Saliency/activation can be grad-CAM or any policy feature map; make sure it overlays or aligns with the NDVI spatial frame.
- Action maps must show the **discrete** VRI bins (**Low, Medium, High**).


## Apply a common NDVI color scale (optional but recommended)
Run this **before** assembling the 3×2 figure if your NDVI inputs are grayscale rasters:

```bash
python Code/normalize_ndvi_for_figure.py \ 
  --sim_in Data_Samples/Sim/NDVI/sim_ndvi.png \ 
  --real_in Data_Samples/Real/NDVI/real_ndvi.png \ 
  --sim_out Data_Samples/Sim/NDVI/sim_ndvi.png \ 
  --real_out Data_Samples/Real/NDVI/real_ndvi.png \ 
  --fixed_vmin -0.2 --fixed_vmax 1.0 --cmap RdYlGn --in_min 0 --in_max 255
```

If your grayscale files already store NDVI in [0,1], add `--input_is_ndvi_01`.
