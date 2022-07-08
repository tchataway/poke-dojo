# -*- coding: utf-8 -*-
import asyncio

from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import LocalhostServerConfiguration
from showdown_team_provider import ShowdownTeamProvider
from battle_tower_player import BattleTowerPlayer
import random

async def main():
    team_provider = ShowdownTeamProvider()

    # Get specific trainer and team.
    #trainer_name_and_team = team_provider.get_specific_team("Palmer", "Team 3")

    # Get random trainer and team from set.
    trainer_name_and_team = team_provider.get_random_team("21 Streak Battle")

    player = BattleTowerPlayer(
        player_configuration=PlayerConfiguration(trainer_name_and_team[0], None),
        battle_format="gen8bdsp3v3singles",
        server_configuration=LocalhostServerConfiguration,
        team=trainer_name_and_team[1],
        log_level=10,
    )

    # Sending challenges to 'your_username'
    await player.send_challenges("Pugnotaur", n_challenges=1)

    # Accepting one challenge from any user
    #await player.accept_challenges(None, 1)

    # Accepting three challenges from 'your_username'
    #await player.accept_challenges('your_username', 3)

    # Playing 5 games on the ladder
    #await player.ladder(5)

    # Print the rating of the player and its opponent after each battle
    for battle in player.battles.values():
        print(battle.rating, battle.opponent_rating)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())