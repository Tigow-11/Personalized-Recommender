from django.db import models
from django.contrib.auth.models import User

# 🔹 Course model
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=50)
    tags = models.CharField(max_length=200, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    difficulty = models.CharField(max_length=50, blank=True)
    source = models.CharField(max_length=100, blank=True)

    # Extra fields from CSV
    module_code = models.CharField(max_length=100, blank=True)  # No longer unique
    prerequisites = models.TextField(blank=True)
    prework = models.TextField(blank=True)
    link = models.URLField(blank=True, null=True)
    course_type = models.CharField(max_length=50, blank=True)  # Free or Paid

    def __str__(self):
        return self.title


# 🔹 Profile model
class Profile(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    interests = models.TextField()
    goals = models.TextField()
    learning_topics = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s Profile"


# 🔹 User-Course interaction model
class UserCourseInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    liked = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    