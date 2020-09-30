#!/usr/bin/env python
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Pango
import sys
import tags_view_base
import tags_storage
import tags_config_view
import os.path
import tags_model


class TagsView(tags_view_base.TagsViewBase):

    def __init__(self, _app):
        tags_view_base.TagsViewBase.__init__(self, app=_app)

        
    def load_model(self, tag_file_name):
        model = tags_storage.load_tags(tag_file_name)        
        for tag_category in model:
            piter = self.tree_store.append(None, [tag_category.category, False, False])
            for tag in tag_category.tags:
                tag.append(True) #append the hidden column ("check box showing") value
                self.tree_store.append(piter, tag)

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
                tags_storage.load_tag_categories(all_tags_file_name)
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
        dialog.add_filter(tags_view_base.TagFileFilter())

        response = dialog.run()
        result = dialog.get_filename()
        dialog.destroy()

        if response == Gtk.ResponseType.CANCEL:
        
            config_view = tags_config_view.get_tags_config_ui(app=self)
            result = "get res" #config_view.run()

            raise ValueError (TagsApp.C_PROVIDE_CONFIGURATION_MESSAGE)
        return result


    def do_startup(self):
        Gtk.Application.do_startup(self)

app = TagsApp()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
