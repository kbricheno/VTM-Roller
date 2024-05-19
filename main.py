from random import randint
from math import floor

successes = 0
hungerSuccesses = 0
crits = 0
messyCrits = 0
failures = 0
hungerFailures = 0
bestialFails = 0

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
    global successes, hungerSuccesses, crits, messyCrits, failures, hungerFailures, bestialFails, \
        normalDiceList, hungerDiceList

    for result in normalDiceList:
        if result == 10:
            crits += 1
        elif result >= 6:
            successes += 1
        else:
            failures += 1

    for result in hungerDiceList:
        if result == 10:
            messyCrits += 1
        elif result >= 6:
            hungerSuccesses += 1
        elif result == 1:
            bestialFails += 1
        else:
            hungerFailures += 1


def print_results(normalDice_, hungerDice_):
    global successes, hungerSuccesses, crits, messyCrits, failures, hungerFailures, bestialFails, normalDiceList, hungerDiceList

    combinedSuccesses = successes + hungerSuccesses

    print()
    if normalDiceList:
        print(f"Normal dice ({normalDice_}): {normalDiceList}")
    if hungerDiceList:
        print(f"Hunger dice ({hungerDice_}): {hungerDiceList}")
    print()

    if combinedSuccesses + crits + messyCrits == 0:
        print(f"Oh no! 0 successes.\n"
              f"Failures: {failures} normal, {hungerFailures} hunger, and {bestialFails} bestial")

    elif crits + messyCrits >= 2:
        if messyCrits >= 1:
            additionalSuccesses = (floor((crits + messyCrits) / 2) * 4) + ((crits + messyCrits) % 2)
            print(f"Messy crit!\n"
                  f"Successes: {combinedSuccesses + additionalSuccesses} ({combinedSuccesses} success(es) + "
                  f"{messyCrits} hunger and {crits} normal crit(s)\n"
                  f"Failures: {failures} normal, {hungerFailures} hunger, and {bestialFails} bestial")
        else:
            additionalSuccesses = (floor(crits / 2) * 4) + (crits % 2)
            print(f"Crit!\n" +
                  f"Successes: {combinedSuccesses + additionalSuccesses} ({combinedSuccesses} success(es) + {crits} "
                  f"normal crits)\n" +
                  f"Failures: {failures} normal, {hungerFailures} hunger, and {bestialFails} bestial")

    else:
        print(f"No crits.\n"
              f"Successes: {combinedSuccesses + crits + messyCrits}\n"
              f"Failures: {failures} normal, {hungerFailures} hunger, and {bestialFails} bestial")

    print()


def clear_results():
    global successes, hungerSuccesses, crits, messyCrits, failures, hungerFailures, bestialFails, normalDiceList, hungerDiceList

    successes = 0
    hungerSuccesses = 0
    crits = 0
    messyCrits = 0
    failures = 0
    hungerFailures = 0
    bestialFails = 0

    normalDiceList.clear()
    hungerDiceList.clear()


def roll_again():

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


def re_roll():
    global normalDiceList

    # show existing normal rolls, receive values to re-roll
    values = get_reroll_values(normalDiceList)
    print(values)

    # pop rerolls
    # roll all popped values
    # append all rolls to normal dice list
    # evaluate again, print again


def get_reroll_values(normalDice_):

    translatedList = []

    for result in normalDice_:
        if result == 10:
            translatedList.append("crit")
        elif result >= 6:
            translatedList.append("success")
        else:
            translatedList.append("fail")

    print(f"\nHere are your normal dice results: "
          f"\nRaw values: {normalDice_}"
          f"\nResults: {translatedList}")

    while True:
        answer = input("\nPlease indicate the number of dice you'd like to re-roll in the format of "
                       "\"FAILURES, SUCCESSES, CRITS\" (up to 3 in total): ").strip()
        chosenValues = []
        for char in [*answer]:
            if char.isdigit():
                chosenValues.append(int(char))

        validValues = validate_reroll_values(chosenValues)
        if not validValues[0]:
            print(validValues[1])
            continue
        else:
            return chosenValues


def validate_reroll_values(chosenValues):

    # first, check that at least 1 number and no more than 3 were entered -- this will naturally catch string answers
    if len(chosenValues) < 1 or len(chosenValues) > 3:
        return False, "Please enter 3 whole numbers."

    # ensure user has only chosen 3 dice total
    if sum(chosenValues) > 3:
        return False, "You cannot re-roll more than 3 dice."

    # now use list comparison to make sure user hasn't tried to re-roll more of any result than they have
    availableValues = {"failures": failures, "successes": successes, "crits": crits}
    errorString = ""

    for choice in range(len(chosenValues)):
        if chosenValues[choice] > [*availableValues.values()][choice]:
            errorString += f"Too many {[*availableValues.keys()][choice]} entered. "
    if errorString:
        return False, errorString

    # passed the validation check
    return True, ""


# def pop_rerolls(normalDice_, rerollValues):

    # pop fails from list
    # pop successes from list
    # pop crits from list


def main():
    global normalDiceList, hungerDiceList

    clear_results()

    normalDice = int(get_dice(True))
    hungerDice = int(get_dice(False))

    normalDiceList = roll_dice(normalDice)
    hungerDiceList = roll_dice(hungerDice)

    evaluate_dice()

    print_results(normalDice, hungerDice)


while True:
    main()
    rollAgain = roll_again()
    if rollAgain == 0:
        re_roll()
    elif rollAgain == 1:
        continue
    else:
        break
