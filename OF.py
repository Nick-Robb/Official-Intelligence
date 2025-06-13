# --- Begin Revised Code ---

# 1. Import and load environment variables
import os
from dotenv import load_dotenv  # Import python-dotenv to load .env file
import logging
load_dotenv()  # Load variables from .env file (ensure .env is in the same directory)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 2. Import other required libraries, including sys for exiting the script
import sys
import requests
import schedule
import time
from openai import OpenAI  # OpenAI client instantiation

# 3. Configuration: Get API keys and URLs from environment variables (no hardcoding)
HASHNODE_API_URL = os.getenv("HASHNODE_API_URL", "https://gql.hashnode.com/")
HASHNODE_API_KEY = os.getenv("HASHNODE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PUBLICATION_ID = os.getenv("PUBLICATION_ID", "67bf728ab1f3d8f525a03222")

# 4. Validate that the API keys are loaded
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")
if not HASHNODE_API_KEY:
    raise ValueError("HASHNODE_API_KEY is not set in environment variables.")

# 5. Initialize the OpenAI client with the loaded API key
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_blog_post():
    prompt = (
        """Write an engaging blog post centered on a real, high-profile cybersecurity incident—such as the SolarWinds hack, the Colonial Pipeline ransomware attack, or the Log4j vulnerability. Use verifiable details from public reports and avoid fictionalizing the event. Focus on the actual timeline, attack vectors, and vulnerabilities that were exploited. Then, provide an in-depth analysis of how AI-driven technologies (including machine learning-based anomaly detection, predictive analytics, and tools like ChatGPT) could have been deployed to detect, mitigate, or prevent the incident.

Your article should include:
- A bold, attention-grabbing title that highlights the incident and the innovative role of AI.
- A concise introduction summarizing the incident and its real-world impact.
- A factual breakdown of the incident, referencing publicly available details.
- A clear discussion on how specific AI solutions might have improved detection, response, or prevention, along with their limitations.
- A forward-looking conclusion offering actionable insights on integrating AI into cybersecurity strategies.

Adopt an authoritative, current, and innovative tone, engaging cybersecurity professionals with accurate analysis and actionable ideas."""

    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a cybersecurity AI blogger."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error("Error generating blog post: %s", e)
        return None

def publish_to_hashnode(title, content):
    headers = {
        "Authorization": f"Bearer {HASHNODE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": """
            mutation PublishPost($input: PublishPostInput!) {
              publishPost(input: $input) {
                post {
                  id
                  slug
                  title
                  url
                }
              }
            }
        """,
        "variables": {
            "input": {
                "title": title,
                "contentMarkdown": content,
                "publicationId": PUBLICATION_ID,
                "tags": []  # Adjust tags as needed
            }
        }
    }
    try:
        response = requests.post(
            HASHNODE_API_URL,
            headers=headers,
            json=payload,
            timeout=10,
        )
        if response.status_code != 200:
            logging.error("Hashnode response error: %s", response.text)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error("Error publishing to Hashnode: %s", e)
        return None

def run_automation():
    logging.info("Generating blog post...")
    blog_content = generate_blog_post()
    if blog_content:
        title = blog_content.split("\n")[0]  # Use the first line as the title
        logging.info("Publishing to Hashnode...")
        result = publish_to_hashnode(title, blog_content)
        if result:
            logging.info("Published Successfully: %s", result)
            # Stop the script after a successful post:
            sys.exit(0)  # Exiting the script on success
        else:
            logging.error("Failed to publish to Hashnode.")
    else:
        logging.error("Failed to generate blog content.")

# Schedule execution every 30 seconds for testing purposes

if __name__ == "__main__":
    schedule.every(30).seconds.do(run_automation)
    logging.info("Automation script is running...")
    while True:
        schedule.run_pending()
        time.sleep(30)

# --- End Revised Code ---
