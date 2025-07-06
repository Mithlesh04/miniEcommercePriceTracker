import re
import os
from datetime import datetime


"""
@save_page_html

Save the given HTML content to a file named after the URL.
This is useful for debugging purposes when the scraper fails to extract product details.
"""
def save_page_html(url: str, page_source: str, site_name: str, folder: str = "./error_html_pages") -> None:
    """
    Save the given HTML content to a file named after the URL.
    Invalid filename characters are replaced with underscores.
    """
    # Make sure folder exists
    os.makedirs(folder, exist_ok=True)

    # Sanitize the URL into a safe filename
    # safe_name = re.sub(r'[\\/*?:"<>|]', "_", url).strip()
    # safe_name = re.sub(r'\s+', "_", safe_name)  # replace spaces with _
    safe_name = datetime.now().strftime("%H-%M-%S-%f")[:-3]
    filename = f"{site_name}_{safe_name}.html"

    filepath = os.path.join(folder, filename)

    # Write to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(page_source)

