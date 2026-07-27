import time
import requests
import os


class GeminiClient:

    def __init__(
        self,
        api_key,
        model="gemini-2.5-flash"
    ):

        self.api_key = api_key
        self.model = model

        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

        self.url = (
            f"{self.base_url}/{model}:generateContent?key={api_key}"
        )

        self.headers = {
            "Content-Type": "application/json"
        }

    # =====================================================
    # Generate AI Response
    # =====================================================

    def generate(
        self,
        prompt,
        retries=3
    ):

        payload = {

            "contents": [

                {

                    "parts": [

                        {

                            "text": prompt

                        }

                    ]

                }

            ],

            "generationConfig": {

                "temperature": 0.2,

                "topP": 0.9,

                "topK": 40,

                "maxOutputTokens": 8192,

                "responseMimeType": "application/json"

            }

        }

        for attempt in range(retries):

            print(
                f"\nCalling Gemini ({attempt+1}/{retries})..."
            )

            try:

                response = requests.post(

                    self.url,

                    headers=self.headers,

                    json=payload,

                    timeout=180

                )

                if response.status_code == 200:

                    data = response.json()

                    candidates = data.get(
                        "candidates",
                        []
                    )

                    if not candidates:

                        print(
                            "No candidates returned."
                        )

                        continue

                    content = candidates[0].get(
                        "content",
                        {}
                    )

                    parts = content.get(
                        "parts",
                        []
                    )

                    if not parts:

                        print(
                            "No content returned."
                        )

                        continue

                    return parts[0].get(
                        "text",
                        ""
                    )

                print("\nGemini API Error")

                print(
                    "Status:",
                    response.status_code
                )

                print(
                    response.text
                )

            except requests.Timeout:

                print(
                    "Gemini request timed out."
                )

            except requests.ConnectionError:

                print(
                    "Unable to connect to Gemini."
                )

            except Exception as ex:

                print(ex)

            time.sleep(5)

        return ""
    
    def generate_image(self, prompt, output_path):

        print("\nGenerating AI Diagram using Pollinations...")

        url = "https://image.pollinations.ai/prompt/" + requests.utils.quote(prompt)

        response = requests.get(
            url,
            timeout=120
        )

        response.raise_for_status()

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        with open(output_path, "wb") as f:
            f.write(response.content)

        print("Image saved:", output_path)

        return output_path
    
# ====================================================
# Health Check
# =====================================================

    def test_connection(self):

        print("\nTesting Gemini Connection...")

        result = self.generate(
            'Return ONLY {"status":"ok"}'
        )

        if result:

            print("Gemini Connected Successfully.")

            return True

        print("Gemini Connection Failed.")

        return False