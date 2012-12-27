import curses
from . import wgmultilinetree

class TreeLineSelectable(wgmultilinetree.TreeLine):
    # NB - as print is currently defined, it is assumed that these will 
    # NOT contain multi-width characters, and that len() will correctly
    # give an indication of the correct offset
    CAN_SELECT              = '[ ]'
    CAN_SELECT_SELECTED     = '[*]'
    CANNOT_SELECT           = '   '
    CANNOT_SELECT_SELECTED  = ' * '
    
    def _print(self, left_margin=0):
        if not hasattr(self._tree_real_value, 'selected'):
            return None
        
        self.left_margin = left_margin
        self.parent.curses_pad.bkgdset(' ',curses.A_NORMAL)
        self.left_margin += self._print_tree(self.relx)
        
        SELECT_DISPLAY = None
        
        
        if self._tree_real_value.selectable:
            if self.value.selected:
                SELECT_DISPLAY = self.CAN_SELECT_SELECTED
            else:
                SELECT_DISPLAY = self.CAN_SELECT
        else:
            if self.value.selected:
                SELECT_DISPLAY = self.CANNOT_SELECT_SELECTED
            else:
                SELECT_DISPLAY = self.CANNOT_SELECT
        
        
        if self.do_colors():
            attribute_list = self.parent.theme_manager.findPair(self, 'CONTROL')
        else:
            attribute_list = curses.A_NORMAL
        
        
        #python2 compatibility
        if isinstance(SELECT_DISPLAY, bytes):
            SELECT_DISPLAY = SELECT_DISPLAY.decode()
        
        
        
        self.add_line(self.rely,
                      self.left_margin+self.relx,
                      SELECT_DISPLAY, 
                      self.make_attributes_list(SELECT_DISPLAY, attribute_list),
                      self.width-self.left_margin,
        )
        
        self.left_margin += len(SELECT_DISPLAY) + 1
        
        
        if self.highlight:
            self.parent.curses_pad.bkgdset(' ',curses.A_STANDOUT)
        super(wgmultilinetree.TreeLine, self)._print()
        
class MLTreeMultiSelect(wgmultilinetree.MLTree):
    _contained_widgets = TreeLineSelectable
    
    def h_select(self, ch):
        vl = self.values[self.cursor_line]
        vl_to_set = not vl.selected
        for v in vl.walkTree(onlyExpanded=False, ignoreRoot=False):        
            if v.selectable:
                v.selected = vl_to_set
        if self.select_exit:
            self.editing = False
            self.how_exited = True
        self.display()
        
    def get_selected_objects(self, return_node=True):
        for v in self._myFullValues.walkTree(onlyExpanded=False, ignoreRoot=False):
            if v.selected:
                if return_node:
                    yield v
                else:
                    yield v.getContent()            
    