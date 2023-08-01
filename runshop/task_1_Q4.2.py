"""Task 1 Q4.2"""

import pandas as pd
from functions import win_lose

horses_df = pd.read_csv(".data/horses.csv").copy()[:2000]

# For this question, I will perform another Monte Carlo simulation similar to
# Q4.1. As before, I draw the winner using the probability given by
# win_fair_price. But this time, I also draw a fictional winner from the
# probabilities suggested by the other odds. I then sum the number of times each
# odds got the winner correct.

# Prepare data by converting odds into probabilities
odds_columns = [
    "win_fair_price",
    "win_starting_price",
    "Early_Market_Price",
    "Early_Model_Price",
    "Starting_Model_Price",
]
horses_df[odds_columns] = 1 / horses_df[odds_columns]

number_of_simulations = 100000
number_of_correct_winners_dict_list = []
for _ in range(number_of_simulations):
    number_of_correct_winners_dict_internal = dict()
    internal_horses_df = horses_df.copy()
    # Draw winners using above probabilities, each odds has a different drawn
    # winner
    horses_df[odds_columns] = horses_df[odds_columns].applymap(win_lose)
    # Sum the number of times each odds got the winner correct
    horses_df = horses_df.loc[horses_df["win_fair_price"] != 0]
    number_of_correct_winners_dict_internal = (
        (horses_df[odds_columns] / number_of_simulations).sum().to_dict()
    )
    number_of_correct_winners_dict_list.append(
        number_of_correct_winners_dict_internal
    )

number_of_correct_winners_dict = {
    key: sum(d[key] for d in number_of_correct_winners_dict_list)
    for key in number_of_correct_winners_dict_list[0].keys()
}

summary_dict = {
    key: value / number_of_correct_winners_dict["win_fair_price"]
    for key, value in number_of_correct_winners_dict.items()
}

print(summary_dict)
