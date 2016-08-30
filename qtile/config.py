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

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
import os
import subprocess

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.call([home + '/startup_script.sh'])

mod = "mod4"

keys = [
    # Switch between windows in current stack pane
    Key(
        [mod], "k",
        lazy.layout.down()
    ),
    Key(
        [mod], "j",
        lazy.layout.up()
    ),
    Key(
        [mod], "h",
        lazy.layout.left()
    ),
    Key(
        [mod], "l",
        lazy.layout.right()
    ),
    Key(
        [mod, "shift"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, "shift"], "j",
        lazy.layout.shuffle_up()
    ),
    Key(
        [mod, "shift"], "h",
        lazy.layout.swap_left()
    ),
    Key(
        [mod, "shift"], "l",
        lazy.layout.swap_right()
    ),
    Key(
        [mod, "control"], "k",
        lazy.layout.grow()
    ),
    Key(
        [mod, "control"], "j",
        lazy.layout.shrink()
    ),
    Key(
        [mod, "control","shift"], "k",
        lazy.layout.grow_main()
    ),
    Key(
        [mod, "control","shift"], "j",
        lazy.layout.shrink_main()
    ),
    Key(
        [mod, "control"], "h",
        lazy.layout.normalize()
    ),
    Key(
        [mod, "control"], "l",
        lazy.layout.maximize()
    ),
    Key(
        [mod, "shift"], "space", 
        lazy.layout.flip()
    ),
    # start a python console by pressing p button
    Key(
        [mod], "p", 
        lazy.spawn("urxvt -e python")
    ),
    Key(
        [mod], "F12", 
        lazy.spawn("xfce4-screenshooter")
    ),




    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split()
    ),
    Key([mod], "Return", lazy.spawn("urxvt")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
]

groups = [
    Group('Web1', spawn="chromium"),
    Group('Web2', spawn="thunderbird"),
    Group('Chats', spawn=["pidgin","franz"]),
    Group('Games', spawn="steam"),
    Group('Dev'),
    Group('Notes', spawn="xfce4-notes"),
    Group('tmp1'),
    Group('tmp2'),
    Group('tmp3'),
]

for index, grp in enumerate(groups):
    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], str(index+1), lazy.group[grp.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], str(index+1), lazy.window.togroup(grp.name))
    )

layouts = [
    layout.MonadTall(), 
    #layout.Stack(autosplit=True, border_focus="#ff0000", border_width=2, num_stacks=2 ) # good..
    layout.Max(),
    layout.Matrix(border_focus="#ff0000", border_width=2),
]

widget_defaults = dict(
    font='Arial',
    fontsize=16,
    padding=3,
)

screens = [
    Screen(
        top=bar.Bar( 
            [
                widget.GroupBox(),
                widget.WindowTabs(),
                widget.Clock(format='%Y-%m-%d %a %I:%M:%S %p'),
                widget.CurrentLayout(),
            ],
            30,
         ),
                  
    ),
    Screen(
        top=bar.Bar( 
            [
                widget.GroupBox(),
                #widget.WindowName(),
                widget.WindowTabs(),
                widget.TextBox("Flo", name="default"), 
                widget.Pacman(),
                widget.Notify(),
                widget.Systray(),
                #widget.YahooWeather(woeid="GMXX0035"),
                widget.Clock(format='%Y-%m-%d %a %I:%M:%S %p'),
                widget.CurrentLayout(),
            ],
            30,
        ),
        bottom=bar.Bar(
             [
                widget.Prompt(),
                widget.Spacer(),
                widget.Memory(),

                widget.CPUGraph(graph_color="#FF0000", border_color="#FF0000"),
             
                widget.NetGraph(graph_color="#086FA1",
                                border_color="#086FA1",
                                interface="enp4s0",
                                bandwidth_type="down"),
             
             ],
             30,
         ),

    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.toggle_floating())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
