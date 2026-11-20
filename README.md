# Speak & Write IELTS

IELTS 口语与写作学习站：首页、登录注册、学习中心、口语题库、客服二维码。

## 本地运行

```bash
python3 -m pip install -r requirements.txt
python3 server.py
```

打开 http://127.0.0.1:8000 。未设置 `DATABASE_URL` 时默认使用本地 SQLite。

## 线上部署（Render + Supabase）

见 [DEPLOY.md](DEPLOY.md)。

## 结构

- `server.py` — Python HTTP 服务与 API
- `index.html` — 首页
- `login.html` — 登录 / 注册
- `dashboard.html` — 学习中心
- `question-bank.html` — 口语题库（管理员可导入）
- `wechat-qr.html` — 客服二维码（二维码已内嵌为 data URI）
- `render.yaml` — Render Blueprint 配置
- `migrate_to_postgres.py` — 把本地 SQLite 题库迁移到 PostgreSQL
