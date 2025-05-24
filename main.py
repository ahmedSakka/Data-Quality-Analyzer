import typer
import pandas as pd
import json
from commands.quality_check import quality_check
from commands.reporting import save_json, save_markdown

app = typer.Typer()

@app.command()
def analyze(file_path: str, 
            save: bool = typer.Option(False, "--save" ,help="Save the report."),
            format: str = typer.Option("json", help="Format of the report (json or markdown)")):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        typer.echo(f"Error loading file {e}")
        raise typer.Exit(code=1)
    
    typer.echo("File loaded successfully.")
    typer.echo("Performing quality check...")

    report = quality_check(df)

    typer.echo("Quality check completed.")

    if save:
        if format == "json":
            path = save_json(report)
        elif format == "markdown":
            path = save_markdown(report)
        else:
            typer.echo("Invalid format. Please choose 'json' or 'markdown'")
            raise typer.Exit(code=1)
        typer.echo(f"Report saved to: {path}")
    else:
        typer.echo(json.dumps(report, indent=4))

if __name__ == "__main__":
    app()