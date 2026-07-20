import os
import json
import wikipediaapi

# 스크립트 파일 기준 경로 설정 (scripts/ 폴더 안에 있다고 가정)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)  # project 루트

RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
MISSING_PATH = os.path.join(BASE_DIR, 'data', 'missing.txt')
ENTITY_IDS_PATH = os.path.join(BASE_DIR, 'entity_ids.del')

os.makedirs(RAW_DIR, exist_ok=True)

wiki = wikipediaapi.Wikipedia(user_agent='2026_KNU_CSE_URP', language='ko')

with open(ENTITY_IDS_PATH, 'r', encoding='utf-8') as f:
    entities = []
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        entity_name = parts[-1]
        entities.append(entity_name)

entities = entities[:1000]
total = len(entities)
count = 0
missing = []

for entity in entities:
    count += 1
    page = wiki.page(entity)
    if page.exists():
        data = {
            "entity": entity,
            "summary": page.summary,
            "sections": [
                {"section_title": s.title, "text": s.text}
                for s in page.sections if s.text.strip()
            ]
        }
        out_path = os.path.join(RAW_DIR, f'{entity.replace("/", "_")}.json')
        with open(out_path, 'w', encoding='utf-8') as out:
            json.dump(data, out, ensure_ascii=False, indent=2)
        print(f'[{count}/{total}] 성공: {entity}')
    else:
        missing.append(entity)
        print(f'[{count}/{total}] {entity} 문서가 존재하지 않음')

with open(MISSING_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(missing))