import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import diceHandling as d

normalDiceList = []
hungerDiceList = []

# set up main application window & title it
root = Tk()
root.title("Vampire: The Masquerade | Dice Roller")
root.geometry("375x375")

# these 2 tell the widget to re-centre in the window if it's resized
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

normalDiceImages = {"success": PhotoImage(file="DiceImages/normalSuccess.png"),
                    "crit": PhotoImage(file="DiceImages/normalCrit.png"),
                    "fail": PhotoImage(file="DiceImages/normalFail.png")}

hungerDiceImages = {"success": PhotoImage(file="DiceImages/hungerSuccess.png"),
                    "crit": PhotoImage(file="DiceImages/hungerCrit.png"),
                    "fail": PhotoImage(file="DiceImages/hungerFail.png"),
                    "bestialFail": PhotoImage(file="DiceImages/hungerBestialFail.png")}

selectedButtons = []  # collects the buttons selected for re-rolling
rerollCount = 0


def assign_image(normal, die):  # function to determine which image should be shown for each die based on vtm rules
    if normal:
        if die == 10:
            image = normalDiceImages["crit"]
        elif die >= 6:
            image = normalDiceImages["success"]
        else:
            image = normalDiceImages["fail"]
    else:
        if die == 10:
            image = hungerDiceImages["crit"]
        elif die >= 6:
            image = hungerDiceImages["success"]
        elif die > 1:
            image = hungerDiceImages["fail"]
        else:
            image = hungerDiceImages["bestialFail"]
    return image


class ListButton(Button):  # i need a button that can store an index in a list of values
    def __init__(self, parent, index):
        super().__init__(master=parent)
        self.index = index
        self.selected = False
        self.defaultColor = self.cget("bg")

    def select_die(self):  # a toggle method
        global selectedButtons

        previousValue = self.selected

        if len(selectedButtons) < 3:  # only allow up to 3 selected dice
            self.selected = not self.selected
        elif self.selected:  # always allow deselection
            self.selected = False

        if self.selected != previousValue:  # update the list of button indexes if the button's state has changed
            if self.selected:
                selectedButtons.append(self.index)
            else:
                selectedButtons.remove(self.index)

        # change the button's background colour depending on whether it's selected
        self.configure(bg="#500000" if self.selected else self.defaultColor)


class ScrollableCanvas:  # class for readability + i need 2, 1 for normal & 1 for hunger
    def __init__(self, spawnParent, spawnColumn, spawnRow, normal):
        # create & configure elements
        self.normal = normal
        self.container = Frame(spawnParent)
        # canvases can have an actual size ("scrollable region") and a screen/view size ("window")
        self.canvas = Canvas(self.container)
        self.yScroll = Scrollbar(self.container, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.yScroll.set)
        # create a frame that will contain all the buttons & therefore act as the canvas' scrollable region
        self.scrollFrame = Frame(self.canvas)
        # when <Configure>d (when the scrollable frame changes size), update the frame's parent's scrollable region
        # i will never understand why this must be bound to configure & cannot just be done once after populating frame
        self.scrollFrame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # place elements
        self.container.grid(column=spawnColumn, row=spawnRow)
        self.canvas.grid(column=0, row=0)
        self.yScroll.grid(column=1, row=0, sticky=NS)
        self.canvas.create_window((0, 0), window=self.scrollFrame, anchor=NW)

        # bind mouse wheel to scroll the canvas whenever the pointer enters any part of the scrollable canvas
        # yview_scroll expects an int in either units or pages which it will scroll the canvas by
        # using a callback enables entering the direction scrolled (which on windows is +/-120 & thus way too large)
        self.container.bind("<Enter>", lambda e: self.container.bind_all("<MouseWheel>", lambda f: self.canvas.
                                                                         yview_scroll(-int(f.delta/50), "units")))
        # unbind mouse wheel scrolling when the pointer leaves the scrollable canvas
        self.container.bind("<Leave>", lambda e: self.container.unbind_all("<MouseWheel>"))

        self.buttonList = []  # store the buttons so they can be indexed for re-rolling

    def populate_frame(self, dice):
        global normalDiceImages, hungerDiceImages

        spawnAtColumn = -1
        spawnAtRow = -1

        for die in dice:
            spawnAtColumn = (spawnAtColumn + 1) % 3  # create a 3 by X grid to present the dice results in
            if spawnAtColumn == 0:
                spawnAtRow += 1

            if self.normal:  # normal-specific because normal dice must spawn as buttons for re-rolling
                button = ListButton(self.scrollFrame, len(self.buttonList))
                button.configure(image=assign_image(True, die), command=button.select_die, relief="groove")
                button.grid(column=spawnAtColumn, row=spawnAtRow)
                self.buttonList.append(button)

            else:  # hunger dice spawn as labels bc user doesn't need to click on them for re-rolling
                (ttk.Label(self.scrollFrame, image=assign_image(False, die)).
                 grid(column=spawnAtColumn, row=spawnAtRow))

        self.finalise_canvas()

    def finalise_canvas(self):  # set width & potentially disable scrollbar
        # set the width & height to show 3x3 dice (i think most people will roll 9 or fewer dice)
        dieWidth = self.scrollFrame.winfo_children()[0].winfo_reqwidth()
        self.canvas.configure(width=dieWidth * 3, height=dieWidth * 3)
        # don't need to scroll if there are 9 or fewer dice
        if len(self.scrollFrame.winfo_children()) <= 9:
            self.yScroll.grid_forget()

    def reroll_dice(self):
        global normalDiceList, hungerDiceList, selectedButtons, rerollCount

        if len(selectedButtons) > 0:  # don't do anything if no dice are selected
            rerollCount += 1

            for die in selectedButtons:
                normalDiceList[die] = d.roll_dice(1)[0]  # re-roll the die, add its value to a list, reassign its image
                self.buttonList[die].configure(image=assign_image(True, normalDiceList[die]))

            # re-evaluate all dice
            evaluatedResults = d.evaluate_dice(normalDiceList, hungerDiceList)

            # update results label, add re-roll counter
            results.set(d.print_results(evaluatedResults))
            rerollText.set(f"Re-rolled {rerollCount} time(s).")

            # deselect all dice
            for die in reversed(selectedButtons):  # select_die() removes dice from list, so reverse index
                self.buttonList[die].select_die()
            selectedButtons.clear()


# special variables that tk can read for the entry fields & text results
normalDice = StringVar()
hungerDice = StringVar()
results = StringVar()
rerollText = StringVar()

# frame widgets that will hold everything on the 2 screens, stored globally so they can be destroyed easily
inputFrame = ttk.Frame(root)
outputFrame = ttk.Frame(root)


def create_roll_input():  # generates the starting frame in which users enter dice numbers and click "roll"
    global inputFrame, rerollCount

    # clean up: if a previous roll took place, remove its frame, re-roll counter, and selected re-roll dice
    outputFrame.destroy()
    rerollCount = 0
    rerollText.set("")
    selectedButtons.clear()

    # top-level frame
    inputFrame = ttk.Frame(root, padding=50, relief="groove")
    inputFrame.grid()  # "grid" places the created widget in the window
    root.minsize(200, 220)  # ensure everything is visible at all times
    root.bind("<Return>", submit_new_roll)  # also bind return (no matter what is selected) to submit the roll

    # create a labelled frame to hold the labels and entry fields
    entryFrame = ttk.LabelFrame(inputFrame, text="Dice:", padding=5)
    entryFrame.grid(column=0, row=0, sticky=NSEW)

    # create entry labels
    ttk.Label(entryFrame, text="Normal:").grid(column=0, row=0)
    ttk.Label(entryFrame, text="Hunger:").grid(column=0, row=1)

    # create entry fields
    normalEntry = ttk.Entry(entryFrame, width=4, textvariable=normalDice, validate="key")  # validate on key press
    # register essentially holds the proposed edit and puts it through validation before setting the stringvar
    normalEntry["validatecommand"] = normalEntry.register(
        entry_validation), "%P", "%d"  # %P = key pressed, %d = action
    normalEntry.grid(column=1, row=0, padx=2.5, pady=2.5)
    # when selecting the entry field, call a temp function that highlights the existing 0s for easy overwriting
    normalEntry.bind("<FocusIn>", lambda e: normalEntry.selection_range(0, END))

    # same again for the hunger entry field
    hungerEntry = ttk.Entry(entryFrame, width=4, textvariable=hungerDice, validate="key")
    hungerEntry["validatecommand"] = hungerEntry.register(entry_validation), "%P", "%d"
    hungerEntry.grid(column=1, row=1, padx=2.5, pady=2.5)
    hungerEntry.bind("<FocusIn>", lambda e: hungerEntry.selection_range(0, END))

    # reset the default values in the entry fields (any input will overwrite this)
    normalDice.set("0")
    hungerDice.set("0")

    # create the "roll" button
    ttk.Button(inputFrame, text="Roll", command=submit_new_roll).grid(column=0, row=1, sticky=NSEW, pady=5)


def entry_validation(attemptedInput, action):  # validation that happens while the user inserts characters
    if action == "1":  # only validate on inserting characters -- overwriting, deleting, etc. is always allowed
        if not attemptedInput.isdigit():  # only allow numbers
            return False
        if len([*attemptedInput]) > 2:  # character limit of 2
            return False
        else:
            return True
    else:
        return True


def submit_new_roll(*args):  # validate the entry, then request the roll and output generation
    # this function uses *args because it can be called by both a button (no argument) and a <Return> event
    # (event argument), so it must be able to receive either 0 or 1 argument

    global normalDiceList, hungerDiceList

    # turn entry blanks into 0, ensure entry total > 0
    if not normalDice.get(): normalDice.set("0")
    if not hungerDice.get(): hungerDice.set("0")

    try:
        # check for a zero division error, meaning user entered no dice
        1 / (int(normalDice.get()) + int(hungerDice.get()))

        # roll the dice
        normalDiceList = d.roll_dice(int(normalDice.get()))
        hungerDiceList = d.roll_dice(int(hungerDice.get()))

        # generate the output
        create_roll_output()

    except ZeroDivisionError:
        tkinter.messagebox.showerror("Invalid Input", "Please enter at least one number.")


def create_roll_output():
    global normalDiceList, hungerDiceList, inputFrame, outputFrame

    inputFrame.destroy()
    outputFrame = ttk.Frame(root, padding=50, relief="groove")
    outputFrame.grid()
    root.minsize(430, 435)
    root.unbind("<Return>")  # unbind return from submitting a new roll on this screen

    # create a label to show the evaluated text results
    ttk.Label(outputFrame, textvariable=results).grid(column=0, row=0, columnspan=2, sticky=W, padx=10)

    # evaluate the dice
    evaluatedResults = d.evaluate_dice(normalDiceList, hungerDiceList)

    # populate label with evaluations
    results.set(d.print_results(evaluatedResults))

    ttk.Separator(outputFrame, orient=HORIZONTAL).grid(column=0, row=1, sticky=EW, columnspan=2, padx=10, pady=15)

    # generate scrollable canvas of buttons for normal dice, scrollable canvas of labels for hunger dice
    if normalDiceList:
        normalFrame = ttk.LabelFrame(outputFrame, text="Normal Results:")
        normalFrame.grid(column=0, row=2, sticky=N, columnspan=1 if hungerDiceList else 2, padx=10)
        normalScrollCanvas = ScrollableCanvas(normalFrame, 0, 0, True)
        normalScrollCanvas.populate_frame(normalDiceList)
        # create a button for re-rolling only if normal dice are available
        (ttk.Button(normalFrame, text="Re-Roll (Pick up to 3)", command=normalScrollCanvas.reroll_dice).
         grid(column=0, row=1, sticky=EW, padx=10, pady=10))
        # create a re-roll label only if normal dice are available
        rerollLabel = ttk.Label(outputFrame, textvariable=rerollText)
        rerollLabel.grid(column=0, row=3, sticky=N, columnspan=1 if hungerDiceList else 2, padx=10)

    if hungerDiceList:
        hungerFrame = ttk.LabelFrame(outputFrame, text="Hunger Results:")
        hungerFrame.grid(column=1 if normalDiceList else 0, row=2, sticky=N, columnspan=1 if normalDiceList else 2,
                         padx=10)
        hungerScrollCanvas = ScrollableCanvas(hungerFrame, 0, 0, False)
        hungerScrollCanvas.populate_frame(hungerDiceList)

    # create button for new roll
    ttk.Button(outputFrame, text="New Roll", command=create_roll_input).grid(column=0, row=4, sticky=N, columnspan=2,
                                                                             padx=10, pady=(15, 0))


create_roll_input()  # start the program

root.mainloop()
