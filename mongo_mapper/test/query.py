from mongo_mapper.core.query import Query

print(Query.eq("hotel_code", "%1%"))
print(Query.eq("hotel_code", "1%"))
print(Query.eq("hotel_code", "%1"))

print(Query.add_and(Query.eq("hotel_code", "H1"), Query.gt("value", 1000), Query.ne("category", "5*")))

