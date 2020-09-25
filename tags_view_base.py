#!/usr/bin/env python
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Pango


class TagsViewBase(Gtk.ApplicationWindow):

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

        tags_col_renderer = Gtk.CellRendererText()
        col_tags = Gtk.TreeViewColumn("Tags", tags_col_renderer, text=0)
        tags_view.append_column(col_tags)
        col_tags.set_sort_column_id(0)

        include_col_renderer = Gtk.CellRendererToggle()
        column_in_out = Gtk.TreeViewColumn("Included", include_col_renderer, active=1, visible=2)
        tags_view.append_column(column_in_out)
        include_col_renderer.connect("toggled", self.on_toggled)

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


    # An abstract method
    def on_bt_open_file_set(self, button, view, header_bar):
        pass


class TagFileFilter(Gtk.FileFilter):
    def __init__(self):
        Gtk.FileFilter.__init__(self)
        self.set_name("Tag files")
        self.add_pattern("*-tags.html")

