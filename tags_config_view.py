#!/usr/bin/env python
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Pango


def get_tags_config_ui(parent_window=None):
    result = Gtk.Dialog(title="My dialog", parent=parent_window,
        buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
        Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))

    label = Gtk.Label("Simple dialog")
    result.vbox.add(label)
    label.show()
    return result


get_tags_config_ui()
