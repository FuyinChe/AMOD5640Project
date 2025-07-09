# AMOD5640Project
The project for AMOD 5640 Course

## Step 1: 
Building a backend API server for the front end web development based on Django

---

## API Documentation

### Swagger/OpenAPI (Interactive)
- **Swagger UI:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **ReDoc:** [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
- **OpenAPI JSON:** [http://localhost:8000/swagger.json](http://localhost:8000/swagger.json)
- **OpenAPI YAML:** [http://localhost:8000/swagger.yaml](http://localhost:8000/swagger.yaml)

> **Note:** Swagger UI and ReDoc are public. Actual API endpoints are protected by authentication and permissions.

---

## Security & CORS
- **CORS is restricted** to `trentfarmdata.org` and subdomains (see `CORS_ALLOWED_ORIGINS` and `CORS_ALLOWED_ORIGIN_REGEXES` in `settings.py`)
- **ALLOWED_HOSTS** is set to only allow trusted domains in production
- **Sensitive endpoints** (admin, user info, etc.) require authentication and/or admin group membership

---

## Running the Project

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```
3. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```
4. **Run the server:**
   ```bash
   python manage.py runserver
   ```

---

## Project Structure
- `dashboard_api/` - Main Django app
- `core/` - Core API logic, views, permissions, documentation
- `tests/` - Test scripts for API endpoints

---

## Contact
For questions, contact the project maintainer at [admin@trentfarmdata.org](mailto:admin@trentfarmdata.org)
