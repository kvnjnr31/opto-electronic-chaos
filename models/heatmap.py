import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Constants
C = 100e-9  # 100 nF capacitor

# Realistic BPW34 photodiode resistances (reverse-biased, light-dependent)
bpw34_r_pd = np.array([10e3, 33e3, 100e3, 330e3, 1e6])  # 10kΩ to 1MΩ

# Linear resistor range (1Ω to 1MΩ)
r_linear = np.logspace(0, 6, num=10)

# Compute time constants τ = RC
bpw_tau_data = []
for R_pd in bpw34_r_pd:
    for R_lin in r_linear:
        R_total = R_pd + R_lin
        tau = R_total * C
        bpw_tau_data.append({
            'Photodiode R (Ω)': R_pd,
            'Linear Resistor R (Ω)': R_lin,
            'Tau (s)': tau
        })

# Create DataFrame
df_bpw_tau = pd.DataFrame(bpw_tau_data)

# Pivot table for heatmap
bpw_heatmap = df_bpw_tau.pivot(
    index='Photodiode R (Ω)',
    columns='Linear Resistor R (Ω)',
    values='Tau (s)'
)

# Format labels for clarity
bpw_heatmap.index = [f"{r:.1e}" for r in bpw_heatmap.index]
bpw_heatmap.columns = [f"{r:.1e}" for r in bpw_heatmap.columns]

# Plot the heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(
    bpw_heatmap,
    annot=True,
    fmt=".5f",
    cmap="magma",
    cbar_kws={'label': 'Tau (s)'}
)
plt.title("Time Constants τ = RC for BPW34 Photodiode Ranges\nSeries R with 100nF Cap")
plt.xlabel("Linear Resistor R (Ω)")
plt.ylabel("Photodiode R (Ω)")
plt.tight_layout()
plt.show()
