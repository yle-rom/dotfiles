#!/usr/bin/env bash
# Shared rofi look for the bar's menus (powermenu, powerprofile-menu).
# Colors come from the bar itself (colors-active.css), so menus follow pywal *and* `rice` custom colors.
#   source ~/.config/waybar/scripts/menu-theme.sh
#   rofi -dmenu -theme-str "$(menu_theme <lines>)" ...

_COLORS=~/.config/waybar/colors-active.css
_color() { sed -nE "s/^@define-color[[:space:]]+$1[[:space:]]+(#[0-9a-fA-F]{6}).*/\1/p" "$_COLORS" | head -1; }

bg=$(_color bg);   bg=${bg:-#000000}
fg=$(_color fg);   fg=${fg:-#f3701e}
red=$(_color red); red=${red:-#fb4934}

# fg mixed 35% toward white = the bar's "bright" color (active workspace, hour)
_bright() {
  local h=${1#\#} out="#" i c
  for i in 0 2 4; do c=$((16#${h:$i:2})); out+=$(printf '%02x' $(( c + (255 - c) * 35 / 100 ))); done
  echo "$out"
}
bright=$(_bright "$fg")

menu_theme() {
  local lines=${1:-3}
  cat <<THEME
* { font: "JetBrainsMono Nerd Font Bold 11"; background-color: transparent; text-color: ${fg}; }
window {
  width: 300px;
  border: 1px solid;
  border-color: ${fg}99;
  border-radius: 0px;
  padding: 0px;
  background-color: ${bg};
}
mainbox { padding: 0px; spacing: 0px; border: 0px; children: [inputbar, listview]; }
inputbar {
  padding: 12px 16px;
  border: 0px 0px 1px 0px;
  border-color: ${fg}66;
  children: [prompt];
}
prompt { text-color: ${fg}b3; font: "JetBrainsMono Nerd Font Bold 9"; }
listview { padding: 6px 0px; spacing: 0px; lines: ${lines}; fixed-height: true; scrollbar: false; border: 0px; }
element { padding: 10px 16px; border: 0px 0px 0px 3px; border-color: transparent; }
/* the base rofi theme colors every state; reset them all */
element normal.normal, element alternate.normal, element normal.urgent, element alternate.urgent,
element normal.active, element alternate.active { background-color: transparent; }
element normal.normal, element alternate.normal { text-color: ${fg}b3; }
element selected.normal { text-color: ${bright}; border-color: ${fg}; background-color: ${fg}1a; }
element normal.urgent, element alternate.urgent { text-color: ${fg}b3; }
element selected.urgent { text-color: ${red}; border-color: ${red}; background-color: ${red}1a; }
element normal.active, element alternate.active { text-color: ${fg}; }
element selected.active { text-color: ${bright}; border-color: ${fg}; background-color: ${fg}1a; }
element-text, element-icon { background-color: transparent; text-color: inherit; vertical-align: 0.5; }
THEME
}
