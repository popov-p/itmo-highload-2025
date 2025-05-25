from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://mongo:27017/iotdata"
client = AsyncIOMotorClient(MONGO_URI)
db = client.iotdata
data = db.data
instant = db.instant
ongoing = db.ongoing