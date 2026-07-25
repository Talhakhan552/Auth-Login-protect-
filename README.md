# FlyRank Auth API

A secure FastAPI backend that handles user authentication — sign up, log in, log out — using **Supabase Auth** as the Identity Provider. Issued JWTs are verified on protected routes via a reusable dependency, and the whole flow is documented in Swagger UI with bearer authentication.

Built for FlyRank Internship · Backend Track · Week 2 · Assignment A4.

## What this project does

- Registers and authenticates users through Supabase Auth (no passwords are ever hashed or stored by this server — Supabase handles that).
- Issues and verifies JSON Web Tokens (JWTs) on every request to a protected route.
- Guards protected endpoints with a single reusable dependency (`get_current_user`), applied to more than one route.
- Documents every endpoint in Swagger UI at `/docs`, with a bearer-token "Authorize" flow.

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2. Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up environment variables
Copy the example file and fill in your own Supabase project values:
```bash
cp .env.example .env
```

`.env` should contain:
```
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_anon_key
PORT=8000
```

Get these from your [Supabase Dashboard](https://supabase.com) → **Project Settings → API** (use the **anon** key, never the `service_role` key here).

> For this project's Supabase instance, "Confirm email" is turned off under **Authentication → Sign In / Providers → Email**, so a fresh signup can log in immediately without clicking a confirmation link.

## Run the project

```bash
uvicorn main:app --reload --port 8000
```

Server starts at `http://localhost:8000`. Interactive Swagger docs are available at `http://localhost:8000/docs`.

## API reference

| Route | Method | Auth required | Description |
|---|---|---|---|
| `/auth/signup` | POST | No | Create a new user account |
| `/auth/login` | POST | No | Authenticate and receive a JWT |
| `/auth/logout` | POST | Yes (Bearer) | End the current session |
| `/protected/profile` | GET | Yes (Bearer) | Read the logged-in user's private profile |
| `/protected/dashboard` | GET | Yes (Bearer) | Second protected route reusing the same auth guard |
| `/public/info` | GET | No | Open, public data |

### Status codes used

| Code | Meaning |
|---|---|
| `201` | User created (signup) |
| `200` | Successful login / read |
| `204` | Logout succeeded, no content returned |
| `400` | Missing email or password |
| `401` | Missing, malformed, invalid, or expired token / bad login credentials |

## Example requests

**Sign up**
```bash
curl -i -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"yourpassword"}'
```

**Log in**
```bash
curl -i -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"yourpassword"}'
```

**Call a protected route**
```bash
curl -i http://localhost:8000/protected/profile \
  -H "Authorization: Bearer <your_access_token>"
```

## Swagger UI

Visit `http://localhost:8000/docs`, click **Authorize**, paste your access token, and use **Try it out** on any protected route directly from the browser.

![Swagger UI with Authorize padlock](Screenshot)

*(Replace the image above with your own screenshot showing the lock icons and a successful authorized request.)*

## Project structure

```
.
├── main.py              # FastAPI app and route definitions
├── auth.py               # Reusable auth dependency (token verification)
├── supabase_client.py    # Supabase client initialization
├── requirements.txt
├── .env.example
└── README.md
```

## Security notes

- No password hashing or JWT signing is implemented in this codebase — Supabase handles both.
- Only the Supabase **anon** key is used server-side; the `service_role` key is never referenced.
- `.env` is git-ignored and was never committed to this repository.