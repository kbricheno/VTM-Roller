import methods as m

normalDiceList = []
hungerDiceList = []


def new_roll():  # roll a fresh set of dice
    global normalDiceList, hungerDiceList
    m.clear_results(normalDiceList, hungerDiceList)

    normalDice = int(m.get_dice(True))
    hungerDice = int(m.get_dice(False))

    normalDiceList = m.roll_dice(normalDice)
    hungerDiceList = m.roll_dice(hungerDice)

    results = m.evaluate_dice(normalDiceList, hungerDiceList)

    m.print_results(results, normalDiceList, hungerDiceList)

    return results


def roll_again_input():

    while True:
        answer = input("Roll again? (Or \"re-roll\"). ").lower().strip()
        acceptableTerms = ["re-roll", "reroll", "redo", "re-do", "willpower"]
        for word in answer.split():
            if word in acceptableTerms:
                return 0
        if "n" in [*answer]:
            return 2
        elif "y" in [*answer]:
            return 1
        else:
            print("Please type \"Y\", \"N\", or \"re-roll\"\n")
            continue


def re_roll(results):  # spend willpower to re-roll 3 existing normal dice
    global normalDiceList

    # show existing normal rolls, receive values to re-roll
    values = m.get_reroll_values(normalDiceList, results)
    diceToReroll = sum(values)

    # remove the dice we're going to re-roll from the list, return the amended list
    normalDiceList = m.pop_rerolls(normalDiceList, values)

    # roll all popped values
    newRolls = m.roll_dice(diceToReroll)

    # evaluate & print new rolls
    m.print_rerolls(newRolls, normalDiceList)

    # append all rolls to normal dice list
    normalDiceList += newRolls

    # evaluate entire set again, print again
    newResults = m.evaluate_dice(normalDiceList, hungerDiceList)
    m.print_results(newResults, normalDiceList, hungerDiceList)


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


main()
