# Database Design

## Overview
本システムはユーザーごとにタスクを管理するWebアプリケーションであり、  
ユーザーとタスクは1対多の関係を持つ。

---

## ER Diagram
![ER Diagram](./er-diagram.png)

---

## Tables

### users
ユーザー情報を管理するテーブル。

| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| id | INT | PK, AUTO_INCREMENT | ユーザー識別子 |
| username | VARCHAR(50) | NOT NULL, UNIQUE | 表示用ユーザー名 |
| email | VARCHAR(100) | NOT NULL, UNIQUE | ログイン用メールアドレス |
| password_hash | VARCHAR(255) | NOT NULL | パスワード（ハッシュ化） |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 作成日時 |
| updated_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 更新日時 |

---

### tasks
ユーザーごとのタスク情報を管理するテーブル。

| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| id | INT | PK, AUTO_INCREMENT | タスク識別子 |
| user_id | INT | FK, NOT NULL | users.idへの外部キー |
| title | VARCHAR(100) | NOT NULL | タスクタイトル |
| description | TEXT | NULL | 詳細説明 |
| status | ENUM | ('todo','doing','done') | タスク状態 |
| priority | ENUM | ('low','medium','high') | 優先度 |
| due_date | DATE | NULL | 期限日 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 作成日時 |
| updated_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 更新日時 |
| deleted_at | DATETIME | NULL | 論理削除用 |

---

## Relationships

- users（1） : tasks（多）
- tasks.user_id は users.id を参照する外部キー

```text
users.id 1 ──── N tasks.user_id
```
## Design Considerations

### 1. 正規化
- ユーザとタスクを分離し、冗長性を排除
- 第3正規形を満たす設計

### 2. セキュリティ
- パスワードはハッシュ化して保存
- emailは一意制約を付与

### 3. データ整合性
- 外部キー制約により参照整合性を担保
- ENUMで状態・優先度の値を制限

### 4. 拡張性
- tasksにタグ機能などを追加可能
- usersにプロフィール情報を追加可能

### 5. 論理削除
- deleted_atを使用し、データの復元・監査を可能

## Index Strategy
- tasks.user_id: ユーザごとの検索最適化
- tasks.status: ステータス別検索用

```sql
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
```

## Future Improvements
- タグ機能
- カテゴリ管理
- 通知機能
- 監査ログの追加


