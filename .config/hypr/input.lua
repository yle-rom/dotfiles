---@module 'hl'

hl.config({
	input = {
		kb_layout = "us,gr",
		-- kb_options = "grp:alt_shift_toggle", -- Uncomment and remove the '--' to use this
		accel_profile = "flat",
		follow_mouse = 1,
		sensitivity = 0.7,
		repeat_rate = 50,
		repeat_delay = 240,

		touchpad = {
			natural_scroll = true,
			disable_while_typing = true,
			scroll_factor = 0.4,
		},
	},
})

hl.gesture({
	fingers = 3,
	direction = "horizontal",
	action = "workspace",
})

hl.gesture({
	fingers = 3,
	direction = "up",
	action = function()
		hl.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 20%+")
	end,
})

hl.gesture({
	fingers = 3,
	direction = "down",
	action = function()
		hl.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 20%-")
	end,
})
