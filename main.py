from random import randint
from math import floor

normalDiceList = []
hungerDiceList = []


def get_dice(normal):

    while True:
        dice = input("\nNormal dice: ") if normal else input("Hunger dice: ")
        if not dice.isdigit():
            print("Please enter a whole number.\n")
            continue
        else:
            return dice


def roll_dice(dice):

    diceList = []
    for i in range(int(dice)):
        result = randint(1, 10)
        diceList.append(result)

    return diceList


def evaluate_dice():
    global normalDiceList, hungerDiceList

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
    global normalDiceList, hungerDiceList

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

    print()
    if normalDiceList:
        print(f"Normal dice ({len(normalDiceList)}): {normalDiceList}")
    if hungerDiceList:
        print(f"Hunger dice ({len(hungerDiceList)}): {hungerDiceList}")
    print()

    if combinedSuccesses + crits + messyCrits == 0:
        print(f"Oh no! 0 successes.\n"
              f"Failures: {combinedFailures} ({failures} normal, {hungerFailures} hunger, and "
              f"{bestialFailures} bestial)")

    elif crits + messyCrits >= 2:
        if messyCrits >= 1:
            additionalSuccesses = (floor((crits + messyCrits) / 2) * 4) + ((crits + messyCrits) % 2)
            print(f"Messy crit!\n"
                  f"Successes: {combinedSuccesses + additionalSuccesses} ({combinedSuccesses} success(es) + "
                  f"{messyCrits} hunger and {crits} normal crit(s)\n"
                  f"Failures: {combinedFailures} ({failures} normal, {hungerFailures} hunger, and "
                  f"{bestialFailures} bestial)")
        else:
            additionalSuccesses = (floor(crits / 2) * 4) + (crits % 2)
            print(f"Crit!\n" +
                  f"Successes: {combinedSuccesses + additionalSuccesses} ({combinedSuccesses} success(es) + {crits} "
                  f"normal crits)\n" +
                  f"Failures: {combinedFailures} ({failures} normal, {hungerFailures} hunger, and "
                  f"{bestialFailures} bestial)")

    else:
        print(f"No crits.\n"
              f"Successes: {combinedSuccesses + crits + messyCrits}\n"
              f"Failures: {combinedFailures} ({failures} normal, {hungerFailures} hunger, and "
              f"{bestialFailures} bestial)")

    print()


def clear_results():
    global normalDiceList, hungerDiceList

    normalDiceList.clear()
    hungerDiceList.clear()


def roll_again_input():

    while True:
        answer = input("Roll again? (Or \"re-roll\"). ").lower().strip().split()
        acceptableTerms = ["re-roll", "reroll", "redo", "re-do", "willpower"]
        for word in answer:
            if word in acceptableTerms:
                return 0
        if "n" in [*answer]:
            return 2
        elif "y" in [*answer]:
            return 1
        else:
            print("Please type \"Y\", \"N\", or \"re-roll\"\n")
            continue


def re_roll(results):
    global normalDiceList

    # show existing normal rolls, receive values to re-roll
    values = get_reroll_values(normalDiceList, results)
    diceToReroll = sum(values)

    # remove the dice we're going to re-roll from the list, return the amended list
    normalDiceList = pop_rerolls(normalDiceList, values)

    # roll all popped values
    newRolls = roll_dice(diceToReroll)

    # evaluate & print new rolls
    print_rerolls(newRolls, normalDiceList)

    # append all rolls to normal dice list
    normalDiceList += newRolls

    # evaluate entire set again, print again
    newResults = evaluate_dice()
    print_results(newResults)


def get_reroll_values(normalDiceList_, priorResults):

    translatedList = []

    for result in normalDiceList_:
        if result == 10:
            translatedList.append("crit")
        elif result >= 6:
            translatedList.append("success")
        else:
            translatedList.append("fail")

    print(f"\nHere are your normal dice results: "
          f"\nRaw values: {normalDiceList_}"
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


def pop_rerolls(normalDiceList_, rerollValues):

    failsPopped = []
    successesPopped = []
    critsPopped = []

    # pop fails from list
    for resultType in range(len(rerollValues)):  # loop once for each of: fails, successes, crits
        popCounter = 0  # counter for how many fails/successes/crits we want popped

        if resultType == 0:
            for dice in reversed(normalDiceList_):  # reverse list to iterate and modify in the same loop
                if dice < 6 and popCounter < rerollValues[resultType]:
                    failsPopped.append(normalDiceList_.pop(normalDiceList.index(dice)))
                    popCounter += 1
        elif resultType == 1:
            for dice in reversed(normalDiceList_):
                if 6 <= dice < 10 and popCounter < rerollValues[resultType]:
                    successesPopped.append((normalDiceList_.pop(normalDiceList.index(dice))))
                    popCounter += 1
        else:
            for dice in reversed(normalDiceList_):
                if dice == 10 and popCounter < rerollValues[resultType]:
                    critsPopped.append((normalDiceList_.pop(normalDiceList.index(dice))))
                    popCounter += 1

    return normalDiceList_


def print_rerolls(rerollList, normalDiceList_):
    print(f"\nThe results of your re-rolls are: {rerollList}")
    print(f"New normal dice ({len(normalDiceList_) + len(rerollList)}): "
          f"{normalDiceList_ + rerollList}")
    input("\nPress Enter to re-evaluate all of your rolls. ")


def main():

    results = new_roll()
    while True:
        rollAgain = roll_again_input()
        if rollAgain == 0:
            re_roll(results)
        elif rollAgain == 1:
            results = new_roll()
        else:
            break


def new_roll():
    global normalDiceList, hungerDiceList

    clear_results()

    normalDice = int(get_dice(True))
    hungerDice = int(get_dice(False))

    normalDiceList = roll_dice(normalDice)
    hungerDiceList = roll_dice(hungerDice)

    results = evaluate_dice()

    print_results(results)

    return results


main()
