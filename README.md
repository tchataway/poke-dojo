# The offline Pokemon Dojo
In conjunction with an offline Pokemon Showdown server, battle the teams from Brilliant Diamond and Shining Pearl's Singles format Battle Tower.
- Leverages the excellent [`poke-env`](https://github.com/hsahovic/poke-env) library to challenge a player, behaving like the in-game trainer AI does<sup>†</sup>
- Will challenge in 8 sets (sets numbered 1 to 7 and Master class) of 7 trainers each (with the 21st and 49th battles being against Palmer)
	- What trainers and teams appear in each set was taken from [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/List_of_Battle_Tower_Trainers_(Brilliant_Diamond_and_Shining_Pearl))
	- Pokemon data for each team was scraped from [Serebii](https://www.serebii.net/brilliantdiamondshiningpearl/battletower.shtml)

<sup>†</sup>AI has been coded by hand based on observations of in-game behaviour and online research and is still a work-in-progress. If you see erroneous logic, pull requests are most welcome!
## How to Use
### Environment Setup
#### Install `poke-env`
`poke-dojo` makes heavy use of the `poke-env` library. `poke-env` requires python >= 3.6 and a local [Pokemon Showdown](https://github.com/Zarel/Pokemon-Showdown) server.
```
pip install poke-env
```
#### Showdown Installation
There's one thing you need to update for your local server when running it, otherwise the normal installation instructions in the README suffice:
Trainers in the Battle Tower aren't restricted by the Item Clause. Some teams have multiple Pokemon holding a Focus Sash, for example. With that in mind, your BDSP 3v3 singles format needs to remove that clause. You can do so by:
1. Find and open `pokemon-showdown/config/formats.ts`.
2. Find the config for `[Gen 8 BDSP] 3v3 Singles` (last I checked it was lines `1015` - `1022`)
3. In the list for `ruleset`, add `'! Item Clause'`. The ruleset line should now look like:
```
ruleset: ['Flat Rules', '! Item Clause', 'Min Source Gen = 8'],
```
Without this change, Showdown will reject Battle Tower trainers' attempts to challenge you if their team violates the item clause.
#### Running the Simulator
1. Once your Showdown server is up and running, connect to it and log in.
2. Ensure you have a 3v3 singles format team ready to go.
3. Note your username (top right corner, if you're unfamiliar with Showdown).
4. Create a new folder, `config`, in `poke-dojo`'s root directory.
5. Inside `config`, create a `challenger.txt` file and inside it add the username noted in step 3, and nothing else. E.g., if your username is `SaltyBoi420`, the file would simply contain
```
SaltyBoi420
```
6. In `poke-dojo`'s root directory, run the simulator.
```PowerShell
python .\battle_tower_simulator.py
```
7. Back in Pokemon Showdown, you should have a challenge waiting for you. Accept it and get down to battling!
