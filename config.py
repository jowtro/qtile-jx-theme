# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import subprocess
from libqtile.config import Click, Drag, Group, Key, Match
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook, layout
from libqtile.dgroups import simple_key_binder
from libqtile.log_utils import logger
from jx_bar_blue import SCREEN1, SCREEN2, BORDER_FOCUS, BORDER_NORMAL

logger.setLevel(logging.INFO)


@hook.subscribe.startup_once
def autostart():
    # add nitrogen to the qtile startup
    subprocess.Popen(["bash", "/home/jowtro/.config/qtile/init_qtile.sh"])


def init_layout_theme():
    return {
        "margin": 5,
        "border_width": 1,
        "border_focus": BORDER_FOCUS,
        "border_normal": BORDER_NORMAL,
    }


layout_theme = init_layout_theme()

if __name__ in ["config", "__main__"]:
    mod = "mod4"
    terminal = guess_terminal()
    # region KEYS
    keys = [
        # A list of available commands that can be bound to keys can be found
        # at https://docs.qtile.org/en/latest/manual/config/lazy.html
        # Switch between windows
        Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
        Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
        Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
        Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
        Key([mod], "space", lazy.layout.next(), desc="Change to next layout"),
        # Move windows between left/right columns or move up/down in current stack.
        # Moving out of range in Columns layout will create new column.
        Key(
            [mod, "shift"],
            "h",
            lazy.layout.shuffle_left(),
            desc="Move window to the left",
        ),
        Key(
            [mod, "shift"],
            "l",
            lazy.layout.shuffle_right(),
            desc="Move window to the right",
        ),
        Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
        Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
        # Grow windows. If current window is on the edge of screen and direction
        # will be to screen edge - window would shrink.
        Key(
            [mod, "control"],
            "h",
            lazy.layout.grow_left(),
            desc="Grow window to the left",
        ),
        Key(
            [mod, "control"],
            "l",
            lazy.layout.grow_right(),
            desc="Grow window to the right",
        ),
        Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
        Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
        Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
        # Toggle between split and unsplit sides of stack.
        # Split = all windows displayed
        # Unsplit = 1 window displayed, like Max layout, but still with
        # multiple stack panes
        Key(
            [mod, "shift"],
            "Return",
            lazy.layout.toggle_split(),
            desc="Toggle between split and unsplit sides of stack",
        ),
        Key([mod, "shift"], "Return", lazy.spawn("tilix"), desc="Launch terminal"),
        # Toggle between different layouts as defined below
        Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
        Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
        Key([mod, "shift"], "q", lazy.reload_config(), desc="Reload the config"),
        # Key([mod], "p", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
        Key([mod], "p", lazy.spawn("rofi -show run")),
        # Sound
        Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
        Key([], "XF86AudioLowerVolume", lazy.spawn("amixer set Master 5%- unmute")),
        Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer set Master 5%+ unmute")),
    ]
    # endregion

    # groups = [Group(i) for i in "123456789"]
    groups = [
        Group("WWW", layout="monadtall"),
        Group("TER", layout="max"),
        Group("DEV", layout="monadtall"),
        Group("TER", layout="monadtall"),
        Group("VBOX", layout="monadtall"),
        Group("MUS", layout="monadtall"),
        Group("CHAT", layout="monadtall"),
        Group("VID", layout="monadtall"),
        Group("MISC", layout="floating"),
    ]
    # bind the groups above to MOD key + [0-9] and MOD + shift + [0-9] to sendo to another group
    dgroups_key_binder = simple_key_binder("mod4")

    layouts = [
        layout.Max(),
        layout.MonadTall(**layout_theme),
        layout.Columns(**layout_theme),
        # layout.TreeTab(**layout_theme),
        # layout.Bsp(**layout_theme),
        # layout.MonadWide(**layout_theme),
        # Try more layouts by unleashing below layouts.
        # layout.Stack(num_stacks=3),
        # layout.Matrix(),
        # layout.RatioTile(),
        # layout.Tile(**layout_theme),
        # layout.VerticalTile(),
        # layout.Zoomy(),
    ]

    widget_defaults = dict(
        font="DejaVuSansMono Nerd Font Mono",
        fontsize=12,
        padding=3,
    )
    extension_defaults = widget_defaults.copy()

    # screen and bars
    screens = [SCREEN1, SCREEN2]

    # Drag floating layouts.
    mouse = [
        Drag(
            [mod],
            "Button1",
            lazy.window.set_position_floating(),
            start=lazy.window.get_position(),
        ),
        Drag(
            [mod],
            "Button3",
            lazy.window.set_size_floating(),
            start=lazy.window.get_size(),
        ),
        Click([mod], "Button2", lazy.window.bring_to_front()),
    ]

    dgroups_app_rules = []  # type: list
    follow_mouse_focus = True
    bring_front_click = False
    cursor_warp = False
    floating_layout = layout.Floating(
        float_rules=[
            # Run the utility of `xprop` to see the wm class and name of an X client.
            *layout.Floating.default_float_rules,
            Match(wm_class="confirmreset"),  # gitk
            Match(wm_class="makebranch"),  # gitk
            Match(wm_class="maketag"),  # gitk
            Match(wm_class="ssh-askpass"),  # ssh-askpass
            Match(title="branchdialog"),  # gitk
            Match(title="pinentry"),  # GPG key password entry
            Match(title="gimp"),
            Match(title="nitrogen"),
        ]
    )
    auto_fullscreen = True
    focus_on_window_activation = "smart"
    reconfigure_screens = True

    # If things like steam games want to auto-minimize themselves when losing
    # focus, should we respect this or not?
    auto_minimize = True

    # When using the Wayland backend, this can be used to configure input devices.
    wl_input_rules = None

    wmname = "LG3D"
