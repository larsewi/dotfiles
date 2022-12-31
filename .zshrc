autoload -U colors && colors
PS1="%{$fg[green]%}%n@%m%{$reset_color%}:%{$fg[blue]%}%1~ %{$reset_color%}%% "
export PATH="$PATH:/Users/larsewi/Library/Python/3.9/bin"
export PATH="/usr/local/opt/curl/bin:$PATH"
GPG_TTY=$(tty)
export GPG_TTY

export LANG="en_US.UTF-8"

# For Compilers to find OpenSSL
export LDFLAGS="-L/usr/local/opt/openssl@3/lib"
export CPPFLAGS="-I/usr/local/opt/openssl@3/include"

# For pkg-config to find OpenSSL
export PKG_CONFIG_PATH="/usr/local/opt/openssl@3/lib/pkgconfig"
