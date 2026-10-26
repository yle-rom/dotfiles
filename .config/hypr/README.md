# hypr

Hyprland 0.56, Lua config. Entry: `hyprland.lua` (beats `hyprland.conf` if both exist).
Check what loaded: `command grep cfg $XDG_RUNTIME_DIR/hypr/*/hyprland.log`
Apply changes: `hyprctl reload`, then `hyprctl configerrors` (empty = ok).

| file | what |
|---|---|
| hyprland.lua | monitors, then `require`s the modules below in this order |
| env.lua | env vars: cursor, nvidia/DRM, XDG session |
| autostart.lua | `hyprland.start` hook: waybar, nm-applet, `rice --apply`, wallpaper; `config.reloaded` hook: `rice --apply` (keeps the theme border) |
| keybinds.lua | all binds |
| windowrules.lua | window rules (e.g. dashboard window) |
| lookandfeel.lua | gaps, borders, decoration, animations |
| input.lua | keyboard/touchpad |

Old hyprlang `.conf` set (pre-Lua, stale): `~/.config/vault/hypr/conf/`.
Restore from a TTY if Lua ever breaks: `mv ~/.config/vault/hypr/conf/*.conf ~/.config/hypr/`
