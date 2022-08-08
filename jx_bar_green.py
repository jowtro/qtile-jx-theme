from libqtile.widget.textbox import TextBox
from libqtile import bar, widget
from libqtile.config import Screen

COLORS = [
    ["#17724B", "#25B576"],  # 0
    ["#0D412B", "#17724B"],  # 1
    ["#2f3e46", "#2f3e46"],  # 2 BAR DEFAULT COLOR
    ["#ffffff", "#ffffff"],  # 3 WHITE
    ["218177", "218177"],  # 4 when workspace is selected
    ["000000", "000000"],  # 5 BLACK when workspace is not selected
    ["218177", "218177"],  # 6 right side of the bar
]

GROUP_LAYOUT = dict(
    fontsize=12,
    margin_y=3,
    margin_x=0,
    padding_y=5,
    padding_x=3,
    borderwidth=3,
    active=COLORS[3],
    inactive=COLORS[3],
    rounded=False,
    highlight_color=COLORS[4],
    highlight_method="line",
    this_current_screen_border=COLORS[6],
    this_screen_border=COLORS[4],
    other_current_screen_border=COLORS[6],
    other_screen_border=COLORS[4],
    foreground=COLORS[2],
    background=COLORS[2],
)

LEFT_ARROW_BACK = TextBox(
    # left arrow back
    font="DejaVuSansMono Nerd Font Mono",
    text="\uf438",
    fontsize=46,
    foreground=COLORS[2],
    background=COLORS[4],
    padding=-9,
)

LEFT_ARROW_FRONT = TextBox(
    # left arrow front
    font="DejaVuSansMono Nerd Font Mono",
    text="\uf438",
    fontsize=46,
    foreground=COLORS[4],
    background=COLORS[2],
    padding=-9,
)


SCREEN1 = Screen(
    top=bar.Bar(
        [
            widget.Sep(
                linewidth=0,
                padding=6,
                foreground=COLORS[4],
                background=COLORS[4],
            ),
            widget.GroupBox(**GROUP_LAYOUT),
            widget.CurrentLayout(background=COLORS[2]),
            widget.Prompt(
                background=COLORS[2],
            ),
            widget.WindowName(background=COLORS[2], padding=0),
            widget.Chord(
                chords_colors={
                    "launch": ("#ff0000", "#ffffff"),
                },
                name_transform=lambda name: name.upper(),
            ),
            LEFT_ARROW_FRONT,
            widget.Systray(background=COLORS[4], padding=5),
            widget.TextBox(
                font="DejaVuSansMono Nerd Font Mono",
                text="\uf1eb",
                fontsize=27,
                foreground=COLORS[3],
                background=COLORS[4],
            ),
            widget.Net(
                interface="wlan0",
                format="{down} ↓↑ {up}",
                foreground=COLORS[3],
                background=COLORS[4],
                padding=0,
            ),
            LEFT_ARROW_BACK,
            widget.Sep(linewidth=30, foreground=COLORS[2], background=COLORS[2]),
            LEFT_ARROW_FRONT,
            widget.TextBox(
                # thermal icon
                font="DejaVuSansMono Nerd Font Mono",
                text="\uf8c7",
                fontsize=30,
                foreground=COLORS[3],
                background=COLORS[4],
            ),
            widget.ThermalSensor(
                foreground=COLORS[3],
                background=COLORS[4],
                threshold=90,
                fmt="{}",
                padding=5,
            ),
            widget.TextBox(
                font="DejaVuSansMono Nerd Font Mono",
                text="\uf073",
                fontsize=30,
                foreground=COLORS[3],
                background=COLORS[4],
            ),
            widget.Clock(
                format="%B %d %Y %a %H:%M",
                background=COLORS[4],
            ),
            widget.Sep(
                foreground=COLORS[3],
                background=COLORS[4],
            ),
            widget.QuickExit(
                default_text="\uf011",
                countdown_format="{}",
                fontsize=25,
                background=COLORS[4],
            ),
        ],
        20,
    ),
)


SCREEN2 = Screen(
    top=bar.Bar(
        [
            widget.Sep(
                linewidth=0,
                padding=6,
                foreground=COLORS[4],
                background=COLORS[4],
            ),
            widget.GroupBox(**GROUP_LAYOUT),
            widget.WindowName(background=COLORS[2], padding=0),
        ],
        20,
    ),
)
