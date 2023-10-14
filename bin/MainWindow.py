import os
import time
import threading
import gi
from WorkerThread import WorkerThread

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk , GLib
GLib.threads_init() # Don' forget!



class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Diagnose Tool")
        self.set_border_width(10)
        self.set_default_size(800,800)
        self.diagnostic_tool_home=os.getenv("DIAGNOSTIC_TOOL_HOME")
        self.diagnose_list=os.listdir(self.diagnostic_tool_home+"/lib")
        self.diagnose_list.sort() # sort is an inplace function

        # Setting up the self.grid in which the elements are to be positioned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        # Creating the ListStore model
        self.liststore = Gtk.ListStore(bool,str, str)
        for diagnose in self.diagnose_list:
            listStoreEntry=[True,diagnose,"Waiting for Execution"]
            self.liststore.append(listStoreEntry)

        # creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView(model=self.liststore.filter_new())

        for i, column_title in enumerate( ["SELECT","DIAGNOSE", "STATUS"]):
            renderer = Gtk.CellRendererText()
            if column_title == "SELECT" :
               renderer = Gtk.CellRendererToggle()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.pack_start(renderer, True)
            if column_title == "SELECT" :
               column.add_attribute(renderer, "active", 0)
               renderer.connect('toggled', self.on_toggled)

            self.treeview.append_column(column)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.scrollable_treelist.add(self.treeview)

        # creating buttons 
        self.buttons = list()
        for functionality in ["RUN SELECTED", "SELECT ALL", "DESELECT ALL"]:
            button = Gtk.Button(label=functionality)
            self.buttons.append(button)
            button.connect("clicked", self.on_button_clicked)

        self.grid.attach_next_to(
            self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1
        )
        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(
                button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1
            )

        self.show_all()

    def on_toggled(self,widget,listIndex):
        """Called on any of the toggle clicks"""
        if self.liststore[listIndex][0] :
           self.liststore[listIndex][0]=False
        else:
           self.liststore[listIndex][0]=True
        

    def on_button_clicked(self,widget):
        if widget.get_label() == "SELECT ALL" :
            for store in self.liststore:
                store[0]=True
        elif widget.get_label() == "DESELECT ALL" :
            for store in self.liststore:
                store[0]=False
        elif widget.get_label() == "RUN SELECTED" :
            
            at_least_one_task_is_selected=False
            for store in self.liststore:
               if store[0] :
                     at_least_one_task_is_selected=True
            if  at_least_one_task_is_selected :        
                widget.set_sensitive(False)
                
                
            for store in self.liststore:
                if store[0] :
                    diagnose=store[1]
                    #exec_thread = threading.Thread(target=self.do_processing,args=(diagnose,),daemon=True)
                    exec_thread = WorkerThread(self.work_finished,diagnose)
                    exec_thread.start()
                    store[2] = "RUNNING ...."
                else :
                    store[2] = "NOT SELECTED FOR EXECUTION ...."




        else :
            print("Not Recognized Command ")


    def work_finished(self,diagnose,returnValue,message):
        print("Work finished is called")
        
        for store in self.liststore:
                if store[1] == diagnose :
                    if returnValue == 0 :
                       store[2] = "SUCCESS: "+message
                    else :
                       store[2] = "FAILURE: "+message

        all_threads_are_finished=True   
        for store in self.liststore:
            if store[2] ==  "RUNNING ...." :
                     all_threads_are_finished=False
        
        if all_threads_are_finished :                 
           self.buttons[0].set_sensitive(True)

        #return GLib.SOURCE_CONTINUE # GLib.SOURCE_REMOVE
        return  GLib.SOURCE_REMOVE
        





