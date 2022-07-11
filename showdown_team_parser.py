import re

class ShowdownTeamParser():
    def parse_team(self, team: str):
        result = {}
        current_pokemon = {}
        lines = team.split("\n")

        for line in lines:
            if line == "" and "species" in current_pokemon.keys():
                # Empty line indicates current Pokemon has been parsed.
                result[current_pokemon["species"]] = current_pokemon
                current_pokemon = {}
                continue
            elif line == "":
                continue

            if "species" not in current_pokemon.keys():
                # Parse species and hold item line.
                parts = re.findall("([A-Za-z\\s]{2,})", line)
                print("Species line, I think. Line: " + line)
                print("RegEx findall result:")
                print(parts)
                has_nickname = "(" in line
                has_hold_item = "@" in line
                current_pokemon["species"] = parts[0].strip()

                if has_nickname and has_hold_item:
                    current_pokemon["item"] = parts[2].strip()
                elif has_hold_item:
                    current_pokemon["item"] = parts[1].strip()

                continue

            if line.startswith("Ability: "):
                current_pokemon["ability"] = line.replace("Ability: ", "")
                continue

            if line.startswith("Level: "):
                current_pokemon["level"] = line.replace("Level: ", "")
                continue

            if line.endswith(" Nature"):
                current_pokemon["nature"] = line.replace(" Nature", "")
                continue

            if line.startswith("EVs: "):
                current_pokemon["evs"] = self.showdown_stat_line_to_dict(line.replace("EVs: ", ""))
                continue

            if line.startswith("IVs: "):
                current_pokemon["ivs"] = self.showdown_stat_line_to_dict(line.replace("IVs: ", ""))
                continue

            if line.startswith("- "):
                # All of our current applications for this format don't use the
                # Pokemon's known moves, but we'll save them just in case.
                if "moves" not in current_pokemon.keys():
                    current_pokemon["moves"] = []

                current_pokemon["moves"].append(line.replace("- ", ""))
                continue

        result[current_pokemon["species"]] = current_pokemon
        return result

                
    # "hp", "atk", "spa", "def", "spd", "spe"
    def showdown_stat_line_to_dict(self, stat_line):
        stats = stat_line.split("/")
        stat_dict = {}

        for stat in stats:
            parts = stat.strip().split()
            stat_dict[parts[1].lower()] = parts[0]

        return stat_dict
