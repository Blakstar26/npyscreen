#!/usr/bin/env python
import npyscreen
import curses


class ActionControllerSearch(npyscreen.ActionControllerSimple):
    def __init__(self, *args, **keywords):
        super(ActionControllerSearch, self).__init__(*args, **keywords)
        self.add_action('^/.*', self.set_search, False)
    
    def set_search(self, command_line, widget_proxy, live):
        self.parent.value.set_filter(command_line[1:])
        self.parent.wMain.values = self.parent.value.get()
        self.parent.wMain.display()


class SearchActive(npyscreen.FormMuttActive):
    ACTION_CONTROLER = ActionControllerSearch

class TestApp(npyscreen.NPSApp):
    def main(self):
        F = SearchActive()
        F.wStatus1.value = "Status Line "
        F.wStatus2.value = "Second Status Line "
        F.value.set_values([str(x) for x in range(500)])
        F.wMain.values = F.value.get()
        
        F.edit()


if __name__ == "__main__":
    App = TestApp()
    App.run()
