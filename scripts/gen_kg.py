import os
import json
from dotenv import load_dotenv
from kg_gen import KGGen

load_dotenv()

kg = KGGen(
    model="openai/gpt-4o",
    temperature=0.0,
    api_key=os.getenv("OPENAI_API_KEY")
)

raw_files = os.listdir('data/raw')

for filename in raw_files:
    entity_name = filename.replace('.txt', '')
    output_path = f'data/kg/{entity_name}.json'
    if os.path.exists(output_path):
        continue
    with open(f'data/raw/{filename}', 'r', encoding='utf-8') as f:
        text = f.read()
    try:
        graph = kg.generate(input_data=text, context=entity_name)
        result = {
            "entities": list(graph.entities),
            "edges": list(graph.edges),
            "relations": [list(r) for r in graph.relations]
        }
        with open(output_path, 'w', encoding='utf-8') as out:
            json.dump(result, out, ensure_ascii=False, indent=2)
        print(f'KG 생성 완료: {entity_name}')
    except Exception as e:
        print(f'실패: {entity_name} - {e}')