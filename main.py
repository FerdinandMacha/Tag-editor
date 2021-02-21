#!/usr/bin/env python

import os.path
import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gio, Gtk

import tags_storage
from tags_view import TagsView


class TagFileFilter(Gtk.FileFilter):
    def __init__(self):
        Gtk.FileFilter.__init__(self)
        self.set_name("Tag files")
        self.add_pattern("*-tags.html")



class TagsApp(Gtk.Application):

    C_PROVIDE_CONFIGURATION_MESSAGE = "You have to provide the tags configuration."

    def __init__(self):
        super().__init__(application_id='fmacha.gtk.tags-editor',
                         flags=Gio.ApplicationFlags.HANDLES_OPEN)

    def do_open(self, files: list[Gio.File], *hint):
        if files.count == 2:
            # just a basic first check
            if files[1].query_exists():
                self.show_tags_window(files[1].get_path())
        else:
            self.show_tags_window(self.choose_all_tags())

        self.do_activate()
        return 0

    def show_tags_window(self, all_tags_file_name):
            try:
                tags_storage.load_tag_configuration(all_tags_file_name)
                win = TagsView(application=self)
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
        builder: Gtk.Builder = Gtk.Builder()
        builder.add_from_file("dlg_configuration.ui")

        dialog: Gtk.FileChooserDialog = builder.get_object("dlg_config_chooser")
        '''dialog = Gtk.FileChooserDialog(
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
        dialog.add_filter(TagFileFilter())'''

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
