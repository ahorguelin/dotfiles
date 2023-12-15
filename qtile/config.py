#########	CONFIG QTILE AHO	    ###########

import os
import subprocess

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

#### STARTUPS
@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])


#### VARIABLES
mod = "mod4"
terminal = "alacritty"

#### COLORS
def init_colors():
    return[
	["#1d1f21", "#1d1f21"], #bg black
	["#c5c8c6", "#c5c8c6"], #fg light gray
	["#cc6666", "#cc6666"], #color01 red
	["#b5bd68", "#b5bd68"], #color02 green
	["#f0c674", "#f0c674"], #color03 yellow
	["#81a2be", "#81a2be"], #color04 blue
	["#b294bb", "#b294bb"], #color05 purple
	["#8abeb7", "#8abeb7"], #color06 cyan 
	["#ffffff", "#ffffff"], #color15 white
	["#1d1f2180", "#1d1f2180"], #bgtransparent
	["#00000000", "#00000000"], #no color
    ]
    
colors = init_colors()

#### SHORTCUTS
keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod, "control"],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Custom keys config
    Key([mod], "d", lazy.spawn("rofi -show drun -show-icons"), desc=""),
    Key([mod], "e", lazy.spawn("rofi modi emoji -show emoji -emoji-mode insert"), desc=""),
    Key([mod, "shift"], "s", lazy.spawn("flameshot gui"), desc="launch flameshot gui"),
]

#### WORKSPACES
groups = []
group_names = ["z", "x", "c", "v", "b"]
group_labels = ["dev", "ter", "www", "chat", "misc"]


for i in range(len(group_names)):
    groups.append(
	Group(
	    name=group_names[i],
	    label=group_labels[i]
	)
    )

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

#### LAYOUTS
def init_layouts():
    return {
	"margin": 3,
	"border_width": 1,
	"border_focus": colors[1],
	"border_normal": colors[0],
    }

layout_theme = init_layouts()
    

layouts = [
    layout.Columns(**layout_theme),
    layout.Spiral(**layout_theme,
	main_pane="left",
	clockwise=True,
	main_pane_ratio=0.5,
	new_client_position="after_current"
    )
]

#### BAR
def init_widgets_defaults():
    return {
	"font":"hack",
	"fontsize": 14,
	"padding": 5
    }

extension_defaults = init_widgets_defaults()

def init_widgets_list():
    w_list = [
	widget.GroupBox(
	    active=colors[8],
	    inactive=colors[1],
	    urgent_text=colors[2],
	    this_current_screen_border=colors[8],
	    other_current_screen_border=colors[8],
	    this_screen_border=colors[1],
	    other_screen_border=colors[1],
	    border=colors[1],
	    foreground=colors[1],
	    padding_y=3,
	    padding_x=15,
	    margin_x=10,
	    fontsize=14
	),
	widget.Spacer(),
	widget.Clock(
	    format='%d/%m/%y %H:%M',
	    font='hack',
	    fontsize=14,
	),
	widget.Spacer(
	    length=25
	),
    ]
    
    return w_list

widgets = init_widgets_list()

screens = [
    Screen(
        top=bar.Bar(
	    widgets,
            size=26,
	    background=colors[9]
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
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
	Match(title="Thunar"), #thunar file manager
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

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
