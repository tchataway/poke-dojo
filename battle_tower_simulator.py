# -*- coding: utf-8 -*-
import asyncio

from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import LocalhostServerConfiguration
from showdown_team_provider import ShowdownTeamProvider
from battle_tower_player import BattleTowerPlayer
import random
import os.path

async def main():
    team_provider = ShowdownTeamProvider()
    current_set = 1
    current_battle = 1
    used_trainer_names = []
    player_to_challenge = "Default"

    if not os.path.exists('.\\config\\challenger.txt'):
        print("No challenger file found. If you haven't already, follow the setup steps in the README.")
        return

    with open('.\\config\\challenger.txt') as challenger_file:
        lines = challenger_file.readlines()
        if len(lines) > 0:
            player_to_challenge = lines[0].strip()

    # Check for custom start point.
    start_point_path = '.\\config\\start_point.txt'
    if os.path.exists(start_point_path):
        with open(start_point_path) as start_point_file:
            lines = start_point_file.readlines()
            if len(lines) > 1:
                current_set = int(lines[0].strip())
                current_battle = int(lines[1].strip())


    # Check for specific trainer and team config.
    specific_trainer_config_path = '.\\config\\specific_trainer_and_team.txt'
    if os.path.exists(specific_trainer_config_path):
        with open(specific_trainer_config_path) as specific_team_file:
            lines = specific_team_file.readlines()
            if len(lines) > 1:
                trainer_name = lines[0].strip()
                team_name = lines[1].strip()

                trainer_name_and_team = team_provider.get_specific_team(trainer_name, team_name)
                player = BattleTowerPlayer(
                    player_configuration=PlayerConfiguration(trainer_name, None),
                    battle_format="gen8bdsp3v3singles",
                    server_configuration=LocalhostServerConfiguration,
                    team=trainer_name_and_team[1],
                    log_level=10,
                )
                
                await player.send_challenges(player_to_challenge, n_challenges=1)
                return

    rematch = False
    rematch_trainer_name_and_team = []
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
    
            # Get random trainer and team from set.
            trainer_name_and_team = rematch_trainer_name_and_team

            if not rematch:
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
            await player.send_challenges(player_to_challenge, n_challenges=1)
    
            if player.n_won_battles == 0:
                # Only progress to next battle if challenger won.
                current_battle = current_battle + 1
                rematch = False
            else:
                rematch = True
                rematch_trainer_name_and_team = trainer_name_and_team

        else:
            current_set = current_set + 1
            current_battle = 1

        if os.path.exists(start_point_path):
            # Overwrite start point to save progress, if file exists.
            with open(start_point_path, 'w') as start_point_file:
                start_point_file.writelines([str(current_set), '\n', str(current_battle)])

    print("Battle Tower simulation complete.")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())