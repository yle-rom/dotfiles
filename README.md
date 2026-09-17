# dotfiles

Config files for my Arch Linux setup.

## Stack

- **WM**: Hyprland
- **Bar**: Waybar
- **Terminal**: Alacritty
- **Shell**: Zsh
- **Editor**: Neovim

## Structure

Tracked with a bare git repo against `$HOME` (no symlinks) - paths mirror `~/.config/`.

## Usage

Clone as a bare repo against `$HOME`:

\`\`\`bash
git clone --bare git@github.com:yle-rom/dotfiles.git $HOME/.dotfiles
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
dotfiles checkout
dotfiles config --local status.showUntrackedFiles no
\`\`\`

Note: `dotfiles checkout` may fail if any of these files already exist un-tracked in `$HOME` - back them up
or remove them first.
