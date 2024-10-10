call plug#begin()
    Plug 'preservim/nerdtree'
    Plug 'Vimjas/vim-python-pep8-indent'
    Plug 'tpope/vim-commentary'
call plug#end()

" Man page
runtime! ftplugin/man.vim

if system('uname -s') == "Darwin\n"
  set clipboard=unnamed "OSX
else
  set clipboard=unnamedplus "Linux
endif

" Set search to wrap around to top of file
set wrapscan

" Use mouse
set mouse=a

" Indent
filetype indent on
set autoindent

" Syntax
syntax enable
filetype plugin on
let g:markdown_fenced_languages = ['c', 'cpp', 'python', 'bash', 'json', 'cf3']

" Show row/col
set number
set ruler

" Dont use numbers in terminal
autocmd TerminalOpen * setlocal nonumber norelativenumber

" Toggle NERDTree
nnoremap <C-t> :NERDTreeToggle<CR>

" Open preview on <CR> instead
let NERDTreeCustomOpenArgs = {'file':{'where':'p','keepopen':1,'stay':1}}

" Disable code folding
set nofoldenable

" Indent
set autoindent
set expandtab
set tabstop=4
set shiftwidth=4
