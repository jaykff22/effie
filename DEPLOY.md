# 部署到海外（Render + Supabase）

国内分享链接走国内节点，海外访问会超时。本仓库用 Render 跑 Python 服务、Supabase 存数据，部署后得到一个海外可访问的 HTTPS 地址。

## 1. Supabase

1. 打开 https://supabase.com/dashboard ，新建一个 Free 项目（区域建议选离用户近的，例如 Singapore）。
2. 进入 **Project Settings → Database**，找到 **Connection string → URI**，复制形如
   `postgresql://postgres.xxxx:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres`
   的连接串，把 `[YOUR-PASSWORD]` 换成你建项目时设置的数据库密码。
3. 这个连接串只填到 Render 环境变量里，不要提交到仓库或发给别人。

> 服务启动时会自动创建 `users` / `progress` / `questions` 三张表，无需手动执行 SQL。

## 2. Render

1. 打开 https://dashboard.render.com ，用 GitHub 登录并授权仓库 `effie`。
2. 右上角 **New + → Blueprint**，选择 `jaykff22/effie`，Render 会读取仓库根目录的 `render.yaml`。
3. 填写两个环境变量：
   - `DATABASE_URL`：上一步复制的 Supabase 连接串
   - `ADMIN_EMAIL`：管理员邮箱（用这个邮箱注册后即为管理员，可导入题库）
4. 点击 Apply，等待部署完成。
5. 打开分配的 `https://xxx.onrender.com`，确认首页和 `/api/health` 正常。

> 仓库里原有的 `auth.js` / `supabase-setup.sql` 属于旧版静态方案，Render 只运行 `server.py`，不会被用到，可以留着。

## 3. 迁移题库

本机进入本目录执行（需要 Python 3 和 `pip install -r requirements.txt`）：

```bash
python3 migrate_to_postgres.py ../outputs/learning_site.sqlite3
```

脚本会提示输入 Supabase 连接串，输入内容不会显示在屏幕上。它只迁移题库，不迁移本地账号和密码。

迁移后打开线上「口语题库」确认题目数量，并用 `ADMIN_EMAIL` 邮箱注册管理员账号测试导入功能。

## 4. 注意事项

- Render Free 计划约 15 分钟无访问后休眠，首次访问可能需要等待几十秒唤醒。
- Supabase Free 项目长期低活跃可能暂停，需要到控制台恢复。
- 线上和国内 WorkBuddy 分享链接的数据是**两套独立数据**，不会自动同步。
- 以后改了本地页面，重新推送到 `effie` 仓库的 `main` 分支，Render 会自动重新部署。
