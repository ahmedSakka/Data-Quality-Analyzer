import typer
import pandas as pd
import json
from commands.quality_check import quality_check
from commands.reporting import save_json, save_markdown, save_pdf
from typing import List, Optional

app = typer.Typer()

@app.command()
def analyze(file_path: str, 
            save: bool = typer.Option(False, "--save" ,help="Save the report."),
            format: str = typer.Option("json", help="Format of the report (json, markdown, or pdf). Default is json."),
            summary: bool = typer.Option(False, "--summary", help= "Show a concise summary of the report."),
            columns: Optional[List[str]] = typer.Option(None, "--columns", help="Specify columns to analyze. If not provided, all columns will be analyzed."),
            validate: bool = typer.Option(False, "--validate", help="Run validation checks on the data.")):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        typer.echo(f"Error loading file {e}")
        raise typer.Exit(code=1)
    
    typer.echo("File loaded successfully.")
    
    # Running quality checks on specefied columns or all columns
    if columns:
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            typer.echo(f"These columns do not exist in the DataFrame: {', '.join(missing_cols)}")
            raise typer.Exit(code=1)
        df = df[columns]
        typer.echo(f"Analyzing specified columns: {', '.join(columns)}")
    else:
        typer.echo("Analyzing all columns in the DataFrame.")

    report = quality_check(df, validate=validate)

    typer.echo("Quality check completed.")

    # Displaying summary or saving the report
    if summary:
        typer.echo("Summary Report:")
        typer.echo(json.dumps({
            "missing_values": report["missing_values"],
            "duplicate_rows": report["duplicate_rows"],
            "constant_columns": report["constant_columns"]
        }, indent=4))

    elif save:
        if format == "json":
            path = save_json(report)
        elif format == "markdown":
            path = save_markdown(report)
        elif format == "pdf":
            path = save_pdf(report, df)
        else:
            typer.echo("Invalid format. Please choose 'json' or 'markdown'")
            raise typer.Exit(code=1)
        typer.echo(f"Report saved to: {path}")
    else:
        typer.echo(json.dumps(report, indent=4))

if __name__ == "__main__":
    app()