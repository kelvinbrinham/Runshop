"""
Task 1 - Q1-3

For the following questions, assume that you can only bet the Early_Market_Price
and the only information that you have is your Early_Model_Price.
"""

import pandas as pd

horses_df = pd.read_csv(".data/horses.csv").copy()
# Drop duplicates (there aren't any in this case)
horses_df.drop_duplicates(subset=["race_number", "saddle_number"], inplace=True)

# print(horses_df.head())

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

# Q1:
# Work out value for each selection based on Early_Market_Price (Odds) and
# Early_Model_Price (Representing the probability I think the horse will win).
horses_df["early_value"] = (
    horses_df["Early_Market_Price"] / horses_df["Early_Model_Price"] - 1
)
# Work out the selections with value > 0 (worth betting on based on 'my' model)
horses_df["selection"] = horses_df["early_value"] > 0
number_of_selections = len(horses_df[horses_df["selection"] is True])
print(f"Q1: Number of selections: {number_of_selections}")

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

# Q2:
# 2.1 - Unit stakes (I assume this means 1 unit capital per selection)
# Drop non selections
horses_df = horses_df[horses_df["selection"] is True].drop(
    columns=["selection"]
)
total_stake_unit = number_of_selections
# Calculate potential return per selection (assuming I can use the outcome now,
# so It is not really potential return)
horses_df["returns"] = horses_df["Early_Market_Price"] * horses_df["winner"]
# Calculate potential PnL per selection
horses_df["PnL"] = horses_df["returns"] - 1  # -1 to account for unit stake
# Store this for Q3
horses_unit_stake_df = horses_df.copy().drop(columns=["returns", "PnL"])
# Calculate total PnL
total_PnL = horses_df["PnL"].sum()
print(f"Q2.1.1 Unit Stake Total Stake: {total_stake_unit}")
# I can calculate the RoI by dividing the total PnL by the total stake because
# the individual stakes are all the same (1 unit).
total_PnL_RoI = total_PnL / total_stake_unit
print(f"Q2.1.2 Unit Stake Total PnL RoI: {total_PnL_RoI}")

# 2.2 - Kelly Stakes - 100,000 bankroll
# Drop previous returns and PnL columns
horses_df = horses_df.drop(columns=["returns", "PnL"])
# Calculate Kelly stake for each selection (value - 1)/(odds - 1) * bankroll
bankroll = 100000
horses_df["kelly_stake"] = (
    horses_df["early_value"] / (horses_df["Early_Market_Price"] - 1) * bankroll
)
# We see the total stake from kelly is > bankroll.
# I therefore choose to Normalise the total stake to the total bankroll. I.e.
# Use a fractional kelly stake to force our total stake to be equal to our
# bankroll.
normalisation_factor = bankroll / horses_df["kelly_stake"].sum()
horses_df["kelly_stake"] = horses_df["kelly_stake"] * normalisation_factor
# Total stake should now be equal to bankroll
total_stake_kelly = horses_df["kelly_stake"].sum()
print(f"Q2.2.1 Kelly Stake Total Stake: {total_stake_kelly}")

horses_df["potential_returns"] = (
    horses_df["Early_Market_Price"]
    * horses_df["winner"]
    * horses_df["kelly_stake"]
)
# Calculate potential PnL per selection (returns - stake)
horses_df["PnL"] = horses_df["potential_returns"] - horses_df["kelly_stake"]
horses_kelly_stake_df = horses_df.copy().drop(
    columns=["potential_returns", "PnL"]
)
# Calculate total PnL_RoI
total_PnL_RoI = horses_df["PnL"].sum() / total_stake_kelly
print(f"Q2.2.2 Kelly Stake Total PnL RoI: {total_PnL_RoI}")

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

# Q3:
# 3.1 - Unit stakes
# Using the unit stake data from Q2.1:
# Calculate the data needed for EV calculation

horses_unit_stake_df["Prob_win"] = 1 / horses_unit_stake_df["win_fair_price"]
horses_unit_stake_df["Prob_lose"] = 1 - horses_unit_stake_df["Prob_win"]
horses_unit_stake_df["winnings"] = (
    horses_unit_stake_df["Early_Market_Price"] - 1
)
horses_unit_stake_df["losses"] = 1
# Calculate the expected value of each selection
horses_unit_stake_df["EV"] = (
    horses_unit_stake_df["Prob_win"] * horses_unit_stake_df["winnings"]
    - horses_unit_stake_df["Prob_lose"] * horses_unit_stake_df["losses"]
)
print(horses_unit_stake_df.head())
horses_unit_stake_df = horses_unit_stake_df.drop(
    columns=["Prob_win", "Prob_lose", "winnings", "losses"]
)
# Calculate the total EV
total_EV = horses_unit_stake_df["EV"].sum()
# Calculate the EV RoI
total_EV_RoI = total_EV / total_stake_unit
print(f"Q3.1 Unit Stake Total EV RoI: {total_EV_RoI}")


# 3.2 - Kelly Stakes
# Using the kelly stake data from Q2.2:
horses_kelly_stake_df["Prob_win"] = 1 / horses_kelly_stake_df["win_fair_price"]
horses_kelly_stake_df["Prob_lose"] = 1 - horses_kelly_stake_df["Prob_win"]
horses_kelly_stake_df["winnings"] = horses_kelly_stake_df["kelly_stake"] * (
    horses_kelly_stake_df["Early_Market_Price"] - 1
)
horses_kelly_stake_df["losses"] = horses_kelly_stake_df["kelly_stake"]
# Calculate the expected value of each selection
horses_kelly_stake_df["EV"] = (
    horses_kelly_stake_df["Prob_win"] * horses_kelly_stake_df["winnings"]
    - horses_kelly_stake_df["Prob_lose"] * horses_kelly_stake_df["losses"]
)
horses_kelly_stake_df = horses_kelly_stake_df.drop(
    columns=["Prob_win", "Prob_lose", "winnings", "losses"]
)
# Calculate the total EV
total_EV = horses_kelly_stake_df["EV"].sum()
# Calculate the EV RoI
total_EV_RoI = total_EV / total_stake_kelly
print(f"Q3.2 Kelly Stake Total EV RoI: {total_EV_RoI}")
