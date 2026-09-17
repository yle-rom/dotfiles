# XDG Base Directories
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_DATA_HOME="$HOME/.local/share"
export XDG_STATE_HOME="$HOME/.local/state"
export XDG_CACHE_HOME="$HOME/.cache"

# Zsh
export HISTFILE="$XDG_STATE_HOME/zsh/history"

# Rust
export CARGO_HOME="$XDG_DATA_HOME/cargo"
export RUSTUP_HOME="$XDG_DATA_HOME/rustup"

# Go
export GOPATH="$XDG_DATA_HOME/go"

# Bun
export BUN_INSTALL="$XDG_DATA_HOME/bun"

# npm
export NPM_CONFIG_CACHE="$XDG_CACHE_HOME/npm"
export NPM_CONFIG_PREFIX="$XDG_DATA_HOME/npm-global"

# Ollama
export OLLAMA_MODELS="$XDG_DATA_HOME/ollama/models"

# GPG
export GNUPGHOME="$XDG_DATA_HOME/gnupg"

# PulseAudio
export PULSE_COOKIE="$XDG_DATA_HOME/pulse/cookie"

# Readline
export INPUTRC="$XDG_CONFIG_HOME/readline/inputrc"

# MariaDB
export MYSQL_HISTFILE="$XDG_STATE_HOME/mariadb/history"

# NVIDIA shader cache
export __GL_SHADER_DISK_CACHE_PATH="$XDG_CACHE_HOME/nvidia"
export CUDA_CACHE_PATH="XDG_CACHE_HOME/nvidia/nv/ComputeCache"

# Java
export _JAVA_OPTIONS="-Djava.util.prefs.userRoot=$XDG_CACHE_HOME/java"

# Maven
export MAVEN_OPTS="-Dmaven.repo.local=$XDG_DATA_HOME/maven/m2"

# PATH
export PATH="$XDG_DATA_HOME/npm-global/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
export PATH="$CARGO_HOME/bin:$PATH"

# OpenClaude
export OPENCLAUDE_CONFIG_DIR="$XDG_CONFIG_HOME/.config/openclaude"
#export CLAUDE_CODE_USE_OPENAI=1
#export OPENAI_BASE_URL=http://localhost:11434/v1
#export OPENAI_API_KEY=ollama
#export OPENAI_MODEL=hermes3:8b
export SEARXNG_URL="http://localhost:8080"
export OLLAMA_NUM_CTX=32768

# W3M
export W3M_DIR=$XDG_CONFIG_HOME/w3m

# Parallel
export PARALLEL_HOME=$XDG_CONFIG_HOME/parallel

# Bat for man
export MANPAGER="bat -plman"

#ls 777 permission color removal
export LS_COLORS=$LS_COLORS:"ow=00;34:tw=00;34:st=00;34:"
