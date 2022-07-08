# -*- coding: utf-8 -*-
import asyncio

from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import LocalhostServerConfiguration
from showdown_team_provider import ShowdownTeamProvider
from battle_tower_player import BattleTowerPlayer
import random

async def main():
    team_provider = ShowdownTeamProvider()
    current_set = 1
    current_battle = 1
    used_trainer_names = []

    # Standard set rotation
    while current_set < 8: # 8 would be Master.
        if current_battle < 8: # Only 7 battles in each set.
            set_name = str(current_set)

            if current_battle == 7:
                if current_set == 3:
                    # 21st battle, load special set.
                    set_name = "21 Streak Battle"
                elif current_set == 7:
                    # 49th battle, load special set.
                    set_name = "49 Streak Battle"
            # Get specific trainer and team.
            #trainer_name_and_team = team_provider.get_specific_team("Palmer", "Team 3")
    
            # Get random trainer and team from set.
            trainer_name_and_team = team_provider.get_random_team(set_name)

            # Check if we've used this trainer before; if so, update their name.
            trainer_name = trainer_name_and_team[0]
            name_count = 0
            
            while trainer_name in used_trainer_names:
                name_count = name_count + 1
                trainer_name = trainer_name + str(name_count)

            used_trainer_names.append(trainer_name)
    
            player = BattleTowerPlayer(
                player_configuration=PlayerConfiguration(trainer_name, None),
                battle_format="gen8bdsp3v3singles",
                server_configuration=LocalhostServerConfiguration,
                team=trainer_name_and_team[1],
                log_level=10,
            )
        
            # Sending challenges to 'your_username'.
            print("Starting battle for set " + str(current_set) + ", battle number " + str(current_battle))
            await player.send_challenges("Pugnotaur", n_challenges=1)
    
            # Battle complete; proceed to next one (even if we won!).
            current_battle = current_battle + 1
        else:
            current_set = current_set + 1
            current_battle = 1

    print("Battle Tower simulation complete.")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())