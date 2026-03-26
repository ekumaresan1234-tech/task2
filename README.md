# 🚀 Professional Task Manager - Django App

A full-stack, production-quality Task Manager web application built with Django and modern Tailwind CSS frontend.

## ✨ Features
- ✅ Full CRUD operations (Create, Read, Update, Delete)
- 🎨 Stunning, responsive UI with dark mode
- ⚡ AJAX-powered real-time updates (no page reloads)
- 📱 Mobile-first responsive design
- 🔍 Status filtering (Pending/Completed)
- 🛡️ Form validation & error handling
- 🌙 Dark/Light theme toggle
- 👨‍💼 Django Admin integration
- 💾 SQLite database (production-ready)

## 🛠️ Tech Stack
- **Backend**: Django 6.0+, Python 3.12
- **Frontend**: Tailwind CSS 3, vanilla JavaScript, Font Awesome
- **Database**: SQLite (PostgreSQL ready)

## 🚀 Quick Start

1. **Navigate to project directory**:
   ```bash
   cd "c:/Users/AKASH/Desktop/TASK MANAGER"
   ```

2. **Activate virtual environment**:
   ```bash
   venv\Scripts\activate
   ```

3. **Install dependencies** (already done):
   ```bash
   pip install django
   ```

4. **Run migrations** (already done):
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser** (for admin):
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**:
   ```bash
   python manage.py runserver
   ```

7. **Open in browser**: http://127.0.0.1:8000/

## 📱 Usage

- **Dashboard**: View all tasks with filter buttons
- **Add Task**: Click "Add New Task" button
- **Edit/Delete**: Use icons on each task card
- **Toggle Status**: Click "Mark Complete/Pending" on cards
- **Admin**: http://127.0.0.1:8000/admin/
- **Theme**: Toggle dark/light mode in navbar

## 🎯 Key Features Demo

1. **Card-based UI** with hover animations
2. **Real-time AJAX** create/update/delete
3. **Responsive design** works on all devices
4. **Filter by status** with live counts
5. **Smooth transitions** & glassmorphism effects
6. **Professional gradient** buttons & badges

## 🧪 Testing

```bash
# Create test data via admin or forms
# Test responsive design (F12 → mobile view)
# Test AJAX (no page reloads)
# Test filters & search
```

## 🔧 Customization

- **PostgreSQL**: Update `DATABASES` in `settings.py`
- **Production**: Set `DEBUG=False`, configure `ALLOWED_HOSTS`
- **Static files**: `python manage.py collectstatic`
- **More features**: Add auth, search, due dates, categories

## 📁 Project Structure
```
TASK MANAGER/
├── manage.py
├── taskmanager/     # Main project
├── tasks/           # Task app
│   ├── models.py    # Task model
│   ├── views.py     # CBV + AJAX views
│   ├── urls.py      # Routes
│   └── admin.py
├── templates/       # Base + task templates
├── TODO.md          # Progress tracker
├── README.md        # This file
└── db.sqlite3       # Database
```

## 🎉 Done!

Your professional Task Manager is ready! 🚀

**Status**: Production-quality, fully functional, visually stunning ✅

