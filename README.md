# Official Intelligence — Automated Cybersecurity Blog System

**Official Intelligence** is a fully automated content publishing system that generates cybersecurity-focused blog articles using OpenAI, formats them appropriately, and posts them directly to [Hashnode](https://officialintelligence.hashnode.dev).

This project demonstrates:
- Automation of cybersecurity content workflows
- Use of AI to assist, not replace, human oversight
- Secure handling of API keys and publishing credentials

---

## 📚 Features

- Automatically generates technical blog posts on cybersecurity topics.
- Posts articles to Hashnode via API integration.
- Includes modular design for potential multi-platform publishing (LinkedIn, personal websites, etc.).
- Designed with local `.env` file usage to protect sensitive API keys and credentials.

---

## ⚙️ Project Structure

| File | Purpose |
|-----|--------|
| `OF.py` | Main Python script to generate and publish blog articles. |
| `.env` (local only) | Stores API keys securely. Should never be committed to GitHub. |
| `.gitignore` | Ensures sensitive files like `.env` are excluded from version control. |

---

## 🛠️ Requirements

- Python 3.8+
- OpenAI API Key
- Hashnode API Key
- `.env` file containing:
  - `OPENAI_API_KEY`
  - `HASHNODE_API_KEY`
  - (optional) Additional configuration parameters for customization.

Install Python dependencies:

```bash
pip install openai python-dotenv requests
```

Create a `.env` file in the project root with your API keys:

```bash
OPENAI_API_KEY=your-openai-key
HASHNODE_API_KEY=your-hashnode-key
# Optional: customize the Hashnode API URL or publication ID
# HASHNODE_API_URL=https://gql.hashnode.com/
# PUBLICATION_ID=your-publication-id
```

Run the automation script:

```bash
python OF.py
```

The script loads your `.env` file, generates a blog post with OpenAI, and
publishes it to Hashnode automatically.
