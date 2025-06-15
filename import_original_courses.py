import pandas as pd
from recommendation.models import Course

def import_original_courses(csv_path):
    """
    Deletes all non-EXP courses and imports original catalog courses from a CSV.
    Prefixes module_code with 'ORG_1', 'ORG_2', ...
    """
    deleted_count, _ = Course.objects.exclude(module_code__startswith='EXP').delete()
    print(f"🧹 Deleted {deleted_count} old non-EXP courses")

    df = pd.read_csv(csv_path)
    created = 0

    for index, row in df.iterrows():
        try:
            Course.objects.create(
                title=row.get('Course_Learning_Material', f"Course {index+1}"),
                description=row.get('Description', 'No description'),
                level=row.get('Course_Level', 'N/A'),
                tags=row.get('Tags', 'N/A'),
                duration=row.get('Duration', 'N/A'),
                difficulty=row.get('Difficulty', 'N/A'),
                source=row.get('Source', ''),
                module_code=f"ORG_{index+1}",  # ⬅️ Force clean module_code
                prerequisites=row.get('Prerequisites', ''),
                prework=row.get('Prework', ''),
                link=row.get('Course_Learning_Material_Link', ''),
                course_type=row.get('Type_Free_Paid', 'Free'),
            )
            created += 1
        except Exception as e:
            print(f"❌ Error importing row {index+1}: {e}")


    print(f"✅ Successfully imported {created} original courses")

    # import_explore_more_2.py

import json
from recommendation.models import Course
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import Explore More 2 Courses from JSON'

    def handle(self, *args, **kwargs):
        try:
            with open('explore_more_2.json', 'r', encoding='utf-8') as file:
                data = json.load(file)

            created = 0
            for i, item in enumerate(data):
                Course.objects.create(
                    title=item.get('title', f"Course {i+1}"),
                    description=item.get('description', ''),
                    level=item.get('level', 'Beginner'),
                    duration=item.get('duration', ''),
                    module_code=f"EXP2_{i+1}",
                    link=item.get('link', ''),
                    course_type=item.get('course_type', 'Free'),
                    source=item.get('source', 'Online Platform'),
                )
                created += 1

            self.stdout.write(self.style.SUCCESS(f"✅ Successfully imported {created} EXP2 courses."))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Error: {str(e)}"))

