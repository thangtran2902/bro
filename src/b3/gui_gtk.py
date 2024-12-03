import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.1')
from gi.repository import Gtk, WebKit2, Gdk

class BrowserApp:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui.glade")
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("main_window")
        self.scrolled_window = self.builder.get_object("scrolledwindow")
        self.url_entry = self.builder.get_object("address_bar")
        self.web_view = WebKit2.WebView()

        self.web_settings = WebKit2.Settings()
        self.web_settings.set_enable_javascript(True)
        self.web_settings.set_enable_developer_extras(True)
        self.web_view.set_settings(self.web_settings)

        self.scrolled_window.add(self.web_view)
        self.web_view.show()

        default_url = "https://duckduckgo.com"
        self.url_entry.set_text(default_url)
        self.web_view.load_uri(default_url)

        self.web_view.connect("load-failed", self.on_load_failed)
        self.web_view.connect("load-changed", self.on_load_changed)

        self.window.connect("key-press-event", self.on_key_press)
        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show_all()

    def on_load_changed(self, web_view, load_event):
        if load_event == WebKit2.LoadEvent.COMMITTED:
            current_uri = web_view.get_uri()
            self.url_entry.set_text(current_uri)

    def on_load_failed(self, web_view, load_event, uri, error):
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Failed to load page",
        )
        dialog.format_secondary_text(f"Error: {error.message}")
        dialog.run()
        dialog.destroy()

    def on_back_button_clicked(self, button):
        self.web_view.go_back()

    def on_forward_button_clicked(self, button):
        self.web_view.go_forward()

    def on_refresh_button_clicked(self, button):
        self.web_view.reload()

    def on_enter_key_hit(self, button):
        url = self.url_entry.get_text()
        self.web_view.load_uri(url)

    def on_dark_mode_button_clicked(self, button):
        settings = Gtk.Settings.get_default()
        dark_mode = settings.get_property("gtk-application-prefer-dark-theme")
        settings.set_property("gtk-application-prefer-dark-theme", not dark_mode)

    def on_key_press(self, widget, event):
        key = Gdk.keyval_name(event.keyval)
        if event.state & Gdk.ModifierType.CONTROL_MASK:
            if key == "r":
                self.web_view.reload()
            elif key == "t":
                print("Ctrl+T pressed: Add tab feature later!")

if __name__ == "__main__":
    BrowserApp()
    Gtk.main()
