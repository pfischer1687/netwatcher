# NetWatcher

NetWatcher CLI - Monitor outbound network connections.

**Usage**:

```console
$ netwatcher [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `scan`: Scan IP addresses using IP-API with...
* `version`: Print the installed version of the package.

## `netwatcher scan`

Scan IP addresses using IP-API with configurable logging and language support.

Args:
    lang (str): Language code for the IP API response. Defaults to `en`.
    log_to_file (bool): Whether to write logs to a file instead of stderr. Defaults to `False`.
    verbose (int): Verbosity level (-v, -vv, -vvv). Defaults to 0.

**Usage**:

```console
$ netwatcher scan [OPTIONS]
```

**Options**:

* `--lang TEXT`: Language code for the IP API response.  [default: en]
* `--log-to-file / --no-log-to-file`: Whether to log to file or just to stderr.  [default: no-log-to-file]
* `-v, --verbose`: Increase verbosity (-v, -vv, -vvv)  [default: 1]
* `--help`: Show this message and exit.

## `netwatcher version`

Print the installed version of the package.

**Usage**:

```console
$ netwatcher version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
