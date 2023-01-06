# Download Papers from a Notion Database
If you have a Notion database with `Title` and `URL` fields for research papers, this will download them to the `papers/` directory locally.
<p align="center">
  <img width="800" alt="image" src="https://user-images.githubusercontent.com/47067154/209739153-814b31ac-d2e8-4b80-b622-ee0ae607019f.png">
</p>
<p align="center">
  <img width="700" alt="image" src="https://user-images.githubusercontent.com/47067154/210903470-3a52aa5c-30b1-48fd-8de3-914d86430dcc.png">
</p>

## Usage
1. Create an [internal integration](https://www.notion.so/help/create-integrations-with-the-notion-api) in Notion.

2. [Add the integration](https://www.notion.so/help/add-and-manage-connections-with-the-api#add-connections-to-pages) to the database you want to download from.

3. Create a `.env` file with the following variables:

    ```
    NOTION_TOKEN=secret_XXXXXXXX
    NOTION_DATABASE_ID=XXXXXXXXXXXXXXXX
    ```
    Your `NOTION_TOKEN` can be found in your [integrations page](https://www.notion.so/my-integrations) and is called the **Internal Integration Token**. The `NOTION_DATABASE_ID` can be found in the [URL of your database](https://www.notion.so/my-integrations) (`https://www.notion.so/{workspace_name}/{database_id}?v={view_id}`).

4. Install local dependencies:

    ```bash
    python3 -m venv venv
    pip install -r requirements.txt
    ```

5. Run the script:

    ```bash
    python3 download.py
    ```

This will skip over any papers that have already been downloaded (based on the `Title` already existing in `papers/`).

## Notes
- The script will download the PDFs to the `papers/` directory. If you want to change this, you can change the `path` variable in `main.py`.
- I plan on adding support for other databases in the future, but for now it only works with Notion databases.

## Resources
- [Notion API](https://developers.notion.com/)