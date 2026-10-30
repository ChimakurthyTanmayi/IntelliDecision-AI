"""
Decision Templates for IntelliDecision AI
Provides pre-configured scenario templates across various domains for testing and rapid analysis.
"""

from typing import Dict, Any, List

DECISION_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "Pursue MS in US": {
        "title": "Pursuing MS in Computer Science in the US vs. Continuing Career",
        "category": "Education & Career",
        "description": "I have 3 years of experience as a Software Engineer in India ($25k salary). I am evaluating whether to pursue a Master's in Computer Science in the US ($70k tuition + living costs, taking an education loan) or continue working, upskilling, and looking for remote US roles.",
        "options": ["Pursue MS in US with Loan", "Continue Working & Pursue Remote US Jobs", "Defer Admission by 1 Year & Save Capital"]
    },
    "Career Switch": {
        "title": "Switching Jobs: AI Startup Lead vs. Big Tech Manager",
        "category": "Career & Professional",
        "description": "I have two job offers: Offer A is a Lead AI Engineer at a fast-growing Series A AI startup ($160k + 1.2% equity). Offer B is Engineering Manager at Big Tech ($220k total compensation, high stability). I am unsure which best aligns with my 5-year goals.",
        "options": ["Join AI Startup as Lead Engineer", "Join Big Tech as Engineering Manager", "Stay in Current Role & Negotiate"]
    },
    "Laptop Purchase": {
        "title": "Choosing Tech Equipment: MacBook Pro M3 vs. High-End Windows Laptop",
        "category": "Tech Purchase",
        "description": "I am a software developer and content creator needing a new primary machine ($2,500 budget). I am deciding between a MacBook Pro 16-inch (M3 Pro, 36GB RAM) and a Dell XPS 15 (i9, RTX 4070, 32GB RAM). Key factors are battery life, unix terminal compatibility, and video editing performance.",
        "options": ["Buy MacBook Pro 16 M3 Pro", "Buy Dell XPS 15 RTX 4070", "Buy Custom Desktop + Air 15-inch"]
    },
    "Start a Business": {
        "title": "Starting a B2B SaaS Startup vs. Niche Consulting Agency",
        "category": "Business Strategy",
        "description": "I have $50,000 in seed savings and 8 years of engineering experience. I want to decide whether to launch a self-funded AI workflow SaaS product or start an AI & Data Engineering consultancy that generates immediate cash flow.",
        "options": ["Launch Self-Funded SaaS Product", "Start AI Consulting Agency", "Hybrid Consulting to Fund SaaS"]
    },
    "Stock vs. Mutual Funds": {
        "title": "Investing $50k Capital: High-Growth Stocks vs. Broad Mutual Funds / ETFs",
        "category": "Financial Investment",
        "description": "I have $50,000 available to invest for a 5-10 year horizon. I am torn between allocating 100% to low-cost Index Funds / Broad Mutual Funds or building a concentrated portfolio of high-growth technology stocks.",
        "options": ["100% Index / Mutual Fund Allocation", "Concentrated Tech Growth Stock Portfolio", "70/30 Index & Tech Stock Split"]
    }
}
