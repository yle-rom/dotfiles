---@module 'hl'

-- Autostart
hl.on("hyprland.start", function()
	hl.exec_cmd("nm-applet --indicator &")
	hl.exec_cmd("~/.config/waybar/scripts/frame.sh start")   -- 4-bar waybar frame
	hl.exec_cmd("~/.local/bin/rice --apply")
	hl.exec_cmd("dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP")
	hl.exec_cmd("systemctl --user import-environment WAYLAND_DISPLAY XDG_CURRENT_DESKTOP")
	hl.exec_cmd("systemctl --user start hyprpolkitagent")
	hl.exec_cmd("awww-daemon")
	hl.exec_cmd("sleep 1 && awww img $(cat ~/.cache/current-wallpaper) --transition-type fade --transition-duration 1")
	hl.exec_cmd("ollama serve")
	hl.exec_cmd("wl-paste --type text --watch cliphist store")
	hl.exec_cmd("wl-paste --type image --watch cliphist store")
	hl.exec_cmd("mako")
	hl.exec_cmd("cliphist wipe")
end)

-- A reload re-runs lookandfeel.lua (hardcoded MAGI border), so re-apply the current theme's border
hl.on("config.reloaded", function()
	hl.exec_cmd("~/.local/bin/rice --apply")
end)
