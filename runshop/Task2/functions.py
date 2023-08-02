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


def calc_PnL(runner_data: pd.DataFrame) -> pd.DataFrame:
    """
    Add PnL data to a dataframe of runner data.

    Args:
        runner_data: Runner bet dataframe.

    Returns:
        Runner bet dataframe with PnL data added.
    """
    # I assume EW bets are half the stake each way
    # First I calculate the PnL of the winning portion of a bet
    runner_data["returns_winner"] = (
        (1 - 0.5 * runner_data["EW"])
        * runner_data["Stake"]
        * runner_data["PriceTaken"]
        * runner_data["Winner"]
    )
    runner_data["PnL_winner_wout_deduc"] = (
        runner_data["returns_winner"]
        - (1 - 0.5 * runner_data["EW"]) * runner_data["Stake"]
    )
    runner_data["PnL_winner_w_deduc"] = runner_data["PnL_winner_wout_deduc"] * (
        1 - runner_data["Deduction"] * runner_data["Winner"]
    )
    runner_data["PnL_winner"] = runner_data["PnL_winner_w_deduc"]

    # Second, I calculate the PnL of the placed portion of a bet
    # I put the runner_data['EW'] here to cause 0 terms (Non EW bets) to give
    # NaN in this column
    runner_data["EW_odds"] = (
        runner_data["EW"]
        * (runner_data["PriceTaken"] - 1)
        / runner_data["Terms"]
        + 1
    )
    runner_data["EW_odds"] = runner_data["EW_odds"].fillna(0)
    runner_data["returns_EW"] = (
        0.5
        * runner_data["Stake"]
        * runner_data["EW_odds"]
        * runner_data["EW"]
        * runner_data["Placed"]
    )
    runner_data["returns_EW"] = runner_data["returns_EW"].fillna(0)
    runner_data["PnL_EW_wout_deduc"] = (
        runner_data["returns_EW"] - 0.5 * runner_data["Stake"]
    )
    runner_data["PnL_EW"] = runner_data["PnL_EW_wout_deduc"] * (
        1 - runner_data["Deduction"] * runner_data["Placed"]
    )

    # Sum the PnL of the winning and placed portions of a bet
    runner_data["PnL"] = runner_data["PnL_winner"] + runner_data["PnL_EW"]
    # print(len(runner_data))
    # Drop columns with no edge.
    # 1. Drop Win no place bets
    runner_data = runner_data.loc[
        (runner_data["PriceTaken"] > runner_data["BSP"])
        & (runner_data["EW"] == 0)
    ]
    # 2. Drop Place no win bets
    runner_data2 = runner_data.loc[
        (runner_data["EW_odds"] > runner_data["BSPplace"])
        & (runner_data["PriceTaken"] > runner_data["BSP"])
        & (runner_data["EW"] == 1)
    ]
    runner_data = pd.concat([runner_data, runner_data2])

    # print(len(runner_data))

    runner_data = runner_data.drop(
        columns=[
            "returns_winner",
            "PnL_winner_w_deduc",
            "PnL_EW_wout_deduc",
            "PnL_EW",
            "PnL_winner",
            "returns_EW",
            "PnL_winner_wout_deduc",
        ]
    )

    return runner_data
