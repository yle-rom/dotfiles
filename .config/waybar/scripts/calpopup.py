#!/usr/bin/env python3
"""Pop-up calendar beside the bar. Run again to close it (toggle). Esc or "close" also closes.
Arrows / scroll change month, 'today' jumps back. Colors come from pywal via colors-active.css."""
import os, signal, sys
from datetime import date
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("GtkLayerShell", "0.1")
from gi.repository import Gdk, GLib, Gtk, GtkLayerShell

PIDFILE = os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "waybar-calendar.pid")
COLORS = os.path.expanduser("~/.config/waybar/colors-active.css")
BAR_EDGE = 17 + 35 + 10  # bar margin-left + bar width + gap

# toggle: if already open, close it and exit
try:
    pid = int(open(PIDFILE).read())
    if b"calpopup" in open(f"/proc/{pid}/cmdline", "rb").read():  # don't kill a reused pid
        os.kill(pid, signal.SIGTERM)
        os.remove(PIDFILE)
        sys.exit(0)
except (FileNotFoundError, ProcessLookupError, ValueError):
    pass
open(PIDFILE, "w").write(str(os.getpid()))

CSS = open(COLORS).read() + """
* { font-family: "JetBrainsMono Nerd Font", monospace; font-size: 12px; font-weight: bold; }
window, .root { background-color: @bg; }
.root { border: 2px solid @fg; }
calendar, calendar.view { background-color: @bg; color: @fg; padding: 6px; border: none; }
calendar.header { background: @fg; color: @bg; border: none; border-radius: 0; }
calendar.button { color: @bg; background: transparent; border: none; box-shadow: none; }
calendar.button:hover { color: alpha(@bg, 0.55); }
calendar.highlight { color: alpha(@fg, 0.55); }
calendar:indeterminate { color: alpha(@fg, 0.25); }
calendar:selected { background: @fg; color: @bg; border-radius: 0; }
button { background: transparent; color: @fg; border: 1px solid alpha(@fg, 0.4);
         border-radius: 0; box-shadow: none; padding: 2px 8px; margin: 0 6px 6px 6px; }
button:hover { background: @fg; color: @bg; }
"""


def quit_(*_):
    try:
        os.remove(PIDFILE)
    except FileNotFoundError:
        pass
    Gtk.main_quit()


provider = Gtk.CssProvider()
provider.load_from_data(CSS.encode())
Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider,
                                         Gtk.STYLE_PROVIDER_PRIORITY_USER)

win = Gtk.Window()
GtkLayerShell.init_for_window(win)
GtkLayerShell.set_layer(win, GtkLayerShell.Layer.OVERLAY)
GtkLayerShell.set_anchor(win, GtkLayerShell.Edge.LEFT, True)
GtkLayerShell.set_margin(win, GtkLayerShell.Edge.LEFT, BAR_EDGE)
GtkLayerShell.set_keyboard_mode(win, GtkLayerShell.KeyboardMode.ON_DEMAND)

cal = Gtk.Calendar(show_week_numbers=True)
today = date.today()


def mark_today(*_):
    cal.clear_marks()
    y, m, _d = cal.get_date()
    if (y, m + 1) == (today.year, today.month):
        cal.mark_day(today.day)
        cal.select_day(today.day)
    else:
        cal.select_day(0)  # no highlighted day outside the current month


def go_today(*_):
    cal.select_month(today.month - 1, today.year)
    cal.select_day(today.day)


def scroll(_w, ev):
    y, m, _d = cal.get_date()
    step = 1 if ev.direction == Gdk.ScrollDirection.DOWN or ev.delta_y > 0 else -1
    m += step
    cal.select_month(m % 12, y + m // 12)
    return True


cal.connect("month-changed", mark_today)
cal.add_events(Gdk.EventMask.SCROLL_MASK | Gdk.EventMask.SMOOTH_SCROLL_MASK)
cal.connect("scroll-event", scroll)
mark_today()

btn = Gtk.Button(label="today")
btn.connect("clicked", go_today)
close = Gtk.Button(label="close")
close.connect("clicked", quit_)
row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True)
row.pack_start(btn, True, True, 0)
row.pack_start(close, True, True, 0)
box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
box.get_style_context().add_class("root")
box.pack_start(cal, False, False, 0)
box.pack_start(row, False, False, 0)
win.add(box)

win.connect("key-press-event", lambda _w, e: e.keyval == Gdk.KEY_Escape and quit_())
win.connect("destroy", quit_)
try:
    from gi.repository import GLibUnix
    GLibUnix.signal_add(GLib.PRIORITY_DEFAULT, signal.SIGTERM, lambda: quit_() or False)
except ImportError:
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGTERM, lambda: quit_() or False)
win.show_all()
Gtk.main()
