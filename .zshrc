autoload -U colors && colors
PS1="%{$fg[green]%}╭──(%{$reset_color%}"  # ╭──(
PS1+="%{$fg[blue]%}%n@%m%{$reset_color%}" # <USER>☺︎<HOST>
PS1+="%{$fg[green]%})─[%{$reset_color%}"  # )─[
PS1+="%{$fg[yellow]%}%~%{$reset_color%}"  # <CWD>
PS1+="%{$fg[green]%}]%{$reset_color%}"    # ]
PS1+=%"{$fg[red]%} %?%{$reset_color%}"    # <EXIT_CODE>
PS1+="
%{$fg[green]%}╰─%{$reset_color%} "        # ╰─
PS1+="%{$fg[blue]%}$%{$reset_color%} "    # $
export VIRTUAL_ENV_DISABLE_PROMPT=1

export GPG_TTY=$(tty)
export LANG="en_US.UTF-8"

alias la="ls -a"
alias ll="ls -l"
alias lal="ls -al"

alias clear="clear && printf '\e[3J'"

PATH="/usr/local/opt/libtool/libexec/gnubin:$PATH"

source ~/.venv/bin/activate
