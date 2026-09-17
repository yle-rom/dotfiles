return {
  'nvim-neo-tree/neo-tree.nvim',
  version = '*',
  dependencies = {
    'nvim-lua/plenary.nvim',
    'nvim-tree/nvim-web-devicons',
    'MunifTanjim/nui.nvim',
  },
  cmd = 'Neotree',
  keys = {
    { '<leader>e', ':Neotree toggle<CR>', desc = 'Toggle Neo-tree', silent = true },
  },
  opts = {
    filesystem = {
      hijack_netrw_behavior = 'open_default',
      use_libuv_file_watcher = true,
      follow_current_file = { enabled = true },
    },
    window = {
      width = 45,
      mappings = {
        ['h'] = 'open_drop',
        ['l'] = 'close_node',
        ['n'] = function(state)
          require('neo-tree.sources.filesystem.commands').open(state)
          vim.cmd 'Neotree focus'
        end,
      },
    },
  },
}
