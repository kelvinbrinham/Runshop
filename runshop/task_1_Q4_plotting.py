"""Plotting Task 1 Q4"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter

# Import data
stakes = "Unit"
PnL_data = np.load(f"output/Q4.1_PnL_data_200000_{stakes}.npy")
stakes_data = np.load(f"output/Q4.1_Stake_data_100000_{stakes}.npy")
PnL_RoI_data = [PnL / stake for PnL, stake in zip(PnL_data, stakes_data)]

# Mean PnL from each simulation
PnL_RoI_mean = sum(PnL_data) / sum(stakes_data)
check = sum(PnL_RoI_data) / len(PnL_RoI_data)
print(len(PnL_RoI_data))
PnL_std = np.std(PnL_RoI_data)
PnL_RoI_data = [PnL for PnL in PnL_RoI_data if PnL < 5]
print(len(PnL_RoI_data))

# PnL_RoI_mean = PnL_mean / 100000
print(f"Mean PnL RoI: {PnL_RoI_mean}")
print(check)

# Plot the distribution of PnL from each simulation
plt.hist(PnL_RoI_data, bins=40, color="skyblue", edgecolor="black", alpha=0.7)
plt.xlabel("Final PnL")
plt.axvline(PnL_RoI_mean, linestyle="dashed", color="black", label="Mean PnL")
plt.axvline(0, linestyle="dashed", color="red", label="Break Even")
plt.ylabel("Number of Simulations")
plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
plt.title(f"Distribution of PnL - {stakes} Stakes")
plt.legend()
plt.savefig(f"output/Q4.1_PnL_distribution_{stakes}.png", dpi=600)
plt.show()
