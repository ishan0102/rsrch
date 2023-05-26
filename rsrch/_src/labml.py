import json
import string
import time

import arxiv
import requests
from rich.console import Console
from rich.table import Table
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm


def get_authorization_token():
    # Set up options for headless browsing
    options = Options()
    options.add_argument("--headless")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    )

    # Set up the Selenium webdriver
    driver = webdriver.Chrome(options=options)

    # Open the website in the browser
    driver.get("https://papers.labml.ai")

    # Wait for the page to load
    time.sleep(1)

    # Retrieve the authorization token from cookies
    cookies = driver.get_cookies()
    authorization_token = next((cookie["value"] for cookie in cookies if cookie["name"] == "Authorization"), None)

    # Close the browser
    driver.quit()

    return authorization_token


def fetch_paper_details(paper):
    title = paper["title"]["text"].replace("\n", " ")
    title = " ".join(title.split())
    title = title.translate(str.maketrans("", "", string.punctuation))

    search = arxiv.Search(
        query=title,
        max_results=10,
    )

    return next(search.results(), None)


def popular(sort_by="weekly", num_papers=5):
    """
    Retrieves popular papers from papers.labml.ai.

    Parameters:
        sort_by (str): Sorting option for popular papers. Default is "weekly".
        num_papers (int): Number of popular papers to retrieve. Default is 5.

    Returns:
        List[arxiv.arxiv.Result]: List of popular paper results.

    Retrieves popular papers from the papers.labml.ai API.
    Fetches an authorization token and sends a request to retrieve the papers.
    Prints the paper titles and metadata using the 'fetch_paper_details' function.
    Displays progress information using the 'tqdm' library.

    Note:
        - Requires the 'requests', 'json', 'time', 'tqdm', 'rich', 'rich.console', and 'rich.table' libraries.
        - 'get_authorization_token' and 'fetch_paper_details' functions are assumed to be defined elsewhere.

    Example Usage:
        results = popular(sort_by="monthly", num_papers=10)
        print(results[0].title])
    """

    # Validate input parameters
    valid_sort_options = ["daily", "weekly", "monthly"]
    if sort_by not in valid_sort_options:
        raise ValueError(f"Invalid sort_by option. Choose one of {valid_sort_options}.")

    if not isinstance(num_papers, int) or num_papers < 1 or num_papers > 50:
        raise ValueError("num_papers must be a positive integer between 1 and 50.")

    # Get the initial authorization token
    console = Console()
    console.print("Getting authorization token for papers.labml.ai...")
    authorization_token = get_authorization_token()
    console.print(f"Authorization token: {authorization_token}\n")

    url = f"https://papers.labml.ai/api/v1/papers?sorted_by={sort_by}&start=0&end={num_papers}"

    headers = {
        "Authorization": json.dumps({"token": authorization_token}),
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    }

    try:
        with requests.Session() as session:
            response = session.get(url, headers=headers)
            while response.status_code != 200:
                console.print(f"[bold red]Status code:[/bold red] {response.status_code}")
                console.print(f"[bold red]Response:[/bold red] {response.json()}")
                console.print("Retrying...")
                time.sleep(1)
                response = session.get(url, headers=headers)

            papers = response.json()["data"]["papers"]
            paper_data = []
            for paper in tqdm(papers):
                try:
                    metadata = fetch_paper_details(paper)
                    if metadata is not None:
                        paper_data.append(metadata)
                except Exception as e:
                    console.print(f"[bold yellow]Error occurred:[/bold yellow] {e}")

            console.print(f"\nFound {len(paper_data)} out of {len(papers)} paper successfully.\n")
            if len(paper_data) > 0:
                table = Table(title="Popular Papers", header_style="bold blue")
                table.add_column("Title")
                table.add_column("Date")
                table.add_column("URL")

                for paper in paper_data:
                    table.add_row(paper.title, str(paper.published).split()[0], paper.pdf_url)

                console.print(table)

            return paper_data

    except Exception as e:
        console.print(f"[bold red]Error occurred:[/bold red] {e}")
