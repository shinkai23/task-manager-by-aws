# Task Manager

## Overview
タスク管理を行うWebアプリケーション。  
ユーザーごとにタスクの作成・読取・更新・削除（CRUD）を行う。

---

## Features
- ユーザー認証（JWT）
- タスクCRUD
- ステータス管理（todo / doing / done）
- 優先度管理（low / medium / high）

---

## Tech Stack
- Backend: FastAPI
- DB: MySQL (RDS)
- ORM: SQLAlchemy
- Infra: AWS (EC2, RDS)
- Others: Docker（任意）

---

## Architecture
![architecture](docs/aws-architecture.png)

---

## ER Diagram
![er-diagram](docs/er-diagram.png)

---

## API Endpoints

### Auth
- POST /register
- POST /login

### Tasks
- GET /tasks
- POST /tasks
- PUT /tasks/{id}
- DELETE /tasks/{id}

---

## Setup

### 1. Clone
```bash
git clone https://github.com/shinkai23/task-manager-by-aws.git
cd task-manager-by-aws
