"""Task 2"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Import data
runner_bets_df = pd.read_csv(".data/runner_bets.csv")

# Clean data
original_length = len(runner_bets_df)
runner_bets_df = runner_bets_df.dropna()
print(
    "Discarded", original_length - len(runner_bets_df), "rows due to NaN values"
)
# Take -1 values in placed and winner to be 0
runner_bets_df["Placed"] = runner_bets_df["Placed"].replace(-1, 0)
runner_bets_df["Winner"] = runner_bets_df["Winner"].replace(-1, 0)
# Remove duplicates
original_length = len(runner_bets_df)
runner_bets_df.drop_duplicates(inplace=True)
print(
    "Discarded",
    original_length - len(runner_bets_df),
    "rows due to duplicate rows",
)
# Remove rows where PriceTaken is 0
original_length = len(runner_bets_df)
runner_bets_df = runner_bets_df[runner_bets_df["PriceTaken"] != 0]
print(
    "Discarded",
    original_length - len(runner_bets_df),
    "rows due to PriceTaken being 0",
)
# Remove rows where PriceTaken is < 1
original_length = len(runner_bets_df)
runner_bets_df = runner_bets_df[runner_bets_df["PriceTaken"] >= 1]
print(
    "Discarded",
    original_length - len(runner_bets_df),
    "rows due to PriceTaken being < 1",
)
# Remove rows where there is an EW bet but the terms are 0
original_length = len(runner_bets_df)
runner_bets_df = runner_bets_df.loc[
    (runner_bets_df["EW"] != 1) | (runner_bets_df["Terms"] != 0)
]
print(
    "Discarded",
    original_length - len(runner_bets_df),
    "rows due to Terms being 0 in an EW bet",
)
# Remove rows with 0 BSP or BSPplace
original_length = len(runner_bets_df)
runner_bets_df = runner_bets_df.loc[
    (runner_bets_df["BSP"] != 0) & (runner_bets_df["BSPplace"] != 0)
]
print(
    "Discarded",
    original_length - len(runner_bets_df),
    "rows due to 0 BSP or BSPplace",
)

# Save clean data for other scripts
runner_bets_df.to_csv(".data/runner_bets_clean.csv", index=False)
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

# I assume EW bets are half the stake each way
# First I calculate the PnL of the winning portion of a bet
runner_bets_df["returns_winner"] = (
    (1 - 0.5 * runner_bets_df["EW"])
    * runner_bets_df["Stake"]
    * runner_bets_df["PriceTaken"]
    * runner_bets_df["Winner"]
)
runner_bets_df["PnL_winner_wout_deduc"] = (
    runner_bets_df["returns_winner"]
    - (1 - 0.5 * runner_bets_df["EW"]) * runner_bets_df["Stake"]
)
runner_bets_df["PnL_winner_w_deduc"] = runner_bets_df[
    "PnL_winner_wout_deduc"
] * (1 - runner_bets_df["Deduction"] * runner_bets_df["Winner"])
runner_bets_df["PnL_winner"] = runner_bets_df["PnL_winner_w_deduc"]

# Second, I calculate the PnL of the placed portion of a bet
# I put the runner_bets_df['EW'] here to cause 0 terms (Non EW bets) to give
# NaN in this column
runner_bets_df["EW_odds"] = (
    runner_bets_df["EW"]
    * (runner_bets_df["PriceTaken"] - 1)
    / runner_bets_df["Terms"]
    + 1
)
runner_bets_df["EW_odds"] = runner_bets_df["EW_odds"].fillna(0)
runner_bets_df["returns_EW"] = (
    0.5
    * runner_bets_df["Stake"]
    * runner_bets_df["EW_odds"]
    * runner_bets_df["EW"]
    * runner_bets_df["Placed"]
)
runner_bets_df["returns_EW"] = runner_bets_df["returns_EW"].fillna(0)
runner_bets_df["PnL_EW_wout_deduc"] = (
    runner_bets_df["returns_EW"] - 0.5 * runner_bets_df["Stake"]
)
runner_bets_df["PnL_EW"] = runner_bets_df["PnL_EW_wout_deduc"] * (
    1 - runner_bets_df["Deduction"] * runner_bets_df["Placed"]
)

# Sum the PnL of the winning and placed portions of a bet
runner_bets_df["PnL"] = runner_bets_df["PnL_winner"] + runner_bets_df["PnL_EW"]

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

# Calculate EV (EV is distributive => calculate EV for winning and EV for
# placing separately)
# Calculate EV for winning portion of bet
runner_bets_df["EV_win"] = runner_bets_df["Stake"] * (
    (1 / runner_bets_df["BSP"])
    * (1 - 0.5 * runner_bets_df["EW"])
    * (runner_bets_df["PriceTaken"] - 1)
    * (1 - runner_bets_df["Deduction"])
    - (1 - 1 / runner_bets_df["BSP"]) * (1 - 0.5 * runner_bets_df["EW"])
)

# Calculate EV for placing portion of bet
runner_bets_df["EV_placed"] = (
    runner_bets_df["EW"]
    * 0.5
    * runner_bets_df["Stake"]
    * (
        (1 / runner_bets_df["BSPplace"])
        * ((runner_bets_df["PriceTaken"] - 1) / runner_bets_df["Terms"] + 1 - 1)
        * (1 - runner_bets_df["Deduction"])
        - (1 - 1 / runner_bets_df["BSPplace"])
    )
)

runner_bets_df["EV_placed"] = runner_bets_df["EV_placed"].fillna(0)

# Sum EV for winning and placing portions of bet
runner_bets_df["EV"] = runner_bets_df["EV_win"] + runner_bets_df["EV_placed"]
# Calculate EV ROI for Question 2
runner_bets_df["RoI"] = runner_bets_df["PnL"] / runner_bets_df["Stake"]
runner_bets_Q3_df = runner_bets_df.copy()
print(runner_bets_df.head())

# Drop columns used for calculations
runner_bets_df = runner_bets_df.drop(
    columns=[
        "EV_win",
        "returns_winner",
        "EV_placed",
        "PnL_winner_w_deduc",
        "PnL_EW_wout_deduc",
        "PnL_EW",
        "PnL_winner",
        "returns_EW",
        "PnL_winner_wout_deduc",
    ]
)

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

# Plotting
# As I understand the question, I group the data into daily data.
# (I did also convert into timestamps, order and plot the timestamp data but
# the question says 'as a function of time in days')
# First I sum the daily EV and PnL in a new dataframe
runner_bets_daily_df = runner_bets_df.copy()
runner_bets_daily_df = runner_bets_daily_df.groupby("Date")[
    ["PnL", "EV", "ExpROI", "RoI"]
].sum()
runner_bets_daily_Q2_df = runner_bets_daily_df.copy()

# Calculate cumulative PnL
runner_bets_daily_df["cum_PnL"] = runner_bets_daily_df["PnL"].cumsum()
# Calculate cumulative EV
runner_bets_daily_df["cum_EV"] = runner_bets_daily_df["EV"].cumsum()

# Plot cumulative PnL and EV
plt.figure(figsize=(10, 6))
runner_bets_daily_df["cum_PnL"].plot(label="Cumulative PnL")
runner_bets_daily_df["cum_EV"].plot(label="Cumulative EV")
plt.title("Cumulative PnL and EV of runners over time")
plt.xlabel("Date")
plt.legend(loc="lower left")
# plt.savefig('output/cum_PnL_EV.png', dpi=600)


# Calculate 2-week rolling PnL and EV average.
runner_bets_daily_df["rolling_PnL"] = (
    runner_bets_daily_df["PnL"].rolling(14).mean()
)
runner_bets_daily_df["rolling_EV"] = (
    runner_bets_daily_df["EV"].rolling(14).mean()
)
runner_bets_daily_df = runner_bets_daily_df.dropna()

# Plot 2-week rolling PnL and EV average.
plt.figure(figsize=(10, 6))
runner_bets_daily_df["rolling_PnL"].plot(label="2-Week Rolling PnL")
runner_bets_daily_df["rolling_EV"].plot(label="2-Week Rolling EV")
plt.title("2-Week Rolling PnL and EV of runners over time")
plt.xlabel("Date")
plt.legend(loc="lower left")
plt.gca().ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
# plt.savefig('output/rolling_PnL_EV.png', dpi=600)
# plt.show()


runner_bets_daily_df.to_csv(".data/runner_bets_daily.csv", index=False)

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Question 2
print("Mean RoI", runner_bets_daily_Q2_df["RoI"].mean())
print("Mean ExpROI", runner_bets_daily_Q2_df["ExpROI"].mean())

# Are bets with larger ExpROI more valuable?
# I plot the ExpROI against the EV to see if there is a correlation.
plt.figure(figsize=(10, 6))
plt.scatter(runner_bets_df["ExpROI"], runner_bets_df["EV"], alpha=0.5)
# Fit a line to the data with OLS
z = np.polyfit(runner_bets_df["ExpROI"], runner_bets_df["EV"], 1)
p = np.poly1d(z)
plt.plot(runner_bets_df["ExpROI"], p(runner_bets_df["ExpROI"]), "r--")
# Give the correlation coefficient
cor = np.corrcoef(runner_bets_df["ExpROI"], runner_bets_df["EV"])[0, 1]
print("Correlation coefficient:", cor)
# Give the R^2 value
print("R^2 value:", cor**2)
plt.title("EV vs ExpROI")
plt.xlabel("EV")
plt.ylabel("RoI")
# plt.savefig('output/ExpROI_vs_RoI.png', dpi=600)
# plt.show()

# Does time of day effect EV?
# I plot the time of day against the EV to see if there is a correlation.
# First order the dataframe by time
# Convert to datetime
runner_bets_df["Time_Placed"] = pd.to_datetime(runner_bets_df["Time_Placed"])
runner_bets_df["Time_Placed"] = (
    runner_bets_df["Time_Placed"].dt.hour * 3600
    + runner_bets_df["Time_Placed"].dt.minute * 60
    + runner_bets_df["Time_Placed"].dt.second
)
print(runner_bets_df["Time_Placed"])
runner_bets_df = runner_bets_df.sort_values(by=["Time_Placed"])
# Convert time to seconds since midnight


print(runner_bets_df["Time_Placed"])
plt.figure(figsize=(10, 6))
plt.scatter(runner_bets_df["Time_Placed"], runner_bets_df["EV"], alpha=0.5)
# Fit a line to the data with OLS
z = np.polyfit(runner_bets_df["Time_Placed"], runner_bets_df["EV"], 1)
p = np.poly1d(z)
plt.plot(runner_bets_df["Time_Placed"], p(runner_bets_df["Time_Placed"]), "r--")
# Give the correlation coefficient
cor = np.corrcoef(runner_bets_df["Time_Placed"], runner_bets_df["EV"])[0, 1]
print("Correlation coefficient:", cor)
# Give the R^2 value
print("R^2 value:", cor**2)
plt.title("EV vs Time_Placed")
plt.xlabel("Time_Placed")
plt.ylabel("EV")
# plt.savefig('output/Time_Placed_vs_EV.png', dpi=600)
# plt.show()


# Are bets with larger stake more valuable?
# I plot the stake against the EV to see if there is a correlation.
plt.figure(figsize=(10, 6))
plt.scatter(runner_bets_df["Stake"], runner_bets_df["EV"], alpha=0.5)
# Fit a line to the data with OLS
z = np.polyfit(runner_bets_df["Stake"], runner_bets_df["EV"], 1)
p = np.poly1d(z)
plt.plot(runner_bets_df["Stake"], p(runner_bets_df["Stake"]), "r--")
# Give the correlation coefficient
cor = np.corrcoef(runner_bets_df["Stake"], runner_bets_df["EV"])[0, 1]
print("Correlation coefficient:", cor)
# Give the R^2 value
print("R^2 value:", cor**2)
plt.title("EV vs Stake")
plt.xlabel("EV")
plt.ylabel("Stake")
# plt.savefig('output/Stake_vs_EV.png', dpi=600)
# plt.show()

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

# Question 3

# Rank the betters by RoI (PnL / Stake)
# First groupby Runner
runner_bets_Q3_sum_df = runner_bets_Q3_df.copy()
runner_bets_Q3_horse_df = runner_bets_Q3_df.copy()
runner_bets_Q3_sum_df = runner_bets_Q3_sum_df.groupby("Runner")[
    ["PnL", "Stake"]
].sum()
# Calculate RoI
runner_bets_Q3_sum_df["RoI"] = (
    runner_bets_Q3_sum_df["PnL"] / runner_bets_Q3_sum_df["Stake"]
)
# Sort by RoI
runner_bets_Q3_sum_df = runner_bets_Q3_sum_df.sort_values(
    by=["RoI"], ascending=False
)
# Print top 15
print(runner_bets_Q3_sum_df.head(15))
print(len(runner_bets_Q3_sum_df))

# Calculate the number of bets placed by each runner
runner_bets_Q3_df["Num_Bets"] = runner_bets_Q3_df.groupby("Runner")[
    "Runner"
].count()
# Sort by number of bets
runner_bets_Q3_df = runner_bets_Q3_df.sort_values(
    by=["Num_Bets"], ascending=True
)
# Print bottom 15
print(runner_bets_Q3_df.head(15))


# Calculate the total Stake and PnL by horse
runner_bets_Q3_horse_df = runner_bets_Q3_horse_df.groupby("Horse")[
    ["PnL", "Stake"]
].sum()

# Plot PnL vs Stake
plt.figure(figsize=(10, 6))
plt.scatter(
    runner_bets_Q3_horse_df["Stake"], runner_bets_Q3_horse_df["PnL"], alpha=0.5
)
# Fit a line to the data with OLS
z = np.polyfit(
    runner_bets_Q3_horse_df["Stake"], runner_bets_Q3_horse_df["PnL"], 1
)
p = np.poly1d(z)
plt.plot(
    runner_bets_Q3_horse_df["Stake"], p(runner_bets_Q3_horse_df["Stake"]), "r--"
)
# Give the correlation coefficient
cor = np.corrcoef(
    runner_bets_Q3_horse_df["Stake"], runner_bets_Q3_horse_df["PnL"]
)[0, 1]
print("Correlation coefficient:", cor)
# Give the R^2 value
print("R^2 value:", cor**2)
plt.title("PnL vs Stake")
plt.xlabel("Stake")
plt.ylabel("PnL")
# plt.savefig('output/PnL_vs_Stake.png', dpi=600)
plt.show()
