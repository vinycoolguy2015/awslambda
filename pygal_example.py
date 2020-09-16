from random import randint

class Die():
    def __init__(self, num_sides=6):
        self.num_sides = num_sides
    def roll(self):
        return randint(1, self.num_sides)
    
    
def main():
    import pygal
    import webbrowser
    
    die1 = Die()
    die2=Die(10)
    results = []
    for roll_num in range(1000):
        result = die1.roll()+die2.roll()
        results.append(result)
    frequencies = []
    numbers=die1.num_sides+die2.num_sides
    for value in range(2, numbers+1):
        frequency = results.count(value)
        frequencies.append(frequency)
    print (frequencies)
    hist = pygal.Bar()
    hist.title = "Results of rolling D"+str(die1.num_sides)+" and D"+str(die2.num_sides) +" 1000 times."
    hist.x_labels = [x for x in range(2,numbers+1)]
    hist.x_title = "Result"
    hist.y_title = "Frequency of Result"
    hist.add("D"+str(die1.num_sides)+" and D"+str(die2.num_sides), frequencies)
    hist.render_to_file('die_visual.svg')
    webbrowser.open("die_visual.svg", new=0, autoraise=True)

if __name__ == "__main__":
    main()
