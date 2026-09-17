return {
  {
    'mbbill/undotree',
    config = function()
      vim.keymap.set('n', '<leader>ut', vim.cmd.UndotreeToggle, { desc = '[U]ndo [T]ree Panel' })
    end,
  },

  {
    'debugloop/telescope-undo.nvim',
    dependencies = { 'nvim-telescope/telescope.nvim' },
    config = function()
      require('telescope').setup { extensions = { undo = {} } }
      require('telescope').load_extension 'undo'
      vim.keymap.set('n', '<leader>uu', '<cmd>Telescope undo<cr>', { desc = 'Telescope [U]ndo [U]I' })
    end,
  },
}
