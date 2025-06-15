from django.contrib import admin
from django.urls import path
from recommendation import views as recommendation_views

urlpatterns = [
    # 🛠 Django Built-in Admin Panel
    path('admin/', admin.site.urls),

    # 🔒 Custom Super Admin Panel
    path('admin-panel/', recommendation_views.admin_panel, name='admin_panel'),
    path('admin-panel/toggle-user/<int:user_id>/', recommendation_views.toggle_user_status, name='toggle_user_status'),
    path('admin-panel/delete-user/<int:user_id>/', recommendation_views.delete_user, name='delete_user'),
    path('admin-panel/update-course-link/', recommendation_views.update_course_link, name='update_course_link'),

    

    # 🌐 Public Pages
    path('', recommendation_views.home, name='home'),
    path('register/', recommendation_views.register, name='register'),
    path('login/', recommendation_views.login_view, name='login'),
    path('logout/', recommendation_views.logout_view, name='logout'),

    # 👤 Profile Setup & Dashboard
    path('setup-profile/', recommendation_views.setup_profile, name='setup_profile'),
    path('dashboard/', recommendation_views.dashboard, name='dashboard'),

    # 🤖 AI Recommendations
    path('ai-recommendations/', recommendation_views.ai_recommendations, name='ai_recommendations'),

    # 📚 Course Catalog & Detail
    path('catalog/', recommendation_views.course_catalog, name='course_catalog'),
    path('courses/<int:course_id>/', recommendation_views.course_detail, name='course_detail'),

    # 🧠 User Course Interaction
    path('courses/<int:course_id>/viewed/', recommendation_views.mark_viewed, name='mark_viewed'),
    path('courses/<int:course_id>/completed/', recommendation_views.mark_completed, name='mark_completed'),
    path('courses/<int:course_id>/unmark-viewed/', recommendation_views.unmark_viewed, name='unmark_viewed'),
    path('courses/<int:course_id>/unmark-completed/', recommendation_views.unmark_completed, name='unmark_completed'),

    # 📖 My Learning Activity
    path('my-activity/', recommendation_views.my_activity, name='my_activity'),

    # 🌍 Explore Sections
    path('explore-more-1/', recommendation_views.explore_more_1, name='explore_more_1'),
    path('explore-more-2/', recommendation_views.explore_more_2, name='explore_more_2'),
]

