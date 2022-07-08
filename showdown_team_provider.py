import random
import csv
from os import listdir
from os.path import isfile, join

class ShowdownTeamProvider:
    def __init__(self):
        # Build trainer set directory
        self.trainer_set_directory = {}
        self.trainer_names = {}
        csv_path = "C:\\Code\\showdown-parser\\Trainer CSVs"
        trainer_files = [f for f in listdir(csv_path) if isfile(join(csv_path, f))]

        for trainer_file in trainer_files:
            csv_file = open(csv_path + "\\" + trainer_file)
            csv_reader = csv.reader(csv_file)
            name_and_set_data = []
            name_and_set_data = next(csv_reader)
            full_name = name_and_set_data[0]
            short_name = name_and_set_data[1]
            self.trainer_names[short_name] = full_name

            trainer_sets = []
            idx = 2
            while idx < len(name_and_set_data):
                set_name = name_and_set_data[idx]
                if set_name not in self.trainer_set_directory.keys():
                    self.trainer_set_directory[set_name] = []
                
                self.trainer_set_directory[set_name].append(short_name) 
                idx = idx + 1
            csv_file.close()

    def get_specific_team(self, trainer_name, team_name):
        team_file_path = "C:\\Code\\showdown-parser\\Showdown Format Teams\\" + trainer_name + "\\" + team_name + ".txt"
        team_file = open(team_file_path)
        team = team_file.read()
        team_file.close()
        return [trainer_name, team]

    def read_teams(self, trainer_name, set_name):
        print("Reading teams for " + trainer_name)
        trainer_file_path = "C:\\Code\\showdown-parser\\Trainer CSVs\\" + trainer_name + ".csv"
        trainer_file = open(trainer_file_path)
        print("Opened file. Reading first line...")
        csv_reader = csv.reader(trainer_file)
        line = []
        line = next(csv_reader)
        print("Successfully read first line. Searching for correct set...")
        teams = []
        reading_set = False

        for row in csv_reader:
            if not reading_set:
                # Find set first.
                reading_set = row[0] == set_name
                continue

            # Found set. Now collect the team names.
            if len(row) == 1 and "Team" in row[0]:
                # Team label. Add it to collection.
                teams.append(row[0])
            elif len(row) == 1:
                # New set. Bail out.
                break

        trainer_file.close()
        return teams

    def get_random_team(self, set_name: str):
        trainer_name = random.choice(self.trainer_set_directory[set_name])
        trainer_full_name = self.trainer_names[trainer_name]
        print("Randomly selected " + trainer_full_name + " from set " + set_name)
        teams = self.read_teams(trainer_name, set_name)

        # Pick a team at random and find team file.
        team = random.choice(teams)
        log = "Randomly selected " + team + " from set " + set_name
        print(log)
        
        return self.get_specific_team(trainer_name, team)