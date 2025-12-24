from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class DbCredentials(BaseModel):
    uri: str = Field(default="bolt://localhost:7687")
    user: str = Field(default="neo4j")
    password: str = Field(default="password")

class RelationshipInfo(BaseModel):
    type: str
    start_labels: List[str]
    end_labels: List[str]
    statement: Optional[str] = None

class LabelDetails(BaseModel):
    properties: Dict[str, str]
    relationships: List[RelationshipInfo]

class SchemaResponse(BaseModel):
    labels: List[str]
    schema_map: Dict[str, LabelDetails]
    llm_context: str  # A string formatted specifically for GenAI prompts

class LabelRequest(BaseModel):
    labels: List[str]
    credentials: DbCredentials