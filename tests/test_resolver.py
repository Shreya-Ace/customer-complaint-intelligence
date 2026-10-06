from app.llm.analyzer import ComplaintAnalyzer
from app.llm.resolver import ResolutionSupportGenerator


complaint = """
I ordered a laptop 12 days ago and it was supposed to
arrive last week. The payment was already deducted from
my account. I contacted customer support twice but
nobody responded. This is extremely frustrating.
"""


# ==========================================
# COMPONENT 1 & 2
# Complaint Understanding + Information Extraction
# ==========================================

analyzer = ComplaintAnalyzer()

analysis = analyzer.analyze(complaint)

print("\n========== COMPLAINT ANALYSIS ==========\n")

print(
    analysis.model_dump_json(
        indent=2
    )
)


# ==========================================
# COMPONENT 3
# Resolution Support
# ==========================================

resolver = ResolutionSupportGenerator()

resolution = resolver.generate(
    complaint=complaint,
    analysis=analysis
)

print("\n========== RESOLUTION SUPPORT ==========\n")

print(
    resolution.model_dump_json(
        indent=2
    )
)