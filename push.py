import os

import arxiv
from dotenv import load_dotenv
from notion_client import Client

import utils


def create_paper(notion, title, url, date, authors):
    notion.pages.create(
        parent={
            "database_id": os.getenv("NOTION_DATABASE_ID"),
        },
        properties={
            "Title": {
                "title": [
                    {
                        "text": {
                            "content": title,
                        },
                    },
                ],
            },
            "URL": {
                "url": url,
            },
            "Date": {
                "date": {
                    "start": date,
                },
            },
            "Authors": {
                "rich_text": [
                    {
                        "text": {
                            "content": authors,
                        },
                    },
                ],
            },
        },
    )

    print(f"- {title}")


def push_papers(arxiv_urls):
    load_dotenv()
    notion = Client(auth=os.getenv("NOTION_TOKEN"))

    # Extract arXiv IDs from valid URLs
    ids = []
    for url in arxiv_urls:
        if url.startswith("https://arxiv.org/abs/"):
            ids.append(url.replace("https://arxiv.org/abs/", ""))

    # Fetch titles of papers already in Notion
    papers = utils.fetch_table()
    titles = [title for title, _, _, _ in papers]

    # Fetch paper data from arXiv
    print("Pushing papers to Notion...")
    results = arxiv.Search(id_list=ids)
    for paper in results.results():
        # Date is in ISO 8601 format, e.g. 2020-01-01
        date = paper.published.isoformat().split("T")[0]

        # Paper title
        title = paper.title

        # Paper authors (max 5)
        authors = [author.name for author in paper.authors]
        if len(authors) > 5:
            authors = ", ".join(authors[:5]) + ", et al."
        else:
            authors = ", ".join(authors)

        # Paper URL
        pdf_url = paper.pdf_url

        # Create paper in Notion if it doesn't already exist
        if title not in titles:
            create_paper(notion, title, pdf_url, date, authors)
