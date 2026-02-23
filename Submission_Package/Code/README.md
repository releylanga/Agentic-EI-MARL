
# /Code

Contents:
- `airsim_agri_env.py` : AirSim-Agri Gym-like environment that computes NDVI/NDRE from default Scene cameras and logs Jetson-like timestamps & throughput.
- `train_with_logging.py` : Stable-Baselines3 PPO training wrapper that records NDVI/NDRE statistics and saves snapshots.
- `plot_and_assemble.py` : Plots NDVI/NDRE training curves and assembles the 3×2 Feature–Action Map (Sim vs Real) figure.

Purpose: **Transparency of the Agent** (policy, reward shaping, observation construction).

Notes:
- Requires `airsim`, `stable-baselines3`, `gym==0.26.2`, `numpy`, `matplotlib`, `scipy`, `pandas`.
- AirSim APIs used per official Image APIs documentation.
