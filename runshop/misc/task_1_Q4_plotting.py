"""Plotting Task 1 Q4"""

import matplotlib.pyplot as plt
import numpy as np

# Import data
stakes = "Unit"
bankroll_record_record = np.load(f"output/Q4.1_bankroll_10000_1_{stakes}.npy")
PnL_data = np.load(f"output/Q4.1_PnL_data_10000_1_{stakes}.npy")


# Compute some statistics
# Final bankroll from each simulation
final_bankrolls = [
    bankroll_record[-1] for bankroll_record in bankroll_record_record
]
final_bankroll_mean = sum(final_bankrolls) / len(final_bankrolls)
starting_bankroll = bankroll_record_record[0][0]
# Mean PnL from each simulation
PnL_mean = sum(PnL_data) / len(PnL_data)

# Plot time evolution of bankroll for each simulation
plt.figure()
for bankroll_record in bankroll_record_record:
    plt.plot(bankroll_record, linewidth=0.6, alpha=0.7, color="skyblue")

plt.title(f"Time Evolution of Bankroll - {stakes} Stakes")
plt.axhline(
    final_bankroll_mean,
    linestyle="dashed",
    color="red",
    label="Mean Final Bankroll",
)
plt.axhline(
    starting_bankroll,
    linestyle="dashed",
    color="black",
    label="Starting Bankroll",
)
plt.legend()
plt.show()

test = np.load("output/test_unit.npy")
test_mean = sum(test) / len(test)
# Plot the distribution of PnL from each simulation
plt.hist(test, bins=30, color="skyblue", edgecolor="black", alpha=0.7)
plt.xlabel("Final PnL")
plt.axvline(test_mean, linestyle="dashed", color="black", label="Mean PnL")
plt.ylabel("Number of Simulations")
plt.title(f"Distribution of PnL - {stakes} Stakes")
plt.legend()
plt.show()
