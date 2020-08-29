#!/usr/bin/env python
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Pango
import sys
import tags_storage
import os.path


class TagsView(Gtk.ApplicationWindow):

    def __init__(self, app):
        self.current_tag_file = ""

        Gtk.Window.__init__(self, title="Media tagger", application=app)
        self.set_default_size(640, 480)
        self.set_border_width(10)

        top_bar = Gtk.HeaderBar()
        top_bar.set_show_close_button(True)
        top_bar.props.title = self.current_tag_file
        self.set_titlebar(top_bar)

        self.tree_store = Gtk.TreeStore(str, bool, bool)
        self.sorted_model = Gtk.TreeModelSort(model=self.tree_store)
        self.sorted_model.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        
        tags_view = Gtk.TreeView(model=self.sorted_model)

        renderer_books = Gtk.CellRendererText()
        col_tags = Gtk.TreeViewColumn("Tags", renderer_books, text=0)
        tags_view.append_column(col_tags)
        col_tags.set_sort_column_id(0)

        renderer_in_out = Gtk.CellRendererToggle()
        column_in_out = Gtk.TreeViewColumn("Included", renderer_in_out, active=1, visible=2)
        tags_view.append_column(column_in_out)
        renderer_in_out.connect("toggled", self.on_toggled)

        column_chkbox_visibility = Gtk.TreeViewColumn("Check visible", Gtk.CellRendererToggle())
        column_chkbox_visibility.set_visible(False)
        tags_view.append_column(column_chkbox_visibility)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(tags_view)
        self.add(scrolled)
        
        bt_open_file = Gtk.FileChooserButton(title="Select a file containing tags")
        bt_open_file.set_filename(self.current_tag_file)
        bt_open_file.connect("file-set", self.on_bt_open_file_set, tags_view, top_bar)
        bt_open_file.add_filter(TagFileFilter())
        top_bar.pack_start(bt_open_file)

        
    def load_model(self, tag_file_name):
        file_model = tags_storage.load_tags(tag_file_name)        
        for i in range(len(file_model)):
            piter = self.tree_store.append(None, [file_model[i][0], False, False])
            j = 1
            while j < len(file_model[i]):
                file_model[i][j].append(True)
                self.tree_store.append(piter, file_model[i][j])
                j += 1

    def reload_window(self, tag_file_name, view, header_bar):
        self.current_tag_file = tag_file_name
        self.tree_store.clear()
        self.load_model(tag_file_name)
        view.expand_all()
        header_bar.props.title = tag_file_name
        

    def save_to_file(self):
        def extract_tag(model, path, iter, tag_list):
            if model[path][1]:
                tag_list.append(model[path][0])
        selected_tags = []
        self.tree_store.foreach(extract_tag, selected_tags)
        tags_storage.save_tags(self.current_tag_file, selected_tags)


    def on_toggled(self, widget, path):
        def get_tree_store_path(path_string):
            sorted_iter = self.sorted_model.get_iter_from_string(path_string)
            return self.sorted_model.convert_path_to_child_path(
                self.sorted_model.get_path(sorted_iter))
            
        self.tree_store[get_tree_store_path(path)][1] = not self.sorted_model[path][1]

        self.save_to_file()


    def on_bt_open_file_set(self, button, view, header_bar):
        self.reload_window(button.get_filename(), view, header_bar)
        

class TagFileFilter(Gtk.FileFilter):
    def __init__(self):
        Gtk.FileFilter.__init__(self)
        self.set_name("Tag files")
        self.add_pattern("*-tags.html")



class TagsApp(Gtk.Application):

    C_PROVIDE_CONFIGURATION_MESSAGE = "You have to provide the tags configuration."

    def __init__(self):
        Gtk.Application.__init__(self)


    def do_activate(self):
        if len(sys.argv) == 2:
            # just a basic first check
            if os.path.isfile(sys.argv[1]):
                self.show_tags_window(sys.argv[1])
        else:
            print(TagsApp.C_PROVIDE_CONFIGURATION_MESSAGE)
            self.show_tags_window(self.choose_all_tags())


    def show_tags_window(self, all_tags_file_name):
            try:
                tags_storage.load_all_tags(all_tags_file_name)
                win = TagsView(self)
                win.show_all()
            except:
                dialog = Gtk.MessageDialog(
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.CANCEL,
                    text="The tags configuration is invalid.",
                )
                dialog.format_secondary_text(
                    "The file\n" + all_tags_file_name +
                    "\ncontent cannot be loaded as tags.\nPerhaps it is not a configuration file at all?"
                )
                dialog.run()
                dialog.destroy()


    def choose_all_tags(self):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a tags configuration file",
            parent=None,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        dialog.add_filter(TagFileFilter())

        response = dialog.run()
        result = dialog.get_filename()
        dialog.destroy()

        if response == Gtk.ResponseType.CANCEL:
            raise ValueError (TagsApp.C_PROVIDE_CONFIGURATION_MESSAGE)
        return result


    def do_startup(self):
        Gtk.Application.do_startup(self)

app = TagsApp()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
