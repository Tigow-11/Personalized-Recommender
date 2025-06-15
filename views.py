from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import UserRegisterForm, ProfileForm
from .models import Profile, Course, UserCourseInteraction
from recommendation.utils.recommender import get_top_recommendations
import os, json
import pandas as pd
from django.conf import settings

User = get_user_model()

# -----------------------
# 🔹 Public Pages
# -----------------------
def home(request):
    return render(request, 'recommendation/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('setup_profile')
    else:
        form = UserRegisterForm()
    return render(request, 'recommendation/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')
    messages.error(request, 'Invalid username or password')
    return render(request, 'recommendation/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# -----------------------
# 🔹 Profile Setup
# -----------------------
@login_required
def setup_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    interests_tags = [
        "ai", "data", "cloud", "api", "analytics", "debugging", "classification",
        "clustering", "ethics", "engineering", "security", "web", "python"
    ]
    topics_tags = [
        "ai", "machine learning", "python", "data science", "cloud", "frontend", 
        "backend", "sql", "excel", "statistics"
    ]

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.interests = ', '.join(set(tag.strip() for tag in request.POST.getlist('interests') + request.POST.get('interests', '').split(',') if tag.strip()))
            profile.learning_topics = ', '.join(set(tag.strip() for tag in request.POST.getlist('learning_topics') + request.POST.get('learning_topics', '').split(',') if tag.strip()))
            profile.save()
            messages.success(request, "✅ Your profile has been updated successfully!")
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)

    selected_interests = [tag.strip() for tag in profile.interests.split(',')] if profile.interests else []
    selected_topics = [tag.strip() for tag in profile.learning_topics.split(',')] if profile.learning_topics else []

    return render(request, 'recommendation/setup_profile.html', {
        'form': form,
        'profile': profile,
        'interests': interests_tags,
        'topics': topics_tags,
        'selected_interests': selected_interests,
        'selected_topics': selected_topics,
    })

# -----------------------
# 🔹 Dashboard
# -----------------------
@login_required
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)  # ✔ Always ensures a profile exists
@login_required
def dashboard(request):
    profile = request.user.profile
    interactions = UserCourseInteraction.objects.filter(user=request.user).select_related('course')
    show_hint = not interactions.exists()
    return render(request, 'recommendation/dashboard.html', {
        'profile': profile,
        'interactions': interactions,
        'show_hint': show_hint,
    })

# -----------------------
# 🔹 AI Recommendations
# -----------------------
@login_required
def ai_recommendations(request):
    profile = request.user.profile
    user_level = (profile.level or '').strip().lower()
    keywords = f"{profile.interests} {profile.goals} {profile.learning_topics}".lower().split()

    catalog_path = os.path.join(settings.BASE_DIR, 'Courses_and_Learning_Material.csv')
    exp1_path = os.path.join(settings.BASE_DIR, 'explore_more_1.json')
    exp2_path = os.path.join(settings.BASE_DIR, 'explore_more_2.json')

    recommended, seen_titles = [], set()

    def match_course(title, tags, level):
        if not user_level or user_level != level:
            return False
        return any(keyword in f"{title.lower()} {tags}" for keyword in keywords)

    try:
        courses_df = pd.read_csv(catalog_path).fillna('')
        for _, row in courses_df.iterrows():
            title, tags, level, link = row.get('Course_Learning_Material', '').strip(), row.get('Keywords_Tags_Skills_Interests', '').lower(), row.get('Level', '').strip().lower(), row.get('Links', '').strip()
            if title and link and title not in seen_titles and match_course(title, tags, level):
                recommended.append({
                    'title': title, 'tags': tags, 'link': link,
                    'source': row.get('Source', 'Catalog'),
                    'level': row.get('Level', ''),
                    'type': row.get('Course_Type', ''),
                })
                seen_titles.add(title)
    except Exception as e:
        messages.error(request, f"Error reading course catalog: {e}")
        return redirect('dashboard')

    try:
        for item in json.load(open(exp1_path, 'r', encoding='utf-8')) + json.load(open(exp2_path, 'r', encoding='utf-8')):
            title, tags, level, link = item.get('title', '').strip(), item.get('tags', '').lower(), item.get('level', '').strip().lower(), item.get('link', '').strip()
            if title and link and title not in seen_titles and match_course(title, tags, level):
                recommended.append({
                    'title': title, 'tags': tags, 'link': link,
                    'source': item.get('source', 'Explore'),
                    'level': item.get('level', ''),
                    'type': item.get('type', ''),
                })
                seen_titles.add(title)
    except Exception as e:
        messages.error(request, f"Error reading explore data: {e}")
        return redirect('dashboard')

    return render(request, 'recommendation/recommendations.html', {'recommended_courses': recommended})

# -----------------------
# 🔹 Course Catalog + Details
# -----------------------
@login_required
def course_catalog(request):
    courses = Course.objects.filter(module_code__startswith='ORG').order_by('title')
    return render(request, 'recommendation/course_catalog.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    interaction = UserCourseInteraction.objects.filter(user=request.user, course=course).first()
    return render(request, 'recommendation/course_detail.html', {'course': course, 'interaction': interaction})

# -----------------------
# 🔹 Course Interactions
# -----------------------
@login_required
def mark_viewed(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    UserCourseInteraction.objects.update_or_create(user=request.user, course=course, defaults={'viewed': True})
    messages.success(request, f"👁 You marked '{course.title}' as viewed.")
    return redirect('course_detail', course_id=course.id)

@login_required
def mark_completed(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    UserCourseInteraction.objects.update_or_create(user=request.user, course=course, defaults={'completed': True})
    messages.success(request, f"✅ You marked '{course.title}' as completed.")
    return redirect('course_detail', course_id=course.id)

@login_required
def my_activity(request):
    interactions = UserCourseInteraction.objects.filter(user=request.user).select_related('course').order_by('-timestamp')
    return render(request, 'recommendation/my_activity.html', {'interactions': interactions})

@require_POST
@login_required
def unmark_viewed(request, course_id):
    interaction = get_object_or_404(UserCourseInteraction, user=request.user, course_id=course_id)
    interaction.viewed = False
    interaction.save()
    messages.success(request, f"❌ You unmarked '{interaction.course.title}' as viewed.")
    return redirect('my_activity')

@require_POST
@login_required
def unmark_completed(request, course_id):
    interaction = get_object_or_404(UserCourseInteraction, user=request.user, course_id=course_id)
    interaction.completed = False
    interaction.save()
    messages.success(request, f"❌ You unmarked '{interaction.course.title}' as completed.")
    return redirect('my_activity')

# -----------------------
# 🔹 Explore More Pages
# -----------------------
@login_required
def explore_more_1(request):
    courses = Course.objects.filter(module_code__startswith='EXP1')
    return render(request, 'recommendation/explore_more_1.html', {'courses': courses})

@login_required
def explore_more_2(request):
    courses = Course.objects.filter(module_code__startswith='EXP2')
    return render(request, 'recommendation/explore_more_2.html', {'courses': courses})

# -----------------------
# 🔹 Admin Views
# -----------------------
def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def admin_panel(request):
    users = User.objects.all().order_by('-date_joined')
    try:
        courses_csv = pd.read_csv(os.path.join(settings.BASE_DIR, 'Courses_and_Learning_Material.csv')).fillna('').to_dict('records')
    except:
        courses_csv = []

    try:
        courses_exp1 = json.load(open(os.path.join(settings.BASE_DIR, 'explore_more_1.json'), 'r', encoding='utf-8'))
    except:
        courses_exp1 = []

    try:
        courses_exp2 = json.load(open(os.path.join(settings.BASE_DIR, 'explore_more_2.json'), 'r', encoding='utf-8'))
    except:
        courses_exp2 = []

    return render(request, 'recommendation/admin.html', {
        'users': users,
        'courses_csv': courses_csv,
        'courses_exp1': courses_exp1,
        'courses_exp2': courses_exp2,
    })

@require_POST
@user_passes_test(is_admin)
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    status = "unblocked" if user.is_active else "blocked"
    messages.success(request, f"✅ User '{user.username}' has been {status}.")
    return redirect('admin_panel')

@require_POST
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    username = user.username
    user.delete()
    messages.success(request, f"🗑️ User '{username}' has been deleted.")
    return redirect('admin_panel')

@require_POST
@user_passes_test(is_admin)
def update_course_link(request):
    source = request.POST.get('source')
    index = int(request.POST.get('index'))
    new_link = request.POST.get('new_link')

    file_path = os.path.join(settings.BASE_DIR, source)
    with open(file_path, 'r', encoding='utf-8') as f:
        courses = json.load(f)

    if 0 <= index < len(courses):
        courses[index]['link'] = new_link
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(courses, f, indent=2)
        messages.success(request, f"✅ Course link updated successfully in {source}.")
    else:
        messages.error(request, "❌ Invalid course index.")

    return redirect('admin_panel')

