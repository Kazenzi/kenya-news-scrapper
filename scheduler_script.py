import os
from datetime import datetime, timedelta

import click
from flask import Flask
from pymongo import MongoClient

from app import app
from news.scrape_cli import get_all_news as get_news_cli
from news.scrape_web import get_news

# --------------------------------------
# CLI Commands using Flask CLI and Click
# --------------------------------------

@app.cli.command("news_web")
def news_web():
    """
    Gets news from the web, then saves them in the database
    """
    click.echo("Fetching news from web and saving to DB...")
    get_news()


@app.cli.command("news_cli")
def news_cli():
    """
    Gets news from the web and displays in CLI (no DB)
    """
    click.echo("Fetching news for CLI display...")
    get_news_cli()


@app.cli.command("delete_old_news")
def delete_old_news():
    """
    Deletes news older than 48 hours from the database
    """
    click.echo("Deleting news older than 48 hours...")
    client = MongoClient(os.environ['MongoDB_URI'])
    db = client['kenya-news']  # Select the database
    collection = db.news
    time_boundary = datetime.now() - timedelta(hours=48)
    print(f"Deleting news before: {time_boundary.isoformat()}")
    collection.delete_many({'$or': [
        {'date': {'$lt': time_boundary.isoformat()}},
        {'date': {'$eq': 0}}
    ]})
    click.echo("Old news deleted.")


# No need for manager.run() anymore
if __name__ == "__main__":
    app.run(debug=True)