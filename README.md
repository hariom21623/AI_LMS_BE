# AI-LMS Backend

## AI Powered Multi-Branch Learning Management System

**Client:** Shankar Yadav\
**Prepared by:** Bharatcoder.com / Er. Hariom Verma

------------------------------------------------------------------------

# 1. Project Overview

AI-LMS is a secure, scalable, multi-branch Learning Management System
for institutes managing branches, teachers, students, courses, lectures,
notes, live classes, recordings, quizzes, exams, notifications, reports,
and future AI features.

## Final Backend Stack

-   Python 3.13
-   FastAPI
-   SQLAlchemy 2.x
-   Alembic
-   PostgreSQL
-   Pydantic 2.x
-   pydantic-settings
-   Psycopg 3
-   JWT Authentication
-   Google Drive API for recording archive
-   Docker + Nginx + Ubuntu VPS for production

## Frontend Stack

Planned frontend:

-   Next.js
-   TypeScript
-   Tailwind CSS

**Current focus: backend only.**

------------------------------------------------------------------------

# 2. Current Status

  Component                       Status
  ------------------------------- ------------
  Project structure               ✅ Ready
  Python virtual environment      ✅ Ready
  Environment configuration       ✅ Ready
  Local / Dev / Prod separation   ✅ Ready
  FastAPI                         ✅ Ready
  PostgreSQL connection           ✅ Tested
  SQLAlchemy Base                 ✅ Ready
  Timezone utility                ✅ Ready
  Institute model                 ✅ Ready
  Alembic                         ✅ Ready
  First migration                 ✅ Applied
  `institutes` table              ✅ Created
  `alembic current`               ✅ Head
  `alembic check`                 ✅ Clean
  Logging                         ⏳ Next
  Global exception handler        ⏳ Pending
  CORS                            ⏳ Pending
  API routers                     ⏳ Pending
  Docker                          ⏳ Pending
  JWT Auth                        ⏳ Pending
  RBAC                            ⏳ Pending

Current migration:

``` text
257e6c6b4a86 (head)
```

Current schema check:

``` text
No new upgrade operations detected.
```

------------------------------------------------------------------------

# 3. Backend Folder Structure

``` text
aiLMS_Backend/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │
│   ├── core/
│   │
│   ├── db/
│   │
│   ├── middleware/
│   │
│   ├── models/
│   │
│   ├── repositories/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   │   └── 257e6c6b4a86_create_institutes_table.py
│   │
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│
├── scripts/
│   ├── db.py
│   ├── local_run.py
│   ├── dev_run.py
│   └── prod_run.py
│
├── .env.example
├── .env.local
├── .env.dev
├── .env.prod
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------

# 4. Folder Responsibilities

## `app/main.py`

FastAPI application entry point.

It will eventually:

-   create the FastAPI application
-   register middleware
-   register exception handlers
-   register `/api/v1` routers
-   configure startup/shutdown

## `app/api/v1/`

Versioned API routes.

Planned modules:

``` text
auth.py
institutes.py
branches.py
users.py
courses.py
subjects.py
chapters.py
lectures.py
notes.py
recordings.py
quizzes.py
exams.py
notifications.py
reports.py
```

All APIs use:

``` text
/api/v1
```

## `app/core/`

Application-wide configuration and utilities:

``` text
config.py
timezone.py
security.py
logging.py
exceptions.py
```

## `app/db/`

Database infrastructure:

``` text
database.py
health.py
```

## `app/models/`

SQLAlchemy database models.

Current:

``` text
models/
├── __init__.py
└── institute.py
```

## `app/schemas/`

Pydantic request/response schemas.

Database models must not be used directly as API contracts.

## `app/repositories/`

Database query/access layer.

## `app/services/`

Business logic/application services.

## `app/middleware/`

CORS, request logging, security headers, request IDs, rate limiting,
etc.

------------------------------------------------------------------------

# 5. Environment System

Three environments:

``` text
local
dev
prod
```

Selected using:

``` env
APP_ENV
```

## Local

File:

``` text
.env.local
```

Run:

``` powershell
python scripts/local_run.py
```

## Development

File:

``` text
.env.dev
```

Run:

``` powershell
python scripts/dev_run.py
```

## Production

File:

``` text
.env.prod
```

Run:

``` powershell
python scripts/prod_run.py
```

Production will ultimately use Docker + Nginx on Ubuntu.

------------------------------------------------------------------------

# 6. Environment Variables

Example:

``` env
APP_NAME=AI-LMS
APP_ENV=local
DEBUG=true

DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5433/ai_lms

JWT_SECRET=change-this
JWT_REFRESH_SECRET=change-this-too

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

FRONTEND_URL=http://localhost:3000
CORS_ORIGINS=http://localhost:3000
```

Never commit real:

-   database passwords
-   JWT secrets
-   Google credentials
-   production API keys

Use `.env.example` for placeholders.

------------------------------------------------------------------------

# 7. PostgreSQL

Current local configuration:

``` text
Database: ai_lms
User: postgres
Host: localhost
Port: 5433
```

URL format:

``` text
postgresql+psycopg://postgres:PASSWORD@localhost:5433/ai_lms
```

One centralized PostgreSQL database is used.

Branch/institute isolation is enforced by backend authorization and
scoped queries.

------------------------------------------------------------------------

# 8. Virtual Environment Setup

``` powershell
python -m venv venv
```

Activate:

``` powershell
.\venv\Scripts\Activate.ps1
```

Check:

``` powershell
python --version
python -m pip --version
```

Install:

``` powershell
python -m pip install -r requirements.txt
```

------------------------------------------------------------------------

# 9. Run Backend

Local:

``` powershell
python scripts/local_run.py
```

Development:

``` powershell
python scripts/dev_run.py
```

Production-mode local run:

``` powershell
python scripts/prod_run.py
```

URLs:

``` text
Backend: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/docs
ReDoc:   http://127.0.0.1:8000/redoc
```

------------------------------------------------------------------------

# 10. Health API

Endpoint:

``` http
GET /api/v1/health
```

URL:

``` text
http://127.0.0.1:8000/api/v1/health
```

Expected:

``` json
{
  "success": true,
  "environment": "local",
  "api": "healthy",
  "database": "connected"
}
```

------------------------------------------------------------------------

# 11. Timezone Strategy

Institute stores:

``` text
country_code
timezone
```

Default:

``` text
country_code = IN
timezone = Asia/Kolkata
```

Use IANA timezone names:

``` text
Asia/Kolkata
Asia/Dubai
Europe/London
America/New_York
```

Do not use:

``` text
IST
EST
GMT+5:30
```

Future metadata APIs:

``` text
GET /api/v1/metadata/countries
GET /api/v1/metadata/timezones?country_code=IN
```

------------------------------------------------------------------------

# 12. Institute Model

Current table:

``` text
institutes
```

Fields:

``` text
id
name
code
email
phone
address
logo_url
country_code
timezone
is_active
created_at
updated_at
```

------------------------------------------------------------------------

# 13. Alembic Migration System

Workflow:

``` text
SQLAlchemy Model
       ↓
Alembic Autogenerate
       ↓
Migration File
       ↓
Review Migration
       ↓
alembic upgrade head
       ↓
PostgreSQL
```

## Direct Alembic commands

Current migration:

``` powershell
alembic current
```

History:

``` powershell
alembic history
```

Create migration:

``` powershell
alembic revision --autogenerate -m "describe change"
```

Apply:

``` powershell
alembic upgrade head
```

Rollback one:

``` powershell
alembic downgrade -1
```

Rollback all:

``` powershell
alembic downgrade base
```

Check:

``` powershell
alembic check
```

------------------------------------------------------------------------

# 14. Short Database Helper Commands

A project helper is available at:

``` text
scripts/db.py
```

## Model template

``` powershell
python scripts/db.py model user
```

Example:

``` powershell
python scripts/db.py model course
```

This creates a model template under:

``` text
app/models/
```

**Important:** The generated file is only a template. Add the real
fields, relationships, indexes and constraints manually.

Then register the model in:

``` text
app/models/__init__.py
```

------------------------------------------------------------------------

## Create migration

``` powershell
python scripts/db.py migration "create users table"
```

Equivalent:

``` powershell
alembic revision --autogenerate -m "create users table"
```

------------------------------------------------------------------------

## Apply migration

``` powershell
python scripts/db.py upgrade
```

Equivalent:

``` powershell
alembic upgrade head
```

------------------------------------------------------------------------

## Rollback one migration

``` powershell
python scripts/db.py downgrade
```

Equivalent:

``` powershell
alembic downgrade -1
```

------------------------------------------------------------------------

## Current migration

``` powershell
python scripts/db.py current
```

------------------------------------------------------------------------

## Schema check

``` powershell
python scripts/db.py check
```

Expected:

``` text
No new upgrade operations detected.
```

------------------------------------------------------------------------

## Migration history

``` powershell
python scripts/db.py history
```

------------------------------------------------------------------------

# 15. Recommended Migration Workflow

Whenever a database model changes:

``` text
1. Change SQLAlchemy model
          ↓
2. Register model
          ↓
3. Create migration
          ↓
4. Review generated migration
          ↓
5. Apply migration
          ↓
6. Check current revision
          ↓
7. Run schema check
          ↓
8. Verify database in pgAdmin
```

Commands:

``` powershell
python scripts/db.py migration "describe change"

python scripts/db.py upgrade

python scripts/db.py current

python scripts/db.py check
```

Never blindly apply an autogenerated migration.

------------------------------------------------------------------------

# 16. NEW MODULE DEVELOPMENT --- COMPLETE STANDARD WORKFLOW

> This is the most important section for future development.

Every new backend module must follow the same sequence.

Example module:

``` text
Course
```

The same process applies to:

``` text
User
Branch
Subject
Chapter
Lecture
Note
Recording
Quiz
Exam
Notification
Report
```

------------------------------------------------------------------------

## STEP 1 --- Freeze the Requirement

Before coding, define:

``` text
Module name
Purpose
Who can access it
Fields
Relationships
Business rules
Validation rules
Permissions
Branch/institute scope
API endpoints
Response format
Tests
```

Example:

``` text
Module: Course

Who:
SUPER_ADMIN
BRANCH_ADMIN
TEACHER
STUDENT (read only where applicable)

Scope:
Institute + Branch

Main operations:
Create
Read
Update
Delete
List
```

Do not start coding before the module behavior is clear.

------------------------------------------------------------------------

## STEP 2 --- Design Database Model

Create the model file:

``` powershell
python scripts/db.py model course
```

File:

``` text
app/models/course.py
```

Then implement:

``` text
Primary key
Columns
Foreign keys
Relationships
Indexes
Unique constraints
Nullable rules
Created/updated timestamps
Institute/branch relationship where required
```

Example conceptual structure:

``` text
Course
 ├── id
 ├── institute_id
 ├── branch_id
 ├── name
 ├── code
 ├── description
 ├── is_active
 ├── created_at
 └── updated_at
```

------------------------------------------------------------------------

## STEP 3 --- Register Model

Update:

``` text
app/models/__init__.py
```

Example:

``` python
from app.models.course import Course
from app.models.institute import Institute
```

The model must be registered so:

``` python
Base.metadata
```

contains the table.

Verify:

``` powershell
python -c "from app.db.database import Base; import app.models; print(Base.metadata.tables.keys())"
```

------------------------------------------------------------------------

## STEP 4 --- Create Migration

Run:

``` powershell
python scripts/db.py migration "create courses table"
```

A new file appears:

``` text
alembic/versions/
└── <revision>_create_courses_table.py
```

------------------------------------------------------------------------

## STEP 5 --- REVIEW MIGRATION

Before applying:

``` text
Open the generated migration.
```

Check:

``` text
Table name
Columns
Data types
Nullable
Primary key
Foreign keys
Indexes
Unique constraints
Defaults
ondelete behavior
```

Do not blindly trust Alembic autogenerate.

------------------------------------------------------------------------

## STEP 6 --- Apply Migration

After review:

``` powershell
python scripts/db.py upgrade
```

Then:

``` powershell
python scripts/db.py current
```

Then:

``` powershell
python scripts/db.py check
```

Expected:

``` text
No new upgrade operations detected.
```

------------------------------------------------------------------------

## STEP 7 --- Verify PostgreSQL

Open pgAdmin:

``` text
ai_lms
 → Schemas
   → public
     → Tables
```

Refresh and verify the new table.

------------------------------------------------------------------------

## STEP 8 --- Create Pydantic Schemas

Create:

``` text
app/schemas/course.py
```

Typical schemas:

``` text
CourseCreate
CourseUpdate
CourseResponse
CourseListResponse
```

Responsibilities:

``` text
Request validation
Response serialization
Type validation
API contract
```

Do not expose SQLAlchemy models directly.

------------------------------------------------------------------------

## STEP 9 --- Create Repository

Create:

``` text
app/repositories/course_repository.py
```

Repository handles database operations:

``` text
create()
get_by_id()
get_list()
update()
delete()
```

It should contain database/query logic, not HTTP logic.

------------------------------------------------------------------------

## STEP 10 --- Create Service

Create:

``` text
app/services/course_service.py
```

Service handles business rules:

``` text
permission-related checks
duplicate checks
branch scope validation
business validation
repository coordination
```

Example:

``` text
API
 ↓
Service
 ↓
Repository
 ↓
Database
```

------------------------------------------------------------------------

## STEP 11 --- Create API Router

Create:

``` text
app/api/v1/courses.py
```

Typical endpoints:

``` text
POST   /api/v1/courses
GET    /api/v1/courses
GET    /api/v1/courses/{course_id}
PATCH  /api/v1/courses/{course_id}
DELETE /api/v1/courses/{course_id}
```

------------------------------------------------------------------------

## STEP 12 --- Add Authentication

Every protected endpoint must identify the logged-in user.

Flow:

``` text
Request
 ↓
JWT
 ↓
Current User
 ↓
Role
 ↓
Permission
 ↓
Business Logic
```

Never trust:

``` text
user_id
role
branch_id
institute_id
```

coming directly from the frontend when they can be derived securely from
the authenticated user.

------------------------------------------------------------------------

## STEP 13 --- Add RBAC

Define who can perform each operation.

Example:

``` text
Create Course:
SUPER_ADMIN     ✅
BRANCH_ADMIN    ✅
TEACHER         depends on permission
STUDENT         ❌

Update Course:
SUPER_ADMIN     ✅
BRANCH_ADMIN    ✅
TEACHER         depends on permission
STUDENT         ❌

Delete Course:
SUPER_ADMIN     ✅
BRANCH_ADMIN    according to policy
TEACHER         ❌
STUDENT         ❌
```

Exact permissions must follow the project's RBAC matrix.

------------------------------------------------------------------------

## STEP 14 --- Add Institute/Branch Isolation

For branch-sensitive modules:

``` text
JWT user
   ↓
User institute
   ↓
User branch
   ↓
Allowed operation
   ↓
Scoped query
```

Example rule:

``` text
WHERE course.branch_id = current_user.branch_id
```

A user must never access another branch by modifying a URL ID.

------------------------------------------------------------------------

## STEP 15 --- Register Router

Update the API router structure.

Example:

``` text
app/api/v1/
├── __init__.py
└── courses.py
```

Then register it in the central router/main application according to the
project's router architecture.

Final API:

``` text
/api/v1/courses
```

------------------------------------------------------------------------

## STEP 16 --- Add Validation and Error Handling

Handle:

``` text
Invalid ID
Not found
Duplicate record
Unauthorized
Forbidden
Invalid input
Database conflict
Unexpected server error
```

Do not leak:

``` text
database credentials
SQL internals
password hashes
private secrets
stack traces
```

to production clients.

------------------------------------------------------------------------

## STEP 17 --- Test the Module

Create tests:

``` text
tests/
├── unit/
├── integration/
└── api/
```

Minimum test cases:

``` text
Create success
Read success
List success
Update success
Delete success
Validation failure
Unauthorized request
Forbidden request
Not found
Duplicate data
Branch isolation
```

------------------------------------------------------------------------

## STEP 18 --- Swagger/API Verification

Start backend:

``` powershell
python scripts/local_run.py
```

Open:

``` text
http://127.0.0.1:8000/docs
```

Test:

``` text
POST
GET
GET /{id}
PATCH
DELETE
```

Check request and response schemas.

------------------------------------------------------------------------

## STEP 19 --- Final Database Verification

Run:

``` powershell
python scripts/db.py current
```

Then:

``` powershell
python scripts/db.py check
```

Expected:

``` text
No new upgrade operations detected.
```

------------------------------------------------------------------------

## STEP 20 --- Git Verification

Before commit:

``` powershell
git status
git diff
```

Then:

``` powershell
git add .
git commit -m "feat: add course module"
```

------------------------------------------------------------------------

# 17. NEW MODULE FINAL CHECKLIST

Before calling any module complete:

``` text
[ ] Requirement frozen
[ ] Database model created
[ ] Relationships checked
[ ] Model registered
[ ] Migration generated
[ ] Migration manually reviewed
[ ] Migration applied
[ ] PostgreSQL verified
[ ] Pydantic schemas created
[ ] Repository created
[ ] Service created
[ ] Router created
[ ] Router registered
[ ] Authentication added
[ ] RBAC added
[ ] Branch isolation added
[ ] Validation added
[ ] Error handling added
[ ] Unit tests added
[ ] API tests added
[ ] Swagger tested
[ ] alembic current checked
[ ] alembic check passed
[ ] Git diff reviewed
[ ] Documentation updated
```

Only then:

``` text
MODULE = COMPLETE ✅
```

------------------------------------------------------------------------

# 18. API Layer Architecture

Recommended flow:

``` text
Client
  ↓
FastAPI Router
  ↓
Authentication
  ↓
Authorization / RBAC
  ↓
Pydantic Validation
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

Do not put the entire business logic inside route functions.

------------------------------------------------------------------------

# 19. Authentication Plan

``` text
Login
  ↓
Verify credentials
  ↓
Access token + refresh token
  ↓
Client sends access token
  ↓
JWT verification
  ↓
Identify user
  ↓
Role/permission check
  ↓
Protected API
```

Roles:

``` text
SUPER_ADMIN
BRANCH_ADMIN
ACCOUNTS
TEACHER
STUDENT
```

------------------------------------------------------------------------

# 20. RBAC

Backend authorization is mandatory.

Frontend button hiding is not security.

Every protected API must verify permissions server-side.

------------------------------------------------------------------------

# 21. Multi-Branch Isolation

``` text
Request
   ↓
JWT
   ↓
User
   ↓
Role
   ↓
Institute / Branch Scope
   ↓
Scoped Repository Query
   ↓
Authorized Data
```

Branch A must never access Branch B data by changing an ID in a URL.

------------------------------------------------------------------------

# 22. Academic Hierarchy

``` text
Course
   ↓
Subject
   ↓
Chapter
   ↓
Lecture
   ├── Notes
   ├── Documents
   ├── Video
   └── Resources
```

------------------------------------------------------------------------

# 23. Recording Workflow

``` text
Live Class
    ↓
Temporary Local Storage
    ↓
2–3 Day Retention
    ↓
Google Drive Upload
    ↓
Upload Verification
    ↓
Student Notification
    ↓
Authorized Streaming
```

Security:

-   no public Drive link
-   no direct download URL
-   authorization before playback
-   branch/course/student access validation

------------------------------------------------------------------------

# 24. Quiz Workflow

``` text
Teacher creates quiz
       ↓
Questions added
       ↓
Quiz published
       ↓
Student starts quiz
       ↓
Attempt recorded
       ↓
Answers submitted
       ↓
Evaluation
       ↓
Result
```

------------------------------------------------------------------------

# 25. Secure Exam Workflow

Required controls:

-   camera permission mandatory
-   voice detection
-   fullscreen monitoring
-   tab/window violation monitoring
-   violation counter
-   two violations can lock/terminate the attempt
-   admin review
-   admin unlock/re-enable capability

Flow:

``` text
Student starts exam
       ↓
Camera permission
       ↓
Voice detection
       ↓
Fullscreen/tab monitoring
       ↓
Violation
       ↓
Count violation
       ↓
2 violations
       ↓
Lock / terminate
       ↓
Admin review
       ↓
Admin may unlock
```

------------------------------------------------------------------------

# 26. AI Question Generation

AI generates drafts only:

``` text
Teacher selects:
Course
Subject
Chapter
Difficulty
Question count
       ↓
AI generation
       ↓
Draft questions
       ↓
Teacher review
       ↓
Edit / approve
       ↓
Publish
```

**AI-generated questions must never publish directly without teacher
approval.**

------------------------------------------------------------------------

# 27. Question Randomization

``` text
Question Pool
     ↓
Same questions
     ↓
Random question order
     ↓
Random option order
```

------------------------------------------------------------------------

# 28. API Standards

Base prefix:

``` text
/api/v1
```

Examples:

``` text
GET    /api/v1/health

POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout

GET    /api/v1/institutes
POST   /api/v1/institutes
GET    /api/v1/institutes/{id}
PATCH  /api/v1/institutes/{id}
DELETE /api/v1/institutes/{id}
```

Breaking changes should use a new API version.

------------------------------------------------------------------------

# 29. API Response Standard

Success:

``` json
{
  "success": true,
  "data": {},
  "message": "Request successful"
}
```

Error:

``` json
{
  "success": false,
  "message": "Validation failed",
  "error_code": "VALIDATION_ERROR",
  "details": {}
}
```

------------------------------------------------------------------------

# 30. Security Rules

Never:

``` text
Hardcode passwords
Hardcode JWT secrets
Commit production credentials
Expose DB passwords
Trust frontend authorization
Return password hashes
Expose private Google Drive URLs
Disable HTTPS in production
```

Always:

``` text
Validate input
Use ORM/parameterized queries
Hash passwords
Use secure JWT handling
Check RBAC server-side
Check branch scope
Use HTTPS
Log security events
Rate-limit sensitive APIs
```

------------------------------------------------------------------------

# 31. Git Rules

Check:

``` powershell
git status
git diff
```

Do not commit:

``` text
.env
.env.local
.env.dev
.env.prod
venv/
__pycache__/
.pytest_cache/
```

Feature branch:

``` powershell
git checkout -b feature/course-module
```

Commit:

``` powershell
git add .
git commit -m "feat: add course module"
```

Push:

``` powershell
git push -u origin feature/course-module
```

------------------------------------------------------------------------

# 32. Testing

Structure:

``` text
tests/
├── unit/
├── integration/
└── api/
```

Test:

``` text
Authentication
Authorization
Institute
Branch isolation
Courses
Quizzes
Exams
Recordings
AI approval workflow
Notifications
Reports
```

------------------------------------------------------------------------

# 33. Production Architecture

``` text
Internet
   ↓
HTTPS
   ↓
Nginx
   ↓
Docker
   ↓
FastAPI
   ↓
PostgreSQL
```

Recording archive:

``` text
FastAPI
   ↓
Google Drive API
   ↓
Private Recording Archive
```

------------------------------------------------------------------------

# 34. Production Checklist

``` text
[ ] DEBUG=false
[ ] Strong production JWT secrets
[ ] Production DB configured
[ ] HTTPS enabled
[ ] CORS restricted
[ ] Rate limiting enabled
[ ] Security headers enabled
[ ] Database backups configured
[ ] Logging configured
[ ] Global exception handling configured
[ ] Google credentials secured
[ ] Docker health checks configured
[ ] Nginx configured
[ ] Migrations applied
[ ] API smoke tests passed
[ ] No secrets committed
```

------------------------------------------------------------------------

# 35. Development Roadmap

``` text
01. Environment System                  ✅
02. PostgreSQL Connection               ✅
03. SQLAlchemy Base                     ✅
04. Alembic Configuration               ✅
05. Institute Model                     ✅
06. First Migration                     ✅

07. Logging System                      ⏳
08. Global Exception Handler            ⏳
09. CORS                                ⏳
10. API Router Structure                ⏳
11. Production Configuration            ⏳
12. Docker                              ⏳

13. Authentication                     ⏳
14. JWT Access/Refresh                  ⏳
15. RBAC                                ⏳
16. Institute/Branch Management         ⏳
17. User Management                     ⏳
18. Course Management                   ⏳
19. Subject Management                  ⏳
20. Chapter Management                  ⏳
21. Lecture Management                  ⏳
22. Notes/Documents                     ⏳
23. Recording + Google Drive            ⏳
24. Quiz                                ⏳
25. Secure Exam                         ⏳
26. Proctoring                          ⏳
27. Notifications                       ⏳
28. Reports                             ⏳
29. AI Question Generation              ⏳
30. Testing                             ⏳
31. Production Deployment               ⏳
```

------------------------------------------------------------------------

# 36. Rules for Future AI / Developers

Before coding:

``` text
1. Read README.md
2. Read project rules/documentation
3. Check existing architecture
4. Do not change the stack without approval
5. Do not create duplicate systems
6. Do not bypass RBAC
7. Do not bypass branch isolation
8. Do not hardcode secrets
9. Do not directly modify production DB
10. Create migrations for schema changes
```

Permanent decisions:

``` text
Backend       = Python + FastAPI
Database      = PostgreSQL
ORM           = SQLAlchemy
Migrations    = Alembic
Frontend      = Next.js + TypeScript
Auth          = JWT
Storage       = Google Drive for recordings
Deployment    = Ubuntu + Docker + Nginx
Timezone      = Institute-specific IANA timezone
Default       = Asia/Kolkata
```

If a new requirement conflicts with these decisions, review the
architecture before implementation.

------------------------------------------------------------------------

# 37. Current Institute Migration --- Verified

Migration:

``` text
257e6c6b4a86_create_institutes_table.py
```

Applied:

``` powershell
alembic upgrade head
```

Verified:

``` powershell
alembic current
```

Result:

``` text
257e6c6b4a86 (head)
```

Schema:

``` powershell
alembic check
```

Result:

``` text
No new upgrade operations detected.
```

Database currently contains:

``` text
alembic_version
institutes
```

------------------------------------------------------------------------

# 38. Quick Start --- Fresh Developer

``` powershell
git clone <REPOSITORY_URL>
cd aiLMS_Backend

python -m venv venv
.\venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt

# Configure .env.local

alembic upgrade head

python scripts/local_run.py
```

Open:

``` text
http://127.0.0.1:8000/docs
```

Health:

``` text
http://127.0.0.1:8000/api/v1/health
```

------------------------------------------------------------------------

# 39. Final Backend Health Checklist

``` text
✅ Virtual environment works
✅ Dependencies installed
✅ .env.local loads
✅ PostgreSQL connection works
✅ FastAPI starts
✅ /api/v1/health returns 200
✅ Swagger opens
✅ Alembic current shows head
✅ Alembic check reports no changes
✅ Institute model is registered
✅ institutes table exists
```

Current:

``` text
AI-LMS Backend Foundation
=========================

Environment       ✅
FastAPI           ✅
PostgreSQL        ✅
SQLAlchemy        ✅
Alembic           ✅
Institute Model   ✅
First Migration   ✅
Schema Check      ✅

Next:
Logging System
```

# 40. WorkFlow :
Requirement Freeze
      ↓
Database Model
      ↓
Model Register
      ↓
Migration Create
      ↓
Migration Review
      ↓
Migration Upgrade
      ↓
PostgreSQL Verify
      ↓
Pydantic Schema
      ↓
Repository
      ↓
Service
      ↓
API Router
      ↓
Authentication
      ↓
RBAC
      ↓
Branch Isolation
      ↓
Validation
      ↓
Error Handling
      ↓
Tests
      ↓
Swagger Testing
      ↓
Alembic Check
      ↓
Git Review / Commit
      ↓
MODULE COMPLETE ✅

# 41. Major Modules :
| #  | Module                       | Main Purpose                            |
| -- | ---------------------------- | --------------------------------------- |
| 1  | 🔐 Authentication            | Login, JWT, refresh, logout             |
| 2  | 👥 User & RBAC               | Users, roles, permissions               |
| 3  | 🏢 Institute & Branch        | Multi-institute/branch management       |
| 4  | 📚 Course Management         | Course, subject, chapter, lecture       |
| 5  | 📄 Content & Notes           | Notes, documents, resources             |
| 6  | 🎥 Live Class                | Live classes & scheduling               |
| 7  | 🎬 Recording                 | Recording + Google Drive                |
| 8  | 📝 Quiz                      | Quiz/question/answer/result             |
| 9  | 🧪 Examination               | Exam, questions, attempts, results      |
| 10 | 🛡️ Secure Exam / Proctoring | Camera, voice, violations               |
| 11 | 🤖 AI Question Generation    | AI-generated question drafts + approval |
| 12 | 🔔 Notifications             | Student/teacher/admin notifications     |
| 13 | 💰 Accounts & Finance        | Fees, payments, expenses, transactions  |
| 14 | 📊 Reports & Analytics       | Academic, student, branch reports       |
| 15 | ⚙️ Settings & Configuration  | Institute/system settings               |
| 16 | 📝 Audit & Activity          | Security/activity/audit logs            |

# 42. Models :
## Database Modules & Models

The AI-LMS backend is divided into multiple functional modules.  
The following model structure is the current planned database design.

> **Note:** The total number of models is an initial planning estimate.  
> Models may be merged, split, or adjusted during implementation based on finalized business rules and relationships.

---

### 1. Institute & Branch

**Purpose:** Institute and branch-level organization and isolation.

**Models:**

1. `Institute`
2. `Branch`

---

### 2. Authentication / Users / RBAC

**Purpose:** Authentication, user management, roles, and permission-based access control.

**Models:**

3. `User`
4. `Role`
5. `Permission`
6. `RolePermission`
7. `UserRole`

> **Note:** If a simplified RBAC implementation is sufficient, some RBAC models may be combined.

---

### 3. Academic

**Purpose:** Manage the academic hierarchy and student enrollment.

**Models:**

8. `Course`
9. `Subject`
10. `Chapter`
11. `Lecture`
12. `Enrollment`

---

### 4. Content

**Purpose:** Manage notes, documents, and other learning resources.

**Models:**

13. `Note`
14. `Document`
15. `Resource`

> **Note:** Depending on the final content requirements, `Document` and `Resource` may be combined into a single model.

---

### 5. Live Class / Recording

**Purpose:** Manage live classes, recorded lectures, and student access to recordings.

**Models:**

16. `LiveClass`
17. `Recording`
18. `RecordingAccess`

---

### 6. Quiz

**Purpose:** Manage quizzes, questions, options, attempts, and answers.

**Models:**

19. `Quiz`
20. `Question`
21. `QuestionOption`
22. `QuizAttempt`
23. `QuizAnswer`

---

### 7. Examination

**Purpose:** Manage examinations, exam questions, attempts, answers, violations, and results.

**Models:**

24. `Exam`
25. `ExamQuestion`
26. `ExamAttempt`
27. `ExamAnswer`
28. `ExamViolation`
29. `ExamResult`

---

### 8. AI

**Purpose:** Manage AI-assisted question generation and AI-generated question data.

**Models:**

30. `AIQuestionGeneration`
31. `AIGeneratedQuestion`

> **Note:** The AI module will be implemented in a future development phase.  
> AI-generated questions must go through teacher/admin review and approval before being published.

---

### 9. Notification

**Purpose:** Manage system notifications and notification delivery to users.

**Models:**

32. `Notification`
33. `NotificationRecipient`

---

### 10. Accounts

**Purpose:** Manage fees, payments, expenses, and financial transactions.

**Models:**

34. `FeeStructure`
35. `FeePayment`
36. `Expense`
37. `Transaction`

---

### 11. Audit

**Purpose:** Maintain system-level audit records and user activity logs.

**Models:**

38. `AuditLog`
39. `ActivityLog`

---

## Model Count

**Current Planned Models: 39**

The above count is a **planning baseline**, not a permanently fixed number.

During implementation:

- Models may be added if new business requirements are identified.
- Models may be merged if two models have overlapping responsibilities.
- Models may be split if a model becomes too complex.
- Relationships and constraints will be finalized before each module migration.
- Any structural database change must follow the project's migration workflow.


# 43. Short Command Model and Migration :
python scripts/db.py model user
python scripts/db.py migration "create users table"
python scripts/db.py upgrade
python scripts/db.py downgrade
python scripts/db.py current
python scripts/db.py check
python scripts/db.py history

------------------------------------------------------------------------

# 50. Maintainer

**Er. Hariom Verma**\
**Bharatcoder.com**

**AI Powered Multi-Branch Learning Management System (AI-LMS)**

**Client:** Shankar Yadav
