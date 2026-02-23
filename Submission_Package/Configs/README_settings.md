
# Configs (Regenerated Profiles)

**Profiles included**
- `settings_headless.json`  → camera-only, `NoDisplay`, stable exposure/gamma; ideal for training/logging.
- `settings_preview.json`   → on-screen preview with 3 subwindows (`band0_scene`/`band1_scene`/`band2_scene`) and a `topdown` external camera.
- `settings_spectral.json`  → use if Unreal materials export true `nir`, `red_edge`, `red` band views.
- `settings_multivehicle.json` → preview profile + a `SimpleFlight` quad (`uav1`) with an RGB `front_center` camera.

**Notes**
- Place your active file as `settings.json` in the folder AirSim reads (or launch with `-settings=<path>`).
- Camera and Settings schema follow the official AirSim Settings documentation; image capture is via Image APIs.
