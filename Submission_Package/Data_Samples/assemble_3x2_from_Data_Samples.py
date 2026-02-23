
#!/usr/bin/env python3
import subprocess
import sys

args = [
  'python', 'Code/plot_and_assemble.py',
  '--csv', 'logs/training_metrics.csv',
  '--sim_ndvi', 'Data_Samples/Sim/NDVI/sim_ndvi.png',
  '--real_ndvi', 'Data_Samples/Real/NDVI/real_ndvi.png',
  '--sim_act',  'Data_Samples/Sim/Saliency/sim_saliency.png',
  '--real_act', 'Data_Samples/Real/Saliency/real_saliency.png',
  '--sim_vri',  'Data_Samples/Sim/Actions/sim_vri_actions.png',
  '--real_vri', 'Data_Samples/Real/Actions/real_vri_actions.png',
  '--consistency', '0.92'
]

sys.exit(subprocess.call(args))
