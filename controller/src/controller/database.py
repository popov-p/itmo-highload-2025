from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://mongos:27017/iotdata"
client = AsyncIOMotorClient(MONGO_URI)
db = client.iotdata