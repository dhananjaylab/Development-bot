from fastapi import FastAPI, HTTPException, Depends
from .models import DbCredentials, SchemaResponse, LabelRequest
from .services import GraphService
from .database import get_neo4j_driver

app = FastAPI(
    title="DhananjayLab Dev Bot",
    description="Backend for GenAI-Neo4j Schema Discovery",
    version="2.0.0"
)

@app.post("/api/schema", response_model=SchemaResponse)
async def get_schema(credentials: DbCredentials):
    """
    Analyzes the Neo4j database and returns a complete schema map 
    plus an optimized context string for LLMs.
    """
    driver = None
    try:
        driver = get_neo4j_driver(credentials)
        schema = GraphService.fetch_full_schema(driver)
        return schema
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Neo4j Error: {str(e)}")
    finally:
        if driver:
            driver.close()

@app.get("/health")
async def health_check():
    return {"status": "online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)