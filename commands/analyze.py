import typer
from pathlib import Path


# Analyzing the given CSV file for data quality issues
def analyze_command(file_path: Path):
    if not file_path.exists() or not file_path.suffix == '.csv':
        typer.echo("Please provide a valid CSV file!")
        raise typer.Exit(code=1)
    
    typer.echo(f"Analyzing {file_path}...")