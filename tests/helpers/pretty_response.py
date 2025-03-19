import click
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers import JsonLexer


def handle_response(response):
    """Handles the response and formats it for output."""
    json_data = response.model_dump_json(indent=2)
    formatted_data = highlight(json_data, JsonLexer(), TerminalFormatter())
    click.echo(click.style(formatted_data))
