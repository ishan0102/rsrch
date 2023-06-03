# rsrch
Manage your research papers from Python. This project lets you update a Notion database with arXiv links and download PDFs of papers to your local machine.

<p align="center">
    <img width="1095" alt="image" src="https://user-images.githubusercontent.com/47067154/219932040-ab4962f8-b01e-4d94-9eba-77a155b0e933.png">
</p>

## Installation
1. Create an [internal integration](https://www.notion.so/help/create-integrations-with-the-notion-api) in Notion.

2. [Add the integration](https://www.notion.so/help/add-and-manage-connections-with-the-api#add-connections-to-pages) to the database you want to download from.

3. Store your `NOTION_TOKEN` and `NOTION_DATABASE_ID` somewhere safe. Your `NOTION_TOKEN` can be found in your [integrations page](https://www.notion.so/my-integrations) and is called the **Internal Integration Token**. The `NOTION_DATABASE_ID` can be found in the [URL of your database](https://www.notion.so/my-integrations) (`https://www.notion.so/{workspace_name}/{database_id}?v={view_id}`).

4. Install local dependencies:

    ```bash
    pip install rsrch
    ```

5. **Important**: Your Notion database must have the following columns with the corresponding types:
    - **Title**: `Title`
    - **URL**: `URL`
    - **Date**: `Date`
    - **Authors**: `Text`

    You can add more columns, but these are the ones that are required.

## Usage
### Setup
```python
from rsrch import RsrchClient

client = RsrchClient(
    token=NOTION_TOKEN,
    database_id=NOTION_DATABASE_ID,
)
```

### Download
This will download all the papers from your Notion database to the `papers/` directory.

```python
client.download()
```

<p>
    <img width="1097" alt="image" src="https://user-images.githubusercontent.com/47067154/232264456-4bdef487-36e8-4627-95c3-82f5c3876082.png">
</p>

### Upload
You can upload arXiv abstract links, PDF links, or IDs to your Notion database and have it autofill all of the relevant fields.

```python
client.upload(
    arxiv_urls=[
        "https://arxiv.org/abs/1706.03762",
        "https://arxiv.org/pdf/1706.03762.pdf",
        "1706.03762",
    ]
)
```

<p>
    <img width="1095" alt="image" src="https://user-images.githubusercontent.com/47067154/232264615-82b42d8c-ca1c-4f21-899f-439a6c8a7879.png">
</p>

Alternatively, you can add non-arXiv links manually to Notion.

## Notes
- Uploading papers to Notion is currently only supported for arXiv links. Papers with titles that already exist in the database will not be uploaded.
- I plan on adding support for other databases in the future, but for now it only works with Notion databases.
- To build and release this:
  - Make new code accessible in `src/__init__.py`
  - Update the version in `src/__about__.py`
  - Run `python3 -m build`
  - Run `python3 -m twine upload dist/*`

### Resources
- [Notion API](https://developers.notion.com/)
