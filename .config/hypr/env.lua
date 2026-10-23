---@module 'hl'

hl.env("XCURSOR_THEME", "Sunset Cursors")

hl.env("XCURSOR_SIZE", 24)

hl.env("HYPRCURSOR_THEME", "Sunset Cursors")

hl.env("HYPRCURSOR_SIZE", 24)

hl.env("LIBVA_DRIVER_NAME", "i915")

hl.env("GBM_BACKEND", "i915")

hl.env("__GLX_VENDOR_LIBRARY_NAME", "mesa")

hl.env("AQ_DRM_DEVICES", "/dev/dri/card2:/dev/dri/card1")

hl.env("WLR_DRM_NO_ATOMIC", 1)

hl.env("__GL_SHADER_DISK_CACHE_PATH", os.getenv("HOME") .. "/.cache/nvidia")

hl.env("CUDA_CACHE_PATH", os.getenv("HOME") .. "/.cache/nvidia/nv/ComputeCache")

--env = LIBVA_DRIVER_NAME,nvidia

--env = GBM_BACKEND,nvidia-drm

--env = __GLX_VENDOR_LIBRARY_NAME,nvidia

--env = __GL_SHADER_DISK_CACHE_PATH,$HOME/.cache/nvidia

--env = CUDA_CACHE_PATH,$HOME/.cache/nvidia/nv/ComputeCache

hl.env("XDG_CURRENT_DESKTOP", "Hyprland")

hl.env("XDG_SESSION_DESKTOP", "Hyprland")

hl.env("XDG_SESSION_TYPE", "wayland")
