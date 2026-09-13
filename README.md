# Simple Todo API — CI/CD 練習專案

一個刻意做得很簡單的 Flask Todo API，重點不在功能複雜度，而是完整走過一次 CI/CD 流程：
**Git → Jenkins → Pytest → Docker → 部署**。

## 架構圖（文字版）

```
開發者 push code
      │
      ▼
   Git repo (GitHub)  ──webhook──▶  Jenkins
                                       │
                          ┌────────────┼────────────┐
                          ▼            ▼             ▼
                     Checkout    安裝依賴       Lint (flake8)
                          │
                          ▼
                    Pytest 單元測試
                          │
                    測試通過？
                     ┌────┴────┐
                    Yes        No → Pipeline 標記失敗，通知
                     │
                     ▼
              docker build image
                     │
                     ▼
          docker run 部署到目標環境
                     │
                     ▼
            Smoke Test（打 /health 確認存活）
```

## 專案結構

```
simple-todo-api/
├── app/
│   ├── __init__.py
│   └── main.py          # Flask API 主程式
├── tests/
│   └── test_main.py     # pytest 測試
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile           # Pipeline 定義（Pipeline as Code）
└── .gitignore
```

## API 端點

| Method | Path            | 說明             |
|--------|-----------------|------------------|
| GET    | /health         | 健康檢查         |
| GET    | /todos          | 取得所有待辦事項 |
| GET    | /todos/<id>     | 取得單一待辦事項 |
| POST   | /todos          | 新增待辦事項     |
| PUT    | /todos/<id>     | 更新待辦事項     |
| DELETE | /todos/<id>     | 刪除待辦事項     |

## 本機開發

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 跑測試
pytest tests/ -v

# 本機啟動
python app/main.py
```

## 用 Docker 跑

```bash
docker build -t simple-todo-api .
docker run -p 5000:5000 simple-todo-api

# 或直接用 docker-compose
docker-compose up --build
```

## 設定 Jenkins Pipeline

1. 把這個專案 push 到你自己的 GitHub repo
2. Jenkins 安裝 Docker Pipeline plugin（讓 agent 能執行 `docker` 指令）
3. 新增一個 Pipeline Job，Pipeline 來源選擇「Pipeline script from SCM」，指向你的 repo，Script Path 填 `Jenkinsfile`
4. 在 GitHub repo 設定 webhook，指向 Jenkins 的 `/github-webhook/` endpoint，讓 push 自動觸發 build
5. （選用）如果要推送到 Docker Hub，先在 Jenkins 的 Credentials 裡新增帳密，Jenkinsfile 裡的註解區塊可以直接打開使用

## 下一步可以加強的地方

- 加上 `pytest-cov` 的覆蓋率門檻（例如低於 80% 就讓 pipeline fail）
- 把部署目標換成真正的雲端 VM（GCP/AWS 免費額度）或 Kubernetes
- 加上 Slack/Email 通知，pipeline 失敗時自動通知
- 導入 staging / production 兩階段部署，加上人工核准（Jenkins 的 `input` step）
