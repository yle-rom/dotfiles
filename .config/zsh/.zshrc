# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# History
HISTFILE="$XDG_STATE_HOME/zsh/history"
HISTSIZE=5000
SAVEHIST=5000
[[ -f ~/.histfile ]] && rm -f ~/.histfile # Claude subshells fall back to ~/.histfile (bash, no .zshenv)

# Prompt
PROMPT='%K{0}%B%F{3}%n@%m %~ ツ%f%b%E%k '

# Vim motions
#bindkey -v

# Completion
autoload -Uz compinit
compinit -d "$XDG_CACHE_HOME/zsh/zcompdump"

# Plugins
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=245"
bindkey '^[ ' autosuggest-accept

# Aliases
alias grep='grep --color=auto'
alias ls='ls --color=auto'
#alias la='ls -la'
alias c="clear"

alias speedtest="speedtest --secure"
alias wifi="nmtui"
alias bluetooth="blueman-manager"
alias powerset="powerprofilesctl set"
alias powerget="powerprofilesctl get"

alias pdf="zathura"
alias md='glow'
alias json='jq .'
alias img="imv"
alias imgedit="gthumb"
alias v="nvim"
alias bloodborne="bb_launcher"
alias copy="wl-copy"
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'

unset zle_bracketed_paste

# Functions
function cdl() {
	cd "$@" && ls
}

function la() {
  ls -la --color=always "$@" | grep -v '^l'
}
