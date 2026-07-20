import os
import json
import re
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

def sanitize_rel_type(rel: str) -> str:
    rel = re.sub(r'[^0-9a-zA-Z가-힣_]', '_', rel.strip())
    rel = re.sub(r'_+', '_', rel).strip('_')
    if not rel:
        rel = "RELATION"
    if rel[0].isdigit():
        rel = f"REL_{rel}"
    return rel

def add_relation(tx, subj, rel, obj):
    rel_type = sanitize_rel_type(rel)
    query = (
        "MERGE (a:Entity {name: $subj}) "
        "MERGE (b:Entity {name: $obj}) "
        f"MERGE (a)-[r:`{rel_type}`]->(b) "
        "SET r.original_label = $rel"
    )
    tx.run(query, subj=subj, obj=obj, rel=rel)

kg_files = os.listdir('data/kg')

with driver.session() as session:
    for filename in kg_files:
        with open(f'data/kg/{filename}', 'r', encoding='utf-8') as f:
            data = json.load(f)
        for subj, rel, obj in data['relations']:
            session.execute_write(add_relation, subj, rel, obj)
        print(f'적재 완료: {filename}')

driver.close()