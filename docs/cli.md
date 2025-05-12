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

* `scan`: _summary_.
* `version`: Print the installed version of the package.

## `netwatcher scan`

_summary_.

Args:
    verbose (int, optional): _description_. Defaults to typer.Option(1, &quot;--verbose&quot;, &quot;-v&quot;, count=True,
        help=&quot;Increase verbosity (-v, -vv, -vvv)&quot;).
    log_to_file (bool, optional): _description_. Defaults to typer.Option(False, help=&quot;Override default log file
        path&quot;).

**Usage**:

```console
$ netwatcher scan [OPTIONS]
```

**Options**:

* `-v, --verbose`: Increase verbosity (-v, -vv, -vvv)  [default: 0]
* `-l`: Whether to log to file or just to stderr.
* `--help`: Show this message and exit.

## `netwatcher version`

Print the installed version of the package.

**Usage**:

```console
$ netwatcher version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
