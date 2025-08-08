# CTH‑HRMIS Backend (CTH‑2025)

> **Clinic / Hospital Human‑Resource Management Information System** － Python Flask API ＋ MySQL 8.0
>
> 目前已完成 **登入、使用者管理、部門管理、組織管理**；後續將加入職能／年度目標模組與自動產生組織圖。

---

## ✨ 專案亮點

| 模組               | 已完成                      | 技術要點                            |
| ---------------- | ------------------------ | ------------------------------- |
| **Auth**         | ✅ JWT 登入 / Refresh Token | `flask-jwt-extended`, `bcrypt`  |
| **User**         | ✅ CRUD、日期欄位驗證            | `Marshmallow`, `SQLAlchemy` ORM |
| **Department**   | ✅ CRUD＋第一/第二主管           | 外鍵 & 索引優化                       |
| **Organization** | ✅ 四層架構、CRUD              | Tree 走訪產生 Org Chart JSON        |
| **Org Chart**    | 🔧 產生 SVG 圖（進行中）         | `pydot` → Vue `v-network-graph` |

---

## 🏗️ 專案結構

```text
CTH-2025/
├── backend/
│   ├── app/
│   │   ├── __init__.py        # 建立 Flask App & JWT
│   │   ├── models/            # SQLAlchemy 資料模型
│   │   ├── routes/            # Blueprint: auth, users, departments, orgs
│   │   └── utils/             # 工具函式（日期轉換等）
│   ├── config.py              # 環境變數讀取
│   ├── requirements.txt
│   └── run.py                 # `flask --app run run` 入口
├── docker-compose.yml         # MySQL 8.0 + Adminer + Backend
└── README.md                  # 本文件
```

---
## 📑 API 一覽

| Method   | Path               | 說明                                     |
| -------- | ------------------ | -------------------------------------- |
| `POST`   | `/api/login`       | 取得 JWT／Refresh Token                   |
| `GET`    | `/api/users`       | 使用者列表（支援分頁）                            |
| `POST`   | `/api/users`       | 新增使用者                                  |
| `PUT`    | `/api/users/<id>`  | 更新使用者                                  |
| `DELETE` | `/api/users/<id>`  | 刪除使用者                                  |
| `GET`    | `/api/departments` | 部門列表                                   |
---
## 🔗 前端 Repo

前端 Vue 專案請見 👉 [https://github.com/onelovehch/CTH‑HRMIS-Frontend]
---
## 📝 License

Released under the MIT License © 2025 onelovehch
