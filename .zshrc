autoload -U colors && colors
PS1="%{$fg[green]%}%n@%m%{$reset_color%}:%{$fg[blue]%}%1~ %{$reset_color%}%% "
export PATH="$PATH:/Users/larsewi/Library/Python/3.9/bin"
export PATH="/usr/local/opt/curl/bin:$PATH"
GPG_TTY=$(tty)
export GPG_TTY

export LANG="en_US.UTF-8"

# For pkg-config to work with OpenSSL installed from brew
export PKG_CONFIG_PATH="/usr/local/opt/openssl@3/lib/pkgconfig"
