import logging
from typing import List, Dict, Any
from .database import get_neo4j_driver, determine_type
from .models import SchemaResponse, LabelDetails, RelationshipInfo

logger = logging.getLogger(__name__)

class GraphService:
    @staticmethod
    def fetch_full_schema(driver) -> SchemaResponse:
        schema_query = "CALL db.schema.visualization()"
        
        with driver.session() as session:
            result = session.run(schema_query)
            record = result.single()
            
            if not record:
                return SchemaResponse(labels=[], schema_map={}, llm_context="")

            nodes = record.get("nodes", [])
            rels = record.get("relationships", [])
            
            schema_map = {}
            # 1. Process Nodes/Labels
            for node in nodes:
                for label in node.get("labels", []):
                    props = {p["propertyKey"]: determine_type(p.get("propertyValue")) 
                             for p in node.get("properties", [])}
                    schema_map[label] = LabelDetails(properties=props, relationships=[])

            # 2. Process Relationships
            for rel in rels:
                start_labels = list(rel.get("startNode", {}).get("labels", []))
                end_labels = list(rel.get("endNode", {}).get("labels", []))
                rel_type = rel.get("type")
                
                info = RelationshipInfo(
                    type=rel_type,
                    start_labels=start_labels,
                    end_labels=end_labels,
                    statement=f"(:{':'.join(start_labels)})-[:{rel_type}]->(:{':'.join(end_labels)})"
                )
                
                # Attach relationship info to all starting labels
                for label in start_labels:
                    if label in schema_map:
                        schema_map[label].relationships.append(info)

            # 3. Generate LLM Context String
            context_parts = ["Database Schema Context:"]
            for label, detail in schema_map.items():
                prop_str = ", ".join([f"{k}: {v}" for k, v in detail.properties.items()])
                context_parts.append(f"- Node Label: {label} {{ {prop_str} }}")
                for r in detail.relationships:
                    context_parts.append(f"  Relationship: {r.statement}")

            return SchemaResponse(
                labels=list(schema_map.keys()),
                schema_map=schema_map,
                llm_context="\n".join(context_parts)
            )