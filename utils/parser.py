def priceParse(query: str):
    query = query.lower()
    query = query.replace(" ", "_")
    return query