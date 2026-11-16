return {
  'MeanderingProgrammer/render-markdown.nvim',
  ft = 'markdown',
  dependencies = { 'nvim-treesitter/nvim-treesitter', 'nvim-tree/nvim-web-devicons' },
  opts = {
    heading = { icons = { '◉ ', '○ ', '✸ ', '✿ ', '◆ ', '◇ ' } },
    anti_conceal = { enabled = false },
  },
  keys = {
    { '<leader>tm', '<cmd>RenderMarkdown toggle<CR>', desc = '[T]oggle [M]arkdown render', ft = 'markdown' },
  },
}
