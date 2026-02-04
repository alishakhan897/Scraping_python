from fastapi import FastAPI
from pydantic import BaseModel
from detailed_scraping import scrape_single_college
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Production mein ise apne frontend URL se replace karein
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"status": "StudyCups Python Scraper Running"}

@app.post("/scrape")
def scrape(req: ScrapeRequest):
    try:
        data = scrape_single_college(req.url)

        return {
            "success": True,
            "data": data   # ✅ PURE JSON
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
