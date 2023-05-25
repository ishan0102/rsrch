import math
import os

import arxiv
import requests
import urllib3
from dotenv import load_dotenv
from notion_client import Client
from tqdm import tqdm


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


def download():
    """
    Downloads papers from Notion.

    Returns:
        None

    Downloads papers from the Notion database.
    Paper URLs are fetched from the table using the 'fetch_table' function.
    The downloaded papers are saved in a 'papers' directory.
    Existing files are skipped.
    Prints progress information for each paper being downloaded.

    Note:
        - Requires the 'python-dotenv', 'urllib3', 'requests', and 'tqdm' libraries.
        - 'fetch_table' function is assumed to be defined elsewhere.

    Example Usage:
        download()
    """
    print("Downloading papers from Notion...")
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    load_dotenv()
    papers = fetch_table()

    if not os.path.exists("papers"):
        os.mkdir("papers")

    for title, url, _, _ in papers:
        path = f"papers/{title.replace(' ', '_')}.pdf"
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


def upload(arxiv_urls):
    """
    Uploads papers from arXiv to Notion.

    Parameters:
        arxiv_urls (list): List of arXiv URLs or IDs.

    Returns:
        None

    Connects to Notion API and uploads papers from arXiv.
    Creates new papers in Notion, skipping existing ones.
    Prints "Done!" when finished.

    Example:
        urls = [
            "https://arxiv.org/abs/2105.12345",
            "https://arxiv.org/abs/2106.67890",
            "https://arxiv.org/pdf/2107.24680.pdf"
        ]
        upload(urls)
    """
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
    papers = fetch_table()
    titles = [title for title, _, _, _ in papers]

    # Fetch paper data from arXiv
    print("Uploading papers to Notion...\n")
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

    print("\nDone!")
