local theme_config = {
  wal = { termguicolors = false },
  evergarden = {
    setup = function()
      require('evergarden').setup {
        theme = { variant = 'fall', accent = 'green' },
        editor = {
          transparent_background = false,
          sign = { color = 'none' },
          float = { color = 'mantle', solid_border = false },
          completion = { color = 'surface0' },
        },
      }
    end,
  },
  terafox = { setup = function() require('nightfox').setup { options = { transparent = true } } end },
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
  { 'xero/miasma.nvim' },
  { 'EdenEast/nightfox.nvim' },
  { 'everviolet/nvim', name = 'evergarden' },
  { 'savq/melange-nvim' },
  { 'rebelot/kanagawa.nvim' },
}
