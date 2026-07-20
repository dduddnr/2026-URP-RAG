import wikipediaapi

wiki = wikipediaapi.Wikipedia(user_agent='2026_KNU_CSE_URP', language='ko')

with open('entity_ids.del', 'r', encoding='utf-8') as f:
    entities = []
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        entity_name = parts[-1]
        entities.append(entity_name)

entities = entities[:1000]
missing = []

for entity in entities:
    page = wiki.page(entity)
    if page.exists():
        with open(f'data/raw/{entity.replace("/", "_")}.txt', 'w', encoding='utf-8') as out:
            out.write(page.text)
    else:
        missing.append(entity)
        print(f'{entity} 문서가 존재하지 않음')

with open('data/missing.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(missing))