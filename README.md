# lambda-ai
Create APIs easily!

Setup guide:
1. Install Python 3
2. Optional: Create a python venv and activate it
3. In your terminal, install dependencies by running "pip install -r requirements.txt"
4. Install postgres. Then in your terminal, run the command "createdb lambdaai". If that doesn't work, run psql and create the database there.
5. Copy .env.example into a new file .env then change YOUR_NAME_HERE in POSTGRES_DB_URL to your postgres username.  
6. Start the backend. While in top-level directory lambda-ai, run "uvicorn lambda_ai.app:app"
7. Start the backend. While in UI top-level directory lambda_ui_v2 run "npm run serve"

Created by Adam Stecklov, 2023.
Use, modification, or licensing of this software is only with the author's permission.
