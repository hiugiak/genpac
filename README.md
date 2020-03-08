# GenPAC

Generate PAC file from gfwlist and user rules

## Install

This project requires Python >= 3.3. You can clone this project to run:

```shell
$ git clone https://github.com/hiugiak/genpac.git
```

## Usage

You can print help message to your console:

```shell
$ ./genpac.py

usage: genpac [-h] [-v] [-g GFWLIST] [-u /path/to/user-rule]
              [--log-level LEVEL] -p PROXY
              output

generate PAC file from gfwlist and user-rules

positional arguments:
  output                the path to the output PAC file

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -g GFWLIST, --gfwlist GFWLIST
                        a local path or remote url to the gfwlist encoded in
                        base64
  -u /path/to/user-rule, --user-rule /path/to/user-rule
                        the file contains user rules
  --log-level LEVEL     the value must be "DEBUG", "INFO" (default), "WARN",
                        "ERROR" or "FATAL
  -p PROXY, --proxy PROXY
                        proxy string in PAC file
```

You can generate a pac file with proxy set to `PROXY http://localhost:1080`:

```shell
$ ./genpac.py -p "PROXY http://localhost:1080;" proxy.pac
```

You can use a custom gfwlist in Base64 format:

```shell
$ ./genpac.py -g gfwlist.txt -p "PROXY http://localhost:1080;" proxy.pac
```

Or you can use a online gfwlist instead:

```shell
$ ./genpac.py -g https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt -p "PROXY http://localhost:1080;" proxy.pac
```

If `-g` option is not specified, the program will use `https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt` by default.

Plus, you can add additional rules of your own:

```shell
$ ./genpac.py -u user-rule.txt -p "PROXY http://localhost:1080;" proxy.pac
```

## Contributing

Want to contribute? [Open an issue](https://github.com/hiugiak/genpac/issues/new) or submit PRs.

## License

MIT © [HiuGiak](https://github.com/hiugiak)