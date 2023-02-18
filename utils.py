import os

from notion_client import Client


def fetch_table():
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    paper_db = notion.databases.query(database_id=os.getenv("NOTION_DATABASE_ID"))

    papers = []
    for paper in paper_db["results"]:
        if not paper["properties"]["Title"]["title"] == []:
            title = paper["properties"]["Title"]["title"][0]["plain_text"]
            url = paper["properties"]["URL"]["url"]
            date = paper["properties"]["Date"]["date"]["start"]
            authors = paper["properties"]["Authors"]["rich_text"][0]["plain_text"]
            if not url == None and url.startswith("http"):
                papers.append((title, url, date, authors))

    return papers
