# Task Manager

## Overview
ユーザーごとにタスクを管理できる FastAPI 製のタスク管理 API です。
JWT 認証により、ログイン中のユーザーは自分のタスクだけを作成・取得・更新・削除できます。

## Features
- ユーザー登録
- JWT ログイン認証
- ユーザー別タスク CRUD
- タスクステータス管理: `todo` / `doing` / `done`
- 優先度管理: `low` / `medium` / `high`

## Tech Stack
- Backend: FastAPI
- ORM: SQLAlchemy
- DB: SQLite for local development, MySQL/RDS for production
- Auth: JWT
- Infra: AWS EC2 / RDS

## Architecture
![architecture](docs/aws-architecture.png)

## ER Diagram
![er-diagram](docs/er-diagram.png)

## API Endpoints

### Users
- `POST /users/`
- `GET /users/me`

### Auth
- `POST /auth/login`

### Tasks
- `GET /tasks/`
- `POST /tasks/`
- `GET /tasks/{task_id}`
- `PUT /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

## Setup

### 1. Clone
```bash
git clone https://github.com/shinkai23/task-manager-by-aws.git
cd task-manager-by-aws
```

### 2. Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
```bash
cp app/.env.example app/.env
```

Example:

```env
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

For MySQL/RDS:

```env
DATABASE_URL=mysql+pymysql://user:password@host:3306/dbname
```

### 5. Run
```bash
uvicorn app.main:app --reload
```

## Directory Structure

```text
app/
  db/
  models/
  repositories/
  routers/
  schemas/
  services/
  utils/
  main.py

docs/
  aws-architecture.png
  db-design.md
  er-diagram.png
  schema.sql
```

## Database Design
[docs/db-design.md](docs/db-design.md)

## Future Improvements
- AWS RDS 接続の本番設定
- CI/CD 構築
- Docker 対応
- Cognito 導入

## Author
https://github.com/shinkai23
