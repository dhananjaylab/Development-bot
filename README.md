# DhananjayLab Development Bot 🤖

A specialized FastAPI backend designed to bridge the gap between GenAI agents and Neo4j Databases. It automatically discovers schemas, labels, property types, and relationship constraints.

## 🚀 Features
- **Schema Autodiscovery**: Extracts node labels and relationship types without manual configuration.
- **Type Mapping**: Automatically detects Neo4j data types (Long, String, DateTime) and maps them to JSON-compatible formats.
- **Bot-Ready Context**: Generates relationship statements like `(A)-[:TYPE]->(B)` which are ideal for LLM context windows.
- **Interactive API**: Fully documented via Swagger UI.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/dhananjaylab-development-bot.git
   cd dhananjaylab-development-bot
   ```

1. Install Dependencies:
```bash
pip install -r requirements.txt
```

2. Set Environment Variables:
## Create a .env file or export them:
```bash
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=your_password
```

🚦 How to Run
1. Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

2. Access the Documentation:
## Open your browser and navigate to:
### Swagger UI: http://127.0.0.1:8000/docs
### ReDoc: http://127.0.0.1:8000/redoc

dhananjaylab-development-bot/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI entry point & routes
│   ├── database.py      # Neo4j connection logic
│   ├── models.py        # Pydantic schemas
│   └── services.py      # Core business logic (schema & node fetching)
├── .env                 # Environment variables (URI, User, Password)
├── requirements.txt     # Dependencies
└── README.md            # Documentation