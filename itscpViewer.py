#  import curses_util
#
#  menu = curses_util.Menu()
#
#  items = [ str(i) for i in range(100) ]
#  selected = menu.vend(items)
#
#  print("The following items were selected: \n")
#  print("\n".join(items), "\n")
#
#
#  import curses_util
#
#
#  def handle_input(console, input):
#      console.log("Got input: " + input) #Logs result to the output window.
#
#  console = curses_util.SimpleConsole(handle_input)
#  console.log("Welcome")


#  (0,0) to (curses.LINES - 1, curses.COLS - 1).
# begin_x = 20; begin_y = 7
#  height = 5; width = 40
#  win = curses.newwin(height, width, begin_y, begin_x)
# always add refresh()

# curs_set(False)
#



import curses
import time
import math

class itscpViewer:
        
    PL = ["adsfad", "fdsa", "aadfasdfadfaldkfj;lkj;lkjadflkjadsfjkhlkjadhflkjhkljhlkasjdhfkljahdklfjhalkdjfhalkjdhfklajhdflkajhdflkajhdlfkjahdslfkjahdlkfjhadklfhalkdjfhladdfasdfadfaldkfj;lkj;lkjadflkjadsfjkhlkjadhflkjhkljhlkasjdhfkljahdklfjhalkdjfhalkjdhfklajhdflkajhdflkajhdlfkjahdslfkjahdlkfjhadklfhalkdjfhlad", "adf32135adf3213513513adsf"]
    
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_CYAN)
        self.navigation_index = 0
        self.count = 0
        self.entry_dict = {}
        self.print_list = []

    def stop_curses(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def example_window(self):
        w = curses.newwin(20, 40, 5, 20)
        w.addstr(0, 10, "napis testowy\n")
        w.addstr( "napis testowy\n", curses.A_BLINK)
        w.addstr( "napis testowy\n", curses.A_BOLD)
        w.addstr( "napis testowy\n", curses.A_DIM)
        w.addstr( "napis testowy\n", curses.A_REVERSE)
        w.addstr( "napis testowy\n", curses.A_STANDOUT)
        w.addstr( "napis testowy\n", curses.A_UNDERLINE)
        w.addstr( "napis testowyK\n", curses.color_pair(1))
        w.refresh()

    def _build_list_entries(self):
        # TODO - change to proper lines from parser
        index = 0
        for line in itscpViewer.PL:
            self.print_list.append({"YX": (0,0), "str": "{}: {}\n".format(index, line)})
            index+=1

    def _set_entry_coordinates(self, entry_index, x, y):
        self.print_list[entry_index]['YX'] = (y,x)
    
    def _print_entry(self, entry_index, coordinates=None, highlight=False):
        
        if coordinates:
            self.stdscr.move(*coordinates)
        if highlight:
            attrib = curses.A_STANDOUT
        else:
            attrib = curses.A_NORMAL
        self.stdscr.addstr(self.print_list[entry_index]['str'],attrib)

    def defaul_window(self):
        self.stdscr.move(0,0)
        self._build_list_entries()

        for index in range(len(self.print_list)):
            y, x = self.stdscr.getyx()
            self._set_entry_coordinates(index, x, y)
            self._print_entry(index)
            self.count+=1

        self.stdscr.refresh()

    #  def _get_new_entry_coordinate(self, current_entry_number, next=True):
    #      if current_entry_number > self.count:
    #          current_entry_number = self.count
    #      elif current_entry_number < 0:
    #          return 0
    #      y, x = self.stdscr.getyx()
    #
    #      return  y + math.ceil(len(self.print_list[current_entry_number]) / curses.COLS)

    def _highligh_entry(self, entry_number):
        y, x = self.print_list[entry_number]['YX']
        self._print_entry(entry_number, (y, x), True)
        self.stdscr.refresh()

                

    def default_navigate(self):
        c = self.stdscr.getch()

        if c == ord('j'):
            self.navigation_index += 1
            if self.navigation_index > self.count:
                self.navigation_index = self.count

        elif c == ord('k'):
            self.navigation_index -= 1
            if self.navigation_index < 0:
                self.navigation_index = 0

        else:
            pass



def main(stdscr):

    i = itscpViewer()
    #  i.example_window()
    #  time.sleep(2)
    i.defaul_window()
    time.sleep(1)
    i._highligh_entry(2)
    time.sleep(5)


if __name__ == "__main__":
    #  i = itscpViewer()
    #  i.stop_curses()
    curses.wrapper(main)
    
