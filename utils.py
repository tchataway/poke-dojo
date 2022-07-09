class UtilityFunctions():
    def move_targets_single_pokemon(self, move_target: str):
        match move_target:
            case "adjacentAlly":
                return True
            case "adjacentAllyOrSelf":
                return True
            case "adjacentFoe":
                return True
            case "any":
                return True
            case "normal":
                return True
            case "randomNormal":
                return True
            case "scripted":
                return True
            case "self":
                return True

        return False