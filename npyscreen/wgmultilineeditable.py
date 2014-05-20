import curses
from . import wgmultiline
from . import wgtextbox as textbox


class MultiLineEditable(wgmultiline.MultiLine):
    _contained_widgets = textbox.Textfield 
    CHECK_VALUE        = True
    
    def get_new_value(self):
        return ''
        
    def check_line_value(self, vl):
        if not vl:
            return False
        else:
            return True
            
    def edit_cursor_line_value(self):
        if len(self.values) == 0:
            self.insert_line_value()
            return True
        try:
            active_line = self._my_widgets[(self.cursor_line-self.start_display_at)]
        except IndexError:
            self._my_widgets[0]
            self.cursor_line = 0
            self.insert_line_value()
            return True
        active_line.highlight = False
        active_line.edit()
        try:
            self.values[self.cursor_line] = active_line.value
        except IndexError:
            self.values.append(active_line.value)
            if not self.cursor_line:
                self.cursor_line = 0
            self.cursor_line = len(self.values) - 1
        self.reset_display_cache()
        
        if self.CHECK_VALUE:
            if not self.check_line_value(self.values[self.cursor_line]):
                self.delete_line_value()
        
        self.display()
    
    def insert_line_value(self):
        if self.cursor_line is None:
            self.cursor_line = 0
        self.values.insert(self.cursor_line, self.get_new_value())
        self.display()
        self.edit_cursor_line_value()
    
    def delete_line_value(self):
        if len(self.values) > 0:
            del self.values[self.cursor_line]
            self.display()
    
    def h_insert_next_line(self, ch):
        if len(self.values) == self.cursor_line - 1 or len(self.values) == 0:
            self.values.append(self.get_new_value())
            self.cursor_line += 1
            self.display()
            self.edit_cursor_line_value()
        else:
            self.cursor_line += 1
            self.insert_line_value()
    
    def h_edit_cursor_line_value(self, ch):
        self.edit_cursor_line_value()
    
    def h_insert_value(self, ch):
        return self.insert_line_value()
    
    def h_delete_line_value(self, ch):
        self.delete_line_value()
    
    def set_up_handlers(self):
        super(MultiLineEditable, self).set_up_handlers()
        self.handlers.update ( {
                    ord('i'):           self.h_insert_value,
                    ord('o'):           self.h_insert_next_line,
                    curses.ascii.CR:    self.h_edit_cursor_line_value,
                    curses.ascii.NL:    self.h_edit_cursor_line_value,
                    curses.ascii.SP:    self.h_edit_cursor_line_value,
                    
                    curses.ascii.DEL:       self.h_delete_line_value,
                    curses.ascii.BS:        self.h_delete_line_value,
                    curses.KEY_BACKSPACE:   self.h_delete_line_value,
                } )
                
class MultiLineEditableTitle(wgmultiline.TitleMultiLine):
    _entry_type = MultiLineEditable
    