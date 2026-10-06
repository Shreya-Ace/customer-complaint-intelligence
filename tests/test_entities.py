from app.nlp.entities import extract_entities


text = """
I ordered a Samsung Galaxy phone from Amazon
on September 20 for $800. The package was supposed
to arrive in Jaipur.
"""


result = extract_entities(text)

print(result)