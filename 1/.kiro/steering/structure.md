# Project Structure

```
/
├── 启动.bat                  # Windows one-click launcher (root)
├── README.md
├── backend/
│   ├── app.py               # Flask app entry point — routes, auth, DB init
│   ├── models.py            # SQLAlchemy models: Category, Website, User
│   ├── config.py            # Config class (DB URI, secret keys via env vars)
│   ├── requirements.txt
│   ├── reset_data.py        # Utility to reset seed data
│   ├── test_db.py           # DB connection smoke test
│   ├── start.bat            # Backend-only launcher
│   └── instance/
│       └── navdb.db         # (legacy/unused SQLite file — MySQL is active DB)
└── frontend/
    ├── index.html           # Vite HTML entry
    ├── vite.config.js       # Vite config + /api proxy
    ├── package.json
    └── src/
        ├── main.js          # Vue app bootstrap
        ├── App.vue          # Root component: Navbar + Search + router outlet
        ├── views/
        │   └── Home.vue     # Fetches categories & websites, renders CategoryList
        └── components/
            ├── Navbar.vue
            ├── Search.vue
            ├── CategoryList.vue   # Renders one category + its WebsiteCards
            └── WebsiteCard.vue    # Single site tile
```

## Key Conventions

- All backend logic lives in `backend/app.py` (single-file Flask app — no blueprints).
- Models are defined in `backend/models.py` and imported into `app.py`.
- Frontend uses Vue SFCs with `<script setup>` and scoped styles where appropriate.
- API calls in the frontend always use relative paths (`/api/...`) — never hardcoded ports.
- No frontend router — the app is a single-page view (`Home.vue` rendered directly in `App.vue`).
- DB seed data (categories + websites) is initialized in `app.py` on startup using `force_init` flags.
