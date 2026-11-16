---@module 'hl'

hl.config({
    xwayland = {
        force_zero_scaling = true,
    },
})

hl.window_rule({
    name  = "suppress-maximize-events",
    match = {
        class = ".*",
    },
    suppress_event = "maximize",
})

hl.window_rule({
    name  = "fix-xwayland-drags",
    match = {
        class = "^$",
        title = "^$",
        xwayland = true,
        float = true,
        fullscreen = false,
        pin = false,
    },
    no_focus = true,
})

hl.window_rule({
    name  = "music-player",
    match = {
        class = "^(spotify)$",
    },
    workspace = "special:magic",
})

hl.window_rule({
    name  = "magi-dashboard",
    match = {
        class = "^(magi-dashboard)$",
    },
    float = true,
    move = { 35, 35 },
    size = { 1530, 930 },
    animation = "slide left",
})
