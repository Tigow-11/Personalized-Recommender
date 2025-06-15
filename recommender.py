import pandas as pd
import json
import os

def get_top_recommendations(user_text, user_level, n=6):
    """
    Return top N course recommendations filtered by user level and keywords from three datasets:
    - Courses_and_Learning_Material.csv
    - explore_more_1.json
    - explore_more_2.json
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    catalog_path = os.path.join(base_dir, '../../Courses_and_Learning_Material.csv')
    exp1_path = os.path.join(base_dir, '../../explore_more_1.json')
    exp2_path = os.path.join(base_dir, '../../explore_more_2.json')

    keywords = [kw.strip().lower() for kw in user_text.split()]
    user_level = (user_level or '').strip().lower()

    recommendations = []

    # 🔹 Load CSV
    try:
        df = pd.read_csv(catalog_path).fillna('')
        for _, row in df.iterrows():
            title = str(row.get('Course_Learning_Material', '')).strip()
            tags = str(row.get('Keywords_Tags_Skills_Interests', '')).lower()
            link = str(row.get('Links', '')).strip()
            level = str(row.get('Level', '')).strip().lower()

            if not title or not link:
                continue
            if user_level and level != user_level:
                continue

            text_blob = f"{title.lower()} {tags}"
            if any(kw in text_blob for kw in keywords):
                recommendations.append({
                    'title': title,
                    'tags': tags,
                    'link': link,
                    'source': row.get('Source', 'Catalog'),
                    'level': row.get('Level', ''),
                    'type': row.get('Type', ''),
                })
    except Exception as e:
        print(f"Error reading catalog CSV: {e}")

    # 🔹 Load JSONs
    for json_path in [exp1_path, exp2_path]:
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for item in data:
                title = str(item.get('title', '')).strip()
                tags = str(item.get('tags', '')).lower()
                link = item.get('link', '').strip()
                level = str(item.get('level', '')).strip().lower()

                if not title or not link:
                    continue
                if user_level and level != user_level:
                    continue

                text_blob = f"{title.lower()} {tags}"
                if any(kw in text_blob for kw in keywords):
                    recommendations.append({
                        'title': title,
                        'tags': tags,
                        'link': link,
                        'source': item.get('source', 'Other'),
                        'level': item.get('level', ''),
                        'type': item.get('type', ''),
                    })
        except Exception as e:
            print(f"Error reading {json_path}: {e}")

    # 🔹 Return top N matches
    return recommendations[:n]