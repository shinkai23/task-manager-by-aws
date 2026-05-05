# Database Design

## Overview
Task Manager は、ユーザーごとにタスクを管理する Web API です。
`users` と `tasks` は 1 対多の関係を持ち、各タスクは必ず 1 人のユーザーに紐づきます。

## ER Diagram
![ER Diagram](./er-diagram.png)

## Tables

### users
ユーザー情報を管理するテーブルです。

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PK, AUTO_INCREMENT | ユーザー ID |
| username | VARCHAR(50) | NOT NULL, UNIQUE | 表示用ユーザー名 |
| email | VARCHAR(100) | NOT NULL, UNIQUE | ログイン用メールアドレス |
| password_hash | VARCHAR(255) | NOT NULL | ハッシュ化済みパスワード |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 作成日時 |
| updated_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 更新日時 |

### tasks
ユーザーごとのタスク情報を管理するテーブルです。

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PK, AUTO_INCREMENT | タスク ID |
| user_id | INT | FK, NOT NULL | `users.id` への外部キー |
| title | VARCHAR(100) | NOT NULL | タスクタイトル |
| description | TEXT | NULL | 詳細説明 |
| status | ENUM | `todo`, `doing`, `done` | タスク状態 |
| priority | ENUM | `low`, `medium`, `high` | 優先度 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 作成日時 |

## Relationships

```text
users.id 1 ---- N tasks.user_id
```

## Design Considerations
- タスクは `user_id` でユーザーに紐づける
- タスク取得時はログインユーザーの `user_id` で必ず絞り込む
- パスワードはハッシュ化して保存する
- `email` は一意制約で重複登録を防ぐ

## Index Strategy
ユーザー単位でタスクを検索するため、MySQL/RDS では `tasks.user_id` の index を利用します。

```sql
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```
