from functools import lru_cache
from typing import Dict, List


@lru_cache(maxsize=1)
def get_nlp():
    import spacy

    return spacy.load("en_core_web_sm")


def extract_entities(text: str) -> Dict[str, List[str]]:
    """
    Extracts basic named entities using spaCy.

    These are mapped into our project-level entity categories.
    """

    nlp = get_nlp()
    doc = nlp(text)

    entities = {
        "product": [],
        "order_id": [],
        "date": [],
        "amount": [],
        "location": [],
        "organization": [],
        "duration": []
    }

    for ent in doc.ents:

        if ent.label_ == "DATE":
            entities["date"].append(ent.text)

        elif ent.label_ == "MONEY":
            entities["amount"].append(ent.text)

        elif ent.label_ in {"GPE", "LOC"}:
            entities["location"].append(ent.text)

        elif ent.label_ == "ORG":
            entities["organization"].append(ent.text)

    return entities