import os
from libqtile.widget.textbox import TextBox
from libqtile import bar, widget
from libqtile.config import Screen

#load from env
CITY_CODE = os.getenv("CITY_CODE_WEATHER")

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
            widget.WindowName(background=COLORS[2], padding=0),
            LEFT_ARROW_FRONT,
            widget.TextBox(
                # thermal icon
                font="DejaVuSansMono Nerd Font Mono",
                text="\ue350",
                fontsize=18,
                foreground=COLORS[3],
                background=COLORS[4],
            ),
            widget.OpenWeather(
                cityid=CITY_CODE,
                format="{main_temp} °{units_temperature} {humidity}% {weather_details}",
                foreground=COLORS[3],
                background=COLORS[4],
            ),
            LEFT_ARROW_BACK,
            LEFT_ARROW_FRONT,
            widget.CryptoTicker(
                crypto="BTC",
                foreground=COLORS[3],
                background=COLORS[4],
                symbol="$",
                update_interval=300,
                currency="USD",
            ),
            LEFT_ARROW_BACK,
            LEFT_ARROW_FRONT,
            widget.TextBox(
                font="DejaVuSansMono Nerd Font Mono",
                text="\uf2db",
                fontsize=20,
                foreground=COLORS[3],
                background=COLORS[4],
            ),
            widget.Memory(
                format="{MemUsed:.0f}{mm}/{MemTotal:.0f}{mm}",
                measure_mem="G",
                foreground=COLORS[3],
                background=COLORS[4],
            ),
            widget.Sep(
                linewidth=1,
                padding=6,
                foreground=COLORS[1],
                background=COLORS[4],
            ),
            widget.TextBox(
                # thermal icon
                font="DejaVuSansMono Nerd Font Mono",
                text="\uf8c7",
                fontsize=25,
                foreground=COLORS[3],
                background=COLORS[4],
            ),
            widget.ThermalSensor(
                foreground=COLORS[3],
                background=COLORS[4],
                threshold=80,
                tag_sensor="Package id 0",
                fmt="CPU {}",
                padding=5,
            ),
            widget.Sep(
                linewidth=1,
                padding=6,
                foreground=COLORS[1],
                background=COLORS[4],
            ),
            widget.TextBox(
                font="DejaVuSansMono Nerd Font Mono",
                text="\uf109",
                fontsize=20,
                foreground=COLORS[3],
                background=COLORS[4],
            ),
            widget.CPU(
                format="CPU {freq_current}GHz {load_percent}%",
                foreground=COLORS[3],
                background=COLORS[4],
            ),
            LEFT_ARROW_BACK,
            LEFT_ARROW_FRONT,
             widget.TextBox(
                font="DejaVuSansMono Nerd Font Mono",
                text="\uf025",
                fontsize=25,
                foreground=COLORS[3],
                background=COLORS[4],
            ),
            widget.PulseVolume(
                fmt="{}",
                foreground=COLORS[3],
                background=COLORS[4],
            ),
            widget.Sep(
                linewidth=1,
                padding=6,
                foreground=COLORS[1],
                background=COLORS[4],
            ),
            widget.Wlan(
                foreground=COLORS[3],
                background=COLORS[4],
            ),
            LEFT_ARROW_BACK,
            widget.Sep(linewidth=30, foreground=COLORS[2], background=COLORS[2]),
            LEFT_ARROW_FRONT,
            widget.TextBox(
                font="DejaVuSansMono Nerd Font Mono",
                text="\uf073",
                fontsize=30,
                foreground=COLORS[3],
                background=COLORS[4],
            ),
            widget.Clock(
                format="%d/%m/%Y %H:%M",
                background=COLORS[4],
            ),
            widget.Sep(
                linewidth=10,
                foreground=COLORS[4],
                background=COLORS[4],
            ),
            widget.QuickExit(
                default_text="\uf011",
                countdown_format="{}",
                fontsize=25,
                background=COLORS[4],
            ),
            widget.Systray(background=COLORS[2], padding=5),
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
