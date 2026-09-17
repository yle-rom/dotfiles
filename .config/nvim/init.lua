-- globals
vim.g.mapleader = ' '
vim.g.maplocalleader = ' '
vim.g.have_nerd_font = true
vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

-- options
vim.schedule(function() vim.o.clipboard = 'unnamedplus' end)
vim.o.number = true
vim.o.relativenumber = true
vim.o.mouse = 'a'
vim.o.showmode = false
vim.o.breakindent = true
vim.o.undofile = true
vim.opt.undodir = os.getenv 'HOME' .. '/.local/share/nvim/undodir'
vim.o.ignorecase = true
vim.o.smartcase = true
vim.o.signcolumn = 'yes'
vim.o.updatetime = 250
vim.o.timeoutlen = 300
vim.o.splitright = true
vim.o.splitbelow = true
vim.o.list = true
vim.opt.listchars = { tab = '» ', trail = '·', nbsp = '␣' }
vim.o.inccommand = 'split'
vim.o.cursorline = true
vim.o.scrolloff = 10
vim.o.tabstop = 2
vim.o.shiftwidth = 2
vim.o.softtabstop = 2
vim.o.expandtab = true
vim.o.confirm = true

-- keymaps
vim.keymap.set('n', '<Esc>', '<cmd>nohlsearch<CR>')
vim.keymap.set('n', '<C-d>', '<C-d>zz', { desc = 'Scroll down and center' })
vim.keymap.set('n', '<C-u>', '<C-u>zz', { desc = 'Scroll up and center' })
vim.keymap.set('n', '<leader>e', ':Neotree toggle<CR>', { desc = 'Toggle file tree', silent = true })
vim.keymap.set('t', '<Esc><Esc>', '<C-\\><C-n>', { desc = 'Exit terminal mode' })
vim.keymap.set('n', '<C-h>', '<C-w><C-h>', { desc = 'Move focus to the left window' })
vim.keymap.set('n', '<C-l>', '<C-w><C-l>', { desc = 'Move focus to the right window' })
vim.keymap.set('n', '<C-j>', '<C-w><C-j>', { desc = 'Move focus to the lower window' })
vim.keymap.set('n', '<C-k>', '<C-w><C-k>', { desc = 'Move focus to the upper window' })
vim.keymap.set('n', '<leader>q', vim.diagnostic.setloclist, { desc = 'Open diagnostic [Q]uickfix list' })
vim.keymap.set('i', '<C-k>', vim.lsp.buf.signature_help, { desc = 'Show signature help' })
vim.keymap.set('n', 'SS', '<cmd>x<CR>', { desc = 'Save and Quit' })
vim.keymap.set({ 'n', 'v' }, 'd', '"_d', { noremap = true })
vim.keymap.set({ 'n', 'v' }, 'D', '"_D', { noremap = true })
vim.keymap.set({ 'n', 'v' }, 'x', '"_x', { noremap = true })
vim.keymap.set({ 'n', 'v' }, 'X', '"_X', { noremap = true })
vim.keymap.set('v', 'p', '"_dP', { noremap = true })
--vim.keymap.set({ 'n', 'v' }, '<leader>d', '"+d', { noremap = true })
vim.keymap.set('n', '<leader>ya', 'ggVGy', { noremap = true, silent = true })
vim.keymap.set('n', '<leader>da', 'ggVG"_d', { noremap = true, silent = true })
vim.keymap.set('n', 'U', '<C-r>', { desc = 'Redo' })

-- diagnostics
vim.diagnostic.config {
  update_in_insert = false,
  severity_sort = true,
  float = { border = 'rounded', source = 'if_many' },
  underline = { severity = { min = vim.diagnostic.severity.WARN } },
  virtual_text = true,
  virtual_lines = false,
  jump = { float = true },
}

-- autocommands
vim.api.nvim_create_autocmd('ColorScheme', {
  group = vim.api.nvim_create_augroup('transparent-bg', { clear = true }),
  callback = function()
    vim.cmd 'highlight Normal guibg=NONE ctermbg=NONE'
    vim.cmd 'highlight NormalNC guibg=NONE ctermbg=NONE'
  end,
})

vim.api.nvim_create_autocmd('BufEnter', {
  callback = function()
    if vim.fn.isdirectory(vim.fn.bufname()) == 1 then vim.cmd 'bwipeout' end
  end,
})

vim.api.nvim_create_autocmd('TextYankPost', {
  desc = 'Highlight when yanking (copying) text',
  group = vim.api.nvim_create_augroup('kickstart-highlight-yank', { clear = true }),
  callback = function() vim.hl.on_yank() end,
})

vim.opt.mouse = ''

-- lazy bootstrap
local lazypath = vim.fn.stdpath 'data' .. '/lazy/lazy.nvim'
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  local lazyrepo = 'https://github.com/folke/lazy.nvim.git'
  local out = vim.fn.system { 'git', 'clone', '--filter=blob:none', '--branch=stable', lazyrepo, lazypath }
  if vim.v.shell_error ~= 0 then error('Error cloning lazy.nvim:\n' .. out) end
end
vim.opt.rtp:prepend(lazypath)

-- plugins (added in lua/plugins/)
require('lazy').setup({ { import = 'plugins' } }, {
  ui = {
    icons = vim.g.have_nerd_font and {} or {
      cmd = '⌘',
      config = '🛠',
      event = '📅',
      ft = '📂',
      init = '⚙',
      keys = '🗝',
      plugin = '🔌',
      runtime = '💻',
      require = '🌙',
      source = '📄',
      start = '🚀',
      task = '📌',
      lazy = '💤 ',
    },
  },
})
