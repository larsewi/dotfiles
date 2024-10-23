autoload -U colors && colors
PS1="%{$fg[green]%}╭──(%{$fg[blue]%}%n☺︎%m%{$fg[green]%})─[%{$fg[yellow]%}%~%{$fg[green]%}]
╰─%{$reset_color%} %{$fg[blue]%}$%{$reset_color%} "
export VIRTUAL_ENV_DISABLE_PROMPT=1

export GPG_TTY=$(tty)
export LANG="en_US.UTF-8"

alias la="ls -a"
alias ll="ls -l"
alias lal="ls -al"

alias clear="clear && printf '\e[3J'"

PATH="/usr/local/opt/libtool/libexec/gnubin:$PATH"

source ~/.venv/bin/activate
