# Nebula - ULTRAMAN Card Game Collection App API

#### Alpha 111625

## To run

### API

You need Python 3.11+, and what is listed in requirements.txt

`
pip install -r requirements.txt
`

To launch the API, from project directory

`
uvicorn nebula_api:app --reload
`

This runs the API on local port 8000

🔹 http://127.0.0.1:8000/docs → interactive Swagger UI

🔹 /cards → list cards

🔹 /cards?rarity=R → filter by rarity

🔹 /search?q=Tiga → search by name, effect, flavor text

🔹 /cards?feature=Kaiju → get Kaiju cards

🔹 /stats → see totals and distributions
