#import curses_util
#
#menu = curses_util.Menu()
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


class Window:
    # TODO - add dimention?
    def __init__(self, curses_window):

        self.cursor_position = (0,0)
        self.navigation_index = 0
        self.navigation_max = 0
        self._item_count = 0
        self._window = curses_window

        self._item_list = []

        curses.use_default_colors()
        curses.start_color()
        curses.init_color(100, 280, 280, 280)
        curses.init_pair(100, curses.COLOR_YELLOW, 100)

    def _setItemPosition(self, item_index, y, x):
        self._item_list[item_index]['YX'] = (y,x)
    
    def _createItem(self, text:str):
        
        #  if coordinates:
        #      yx = coordinates
        #  else:
        #      yx = self._window.getyx()

        item = {"YX": (0,0), "text": text, "attrib": curses.A_NORMAL}

        self._item_list.append(item)
        self._item_count += 1
    
    def _highlighItem(self, item_index:int):
        assert self._item_count > item_index, "Item index out of range"
        #  self._item_list[item_index]['attrib'] = curses.A_STANDOUT

        self._window.move(*self._item_list[item_index]["YX"])
        self._window.chgat(curses.color_pair(100))

    def _printItem(self, item:dict, coordinates:tuple):
        self._window.move(*coordinates)
        self._window.addstr(item['text'], item['attrib'])
        return self._window.getyx()
        
        
    def _printItemList(self):
        coordinates = (0,0) 
        for idx in range(len(self._item_list)):
            self._setItemPosition(idx, *coordinates)
            coordinates = self._printItem(self._item_list[idx], coordinates) 

    def printWindow(self, list_to_print:list):
        for i in list_to_print:
            self._createItem(i)

        self._printItemList()

        self._highlighItem(0)

        self._window.refresh()

    #  def defaul_window(self):
    #      self.main_window.move(0,0)
    #      self._build_list_entries()
    #
    #      for index in range(len(self.print_list)):
    #          y, x = self.main_window.getyx()
    #          self._set_entry_coordinates(index, x, y)
    #          self._print_entry(index)
    #          self.count+=1
    #
    #      self.main_window.refresh()

    def navigateWindow(self):
        naviMax = self._item_count - 1

        c = self._window.getch()

        if c == ord('j'):
            self.navigation_index += 1
            if self.navigation_index > naviMax:
                self.navigation_index = naviMax

        elif c == ord('k'):
            self.navigation_index -= 1
            if self.navigation_index < 0:
                self.navigation_index = 0

        elif c == ord('q'):
            return False

        else:
            pass

        self._highlighItem(self.navigation_index)
        self._window.refresh()
        return True


class itscpViewer:
        
    PL = ["adsfad", "fdsa", "aadfasdfadfaldkfj;lkj;lkjadflkjadsfjkhlkjadhflkjhkljhlkasjdhfkljahdklfjhalkdjfhalkjdhfklajhdflkajhdflkajhdlfkjahdslfkjahdlkfjhadklfhalkdjfhladdfasdfadfaldkfj;lkj;lkjadflkjadsfjkhlkjadhflkjhkljhlkasjdhfkljahdklfjhalkdjfhalkjdhfklajhdflkajhdflkajhdlfkjahdslfkjahdlkfjhadklfhalkdjfhlad", "adf32135adf3213513513adsf"]
    
    def __init__(self, stdscr=None):

        if not stdscr:
            self.main_window = curses.initscr()
        else:
            self.main_window = stdscr

        curses.noecho()
        curses.cbreak()
        self.main_window.keypad(True)
        #curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_CYAN)
        self.navigation_index = 0
        self.print_list = []

    def stop_curses(self):
        curses.nocbreak()
        self.main_window.keypad(False)
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
            self.print_list.append("{}: {}\n".format(index, line))
            index += 1


    def SHOW(self):
        w = Window(self.main_window)
        self._build_list_entries()
        w.printWindow(self.print_list)
        while w.navigateWindow():
            pass

        #  self.example_window()

    


    #  def _get_new_entry_coordinate(self, current_entry_number, next=True):
    #      if current_entry_number > self.count:
    #          current_entry_number = self.count
    #      elif current_entry_number < 0:
    #          return 0
    #      y, x = self.stdscr.getyx()
    #
    #      return  y + math.ceil(len(self.print_list[current_entry_number]) / curses.COLS)


                

    def default_navigate(self, window:Window):
        c = self.main_window.getch()

        if c == ord('j'):
            self.navigation_index += 1
            if self.navigation_index > self.count:
                self.navigation_index = self.count

        elif c == ord('k'):
            self.navigation_index -= 1
            if self.navigation_index < 0:
                self.navigation_index = 0

        elif c == ord('q'):
            return False

        else:
            pass



def main(stdscr):

    i = itscpViewer(stdscr)
    #  i.example_window()
    #  time.sleep(2)
    i.SHOW()

    #  time.sleep(5)


   


def demo(screen):
    # save the colors and restore it later
    save_colors = [curses.color_content(i) for i in range(curses.COLORS)]
    curses.curs_set(0)
    curses.start_color()

    # use 250 to not interfere with tests later
    curses.init_color(250, 1000, 0, 0)
    curses.init_pair(250, 250, curses.COLOR_BLACK)
    curses.init_color(251, 0, 1000, 0)
    curses.init_pair(251, 251, curses.COLOR_BLACK)

    screen.addstr(0, 20, 'Test colors for r,g,b = {0, 200}\n',
                  curses.color_pair(250) | curses.A_BOLD | curses.A_UNDERLINE)
    i = 0
    for r in (0, 200):
        for g in (0, 200):
            for b in (0, 200):
                i += 1
                curses.init_color(i, r, g, b)
                curses.init_pair(i, i, curses.COLOR_BLACK)
                screen.addstr('{},{},{}  '.format(r, g, b), curses.color_pair(i))

    screen.addstr(3, 20, 'Test colors for r,g,b = {0..1000}\n',
                  curses.color_pair(251) | curses.A_BOLD | curses.A_UNDERLINE)
    j=0
    for r in range(0, 1001, 200):
        for g in range(0, 1001, 200):
            for b in range(0, 1001, 200):
                i += 1
                j += 1
                curses.init_color(i, r, g, b)
                curses.init_pair(i, curses.COLOR_BLACK, i)
                # screen.addstr('{},{},{} '.format(r, g, b), curses.color_pair(i))
                #  s = "test{0} {1} {2} {3}".format(i,r,g,b)
                #  print(s)
                screen.addstr(j, 0, "ad", curses.color_pair(i))
                #screen.addstr("test{0}: {1} {2} {3} ".format(i,r,g,b), curses.color_pair(i))

    screen.getch()
    # restore colors
    for i in range(curses.COLORS):
        curses.init_color(i, *save_colors[i])



if __name__ == "__main__":
    #  i = itscpViewer()
    #  i.stop_curses()
    curses.wrapper(main)
    #curses.wrapper(demo)

