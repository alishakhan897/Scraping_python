from fastapi import FastAPI
from pydantic import BaseModel
from detailed_scraping import scrape_single_college

app = FastAPI()

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
            "data": data   # 🔑 THIS IS CRITICAL
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
