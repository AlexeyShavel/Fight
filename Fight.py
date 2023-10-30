import random
import datetime
from Common import State
from Perks import allPerks
import pandas as pd
import itertools


def get_perks_statistics(tries, allPerks):

    # creating empty data frame
    df_perks_full = pd.DataFrame(columns=['fight_id', 'perk', 'wins', 'fights', 'hp_diff'])

    #creating all possible pairs of perks
    perk_pairs = list(itertools.permutations(allPerks, 2))

    #the battle of one pair is repeated a specified number of times
    for perk1, perk2 in perk_pairs:
        for i in range(tries):

            #resetting inputs
            result = [0,0]

            random.seed(i)   #can be disabled to add more randomness
            state = State()
            warrior = state.Players[0]
            wizard = state.Players[1]
            warrior.addPerk(perk1)
            wizard.addPerk(perk2)

            #creating empty dataframes for each try
            df_perks = pd.DataFrame(columns = ['fight_id', 'perk', 'wins', 'hp_diff'])

            state.Game(result)

            # fixing results
            df_perks['perk'] = [perk1.name, perk2.name]
            df_perks['wins'] = result
            hp_diff = warrior.hp - wizard.hp
            df_perks['hp_diff'] = [hp_diff, -hp_diff]
            df_perks['fights'] = [1, 1]

            #merge local df with main df
            df_perks_full = pd.concat([df_perks_full, df_perks], axis=0)

    print("")
    print("WinRate Stat")

    #calculating statistics
    perks_stats = df_perks_full.groupby('perk').agg({'wins': 'sum', 'fights': 'sum', 'hp_diff': 'mean'}).reset_index()
    perks_stats['winrate'] = perks_stats['wins']/perks_stats['fights']
    perks_stats['winrate'] = perks_stats['winrate'].astype('float')
    perks_stats['winrate'] = perks_stats['winrate'].round(2)
    perks_stats = perks_stats.rename(columns = {'hp_diff':'avg_hp_diff'} )

    print(perks_stats)

    #writing results to csv files
    tm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    tm = tm.replace(':', '-')

    df_perks_full.to_csv(f'fights_perks_results_{tm}.csv', index=False)
    perks_stats.to_csv(f'perks_stats_{tm}.csv', index=False)

#function gets the number of fights for each perk pair and a list of all perks
get_perks_statistics(100, allPerks)