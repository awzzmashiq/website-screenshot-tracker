import os
import pandas as pd
from playwright.sync_api import sync_playwright

# Input and Output file paths
input_file = "urls.txt"  # File containing list of URLs (one per line)
output_dir = "screenshots"  # Directory to save screenshots
output_csv = "url_screenshots.csv"  # CSV file to store URL-image mapping

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def capture_screenshots():
    # Read URLs from file
    with open(input_file, "r") as file:
        urls = [line.strip() for line in file if line.strip()]

    # List to store data for CSV
    url_image_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for url in urls:
            try:
                # Visit the URL
                page.goto(url, timeout=10000)  # 10s timeout
                
                # Generate image file name
                image_filename = os.path.join(output_dir, f"{url.replace('https://', '').replace('http://', '').replace('/', '_')}.png")
                
                # Capture and save screenshot
                page.screenshot(path=image_filename, full_page=True)
                
                # Append to list
                url_image_data.append([url, image_filename])

                print(f"Captured: {url}")

            except Exception as e:
                print(f"Failed to capture {url}: {e}")
                url_image_data.append([url, "ERROR"])

        browser.close()

    # Save results to CSV
    df = pd.DataFrame(url_image_data, columns=["URL", "Image File"])
    df.to_csv(output_csv, index=False)
    print(f"Results saved in {output_csv}")

capture_screenshots()
