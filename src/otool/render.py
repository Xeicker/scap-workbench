#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
import gtk
import gobject

class Menu:
    """ Create Main item for TreeToolBar_toggleButtonGroup and draw all tree
    Menu
    """
    def __init__(self, id, c_toolBar):

        self.id = id
        self.btnList = []
        self.active_item = None
        self.default_item = None
        self.c_toolBar = c_toolBar
	
    def add_item(self, item, position=None):
        """ Add item to the menu list
        """

        if len(self.btnList) == 0:
            self.set_default(item)
        self.btnList.append(item)
        # vizual
        if position != None: 
            self.c_toolBar.insert_space((position*2)+1)
            self.c_toolBar.insert(item.widget, position)
        else: 
            self.c_toolBar.insert(item.widget, self.c_toolBar.get_n_items())

        item.parent = self

    def show(self):
        self.c_toolBar.show()
        self.toggle_button(self.active_item)

    def set_active(self, active):
        if active: self.show()
        else: self.c_toolBar.hide()

    def set_default(self, item):
        self.active_item = item
        self.default_item = item

    def toggle_button(self, item):
        """ Toggle selected button
        @param item selected MenuButton object
        """
        # Deselect all buttons
        if self.active_item: self.active_item.set_active(False)
        # Show selected button
        self.active_item = item
        self.active_item.set_active(True)
		
    def refresh(self):
        """ Refresh graphic content
        Async. method called after data change
        """
        raise NotImplementedError, "Function \"refresh\" is not implemented yet"

class MenuButton:
    """ Class for tree of toogleBar with toggleButtons in group
    """

    def __init__(self, id, name, c_body=None, sensitivity=None):
        """
        @param sensitivity filter function
        """
        # structure
        self.id = id
        self.name = name
        self.sensitivity = sensitivity
        self.parent = None
        self.c_body = c_body
        self.menu = None
        self.body = None

        # setings
        self.widget = gtk.ToggleToolButton()
        self.widget.set_is_important(True)
        self.widget.set_label(name)
        if self.sensitivity == None: 
            self.widget.set_sensitive(True)
        else: self.widget.set_sensitive(False)
        self.widget.show()
        self.widget.connect("toggled", self.cb_toggle, self)


    def set_active(self, active):
        self.widget.handler_block_by_func(self.cb_toggle)
        self.widget.set_active(active)
        self.set_body(active)
        if self.menu: 
            self.menu.set_active(active)
            if self.menu.active_item:
                self.menu.active_item.set_active(active)
        self.widget.handler_unblock_by_func(self.cb_toggle)

    def set_menu(self, menu):
        self.menu = menu

    def cb_toggle(self, widget, item):
        """ Change active of toggleButtons in current toolBar
        and visibility of child
        """
        self.parent.toggle_button(self)

    def set_body(self,active):
        if self.body:
            if active:
                self.body.show_all()
            else:
                self.body.hide_all()

class MenuButton_XCCDF(MenuButton):

    def __init__(self, c_body=None, sensitivity=None):
        MenuButton.__init__(self,"menu:main:btn:xccdf", "XCCDF", c_body, sensitivity)
        self.c_body = c_body
        self.body = self.draw_body()
        self.label_title = None
        self.label_description = None
        self.label_version = None
        self.label_url = None
        self.language = None

    def add_label(self,table, text, left, right, top, bottom):
        label = gtk.Label(text)
        table.attach(label, left, right, top, bottom,gtk.FILL,gtk.FILL)
        label.set_alignment(0, 0.5)
        return label
        
    def set_frame(self,body, text):
        frame = gtk.Frame(text)
        body.add(frame)
        alig = gtk.Alignment(0.5, 0.5, 1, 1)
        alig.set_padding(0, 0, 12, 0)
        frame.add(alig)
        return alig

    def set_detail(self, tile, description, version, url):
        if self.label_title: self.label_title.set_text(title)
        if self.label_description: self.label_description.set_text(description)
        if self.label_version: self.label_version.set_text(version)
        if self.label_url: self.label_url.set_text(url)

    def draw_body(self):
        body = gtk.VBox()
        alig = self.set_frame(body, "Detail")
        table = gtk.Table(5 ,2)
        alig.add(table)

        self.add_label(table, "Name: ", 0, 1, 0, 1)
        self.add_label(table, "Description: ", 0, 1, 1, 2)
        self.add_label(table, "Version: ", 0, 1, 2, 3)
        self.add_label(table, "URL: ", 0, 1, 3, 4)
        self.add_label(table, "Prefered Language: ", 0, 1, 4, 5)

        self.label_title = self.add_label(table, "None ", 1, 2, 0, 1)
        self.label_description = self.add_label(table, "None ", 1, 2, 1, 2)
        self.label_version = self.add_label(table, "None ", 1, 2, 2, 3)
        self.label_url = self.add_label(table, "None ", 1, 2, 3, 4)

        combobox = gtk.combo_box_new_text()
        combobox.append_text('English')
        combobox.append_text('Czech')
        combobox.connect('changed', self.changed_cb)
        combobox.set_active(0)
        table.attach(combobox, 1, 2, 4, 5,gtk.FILL,gtk.FILL)
        
        # generator for oval
        alig = self.set_frame(body, "Generator for OVAL")

        # operations
        alig = self.set_frame(body, "Operations")
        
        box = gtk.HButtonBox()
        box.set_layout(gtk.BUTTONBOX_START)
        btn = gtk.Button("Load File")
        box.add(btn)
        btn = gtk.Button("Save Changes")
        box.add(btn)
        btn = gtk.Button("Validate")
        box.add(btn)
        alig.add(box)

        body.hide_all()
        
        # add to conteiner
        self.c_body.add(body)
        return body

    def changed_cb(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        if index:
            print 'I prefered', model[index][0], 'Language'
        return
        
class MenuButton_profiles(MenuButton):

    def __init__(self, c_body=None, sensitivity=None):
        MenuButton.__init__(self,"menu:main:btn:xccdf", "Profiles", c_body, sensitivity)
        self.c_body = c_body
        self.label_abstract = None
        self.label_extend = None
        self.body = self.draw_body()

    def set_frame(self,body, text,pos = 1):
        frame = gtk.Frame(text)
        #frame.set_shadow_type(gtk.SHADOW_NONE)
        if pos == 1: body.pack1(frame,  resize=False, shrink=False)
        else: body.pack2(frame,  resize=False, shrink=False)
        alig = gtk.Alignment(0.5, 0.5, 1, 1)
        alig.set_padding(0, 0, 12, 0)
        frame.add(alig)
        return alig
        
    def add_label(self,table, text, left, right, top, bottom):
        label = gtk.Label(text)
        table.attach(label, left, right, top, bottom,gtk.FILL,gtk.FILL)
        label.set_alignment(0, 0.5)
        return label
        
    def draw_body(self):
        body = gtk.VPaned()

        # List of profiles
        alig = self.set_frame(body, "List of profiles")
        hbox = gtk.HBox()
        alig.add(hbox)
        scroledWindow = gtk.ScrolledWindow()
        scroledWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        hbox.pack_start(scroledWindow, expand=True, fill=True, padding=3)

        # operations with profiles
        hbox.pack_start(gtk.VSeparator(), expand=False, fill=True, padding=10)
        box = gtk.VButtonBox()
        box.set_layout(gtk.BUTTONBOX_START)
        btn = gtk.Button("Add")
        box.add(btn)
        btn = gtk.Button("Extend")
        box.add(btn)
        btn = gtk.Button("Copy")
        box.add(btn)        
        btn = gtk.Button("Delete")
        box.add(btn)
        hbox.pack_start(box, expand=False, fill=True, padding=0)

        # edit profiles
        #body.pack_start(gtk.HSeparator(), expand=False, fill=True, padding=10)
        
        alig = self.set_frame(body, "Details",2)

        table = gtk.Table(5 ,2)
        alig.add(table)

        self.add_label(table, "Abstract: ", 0, 1, 0, 1)
        self.add_label(table, "Extend: ", 0, 1, 1, 2)
        self.add_label(table, "Version: ", 0, 1, 2, 3)
        self.add_label(table, "Title: ", 0, 1, 3, 4)
        self.add_label(table, "Description: ", 0, 1, 4, 5)


        self.label_abstract = self.add_label(table, "None ", 1, 2, 0, 1)
        self.label_extend = self.add_label(table, "None ", 1, 2, 1, 2)

        self.entry_version = gtk.Entry()
        table.attach(self.entry_version, 1, 2, 2, 3,gtk.EXPAND|gtk.FILL,gtk.FILL)

        hbox = gtk.HBox()
        table.attach(hbox, 1, 2, 3, 4,gtk.EXPAND|gtk.FILL,gtk.EXPAND|gtk.FILL, 0, 3)
        self.texView_title = gtk.TextView()
        hbox.pack_start(self.texView_title, expand=True, fill=True, padding=0)
        self.button_title = gtk.Button("...")
        hbox.pack_start(self.button_title, expand=False, fill=True, padding=0)

        hbox = gtk.HBox()
        table.attach(hbox, 1, 2, 4, 5,gtk.EXPAND|gtk.FILL,gtk.EXPAND|gtk.FILL, 0, 3)
        self.texView_description = gtk.TextView()
        hbox.pack_start(self.texView_description, expand=True, fill=True, padding=0)
        self.button_description = gtk.Button("...")
        hbox.pack_start(self.button_description, expand=False, fill=True, padding=0)
        textbuffer = self.texView_description.get_buffer()
        textbuffer.set_text("asdasdasdasds")

        
        body.hide_all()
        self.c_body.add(body)
        return body



class MenuButton_oval(MenuButton):

    def __init__(self, c_body=None, sensitivity=None):
        MenuButton.__init__(self,"menu:main:btn:oval", "Oval", c_body, sensitivity)
        self.c_body = c_body
        self.title = None
        self.description = None
        self.version = None
        self.url = None
        self.language = None
        self.body = self.draw_body()


    def draw_body(self):
        body = gtk.VBox()
        frame = gtk.Frame("Detail")
        body.add(frame)
        alig = gtk.Alignment(0.5, 0.5, 1, 1)
        alig.set_padding(0, 0, 12, 0)
        frame.add(alig)
        table = gtk.Table(5 ,2)
        alig.add(table)
        
        label = gtk.Label("Name:")
        table.attach(label, 0, 1, 0, 1,gtk.FILL,gtk.FILL)
        label.set_alignment(0, 0.5)
        label = gtk.Label("Prefered Language:")
        table.attach(label, 0, 1, 4, 5,gtk.FILL,gtk.FILL)



        body.hide_all()
        self.c_body.add(body)
        return body

class Main_window:
    """TODO:
    """

    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Main window")
        self.window.set_size_request(600, 400)
        self.window.connect("delete_event", self.delete_event)
        self.vbox_main = gtk.VBox()
        self.vbox_main.show()
        self.window.add(self.vbox_main)
        
        # container for body
        vbox_body = gtk.VBox()
        vbox_body.show()
        
        #create menu

        # main menu
        vbox_menu = gtk.Toolbar()
        self.vbox_main.pack_start(vbox_menu, expand=False, fill=True, padding=0)
        self.menu = Menu("menu:main", vbox_menu)
        menu1_but1 = MenuButton("menu:main:btn:main", "Main", vbox_body)
        self.menu.add_item(menu1_but1)
        menu1_but2 = MenuButton("menu:main:btn:tailoring", "Tailoring", vbox_body)
        self.menu.add_item(menu1_but2)
        menu1_but3 = MenuButton("menu:main:btn:edit", "Edit", vbox_body)
        self.menu.add_item(menu1_but3)
        menu1_but4 = MenuButton("menu:main:btn:scan", "Scen", vbox_body)
        self.menu.add_item(menu1_but4)
        menu1_but5 = MenuButton("menu:main:btn:reports", "Reports", vbox_body)
        self.menu.add_item(menu1_but5)
        
        
        # subMenu_but_main
        vbox_submenu = gtk.Toolbar()
        self.vbox_main.pack_start(vbox_submenu, expand=False, fill=True, padding=0)
        self.submenu = Menu("menu:main", vbox_submenu)
        menu2_but1 = MenuButton_XCCDF(vbox_body)
        self.submenu.add_item(menu2_but1)
        menu2_but2 = MenuButton_oval(vbox_body)
        self.submenu.add_item(menu2_but2)
        menu1_but1.set_menu(self.submenu)

        # subMenu_but_tailoring
        vbox_submenu1 = gtk.Toolbar()
        self.vbox_main.pack_start(vbox_submenu1, expand=False, fill=True, padding=0)
        self.submenu1 = Menu("menu:tailoring", vbox_submenu1)
        menu3_but1 = MenuButton_profiles(vbox_body)
        self.submenu1.add_item(menu3_but1)
        menu3_but2 = MenuButton("menu:OVAL:btn:refines", "Refines", vbox_body)
        self.submenu1.add_item(menu3_but2)
        menu1_but2.set_menu(self.submenu1)

        # subMenu_but_edit

        # subMenu_but_scan

        # subMenu_but_reports



        self.vbox_main.pack_start(vbox_body, expand=True, fill=True, padding=0)
        
        self.window.show()
        self.menu.show()

    def delete_event(self, widget, event, data=None):
        """ close the window and quit
        """
        gtk.main_quit()
        return False

class create_menu():
    # TODO: CZ -> ENG
    """ sem se presune vytvareni menu
    bude obsahovat slovnik (jmeno taggleButtonu a ukazatel na nej), aby se dalo pridavat pod jednotliva menu
    pres ni se tedy budou moci pridavat dalsi menu
    """
    
    def __init__(self):
        return


if __name__ == "__main__":
	#otool_xample = Core_draw()
	Main_window()
	gtk.main()
