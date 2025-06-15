import json
from recommendation.models import Course
import json
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learning_recommender.settings')
django.setup()

from recommendation.models import Course

# Load JSON file
with open('explore_more_2.json', 'r') as f:
    courses = json.load(f)

added = 0
skipped = 0

for course in courses:
    try:
        obj, created = Course.objects.get_or_create(
            module_code=course['module_code'],
            defaults={
                'title': course['title'],
                'description': course['description'],
                'level': course['level'],
                'tags': course['tags'],
                'duration': course['duration'],
                'difficulty': course['difficulty'],
                'source': course['source'],
                'prerequisites': course['prerequisites'],
                'prework': course['prework'],
                'link': course['link'],
                'course_type': course['course_type'],
            }
        )
        if created:
            added += 1
        else:
            skipped += 1
    except Exception as e:
        print(f"❌ Error on {course['title']}: {e}")

print(f"✅ Done. Added: {added}, Skipped (already exists): {skipped}")

def import_from_json(file_path, module_prefix):
    """
    Deletes old courses with a specific module_code prefix
    and imports new courses from a JSON file.

    Args:
        file_path (str): Path to the JSON file.
        module_prefix (str): Prefix to identify and tag course module_code.
    """

    # 🔥 Step 1: Delete existing courses with the prefix
    deleted_count, _ = Course.objects.filter(module_code__startswith=module_prefix).delete()
    print(f"🗑️ Deleted {deleted_count} old courses with prefix '{module_prefix}'")

    # 📥 Step 2: Load and import new courses
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    created = 0
    for index, item in enumerate(data, start=1):
        try:
            Course.objects.create(
                title=item['title'],
                description=item.get('description', ''),
                level=item.get('level', ''),
                tags=item.get('tags', ''),
                duration=item.get('duration', ''),
                difficulty=item.get('difficulty', ''),
                source=item.get('source', ''),
                module_code=item.get('module_code', f"{module_prefix}_{index}"),
                prerequisites=item.get('prerequisites', ''),
                prework=item.get('prework', ''),
                link=item.get('link', ''),
                course_type=item.get('course_type', 'Free'),
            )
            created += 1
        except Exception as e:
            print(f"❌ Error importing course {item.get('title', 'Unknown')}: {e}")

    print(f"✅ Successfully imported {created} courses from '{file_path}' with prefix '{module_prefix}'")
    
# import_original_courses.py

import pandas as pd
from recommendation.models import Course

def import_original_courses(csv_path):
    """
    Deletes all non-EXP courses and imports original catalog courses from a CSV.
    Prefixes module_code with 'ORG_1', 'ORG_2', ...
    """
    # Delete all courses that are not part of EXP1/EXP2
    deleted_count, _ = Course.objects.exclude(module_code__startswith='EXP').delete()
    print(f"🗑️ Deleted {deleted_count} old non-EXP courses")

    df = pd.read_csv(csv_path)
    created = 0

    for index, row in df.iterrows():
        try:
            Course.objects.create(
                title=row.get('title', ''),
                description=row.get('description', ''),
                level=row.get('level', ''),
                tags=row.get('tags', ''),
                duration=row.get('duration', ''),
                difficulty=row.get('difficulty', ''),
                source=row.get('source', ''),
                module_code=row.get('module_code', f"ORG_{index+1}"),
                prerequisites=row.get('prerequisites', ''),
                prework=row.get('prework', ''),
                link=row.get('link', ''),
                course_type=row.get('course_type', 'Free'),
            )
            created += 1
        except Exception as e:
            print(f"❌ Error importing row {index+1}: {e}")

    print(f"✅ Successfully imported {created} original courses")
