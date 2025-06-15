
🎓 Personalized Learning Pathway Recommendation System for Post-Secondary Somali Learners

An intelligent, full-stack web platform that recommends personalized learning pathways to users based on their interests, goals, and skill level. Powered by Django and a SVD-based machine learning model.

---

🚀 Features

- ✅ User Registration & Login
- ✅ Profile Setup (Level, Goals, Interests, Topics)
- ✅ Smart Course Recommendations (Rule-based & ML)
- ✅ Course Catalog with Detail View
- ✅ Track Viewed / Completed Courses
- ✅ Explore More Courses from JSON & CSV Sources
- ✅ Admin Panel for User & Course Management
- ✅ Fully Responsive UI with Bootstrap + Animate.css

---

🧠 How It Works

🔹 Recommendation Engine
By default, the system uses a profile-based smart filter:
- Matches user goals, interests, and level against course tags, titles, and descriptions.

it supports SVD-based collaborative filtering via scikit-surprise:
- Trained model (svd_recommender_model.pkl) can be integrated to predict course ratings per user.

---

🛠️ Tech Stack

Layer         | Stack
--------------|----------------------------
Backend       | Django (Python), MySQL
Frontend      | HTML, Bootstrap, Animate.css
Machine Learning | scikit-surprise (SVD)
Auth          | Django Auth + Custom Profile
Data          | CSV + JSON Course Datasets

---

📁 Project Structure

    ├── db.sqlite3 / MySQL
    ├── manage.py
    ├── recommendation/
    │   ├── models.py
    │   ├── views.py
    │   ├── forms.py
    │   ├── urls.py
    ├── templates/
    │   ├── base.html
    │   ├── home.html
    │   ├── register.html
    │   ├── login.html
    │   ├── dashboard.html
    │   ├── recommendations.html
    │   ├── course_catalog.html
    │   ├── course_detail.html
    │   ├── my_activity.html
    │   ├── admin.html
    ├── static/
    ├── requirements.txt
    ├── svd_recommender_model.pkl
    ├── Courses_and_Learning_Material.csv
    ├── explore_more_1.json
    ├── explore_more_2.json

---

🧪 How to Run

1. Clone the repo  
   git clone https://github.com/your-username/learning-recommender.git
   cd learning-recommender

2. Install dependencies  
   pip install -r requirements.txt

3. Set up MySQL or SQLite  
   - Update settings.py to configure your database

4. Run migrations  
   python manage.py migrate

5. Run the server  
   python manage.py runserver

6. Access the site
   - Open http://localhost:8000

---

🔐 Admin Panel

- URL: /admin
- Superuser setup:
  python manage.py createsuperuser

---

📚 Credits

- ML Model: scikit-surprise (SVD)
- Frontend: Bootstrap 5 + Animate.css
- Backend: Django
- Course Datasets: CSV sources _ Learning path-Index & Courses_and_Learning_Material

---

📦 Deployment

This app can be deployed to:
- PythonAnywhere
- Heroku (with ClearDB)
- VPS (DigitalOcean, AWS EC2)

Supports both WSGI and ASGI.

---

🧠 Future Enhancements

- [ ] Add ratings (1–5 stars)


---

💬 Author

Abdirahman Ibrahim Tigow & Abdirahman Osman Mohamed – passionate about AI, education, and Django 🚀  
Inspired by the goal of improving personalized learning in Somalia and beyond.

---

🌟 Show Your Support

If you like this project:
- ⭐ Star it on GitHub
- 🍴 Fork it and build your own
- 🤝 Share with your team or school
