import typer
import pandas as pd
import json
from commands.quality_check import quality_check

app = typer.Typer()

@app.command()
def analyze(file_path: str, save: bool = False):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        typer.echo(f"Error loading file {e}")
        raise typer.Exit(code=1)
    
    typer.echo("File loaded successfully.")
    typer.echo("Performing quality check...")

    report = quality_check(df)
    typer.echo("Quality check completed.")
    typer.echo(json.dumps(report, indent=4))

    if save:
        with open("Report.json", "w") as f:
            json.dump(report, f, indent=4)
            typer.echo("\nReport saved to 'Report.json'")

if __name__ == "__main__":
    app()