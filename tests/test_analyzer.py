from app.llm.analyzer import ComplaintAnalyzer


complaint = """
I ordered a laptop 12 days ago and it was supposed to
arrive last week. The payment was already deducted from
my account. I contacted customer support twice but
nobody responded. This is extremely frustrating.
"""


analyzer = ComplaintAnalyzer()

result = analyzer.analyze(complaint)

print("\n========== COMPLAINT ANALYSIS ==========\n")

print(result.model_dump_json(indent=2))