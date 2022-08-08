from libqtile.widget.textbox import TextBox

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
