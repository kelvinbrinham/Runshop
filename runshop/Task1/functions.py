"""Useful Functions for Runshop"""

import random

import pandas as pd


def win_lose(probability: float) -> int:
    """
    Draws a 1 or 0 with the given probability.

    Args:
      probability: The probability of drawing a 1.

    Returns:
      1 or 0, depending on the probability.
    """
    random_number = random.random()
    if random_number < probability:
        return 1
    else:
        return 0


def unit_stakes(horses_df: pd.DataFrame) -> float:
    """
    Calculate the total PnL for the unit stakes strategy.

    Args:
        horses_df: Betting dataframe.

    Returns:
        Total PnL.
    """
    # Calculate potential return per selection (assuming I can use the outcome
    # now)
    horses_df["potential_returns"] = (
        horses_df["Early_Market_Price"] * horses_df["winner"]
    )
    # Calculate potential PnL per selection
    horses_df["PnL"] = (
        horses_df["potential_returns"] - 1
    )  # -1 to account for unit stake
    # Calculate total PnL
    total_PnL = horses_df["PnL"].sum()

    return total_PnL


def kelly_stakes(horses_df: pd.DataFrame, bankroll: float) -> float:
    """
    Calculate the total PnL for the unit stakes strategy. Normalise the total
    stake to the bankroll if Kelly suggests a total stake > bankroll. Otherwise,
    use the full Kelly.

    Args:
        horses_df: Betting dataframe.
        bankroll: Current Bankroll.

    Returns:
        Total PnL and total stake.
    """
    horses_df["kelly_stake"] = (
        horses_df["early_value"]
        / (horses_df["Early_Market_Price"] - 1)
        * bankroll
    )

    if horses_df["kelly_stake"].sum() > bankroll:
        normalisation_factor = bankroll / horses_df["kelly_stake"].sum()
        horses_df["kelly_stake"] = (
            horses_df["kelly_stake"] * normalisation_factor
        )

    horses_df["potential_returns"] = (
        horses_df["Early_Market_Price"]
        * horses_df["winner"]
        * horses_df["kelly_stake"]
    )
    # Calculate potential PnL per selection (returns - stake)
    horses_df["PnL"] = horses_df["potential_returns"] - horses_df["kelly_stake"]
    total_PnL = horses_df["PnL"].sum()
    total_stake = horses_df["kelly_stake"].sum()

    return total_PnL, total_stake
