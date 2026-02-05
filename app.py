from fastapi import FastAPI, BackgroundTasks
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor
from detailed_scraping import scrape_single_college

app = FastAPI()

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client["studycups"]
collection = db["college_course_test"]

# Increase workers slightly to handle more than one task if needed
executor = ThreadPoolExecutor(max_workers=4)

def run_scraping(job_id: str, url: str):
    """Worker function that runs in the background"""
    oid = ObjectId(job_id)
    try:
        # Step 1: Running
        collection.update_one({"_id": oid}, {"$set": {"status": "running", "progress": 20}})
        
        # Step 2: Scrape (Blocking call handled by ThreadPool)
        scraped_data = scrape_single_college(url)
        
        # Step 3: Success
        collection.update_one(
            {"_id": oid},
            {"$set": {
                **scraped_data,
                "status": "completed",
                "progress": 100,
                "completedAt": datetime.utcnow()
            }}
        )
    except Exception as e:
        collection.update_one(
            {"_id": oid},
            {"$set": {"status": "error", "error": str(e), "progress": 0}}
        )

@app.post("/scrape")
async def scrape(payload: dict, background_tasks: BackgroundTasks):
    url = payload.get("url")
    job_id = payload.get("jobId")

    if not url or not job_id:
        return {"success": False, "error": "url or jobId missing"}

    # Add task to background - FastAPI finishes the request IMMEDIATELY
    # while run_scraping keeps working on the server.
    background_tasks.add_task(run_scraping, job_id, url)

    return {"success": True, "message": "Scraping started in background"}