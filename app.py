from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os
from detailed_scraping import scrape_single_college

app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["studycups"]
collection = db["college_course_test"]

@app.post("/scrape")
async def scrape(payload: dict):
    url = payload.get("url")
    job_id = payload.get("jobId")

    if not url or not job_id:
        return {"success": False, "error": "url or jobId missing"}

    try:
        oid = ObjectId(job_id)

        collection.update_one(
            {"_id": oid},
            {"$set": {"status": "running", "progress": 10}}
        )

        # ✅ NOW Python knows this function
        scraped = scrape_single_college(url)

        collection.update_one(
            {"_id": oid},
            {
                "$set": {
                    **scraped,
                    "status": "completed",
                    "progress": 100,
                    "completedAt": datetime.utcnow()
                }
            }
        )

        return {"success": True}

    except Exception as e:
        collection.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": {"status": "error", "error": str(e)}}
        )
        return {"success": False, "error": str(e)}
