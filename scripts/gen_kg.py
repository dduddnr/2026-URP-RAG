import os
import json
from dotenv import load_dotenv
from kg_gen import KGGen

load_dotenv()

# 스크립트 파일 기준 경로 설정 (scripts/ 폴더 안에 있다고 가정)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)  # project 루트

RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
KG_DIR = os.path.join(BASE_DIR, 'data', 'kg')

os.makedirs(KG_DIR, exist_ok=True)

kg = KGGen(
    model="openai/gpt-4o",
    temperature=0.0,
    api_key=os.getenv("OPENAI_API_KEY")
)

raw_files = [f for f in os.listdir(RAW_DIR) if f.endswith('.json')]
total = len(raw_files)
count = 0

for filename in raw_files:
    count += 1
    entity_name = filename.replace('.json', '')
    output_path = os.path.join(KG_DIR, f'{entity_name}.json')

    if os.path.exists(output_path):
        print(f'[{count}/{total}] 이미 존재함, 건너뜀: {entity_name}')
        continue

    with open(os.path.join(RAW_DIR, filename), 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    # summary + sections 텍스트를 하나로 합쳐서 KG 생성용 입력으로 사용
    text_parts = [raw_data.get('summary', '')]
    for section in raw_data.get('sections', []):
        title = section.get('section_title', '')
        content = section.get('text', '')
        text_parts.append(f'## {title}\n{content}')
    text = '\n\n'.join(text_parts)

    try:
        graph = kg.generate(input_data=text, context=entity_name)
        result = {
            "entities": list(graph.entities),
            "edges": list(graph.edges),
            "relations": [list(r) for r in graph.relations]
        }
        with open(output_path, 'w', encoding='utf-8') as out:
            json.dump(result, out, ensure_ascii=False, indent=2)
        print(f'[{count}/{total}] KG 생성 완료: {entity_name}')
    except Exception as e:
        print(f'[{count}/{total}] 실패: {entity_name} - {e}')