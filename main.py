import typer
from commands.analyze import analyze_command

app = typer.Typer()

app.command()(analyze_command)

if __name__ == "__main__":
    app()