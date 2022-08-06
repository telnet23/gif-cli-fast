# gif-cli-fast

Watch GIF animations in your terminal.

Inspired by [gif-for-cli](https://github.com/google/gif-for-cli) from Google. However, gif-cli-fast takes noticeably less time to initialize than gif-for-cli due to several optimizations. gif-cli-fast also supports GIPHY and local GIFs in addition to Tenor.

Installation
-
```
$ python -m pip install git+https://github.com/telnet23/gif-cli-fast
```

Usage
-

```
usage: gif [-h] [--provider {giphy,tenor,local}] [--cache CACHE] [--mode {ascii,256color,truecolor}] [--cols COLS] [--rows ROWS] [query ...]

positional arguments:
  query                 query to submit to provider. a trending gif is returned by default

options:
  -h, --help            show this help message and exit
  --provider {giphy,tenor,local}
                        provider to submit query to. giphy by default
  --mode {ascii,256color,truecolor}
                        display mode. ascii by default
  --cols COLS           terminal size. determined automatically by default
  --rows ROWS           terminal size. determined automatically by default
  --cache CACHE         cache directory. determined automatically by default

https://github.com/telnet23/gif-cli-fast
```

Examples
-

```
$ gif happy birthday
$ gif --provider giphy happy birthday
$ gif --provider local ~/gifs/happy-birthday.gif
```

Preferences
-
```
$ alias gif="gif --provider giphy --mode 256color"
```
