"""Task 2"""

import matplotlib.pyplot as plt
import pandas as pd
from functions import calc_PnL, win_lose

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Import data
runner_bets_df = pd.read_csv(".data/runner_bets_clean.csv")


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Monte Carlo Simulations:
# Repeat the process of calculating daily EV from Question 1, but draw winner
# and placed variables (0 or 1) randomly using the probabilities suggested by
# BSP and BSPplace respectively. Repeat this process and plot the distribution
# of EVs.

num_sims = 1000
data = []
for _ in range(num_sims):
    internal_df = runner_bets_df.copy()
    # Draw winner:
    internal_df["Winner"] = (1 / internal_df["BSP"]).apply(win_lose)
    # Ensure horse has been placed if it has won
    # NOTE: BSP represents the odds of winning AND placing as you must place
    # if you win. Therefore, I force all wins to be placed here:
    internal_df.loc[internal_df["Winner"] == 1, "Placed"] = 1

    # Draw placed:
    # NOTE: BSPplace represents the probability of placing GIVEN that you have
    # NOT won. Therefore, I only draw the placed variable for horses that have
    # not won:
    internal_df.loc[internal_df["Winner"] == 0, "Placed"] = (
        1 / internal_df.loc[internal_df["Winner"] == 0, "BSPplace"]
    ).apply(win_lose)

    # To avoid clutter, I repeat the process of calculating EV from Question 1
    # using a function:
    internal_df = calc_PnL(runner_data=internal_df)

    internal_bets_daily_df = internal_df.groupby("Date")[["PnL"]].sum()
    internal_bets_daily_df["cum_PnL"] = internal_bets_daily_df["PnL"].cumsum()
    internal_bets_daily_df["rolling_PnL"] = (
        internal_bets_daily_df["PnL"].rolling(14).mean()
    )
    # internal_bets_daily_df['rolling_PnL'].plot()
    # Calculate total PnL:
    total_PnL = internal_df["PnL"].sum()
    data.append(total_PnL)

runner_bets_daily_df = pd.read_csv(".data/runner_bets_daily.csv")
# total_PnL = runner_bets_daily_df['PnL'].sum()
cumulative_EV = runner_bets_daily_df["EV"].sum()
plt.hist(data, bins=20, color="skyblue", edgecolor="black", alpha=0.7)
plt.axvline(cumulative_EV, color="r", linestyle="dashed", linewidth=1)
# plt.axvline(total_PnL, color='b', linestyle='dashed', linewidth=1)
plt.show()
print("Mean PnL:", sum(data) / len(data))
print("EV", cumulative_EV)
