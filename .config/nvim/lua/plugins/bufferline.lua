return {
  'akinsho/bufferline.nvim',
  version = '*',
  dependencies = 'nvim-tree/nvim-web-devicons',
  config = function()
    require('bufferline').setup {
      options = {
        mode = 'buffers',
        diagnostics = 'nvim_lsp',
        always_show_bufferline = true,
        show_buffer_close_icons = false,
        show_close_icon = false,
      },
    }

    vim.keymap.set('n', '<S-h>', '<cmd>BufferLineCyclePrev<CR>', { desc = 'Previous buffer' })
    vim.keymap.set('n', '<S-l>', '<cmd>BufferLineCycleNext<CR>', { desc = 'Next buffer' })
    vim.keymap.set('n', '<leader>x', '<cmd>bdelete<CR>', { desc = 'Close current buffer' })
  end,
}
