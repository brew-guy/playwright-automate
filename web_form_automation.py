import json
import sys

from playwright.sync_api import sync_playwright


def automate_form(url, input_text):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Wait for and find the input field (adjust selector as needed)
        page.fill("#NameTextBox", input_text)

        # Find and click the submit button
        page.click("#SearchButton")

        # Wait for results to load (adjust selector and timing as needed)
        try:
            result = page.wait_for_selector(
                "#AuthorizationIdValue", timeout=3000
            ).inner_text()
            fname = page.query_selector("#FacilityName").inner_text()
            lname = page.query_selector("#Label2").inner_text()

            return json.dumps(
                {
                    "success": True,
                    "auth_id": result,
                    "first_name": fname,
                    "last_name": lname,
                }
            )
        except Exception as e:
            return json.dumps({"success": False, "error": "Result element not found"})
        finally:
            browser.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python web_form_automation.py <input_text>")
        sys.exit(1)

    URL = "https://autregweb.sst.dk/authorizationsearch.aspx"
    INPUT_TEXT = sys.argv[1]

    result = automate_form(URL, INPUT_TEXT)
    if result:
        print(f"Scraped result: {result}")
