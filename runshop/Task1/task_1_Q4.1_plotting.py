"""Plotting Task 1 Q4.1"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter

# Import data from Q4.1
stakes = "Unit"
PnL_data = np.load(f"output/Q4.1_PnL_data_1000000_{stakes}.npy")
stakes_data = np.load(f"output/Q4.1_Stake_data_1000000_{stakes}.npy")
# Calculate PnL RoI from each simulation
PnL_RoI_data = [PnL / stake for PnL, stake in zip(PnL_data, stakes_data)]

# Mean PnL from each simulation
PnL_RoI_mean = sum(PnL_data) / sum(stakes_data)
print(len(PnL_RoI_data))
# Remove high outliers for plotting
PnL_RoI_data = [PnL for PnL in PnL_RoI_data if PnL < 4]
print(len(PnL_RoI_data))

print(f"Mean PnL RoI: {PnL_RoI_mean}")

# Plot the distribution of PnL RoI from each simulation
plt.hist(PnL_RoI_data, bins=40, color="skyblue", edgecolor="black", alpha=0.7)
plt.xlabel("Final PnL")
plt.axvline(PnL_RoI_mean, linestyle="dashed", color="black", label="Mean PnL")
plt.axvline(0, linestyle="dashed", color="red", label="Break Even")
plt.ylabel("Number of Simulations")
plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
plt.gca().ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
plt.title(f"Distribution of PnL - {stakes} Stakes")
plt.xlim(-0.5, 1.5)
plt.legend()
plt.savefig(f"output/Q4.1_PnL_distribution_{stakes}.png", dpi=600)
plt.show()
