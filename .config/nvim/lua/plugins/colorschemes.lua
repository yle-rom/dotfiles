local theme_config = {
  wal = { termguicolors = false },
  -- kanagawa syntax colors, pywal UI (bg/fg/gutter/floats/menus/selection)
  ['kanagawa-dragon'] = {
    setup = function()
      local ok, data = pcall(function() return vim.json.decode(table.concat(vim.fn.readfile(vim.fn.expand '~/.cache/wal/colors.json'), '\n')) end)
      local ui, hl = {}, {}
      if ok then
        local c, s = data.colors, data.special
        local function blend(a, b, t)
          local r = {}
          for _, i in ipairs { 2, 4, 6 } do
            local x, y = tonumber(a:sub(i, i + 1), 16), tonumber(b:sub(i, i + 1), 16)
            r[#r + 1] = string.format('%02x', math.floor(x * (1 - t) + y * t + 0.5))
          end
          return '#' .. table.concat(r)
        end
        local bg, fg, accent = s.background, s.foreground, c.color3
        local m1, p1, p2 = blend(bg, '#000000', 0.25), blend(bg, fg, 0.07), blend(bg, fg, 0.14)
        ui = {
          fg = fg,
          fg_dim = blend(fg, bg, 0.25),
          fg_reverse = bg,
          bg = bg,
          bg_dim = m1,
          bg_gutter = 'none',
          bg_m3 = blend(bg, '#000000', 0.55),
          bg_m2 = blend(bg, '#000000', 0.4),
          bg_m1 = m1,
          bg_p1 = p1,
          bg_p2 = p2,
          special = c.color8,
          whitespace = blend(bg, fg, 0.2),
          nontext = blend(bg, fg, 0.2),
          bg_visual = blend(bg, accent, 0.3),
          bg_search = blend(bg, accent, 0.45),
          pmenu = { fg = fg, fg_sel = 'none', bg = p1, bg_sel = blend(bg, accent, 0.3), bg_thumb = c.color8, bg_sbar = p1 },
          float = { fg = fg, bg = m1, fg_border = c.color8, bg_border = m1 },
        }
        -- normal-mode block follows the wallpaper accent; other modes keep kanagawa's cues
        hl.MiniStatuslineModeNormal = { fg = bg, bg = accent, bold = true }
      end
      require('kanagawa').setup {
        compile = false,
        transparent = true,
        colors = { theme = { dragon = { ui = ui } } },
        overrides = function() return hl end,
      }
    end,
  },
}

vim.api.nvim_create_autocmd('VimEnter', {
  once = true,
  callback = function()
    local f = vim.fn.expand '~/.cache/nvim-theme'
    local theme = vim.fn.filereadable(f) == 1 and vim.fn.readfile(f)[1] or 'wal'
    local cfg = theme_config[theme] or {}
    vim.opt.termguicolors = cfg.termguicolors ~= false
    if cfg.setup then cfg.setup() end
    vim.cmd.colorscheme(theme)
    vim.cmd 'highlight Normal guibg=NONE ctermbg=NONE'
    vim.cmd 'highlight NormalNC guibg=NONE ctermbg=NONE'
  end,
})

return {
  { 'dylanaraps/wal.vim' },
  { 'rebelot/kanagawa.nvim' },
}
