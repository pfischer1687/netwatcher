"""NetWatcher CLI - Monitor outbound network connections."""

import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    """_summary_.

    Args:
        name (str): _description_
    """
    print(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    """_summary_.

    Args:
        name (str): _description_
        formal (bool, optional): _description_. Defaults to False.
    """
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
