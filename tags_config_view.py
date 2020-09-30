#!/usr/bin/env python
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Pango

import tags_view_base


class TagsConfigView(tags_view_base.TagsViewBase):

    def __init__(self, _app):
        tags_view_base.TagsViewBase.__init__(self, app=_app)

        print("Showing on the class " + self.top_bar.__class__.__name__)
        
        bt_list_add = Gtk.Button()
        bt_list_add.add(Gtk.Image(icon_name='list-add-symbolic', visible=True))
        self.top_bar.pack_start(bt_list_add)


    def on_toggled(self, widget, path):
        pass

    def on_bt_open_file_set(self, button, view, header_bar):
        pass


def get_tags_config_ui(app=None):
    result = TagsConfigView(_app=app)
    result.show_all()
    return result


