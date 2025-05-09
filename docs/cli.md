# NetWatcher

**Usage**:

```console
$ netwatcher [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `hello`: _summary_.
* `goodbye`: _summary_.

## `netwatcher hello`

_summary_.

Args:
    name (str): _description_

**Usage**:

```console
$ netwatcher hello [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

## `netwatcher goodbye`

_summary_.

Args:
    name (str): _description_
    formal (bool, optional): _description_. Defaults to False.

**Usage**:

```console
$ netwatcher goodbye [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--formal / --no-formal`: [default: no-formal]
* `--help`: Show this message and exit.
