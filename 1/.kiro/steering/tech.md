# Tech Stack

## Backend
- Python + Flask (web framework)
- Flask-SQLAlchemy (ORM)
- Flask-CORS (cross-origin support)
- PyMySQL (MySQL driver)
- PyJWT + Werkzeug (auth / password hashing)
- OpenAI SDK pointed at Alibaba DashScope (`qwen-turbo` model) for AI recommendations

## Frontend
- Vue 3 (Composition API, `<script setup>`)
- Vite 6 (build tool)
- Axios (HTTP client)
- No state management library — component-local `ref` and prop/event patterns only

## Database
- MySQL — database name `navdb`, default user `root`
- Schema auto-created by SQLAlchemy on startup (`db.create_all()`)

## Environment Variables
| Variable | Purpose |
|---|---|
| `MYSQL_PASSWORD` | MySQL root password |
| `JWT_SECRET` | JWT signing secret (default: `nav-jwt-secret-2024`) |
| `DASHSCOPE_API_KEY` | Alibaba DashScope API key for AI recommendations |

## Common Commands

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py          # starts Flask dev server on port 5000
```

### Frontend (dev mode)
```bash
cd frontend
npm install
npm run dev            # Vite dev server on port 5173, proxies /api → localhost:5000
npm run build          # outputs to frontend/dist
```

### One-click start (Windows)
Double-click `启动.bat` in the project root — prompts for MySQL password and opens the browser.

## API Base URL
All REST endpoints are prefixed with `/api`. The Vite dev proxy forwards `/api` requests to `http://localhost:5000`.
