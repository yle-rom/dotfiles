return {
  'mfussenegger/nvim-jdtls',
  ft = 'java',
  config = function()
    local mason_path = vim.fn.stdpath 'data' .. '/mason/packages'
    local launcher_jar = vim.fn.glob(mason_path .. '/jdtls/plugins/org.eclipse.equinox.launcher_*.jar', true)
    local workspace_dir = vim.fn.expand '~/.cache/jdtls/workspace/' .. vim.fn.fnamemodify(vim.fn.getcwd(), ':p:h:t')

    require('jdtls').start_or_attach {
      cmd = {
        '/usr/lib/jvm/java-21-openjdk/bin/java',
        '-Declipse.application=org.eclipse.jdt.ls.core.id1',
        '-Dosgi.bundles.defaultStartLevel=4',
        '-Declipse.product=org.eclipse.jdt.ls.core.product',
        '-Dlog.protocol=true',
        '-Dlog.level=ALL',
        '-Xmx1g',
        '-Dmaven.repo.local=' .. os.getenv 'HOME' .. '/.local/share/maven/m2',
        '--add-modules=ALL-SYSTEM',
        '--add-opens', 'java.base/java.util=ALL-UNNAMED',
        '--add-opens', 'java.base/java.lang=ALL-UNNAMED',
        '-jar', launcher_jar,
        '-configuration', mason_path .. '/jdtls/config_linux',
        '-data', workspace_dir,
      },
      root_dir = vim.fs.dirname(vim.fs.find({ 'pom.xml', 'gradlew', '.git', 'mvnw' }, { upward = true })[1]),
    }
  end,
}
