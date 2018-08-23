from mongo_mapper.core.query import Query

print(Query.eq("hotel_code", "%1%"))
print(Query.eq("hotel_code", "1%"))
print(Query.eq("hotel_code", "%1"))

print(Query.add_and(Query.eq("hotel_code", "%100%"), Query.gt("value", 1000), Query.ne("category", "5*")))


print(Query.eq("enabled", False))

print(Query.eq("number", 0))

print(Query.eq("number", 0.0))
