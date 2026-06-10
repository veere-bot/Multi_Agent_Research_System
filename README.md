<img width="1668" height="877" alt="Screenshot 2026-06-10 152130" src="https://github.com/user-attachments/assets/cd010674-0f0c-4e76-9844-bbb57654e58c" />
# 🧠 AI Research Pipeline

An automated multi-agent research pipeline that gathers, analyzes, and refines information on a given topic using specialized AI agents.

## 🚀 Overview

This project implements a step-by-step research workflow powered by multiple AI agents:

1. **Search Agent** – Finds recent and relevant information
2. **Reader Agent** – Selects the best source and extracts detailed content
3. **Writer Chain** – Generates a structured research report
4. **Critic Chain** – Reviews and provides feedback on the report

The pipeline ensures that research is not only gathered but also refined and validated.

---

## 🏗️ Project Structure

```
.
├── tools.py                # Entry point of the pipeline
├── agents.py              # Contains agent builders (search, reader, etc.)
├── pipeline.py              # Writer and critic chains
└── README.md
```

---

## ⚙️ How It Works

The pipeline follows this sequence:

### 1. Search Phase

* Uses the search agent to gather recent and reliable information.
* Stores results in the pipeline state.

### 2. Reading Phase

* Reader agent selects the most relevant URL.
* Scrapes and extracts detailed content.

### 3. Writing Phase

* Combines search + scraped content.
* Generates a structured report.

### 4. Critique Phase

* Reviews the generated report.
* Provides feedback for improvements.

---

## 🧩 Core Function

```python
run_research_pipeline(topic: str) -> dict
```

### Input:

* `topic` (str): Research topic

### Output:

* Dictionary containing:

  * `search_results`
  * `scraped_content`
  * `report`
  * `feedback`

---

## ▶️ Usage

Run the script:

```bash
streamlit run app.py
```

Enter your topic when prompted:

```bash
Enter a research topic: Artificial Intelligence in Healthcare
```

---

## 📌 Example Workflow

```
Step 1 - Search Agent → Collects data  
Step 2 - Reader Agent → Extracts detailed info  
Step 3 - Writer → Generates report  
Step 4 - Critic → Reviews report  
```

---

## 🛠️ Requirements

* Python 3.8+
* Required dependencies (example):

  ```bash
  pip install openai langchain
  ```

---

## ✨ Features

* Modular agent-based design
* Automated research workflow
* Structured report generation
* Built-in critique and feedback system
* Easy to extend with new agents

---

## 🔮 Future Improvements

* Add memory for iterative refinement
* Support multiple sources instead of one
* Export reports to PDF/Markdown
* Add UI (Streamlit or web app)

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

Developed as an experimental AI-powered research assistant.
