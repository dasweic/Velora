import requests
import websocket
import json
import time
import webbrowser


CDP_URL = "http://localhost:9222"


class Browser:

    def __init__(self):
        self.ws = None
        self.message_id = 0

    def open(self, url):
        # New tab create karo
        response = requests.put(
            f"{CDP_URL}/json/new?{url}"
        )

        tab = response.json()

        # WebSocket connect
        self.ws = websocket.create_connection(
            tab["webSocketDebuggerUrl"]
        )

        # Runtime enable
        self.send("Runtime.enable")

        time.sleep(2)

    def send(self, method, params=None):
        self.message_id += 1

        message = {
            "id": self.message_id,
            "method": method
        }

        if params:
            message["params"] = params

        self.ws.send(json.dumps(message))

        while True:
            response = json.loads(self.ws.recv())

            if response.get("id") == self.message_id:
                return response

    def click(self, selector):
        script = f"""
        (() => {{
            const element = document.querySelector({json.dumps(selector)});

            if (!element) {{
                return {{
                    success: false,
                    error: "Element not found"
                }};
            }}

            element.click();

            return {{
                success: true
            }};
        }})()
        """

        result = self.send(
            "Runtime.evaluate",
            {
                "expression": script,
                "returnByValue": True
            }
        )

        return result

    def type(self, selector, text):
        script = f"""
        (() => {{
            const element = document.querySelector({json.dumps(selector)});

            if (!element) {{
                return {{
                    success: false,
                    error: "Element not found"
                }};
            }}

            element.focus();
            element.value = {json.dumps(text)};

            element.dispatchEvent(
                new Event("input", {{ bubbles: true }})
            );

            element.dispatchEvent(
                new Event("change", {{ bubbles: true }})
            );

            return {{
                success: true
            }};
        }})()
        """

        return self.send(
            "Runtime.evaluate",
            {
                "expression": script,
                "returnByValue": True
            }
        )


# --------------------------------
# USE
# --------------------------------

browser = Browser()

browser.open("https://youtube.com")

result = browser.click("#search-button")

ollama pull qwen2.5-vl:7b

print(result)