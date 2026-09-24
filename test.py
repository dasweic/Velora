import json
from pathlib import Path
from playwright.sync_api import sync_playwright


def save_page(url, filename="page.json"):

    with sync_playwright() as p:

        # Open Chromium
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        # Open website
        page.goto(url, wait_until="domcontentloaded")

        # Wait for JavaScript content
        page.wait_for_timeout(2000)

        def get_elements(selector):

            elements = page.locator(selector)
            result = []

            for i in range(elements.count()):

                element = elements.nth(i)

                try:
                    data = element.evaluate("""
                    (el) => {

                        function get_selector(el) {

                            if (el.id)
                                return "#" + CSS.escape(el.id);

                            let path = [];

                            while (el && el.nodeType === 1) {

                                let selector =
                                    el.tagName.toLowerCase();

                                if (el.classList.length) {
                                    selector += "." +
                                        [...el.classList]
                                        .map(c => CSS.escape(c))
                                        .join(".");
                                }

                                let index = 1;
                                let sibling =
                                    el.previousElementSibling;

                                while (sibling) {

                                    if (
                                        sibling.tagName ===
                                        el.tagName
                                    ) {
                                        index++;
                                    }

                                    sibling =
                                        sibling.previousElementSibling;
                                }

                                if (index > 1) {
                                    selector +=
                                        `:nth-of-type(${index})`;
                                }

                                path.unshift(selector);

                                if (el.id)
                                    break;

                                el = el.parentElement;
                            }

                            return path.join(" > ");
                        }

                        return {

                            tag: el.tagName.toLowerCase(),

                            text:
                                (el.innerText || "").trim(),

                            id:
                                el.id || null,

                            name:
                                el.getAttribute("name"),

                            type:
                                el.getAttribute("type"),

                            placeholder:
                                el.getAttribute("placeholder"),

                            href:
                                el.href || null,

                            selector:
                                get_selector(el)
                        };
                    }
                    """)

                    result.append(data)

                except Exception:
                    pass

            return result

        # Only these 3 types
        data = {

            "url": page.url,

            "title": page.title(),

            "links":
                get_elements("a"),

            "inputs":
                get_elements("input"),

            "buttons":
                get_elements("button")
        }

        # Save JSON
        Path(filename).write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        print("✅ Page saved!")
        print(f"📄 {Path(filename).absolute()}")

        browser.close()


if __name__ == "__main__":

    url = input("Enter URL: ").strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    save_page(url)