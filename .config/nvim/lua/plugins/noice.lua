return {
  'folke/noice.nvim',
  event = 'VeryLazy',
  dependencies = {
    'MunifTanjim/nui.nvim',
    {
      'rcarriga/nvim-notify',
      opts = {
        background_colour = '#000000',
        render = 'wrapped-compact',
        stages = 'fade',
      },
    },
  },
  opts = {
    lsp = {},
    presets = {
      bottom_search = false,
      command_palette = true,
      long_message_to_split = true,
      inc_rename = false,
      lsp_doc_border = true,
    },
  },
}
