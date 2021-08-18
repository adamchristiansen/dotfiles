"------------------------------------------------------------------------------
" Color Settings
"------------------------------------------------------------------------------

" Use 24-bit color if supported.
if exists('+termguicolors')
    set termguicolors
endif

"------------------------------------------------------------------------------
" Plugins
"------------------------------------------------------------------------------

" Install vim-plug if it isn't already installed
if empty(glob('~/.local/share/nvim/site/autoload/plug.vim'))
    silent !curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs
        \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
    autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

" Begin the plugin environment
call plug#begin('~/.local/share/nvim/plugged')

" Editing
Plug 'junegunn/vim-easy-align'
Plug 'svermeulen/vim-yoink'

" Git tools
Plug 'tpope/vim-fugitive'
Plug 'airblade/vim-gitgutter'

" Searching and navigation
Plug 'scrooloose/nerdtree'
Plug 'Xuyuanp/nerdtree-git-plugin'
Plug 'christoomey/vim-tmux-navigator'

" Syntax highlighting
Plug 'alker0/chezmoi.vim'
Plug 'sheerun/vim-polyglot'

" End the plugin environment
call plug#end()

" easy-align
xmap ga <Plug>(EasyAlign)
nmap ga <Plug>(EasyAlign)

" gitgutter
let g:gitgutter_sign_added              = '+'
let g:gitgutter_sign_modified           = '±'
let g:gitgutter_sign_modified_removed   = '×'
let g:gitgutter_sign_removed            = '-'
let g:gitgutter_sign_removed_first_line = '×'

" nerdtree
let g:NERDTreeAutoDeleteBuffer = 1
let g:NERDTreeDirArrows = 1
let g:NERDTreeIgnore = ['^\.git$[[dir]]']
let g:NERDTreeMinimalUI = 1
let g:NERDTreeQuitOnOpen = 1
let g:NERDTreeShowHidden = 1
let g:NERDTreeWinSize = 50

" nerdtree git
let g:NERDTreeGitStatusIndicatorMapCustom = {
    \ "Modified"  : "●",
    \ "Staged"    : "✔︎",
    \ "Untracked" : "!",
    \ "Renamed"   : "~",
    \ "Unmerged"  : "≠",
    \ "Deleted"   : "✖",
    \ "Dirty"     : "●",
    \ "Clean"     : "=",
    \ 'Ignored'   : "-",
    \ "Unknown"   : "?"
    \ }

" polyglot
let g:tex_flavor = "latex"

"------------------------------------------------------------------------------
" Keymaps
"------------------------------------------------------------------------------

" Move the cursor to the textwidth on the current line
function! <SID>JumpToTextwidth()
    let l:pos = getpos('.')
    let l:pos[2] = &textwidth
    call setpos('.', l:pos)
endfunction

" Set the leader key
let mapleader = ","

" General
nmap <leader>q :q<CR>
nmap <leader>w :w<CR> :GitGutterAll<CR>
nmap <leader>W :wq<CR>
nmap <leader>e :edit<CR>
nmap <leader>; :call <SID>JumpToTextwidth()<CR>

" Move text under and after cursor to next and previous lines, respectively
nmap <leader>o i<CR><ESC>
nmap <leader>O i<CR><ESC>"oddk"oP

" Copy entire buffer to clipboard
nmap <Leader>Y :%y+<CR>

" Copy/paste to/from clipboard
nmap <Leader>y "+Y
nmap <Leader>p "+p
nmap <Leader>P "+P
xmap <Leader>y "+y
xmap <Leader>p "+p
xmap <Leader>P "+P

" Prevent pasting over selected text from updating the registers. It must now
" be specifically yanked to be stored in register.
xmap p pgvy

" Searching
nmap <leader>/ :noh<CR>

" Splits
nmap <C-w>\| :vs<CR>
nmap <C-w>-  :split<CR>

" GitGutter
nmap <leader>g :GitGutterAll<CR>

" NERDTree
nmap <leader>f :NERDTreeFocus<CR> :NERDTreeRefreshRoot<CR>

" vim-yoink
nmap <leader>[ <plug>(YoinkPostPasteSwapBack)
nmap <leader>] <plug>(YoinkPostPasteSwapForward)
nmap p <plug>(YoinkPaste_p)
nmap P <plug>(YoinkPaste_P)
nmap y <plug>(YoinkYankPreserveCursorPosition)
xmap y <plug>(YoinkYankPreserveCursorPosition)

"------------------------------------------------------------------------------
" Colors and Highlighting
"------------------------------------------------------------------------------

colorscheme uuu

" The file types to exclude from long line highlighting
let g:highlight_long_lines_excluded = [
    \ 'bib',
    \ 'html',
    \ 'json',
    \ 'nerdtree',
    \ 'plaintex',
    \ 'tex',
    \ 'vue'
    \ ]

" Highlight lines longer than the textwidth. Setting the textwidth to 0 or
" adding a file type to g:highlight_long_lines_excluded will disable
" highlighting long lines for that buffer.
function <SID>HighlightLongLines()
    if index(g:highlight_long_lines_excluded, &ft) < 0 && &textwidth > 0
        :execute ":match ErrorMsg '" . printf('\%%>%dv.\+', &textwidth) . "'"
    else
        :execute ":match"
    endif
endfunction

" Automatic highlighting of long lines
autocmd FileType * call <SID>HighlightLongLines()

"------------------------------------------------------------------------------
" Behaviour
"------------------------------------------------------------------------------

" Line numbering
set number relativenumber

" Cursor line
set cursorline
augroup CursorLine
    au!
    au VimEnter,WinEnter,BufWinEnter * setlocal cursorline
    au WinLeave * setlocal nocursorline
augroup end

" Splitting direction
set splitbelow
set splitright

" Vertical split
set fillchars+=vert:\ ,fold:\ "

" Show the invisible characters
set list
set listchars=tab:»·,trail:·,extends:⟩,precedes:⟨,nbsp:≀

" Display
set formatoptions-=t " Remove line wrapping
set laststatus=2
set noruler
set noshowcmd
set noshowmode
set nowrap
set textwidth=79

" Spaces and Tabs
set autoindent
set copyindent
set endofline
set expandtab
set shiftwidth=4
set smartindent
set softtabstop=4
set tabstop=4

" Automatically trim trailing whitepace on each line on write
autocmd BufWritePre * silent! %s/\s\+$//e

" Automatically trim all trailing whitespace at the end of the file on write
autocmd BufWritePre * silent! %s#\($\n\s*\)\+\%$##

" Persistent undo
set undofile

" Disable netrw history
let g:netrw_dirhistmax = 0

" Reload the configuration on SIGUSR1. This is guarded by the if statement so
" that it is not registered every time the signal is received.
if !exists('*ReloadConfig')
    function ReloadConfig()
        source $MYVIMRC
        redraw!
    endfunction

    autocmd Signal SIGUSR1 call ReloadConfig()
end

"------------------------------------------------------------------------------
" Status Line
"------------------------------------------------------------------------------

" A lookup table to convert the result of `mode()` to a human readable string.
let g:statusline_mode_lookup = {
    \ 'n'  : 'Normal',
    \ 'no' : 'N·Pending',
    \ 'v'  : 'Visual',
    \ 'V'  : 'V·Line',
    \ '' : 'V·Block',
    \ 's'  : 'Select',
    \ 'S'  : 'S·Line',
    \ '' : 'S·Block',
    \ 'i'  : 'Insert',
    \ 'R'  : 'Replace',
    \ 'Rv' : 'V·Replace',
    \ 'c'  : 'Command',
    \ 'cv' : 'Vim Ex',
    \ 'ce' : 'Ex',
    \ 'r'  : 'Prompt',
    \ 'rm' : 'More',
    \ 'r?' : 'Confirm',
    \ '!'  : 'Shell',
    \ 't'  : 'Terminal',
    \}

function! StatuslineModeInfo()
    return toupper(g:statusline_mode_lookup[mode()])
endfunction

function! StatuslineBufferInfo()
    let l:s  = ''
    let l:s .= &readonly || !&modifiable ? '' : ''
    let l:s .= &modified ? '●' : ''
    return len(l:s) ?  l:s  : ''
endfunction

" Build a statusline format string. The [window] argument is the window number
" the statusline is attached to.
function! StatuslineBuild(window)
    " Get window information
    let l:current  = a:window == winnr() " Whether the window is current
    let l:width    = winwidth(a:window)  " Window width in characters
    let l:filetype = getwinvar(a:window, '&filetype')
    let l:IfCurr   = { c -> l:current ? c : '' }
    " Build the status line
    let l:s = '%<' " Truncate
    " Mode
    let l:s .= l:IfCurr('%7* %{StatuslineModeInfo()} %0* ')
    " File
    let l:s .=
        \ l:IfCurr('%8* ') .
        \ ("%{&readonly || !&modifiable ? ' ' : ''}") .
        \ (l:width >= 80 ? '%f' : '%t') .
        \ "%{&modified ? ' ●' : ''} %0*"
    " Separator
    let l:s .= '%='
    " File type
    if !empty(l:filetype) && l:width > 60
        let l:s .= l:IfCurr('%3* ' . l:filetype . ' %0*')
    end
    " Column and line
    if l:width > 70
        let l:s .= l:IfCurr(' %8*  %c %0*')
        let l:s .= l:IfCurr(' %7*  %l ╱ %L %0*')
    end
    return l:s
endfunction

" Causes the statusline to be refreshed between active an inactive
function! StatuslineRefresh()
    for i in range(1, winnr('$'))
        call setwinvar(i, '&statusline', StatuslineBuild(i))
    endfor
endfunction

" Refresh the statusline at startup
call StatuslineRefresh()

" Automatically switch the statusline between active an inactive
autocmd
    \ VimEnter,VimResized,WinEnter,BufWinEnter,BufWritePost
    \ *
    \ call StatuslineRefresh()
