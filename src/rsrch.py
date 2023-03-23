import math
import os

import arxiv
import requests
import urllib3
from dotenv import load_dotenv
from notion_client import Client
from tqdm import tqdm

import utils


def download_papers():
    print("Downloading papers from Notion...")
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    load_dotenv()
    papers = utils.fetch_table()

    if not os.path.exists("../papers"):
        os.mkdir("../papers")

    for title, url, _, _ in papers:
        path = f"../papers/{title.replace(' ', '_')}.pdf"
        if not os.path.exists(path):
            print(f'\nDownloading "{title}"')
            try:
                r = requests.get(url, stream=True, verify=True)
            except requests.exceptions.SSLError:
                r = requests.get(url, stream=True, verify=False)

            with open(path, "wb") as f:
                for chunk in tqdm(
                    r.iter_content(chunk_size=1024),
                    total=math.ceil(int(r.headers["Content-Length"]) / 1024),
                    unit="KB",
                ):
                    if chunk:
                        f.write(chunk)


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
        elif url.startswith("https://arxiv.org/pdf/") and url.endswith(".pdf"):
            ids.append(url.replace("https://arxiv.org/pdf/", "").replace(".pdf", ""))
        elif requests.get("https://arxiv.org/abs/" + url).status_code == 200:
            ids.append(url)
        else:
            print(f"ERROR: {url} is not a valid arXiv abstract URL, PDF URL, or ID.")

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
        else:
            print(f"- {title} (already exists)")

    print("Done!")
