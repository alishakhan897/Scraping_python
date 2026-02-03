from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"status": "StudyCups Python Scraper Running"}

@app.post("/scrape")
def scrape(req: ScrapeRequest):
    url = req.url

    # 🔹 abhi sirf test response
    return {
        "success": True,
        "message": "URL received successfully",
        "url": url
    }
