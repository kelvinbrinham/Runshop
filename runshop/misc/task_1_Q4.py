"""
Task 1 - Q4

Here I run Monte Carlo simulations of the betting strategies shown in Q2-3.

NOTE: In Q1-3 I purposely avoided functions so that my method was clear. To
avoid clutter, I will use functions here to perform the steps I took in Q1-3.
Namely, calculating PnL for a given staking strategy. The functions are in the
functions script.
"""

import time
from typing import Tuple

import numpy as np
import pandas as pd
from functions import kelly_stakes, unit_stakes, win_lose

horses_df = pd.read_csv(".data/horses.csv").copy()
# Choose selection (bets with +ve value)
horses_df["early_value"] = (
    horses_df["Early_Market_Price"] / horses_df["Early_Model_Price"] - 1
)
horses_df["selection"] = horses_df["early_value"] > 0
horses_df = horses_df[horses_df["selection"] is True].drop(
    columns=["selection"]
)
horses_df["win_prob"] = 1 / horses_df["win_fair_price"]

start_time = time.time()
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Q4 - Unit Stakes/Kelly Stakes


def monte_carlo_betting(
    stakes: str,
    number_of_simulations: int,
    number_of_betting_days: int,
    horses_df: pd.DataFrame,
) -> Tuple[list, list]:
    """
    Function to perform the simulation.

    Args:
        stakes: 'Kelly' or 'Unit' stakes.
        number_of_simulations: Number of simulations.
        number_of_betting_days: Number of betting days.
        horses_df: Betting dataframe.

    Returns:
        PnL data for each simulation and bankroll data for each simulation.
    """
    # Hardcode bankroll
    if stakes != "Unit" and stakes != "Kelly":
        raise ValueError("Stakes must be either Unit or Kelly")

    starting_bankroll = 100000
    # This stores final PnL for each simulation
    PnL_data = []
    # This stores the time-series bankroll data for each simulation
    bankroll_record_record = []
    for j in range(number_of_simulations):
        bankroll = starting_bankroll
        bankroll_record = [starting_bankroll]
        test = []
        for i in range(number_of_betting_days):
            bankroll = starting_bankroll
            # Choose winner (1 or 0) based on the probability given by 1 /
            # win_fair_price
            internal_horses_df = horses_df.copy()
            internal_horses_df["winner"] = internal_horses_df["win_prob"].apply(
                win_lose
            )
            # Calculate PnL
            if stakes == "Unit":
                # Check there is sufficient bankroll to bet on all selections
                if bankroll < len(internal_horses_df):
                    raise ValueError("Bankroll < number of bets")
                PnL = unit_stakes(internal_horses_df)

            elif stakes == "Kelly":
                PnL = kelly_stakes(
                    horses_df=internal_horses_df, bankroll=bankroll
                )

            # Update bankroll
            bankroll += PnL
            # Record time-series bankroll data
            bankroll_record.append(bankroll)
            test.append(PnL)

        # Store simulation data
        bankroll_record_record.append(bankroll_record)
        PnL_data.append(bankroll_record[-1] / starting_bankroll - 1)

    return PnL_data, bankroll_record_record, test


# Run simulations
number_of_simulations = 1
number_of_betting_days = 5000
stakes = "Unit"
PnL_data, bankroll_record_record, test = monte_carlo_betting(
    stakes=stakes,
    number_of_simulations=number_of_simulations,
    number_of_betting_days=number_of_betting_days,
    horses_df=horses_df,
)

# Save data
np.save(
    f"output/Q4.1_PnL_data_{number_of_betting_days}_{number_of_simulations}_"
    f" {stakes}.npy",
    PnL_data,
)
np.save(
    f"output/Q4.1_bankroll_{number_of_betting_days}_{number_of_simulations}_"
    f" {stakes}.npy",
    bankroll_record_record,
)
np.save("output/test_unit.npy", test)

end_time = time.time()
print(f"Q4.1: Time taken: {(end_time - start_time) // 60} minutes")
