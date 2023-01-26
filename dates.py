# Get dates for arXiv papers
from notion_client import Client
import os
from dotenv import load_dotenv
from main import fetch_table
import arxiv


def fetch_table():
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    paper_db = notion.databases.query(database_id=os.getenv("NOTION_DATABASE_ID"))

    papers = []
    for paper in paper_db["results"]:
        if not paper["properties"]["Title"]["title"] == []:
            title = paper["properties"]["Title"]["title"][0]["plain_text"]
            url = paper["properties"]["URL"]["url"]
            date = paper["properties"]["Date"]["date"]
            if not url == None and url.startswith("https://arxiv.org/pdf/"):
                papers.append((title, url, date))

    return papers


def get_arxiv_dates():
    papers = fetch_table()

    ids = []
    for _, url, date in papers:
        if date == None:
            url = url.replace("https://arxiv.org/pdf/", "")
            url = url.replace(".pdf", "")
            ids.append(url)

    results = arxiv.Search(id_list=ids)
    for paper in results.results():
        date = paper.published.strftime("%b %d %Y")
        date = date + (15 - len(date)) * " "
        shorttitle = " ".join(paper.title.split(" ")[:4])
        print(f"{date} {shorttitle}")


def validate_dates():
    papers = fetch_table()

    ids = []
    datemap = {}
    for _, url, date in papers:
        if date == None:
            continue

        url = url.replace("https://arxiv.org/pdf/", "")
        url = url.replace(".pdf", "")
        ids.append(url)

        datemap[url] = date

    results = arxiv.Search(id_list=ids)
    for paper in results.results():
        arxiv_date = paper.published.strftime("%Y-%m-%d")
        paper_id = paper.entry_id.split("/")[-1].split("v")[0]
        date = datemap[paper_id]["start"]
        shorttitle = " ".join(paper.title.split(" ")[:4])
        if date != arxiv_date:
            print(
                f"Date for {shorttitle} is wrong: It should be {paper.published.strftime('%b %d %Y')}"
            )


if __name__ == "__main__":
    load_dotenv()
    get_arxiv_dates()
    validate_dates()
