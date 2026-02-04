from pymongo import MongoClient
from bson import ObjectId

client = MongoClient(MONGO_URI)
db = client["studycups"]
collection = db["college_course_test"]

@app.post("/scrape")
async def scrape(data: dict):
    url = data["url"]
    job_id = data["jobId"]

    try:
        # 🔄 status = running
        collection.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": {"status": "running", "progress": 10}}
        )

        scraped = run_full_scraper(url)  # tumhara existing logic

        # ✅ FINAL WRITE BACK
        collection.update_one(
            {"_id": ObjectId(job_id)},
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
            {
                "$set": {
                    "status": "error",
                    "error": str(e)
                }
            }
        )
        return {"success": False, "error": str(e)}
