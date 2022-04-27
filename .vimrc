" Use vim settings rather than vi settings
set nocompatible

" Allow plugins
filetype plugin on

" Show line numbers
set number

" Syntax highlighting on
syntax on

" Markdown syntax
let g:markdown_fenced_languages = ['c', 'cpp', 'python', 'bash', 'json', 'cf3']

" Don't interpret numbers preceded by zero as octal
set nrformats-=octal

" Use clipboard
set clipboard=unnamedplus
" set clipboard^=unnamed " on macos

" Indents
set autoindent
set expandtab
set tabstop=4
set softtabstop=4
set shiftwidth=4

" Backspace
set backspace=indent,eol,start

" Show row/col
set ruler

" Explorer
let g:netrw_banner = 0
let g:netrw_liststyle = 3
let g:netrw_browse_split = 4
let g:netrw_altv = 1
let g:netrw_winsize = 25
augroup ProjectDrawer
  autocmd!
  autocmd VimEnter * :Vexplore
augroup END

