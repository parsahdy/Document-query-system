# Document QA Project – Phase 1

This project is a **document and query management system**. Phase 1 focuses on database models and Django admin.

**Key features:**

* Manage **Documents** (`title`, `content`, `tags`)
* Manage **Tags** for categorization
* Manage **Queries** with `answer` and `confidence_score`
* Django admin interface for CRUD operations

**Setup:**

1. Install dependencies: `pip install -r requirements.txt`
2. Configure `.env` for PostgreSQL
3. Run with Docker: `docker-compose up --build -d`
4. Apply migrations: `docker-compose exec web python manage.py migrate`
5. Create superuser: `docker-compose exec web python manage.py createsuperuser`

Admin panel: `http://localhost:8000/admin`