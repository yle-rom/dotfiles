---@module 'hl'

hl.monitor({
	output = "desc:Samsung Display Corp.0x41A4",
	mode = "2560x1600@240",
	position = "0x0",
	scale = 1.6,
	bitdepth = 10,
	cm = "hdr",
})

hl.monitor({
	output = "HDMI-A-1",
	mode = "preferred",
	position = "auto",
	scale = 1,
})

require("env")

require("autostart")

require("keybinds")

require("windowrules")

require("lookandfeel")

require("input")
