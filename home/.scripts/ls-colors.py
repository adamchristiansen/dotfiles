#!/usr/bin/env python3

import copy
import json
import pathlib

class Fg:
  Black   = ('black',   30)
  Red     = ('red',     31)
  Green   = ('green',   32)
  Yellow  = ('yellow',  33)
  Blue    = ('blue',    34)
  Magenta = ('magenta', 35)
  Cyan    = ('cyan',    36)
  White   = ('white',   37)
  All     = [Black, Red, Green, Yellow, Blue, Magenta, Cyan, White]

class Bg:
  Black   = ('black',   40)
  Red     = ('red',     41)
  Green   = ('green',   42)
  Yellow  = ('yellow',  43)
  Blue    = ('blue',    44)
  Magenta = ('magenta', 45)
  Cyan    = ('cyan',    46)
  White   = ('white',   47)
  All     = [Black, Red, Green, Yellow, Blue, Magenta, Cyan, White]

class Mod:
  Normal    = ('normal',    0)
  Bold      = ('bold',      1)
  Underline = ('underline', 4)

class LS:
  """Build LS_COLORS."""

  _colors = {}

  @staticmethod
  def color(do, patterns):
    """Apply a do function to the patterns."""
    do(patterns)

  @staticmethod
  def do(*spec):
    """Create a function that applies the specification to a patterns list."""
    return lambda patterns: LS.apply(patterns, spec)

  @staticmethod
  def _extract(specs, specset):
    """Find the first matching specification in a specification set."""
    for x in specs:
      for y in specset:
        if x == y:
          return x
    return (None, None)

  @staticmethod
  def apply(patterns, specs):
    """Apply the specifications to a patterns list."""
    fg = LS._extract(Fg.All, specs)
    bg = LS._extract(Bg.All, specs)
    bold = Mod.Bold in specs
    underline = Mod.Underline in specs
    for pattern in patterns:
      ls_color = []
      if not bold and not underline:
        ls_color.append(Mod.Normal[1])
      if bold:
        ls_color.append(Mod.Bold[1])
      if underline:
        ls_color.append(Mod.Underline[1])
      if fg[1] is not None:
        ls_color.append(fg[1])
      if bg[1] is not None:
        ls_color.append(bg[1])
      LS._colors[pattern] = {
        'fg_name': fg[0],
        'fg_ansii': fg[1],
        'bg_name': bg[0],
        'bg_ansii': bg[1],
        'bold': bold,
        'bold_ansii': Mod.Bold[1],
        'underline': underline,
        'underline_ansii': Mod.Underline[1],
        'ls_color': ';'.join(map(str, ls_color))
      }

  @staticmethod
  def colors():
    """Generate the colors to export."""
    # This is the default ordering for the core specifications
    core = [
      'rs', 'no', 'fi', 'di', 'ln', 'mh', 'pi', 'do', 'bd', 'cd', 'or', 'so',
      'su', 'sg', 'ca', 'tw', 'ow', 'st', 'ex', 'mi', #'lc', 'rc', 'ec',
    ]
    # Process the patterns in an order so that the highest priority items are
    # last. This ordering is:
    # - core
    # - arbitrary globs
    # - globs at the end
    # - no globs
    keys = set(LS._colors.keys())
    for c in core:
      keys.discard(c)
    no_glob = set(filter(lambda x: '*' not in x, keys))
    keys -= no_glob
    rest = keys
    # The last match found is applied so they are sorted in reverse priority
    order = core + sorted(rest) + sorted(no_glob)
    ls_colors = []
    for k in order:
      # Make sure that all patterns start with a * and do not have a * anywhere
      # else in them
      if k.count('*') >= 2 or ('*' in k and not k.startswith('*')):
        raise ValueError(f"invalid LS_COLORS pattern: {k}")
      pattern = k if '*' in k or k in core else '*' + k
      ls_colors.append(f"{pattern}={LS._colors[k]['ls_color']}")
    return {
      'data': copy.deepcopy(LS._colors),
      'ls_colors': ':'.join(ls_colors),
      'order': order,
    }

# These are the specification functions that can be used.
archive              = LS.do(Fg.Red, Mod.Underline)
code                 = LS.do(Fg.Green)
data_binary          = LS.do(Fg.Red)
data_text            = LS.do(Fg.Red)
device_block         = LS.do(Fg.Cyan, Bg.Black)
device_char          = LS.do(Fg.Magenta, Bg.Black)
directory            = LS.do(Fg.Blue, Mod.Bold)
door                 = LS.do(Fg.Black, Bg.Magenta)
executable           = LS.do(Fg.Green, Mod.Bold)
file_with_capability = LS.do()
font                 = LS.do(Fg.Yellow, Mod.Underline)
media_audio          = LS.do(Fg.Magenta)
media_image          = LS.do(Fg.Yellow)
media_video          = LS.do(Fg.Magenta, Mod.Bold)
multi_hard_link      = LS.do(Fg.Red, Mod.Bold, Mod.Underline)
normal               = LS.do()
office               = LS.do(Fg.Yellow, Mod.Underline)
pipe                 = LS.do(Fg.Cyan, Bg.Black)
socket               = LS.do(Fg.Magenta, Bg.Black)
symbolic_link        = LS.do(Fg.Cyan, Mod.Bold)
symbolic_link_broken = LS.do(Fg.Black, Bg.Red)
terminal_code        = LS.do()
text_license         = LS.do(Mod.Bold)
text_markup          = LS.do(Fg.Green)
text_normal          = LS.do()
text_special         = LS.do(Fg.Yellow, Mod.Bold)
tools                = LS.do(Fg.White)
unimportant          = LS.do(Fg.Black)

# Core LS_COLORS types that are not matched against file names
LS.color(normal, ['rs']) # Reset
LS.color(normal, ['no']) # Global default
LS.color(normal, ['fi']) # Normal file
LS.color(directory, ['di']) # Directory
LS.color(symbolic_link, ['ln']) # Symbolic link
LS.color(multi_hard_link, ['mh']) # Multi hard link
LS.color(pipe, ['pi']) # Named pipe
LS.color(door, ['do']) # Door
LS.color(device_block, ['bd']) # Block device
LS.color(device_char, ['cd']) # Character device
LS.color(symbolic_link_broken, ['or']) # Broken symbolic link
LS.color(socket, ['so']) # Socket
LS.color(normal, ['su']) # File that is setuid (u+s)
LS.color(normal, ['sg']) # File that is setgid (g+s)
LS.color(file_with_capability, ['ca']) # File with capability
LS.color(directory, ['tw']) # Directory: sticky and other-writable (+t,o+w)
LS.color(directory, ['ow']) # Directory: other-writable (o+w), not sticky
LS.color(directory, ['st']) # Directory: sticky (+t) and not other-writable
LS.color(executable, ['ex']) # Executable
LS.color(symbolic_link_broken, ['mi']) # Broken symbolic link (ls -l)

LS.color(archive, [
  # Compressed
  '*.7z', '*.arj', '*.bz', '*.bz2', '*.gz', '*.jar', '*.pkg', '*.rar', '*.tar',
  '*.tbz', '*.tbz2', '*.tgz', '*.xz', '*.z', '*.zip', '*.zst',
  # Images
  '*.bin', '*.dmg', '*.img', '*.iso', '*.toast', '*.vcd',
  # Packages
  '*.apk', '*.deb', '*.rpm',
])
LS.color(code, [
  # ActionScript
  '*.as',
  # AppleScript
  '*.applescript',
  # Arduino
  '*.ino',
  # Awk
  '*.awk',
  # Basic
  '*.vb',
  # Bash
  '*.bash',
  # BibTeX
  '*.bib', '*.bst',
  # Cabal
  '*.cabal',
  # Clojure
  '*.clj',
  # Crystal
  '*.cr',
  # C#
  '*.cs', '*.csx',
  # CSS
  '*.css',
  # C/C++
  '*.c', '*.c++', '*.cc', '*.cp', '*.cpp', '*.cxx', '*.def', '*.h', '*.h++',
  '*.hh', '*.hpp', '*.hxx', '*.inc', '*.inl', '*.ipp',
  # D
  '*.d', '*.di',
  # Dart
  '*.dart',
  # Diff
  '*.diff', '*.patch',
  # Elixir
  '*.ex', '*.exs',
  # Elm
  '*.elm',
  # Erlang
  '*.erl',
  # Elvish
  '*.elv',
  # Fish
  '*.fish',
  # F#
  '*.fs', '*.fsi', '*.fsx',
  # Go
  '*.go',
  # Groovy:
  '*.groovy', '*.gvy', '*.gradle',
  # Haskell
  '*.hs',
  # Java
  '*.java',
  # Javascript
  '*.cjs', '*.htc', '*.js', '*.jsx', '*.mjs', '*.vue',
  # Julia
  '*.jl',
  # KakouneScript
  '*.kak',
  # Kotlin
  '*.kt', '*.kts',
  # LaTeX
  '*.cls', '*.tex', '*.ltx',
  # Less
  '*.less',
  # LLVM
  '*.ll', '*.mir',
  # Lisp
  '*.lisp', '*.el',
  # Lua
  '*.lua',
  # Mathematica
  '*.nb',
  # MatLab
  '*.m', '*.matlab', '*.mn',
  # Nix
  '*.nix',
  # OCaml
  '*.ml', '*.mli',
  # Pascal
  '*.dpr', '*.p', '*.pas',
  # Perl
  '*.cgi', '*.pl', '*.pm', '*.pod', '*.t',
  # PHP
  '*.php',
  # PowerShell
  '*.ps1', '*.psd1', '*.psm1',
  # Puppet
  '*.epp', '*.pp',
  # PureScript
  '*.purs',
  # Python
  '*.ipynb', '*.py',
  # R
  '*.r',
  # Ruby
  '*.rb',
  # Rust
  '.rs',
  # Scala
  '*.sbt', '*.scala',
  # Shell
  '*.sh',
  # SQL
  '*.sql',
  # Swift
  '*.swift',
  # Tcl
  '*.tcl',
  # Typescript
  '*.ts', '*.tsx',
  # Verilog
  '*.sv', '*.svh', '*.v',
  # VHDL
  '*.vhd', '*.vhdl',
  # VimScript
  '*.vim',
  # Zsh
  '*.zsh',
])
LS.color(data_binary, [
  '*.bson', '*.pickle',
])
LS.color(data_text, [
  '*.cfg', '*.conf', '*.config', '*.cson', '*.csv', '*.desktop', '*.hjson',
  '*.ini', '*.json', '*.json5', '*.plist', '*.rc', '*.tml', '*.toml', '*.xml',
  '*.yaml', '*.yml',
])
LS.color(executable, [
  # Library
  '*.a', '*.dll', '*.dylib', '*.ko', '*.so',
  # Windows
  '*.bat', '*.com', '*.exe',
])
LS.color(font, [
  '*.fnt', '*.fon', '*.otf', '*.ttf',
])
LS.color(media_audio, [
  '*.aif', '*.flac', '*.m4a', '*.mid', '*.mp3', '*.ogg', '*.opus', '*.wav',
  '*.wma', '*.wv',
])
LS.color(media_image, [
  '*.bmp', '*.eps', '*.gif', '*.ico', '*.jpeg', '*.jpg', '*.pbm', '*.pgm',
  '*.png', '*.ppm', '*.psd', '*.svg', '*.tif', '*.tiff', '*.xcf',
])
LS.color(media_video, [
  '*.avi', '*.flv', '*.h264', '*.m4v', '*.mkv', '*.mov', '*.mp4', '*.mpeg',
  '*.mpg', '*.rm', '*.swf', '*.vob', '*.webm', '*.wmv',
])
LS.color(office, [
  # Calendar
  '*.ics',
  # Contacts
  '*.contacts', '*.vcard', '*.vcf',
  # Document
  '*.doc', '*.docx', '*.epub', '*.odt', '*.pdf', '*.ps', '*.rtf', '*.sxw',
  # Presentation
  '*.ppt', '*.pptx', '*.odp', '*.sxi', '*.kex', '*.pps',
  # Spreadsheet
  '*.xls', '*.xlsx', '*.ods', '*.xlr',
])
LS.color(text_license, [
  'COPYING', 'COPYING.md', 'COPYING.txt',
  'COPYRIGHT', 'COPYRIGHT.md', 'COPYRIGHT.txt',
  'LICENSE', 'LICENSE-APACHE', 'LICENSE-MIT', 'LICENSE.md', 'LICENSE.txt',
])
LS.color(text_markup, [
  # Man Pages
  '*.1', '*.2', '*.3', '*.4', '*.5', '*.6', '*.7', '*.8', '*.man', '*.roff',
  # Text
  '*.asciidoc', '*.markdown', '*.md', '*.mdx', '*.mdown', '*.pod', '*.rst',
  # Web
  '*.htm', '*.html', '*.shtml', '*.xhtml',
])
LS.color(text_normal, [
  '*.txt',
])
LS.color(text_special, [
  'CHANGELOG', 'CHANGELOG.md', 'CHANGELOG.txt',
  'CODE_OF_CONDUCT', 'CODE_OF_CONDUCT.md', 'CHANGELOG.txt',
  'CONTRIBUTING', 'CONTRIBUTING.md', 'CONTRIBUTING.txt',
  'CONTRIBUTORS', 'CONTRIBUTORS.md', 'CONTRIBUTORS.txt',
  'INSTALL', 'INSTALL.md', 'INSTALL.txt',
  'README', 'README.md', 'README.txt',
  'TODO', 'TODO.md', 'TODO.txt',
])
LS.color(tools, [
  # Automake
  'Makefile.am',
  # Bash
  '.bash_logout', '.bash_profile', '.bashrc',
  # Chezmoi
  '.chezmoi.json.tmpl', '.chezmoi.toml.tmpl', '.chezmoi.yaml.tmpl',
  '.chezmoidata.json', '.chezmoidata.toml', '.chezmoidata.yaml',
  '.chezmoiexternal.json', '.chezmoiexternal.toml', '.chezmoiexternal.yaml',
  '.chezmoiignore', '.chezmoiremove', '.chezmoiroot', '.chezmoiversion',
  '*.tmpl',
  # CI/CD
  '.travis.yml', 'appveyor.yml',
  # CMake
  '*.cmake', '*.cmake.in', 'CMakeLists.txt',
  # CNAME
  'CNAME',
  # Configure
  'configure', 'configure.ac',
  # Desktop
  '*.desktop',
  # Docker
  'Dockerfile',
  # Doxygen
  '*.dox', 'Doxyfile',
  # Editorconfig
  '.editorconfig',
  # Git
  '.gitattributes', '.gitconfig', '.gitignore', '.gitmodules',
  # GitHub
  'CODEOWNERS',
  # Go
  'go.mod', 'go.sum',
  # JavaScript/TypeScript
  '*config.js', '*config.json', '*config.ts',
  # Make
  'Makefile', '*.make',
  # Mercurial
  '.hgrc', 'hgrc',
  # Netlify
  'netlify.toml',
  # NPM
  'npm-shrinkwrap.json', 'package.json', 'package-lock.json',
  # Pip
  'requirements.txt',
  # Python
  'MANIFEST.in', 'setup.py',
  # Readline
  '.inputrc',
  # Ruby
  '*.gemspec',
  # Rust
  'Cargo.lock', 'Cargo.toml',
  # Scons
  'SConscript', 'SConstruct',
  # Style
  '.clang-format', '.flake8', '.prettierrc',
  # X
  '.dmrc', '.Xauthority', '.xinitrc', '.xsession-errors',
  # Yarn
  '.yarnrc', 'yarn.lock',
  # Other
  '.ignore',
])
LS.color(unimportant, [
  # Automake
  'Makefile.in',
  # C/C++
  '*.la', '*.lo', '*.o',
  # CMake
  'CMakeCache.txt',
  # Git Submodule file
  '*.git',
  # Haskell
  '*.cache', '*.dyn_hi', '*.dyn_o', '*.hi',
  # ICE
  '.ICEauthority',
  # Java
  '*.class',
  # Jekyll
  '.nojekyll',
  # LaTeX
  '*.aux', '*.bbl', '*.bcf', '*.blg', '*.fdb_latexmk', '*.figlist', '*.fls',
  '*.glg', '*.glstex', '*.idx', '*.ilg', '*.ind', '*.lof', '*.log', '*.lot',
  '*.out', '*.sty', '*.synctex.gz', '*.toc',
  # LLVM
  '*.bc',
  # macOS
  '.CFUserTextEncoding', '.DS_Store', '.localized',
  # Python
  '*.pyc', '*.pyd', '*.pyo',
  # Rust
  '*.rlib',
  # Scons
  '*.scons_opt', '*.sconsign.dblite',
  # Other
  '*.bak', '*.lock', '*.log', '*.old', '*.orig', '*.pid', '*.swp', '*.tmp',
  '*~', '.hushlogin', '.sudo_as_admin_successful',
])

print(json.dumps(LS.colors(), indent=2, sort_keys=True))
