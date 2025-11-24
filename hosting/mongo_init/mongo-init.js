print("Started adding the users.")
db = db.getSiblingDB("up-mate")
db.createUser({
    user:"user",
    pwd: process.env.MONGO_PASSWORD,
    roles: [{ role: "readWrite", db: "up-mate"}]
})
db.createCollection("messages")
print("End adding users.")
