🧠 AI Agentic Deep Research System
An advanced AI-driven research framework that automates deep web exploration, multilingual translation, and intelligent summarization. Leveraging Tavily for web crawling, LangGraph for structured data management, and LangChain for orchestrating agent workflows, this system streamlines the process of gathering and synthesizing information from diverse online sources.​

📌 Table of Contents
Features

Architecture

Installation

Usage

Environment Variables

Contributing

License

🚀 Features
Automated Web Crawling: Utilizes Tavily to fetch and parse content from specified URLs.

Multilingual Translation: Translates non-English content to English using the Deep Translator API.

Structured Data Ingestion: Ingests and organizes data into LangGraph for efficient retrieval.

Intelligent Summarization: Employs LangChain to generate concise summaries and answers from the ingested data.

Modular Agent Design: Features distinct agents for research, translation, ingestion, retrieval, and drafting, promoting scalability and maintainability.​

🧭 Architecture
mermaid
Copy
Edit
graph TD
    A[User Input: Seed URLs] --> B[Research Agent]
    B --> C[Translation Agent]
    C --> D[Graph Ingestor]
    D --> E[LangGraph Storage]
    E --> F[Graph Retriever]
    F --> G[Drafting Agent]
    G --> H[Final Output]
Components:

Research Agent: Initiates web crawling using Tavily based on user-provided URLs.

Translation Agent: Translates retrieved content to English.

Graph Ingestor: Processes and stores translated data into LangGraph.

Graph Retriever: Fetches relevant information from LangGraph based on queries.

Drafting Agent: Generates summaries or answers using LangChain's language models.​

⚙️ Installation
Clone the Repository:

bash
Copy
Edit
git clone https://github.com/yourusername/ai-agentic-deep-research.git
cd ai-agentic-deep-research
Create a Virtual Environment:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Set Up Environment Variables:

Create a .env file in the project root with the following content:

env
Copy
Edit
TAVILY_API_KEY=your_tavily_api_key
LANGGRAPH_API_KEY=your_langgraph_api_key
OPENAI_API_KEY=your_openai_api_key
🧪 Usage
Run the Main Script:

bash
Copy
Edit
python main.py
Provide Seed URLs:

When prompted, input the URLs you wish the system to research. For example:

bash
Copy
Edit
Enter seed URLs (comma-separated): https://en.wikipedia.org/wiki/Artificial_intelligence
View Results:

The system will output a summarized answer along with the sources used.

🛠️ Environment Variables

Variable	Description
TAVILY_API_KEY	API key for Tavily web crawling.
LANGGRAPH_API_KEY	API key for LangGraph storage.
OPENAI_API_KEY	API key for OpenAI models.
🤝 Contributing
Contributions are welcome! Please follow these steps:​
DEV Community

Fork the Repository

Create a New Branch:

bash
Copy
Edit
git checkout -b feature/your-feature-name
Commit Your Changes:

bash
Copy
Edit
git commit -m "Add your message here"
Push to Your Fork:

bash
Copy
Edit
git push origin feature/your-feature-name
Create a Pull Request

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.​

