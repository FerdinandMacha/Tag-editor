#!/usr/bin/env python
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import tags_storage
from tags_model import (TagCategory, TagItem)

import logging


@Gtk.Template(filename='tags_view.ui')
class TagsView(Gtk.ApplicationWindow):
    __gtype_name__ = 'TagsView'

    tree_store: Gtk.TreeStore = Gtk.Template.Child()
    sorted_model: Gtk.TreeModelSort = Gtk.Template.Child()
    top_bar: Gtk.HeaderBar = Gtk.Template.Child()
    tags_view: Gtk.TreeView = Gtk.Template.Child()
    bt_open_file: Gtk.FileChooserButton = Gtk.Template.Child()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.current_tag_file: str = ""

        self.sorted_model.set_sort_column_id(0, Gtk.SortType.ASCENDING)

 
    def load_model(self, tag_file_name: str):
        tags: list[TagCategory] = tags_storage.load_tags(tag_file_name)        
        for tag_category in tags:
        
            piter = self.tree_store.append(None, [tag_category.name, False, False])
            for item in tag_category.items:
                tag: TagItem = item
                self.tree_store.append(piter, [tag.name, tag.included, True])


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


    def get_tree_store_path(self, path_string):
        sorted_iter = self.sorted_model.get_iter_from_string(path_string)
        return self.sorted_model.convert_path_to_child_path(
            self.sorted_model.get_path(sorted_iter))


    @Gtk.Template.Callback()
    def on_toggled(self, widget, path):
        self.tree_store[self.get_tree_store_path(path)][1] = not self.sorted_model[path][1]
        self.save_to_file()

    @Gtk.Template.Callback()
    def on_bt_open_file_set(self, button):
        self.reload_window(button.get_filename(), self.tags_view, self.top_bar)

    @Gtk.Template.Callback()
    def name_changed(self, widget, path, text):
        self.tree_store[self.get_tree_store_path(path)][0] = text
        self.save_to_file()
        
