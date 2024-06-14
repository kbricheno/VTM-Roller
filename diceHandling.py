from random import randint
from math import floor


def roll_dice(dice):
    diceList = []
    for i in range(int(dice)):
        result = randint(1, 10)
        diceList.append(result)

    return diceList


def evaluate_dice(normalDiceList, hungerDiceList):
    resultTypes = {"successes": 0, "hungerSuccesses": 0,
                   "crits": 0, "messyCrits": 0,
                   "failures": 0, "hungerFailures": 0, "bestialFailures": 0}

    for result in normalDiceList:
        if result == 10:
            resultTypes["crits"] += 1
        elif result >= 6:
            resultTypes["successes"] += 1
        else:
            resultTypes["failures"] += 1

    for result in hungerDiceList:
        if result == 10:
            resultTypes["messyCrits"] += 1
        elif result >= 6:
            resultTypes["hungerSuccesses"] += 1
        elif result == 1:
            resultTypes["bestialFailures"] += 1
        else:
            resultTypes["hungerFailures"] += 1

    return resultTypes


def print_results(results):
    # for ease of readability below
    successes = results["successes"]
    hungerSuccesses = results["hungerSuccesses"]
    crits = results["crits"]
    messyCrits = results["messyCrits"]
    failures = results["failures"]
    hungerFailures = results["hungerFailures"]
    bestialFailures = results["bestialFailures"]

    combinedSuccesses = successes + hungerSuccesses
    combinedFailures = failures + hungerFailures + bestialFailures

    writtenResults = ""

    if combinedSuccesses + crits + messyCrits == 0:
        writtenResults += (f"Oh no! 0 successes.\n"
                           f"Failures: {combinedFailures} ({failures} normal, {hungerFailures} hunger, and "
                           f"{bestialFailures} bestial)")

    elif crits + messyCrits >= 2:
        if messyCrits >= 1:
            additionalSuccesses = (floor((crits + messyCrits) / 2) * 4) + ((crits + messyCrits) % 2)
            writtenResults += (f"Messy crit!\n"
                               f"Successes: {combinedSuccesses + additionalSuccesses} ({combinedSuccesses} "
                               f"success(es) + {messyCrits} hunger and {crits} normal crit(s))\n"
                               f"Failures: {combinedFailures} ({failures} normal, {hungerFailures} hunger, and "
                               f"{bestialFailures} bestial)")
        else:
            additionalSuccesses = (floor(crits / 2) * 4) + (crits % 2)
            writtenResults += (f"Crit!\n" +
                               f"Successes: {combinedSuccesses + additionalSuccesses} ({combinedSuccesses} "
                               f"success(es) + {crits} normal crit(s))\n" +
                               f"Failures: {combinedFailures} ({failures} normal, {hungerFailures} hunger, and "
                               f"{bestialFailures} bestial)")

    else:
        writtenResults += (f"No crits.\n"
                           f"Successes: {combinedSuccesses + crits + messyCrits}\n"
                           f"Failures: {combinedFailures} ({failures} normal, {hungerFailures} hunger, and "
                           f"{bestialFailures} bestial)")

    return writtenResults


def get_reroll_values(normalDiceList, priorResults):
    translatedList = []

    for result in normalDiceList:
        if result == 10:
            translatedList.append("crit")
        elif result >= 6:
            translatedList.append("success")
        else:
            translatedList.append("fail")

    print(f"\nHere are your normal dice results: "
          f"\nRaw values: {normalDiceList}"
          f"\nResults: {translatedList}")

    while True:
        answer = input("\nPlease indicate the number of dice you'd like to re-roll in the format of "
                       "\"FAILURES, SUCCESSES, CRITS\" (up to 3 in total): ").strip()
        chosenValues = []
        for char in [*answer]:
            if char.isdigit():
                chosenValues.append(int(char))

        validValues = validate_reroll_values(chosenValues, priorResults)
        if not validValues[0]:
            print(validValues[1])
            continue
        else:
            return chosenValues


def validate_reroll_values(chosenValues, priorResults):
    # first, check that at least 1 number and no more than 3 were entered -- this will naturally catch string answers
    if len(chosenValues) < 1 or len(chosenValues) > 3:
        return False, "Please enter 3 whole numbers."

    # ensure user has only chosen 3 dice total
    if sum(chosenValues) > 3:
        return False, "You cannot re-roll more than 3 dice."

    # now use list comparison to make sure user hasn't tried to re-roll more of any result than they have
    availableValues = {"failures": priorResults["failures"], "successes": priorResults["successes"],
                       "crits": priorResults["crits"]}
    errorString = ""

    for choice in range(len(chosenValues)):
        if chosenValues[choice] > [*availableValues.values()][choice]:
            errorString += f"Too many {[*availableValues.keys()][choice]} entered. "
    if errorString:
        return False, errorString

    # passed the validation check
    return True, ""


def pop_rerolls(normalDiceList, rerollValues):
    failsPopped = []
    successesPopped = []
    critsPopped = []

    # pop fails from list
    for resultType in range(len(rerollValues)):  # loop once for each of: fails, successes, crits
        popCounter = 0  # counter for how many fails/successes/crits we want popped

        if resultType == 0:
            for dice in reversed(normalDiceList):  # reverse list to iterate and modify in the same loop
                if dice < 6 and popCounter < rerollValues[resultType]:
                    failsPopped.append(normalDiceList.pop(normalDiceList.index(dice)))
                    popCounter += 1
        elif resultType == 1:
            for dice in reversed(normalDiceList):
                if 6 <= dice < 10 and popCounter < rerollValues[resultType]:
                    successesPopped.append((normalDiceList.pop(normalDiceList.index(dice))))
                    popCounter += 1
        else:
            for dice in reversed(normalDiceList):
                if dice == 10 and popCounter < rerollValues[resultType]:
                    critsPopped.append((normalDiceList.pop(normalDiceList.index(dice))))
                    popCounter += 1

    return normalDiceList


def print_rerolls(rerollList, normalDiceList):
    print(f"\nThe results of your re-rolls are: {rerollList}")
    print(f"New normal dice ({len(normalDiceList) + len(rerollList)}): "
          f"{normalDiceList + rerollList}")
    input("\nPress Enter to re-evaluate all of your rolls. ")


def clear_results(normalDiceList, hungerDiceList):
    normalDiceList.clear()
    hungerDiceList.clear()
