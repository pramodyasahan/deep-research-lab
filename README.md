
---

# 🧠 Deep Research Lab

**Deep Research Lab** is an AI-powered research assistant that automates deep web research, report generation, and email delivery — all orchestrated using LLM agents. It helps you turn any query into a full-length report backed by automated web search and structured summarization.

## 🚀 Features

- ✍️ **Research Planner Agent**: Breaks down a user query into web search tasks.
- 🔎 **Web Search Agent**: Executes searches and summarizes findings into clean outputs.
- 📄 **Writer Agent**: Compiles findings into a detailed, markdown-formatted report.
- 📧 **Email Agent**: Sends the report via email in a beautifully formatted HTML template.
- 🧩 **Agent Runner**: Modular orchestration with tracing and async execution.
- 🖥️ **Gradio UI**: Clean and interactive interface to enter queries and view results.

---

## 📁 Project Structure


## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/pramodyasahan/deep-research-lab.git
cd deep-research-lab/app



````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory:

```env
SENDGRID_API_KEY=your_sendgrid_key_here
OPENAI_API_KEY=your_openai_key_here
```

> ⚠️ Make sure your sender email is verified in SendGrid.

---

## ✅ Usage

```bash
python main.py
```

This will launch the Gradio interface in your browser.
Enter a research query and click "Run" to generate a full report and email it.

---

## 🧠 Agent Pipeline

```text
User Query
   ↓
Planner Agent ──> generates web search queries
   ↓
Search Agent ───> executes each search and summarizes
   ↓
Writer Agent ───> generates a markdown report
   ↓
Email Agent ────> emails the report to user
```

---

## 📬 Example Use Cases

* Academic literature overviews
* Market or industry research
* Competitive analysis
* Learning a new technical topic
* Email-based briefings on complex topics

---

## 🧪 Sample Queries

* *“State of AI research in 2024”*
* *“Comparison of electric vehicle battery technologies”*
* *“Impact of inflation on supply chain logistics”*

---

## 🤖 Built With

* [OpenAI GPT-4o](https://platform.openai.com/)
* [Gradio](https://www.gradio.app/)
* [SendGrid](https://sendgrid.com/)
* [Pydantic](https://docs.pydantic.dev/)

---

## 📄 License

MIT License. See `LICENSE` for more info.

---

## 💡 Future Improvements

* User-defined recipient emails
* Richer UI with report preview and download
* Local PDF report generation
* Multi-language support

---


