"""
AgneticAI Solution Catalog

This module contains the consulting knowledge base used by
Discovery, Research, Lead Scoring, Proposal Generation,
Email Generation, and future AI agents.

Priority Order

1. Recommend AgneticAI catalog services.
2. If no catalog service matches, recommend generic AI opportunities.
"""

CATALOG_VERSION = "1.0"

AI_SOLUTION_CATALOG = {

    "Manufacturing": {

        "id": "manufacturing",

        "name": "Manufacturing",

        "description": (
            "Industrial manufacturing, production, engineering, "
            "factory automation and industrial equipment."
        ),

        "keywords": [
            "manufacturing",
            "factory",
            "industrial",
            "production",
            "automation",
            "engineering",
            "machinery"
        ],

        "pain_points": [
            "Manual documentation",
            "Quality inspection",
            "Production planning",
            "Machine downtime",
            "Inventory optimization",
            "Quotation preparation",
            "Technical documentation"
        ],

        "services": [

            {
                "id": "proposal_generator",

                "name": "Proposal Generator",

                "category": "Document AI",

                "type": "catalog",

                "priority": "HIGH",

                "difficulty": "LOW",

                "roi": (
                    "Reduce proposal preparation time by "
                    "up to 80%."
                ),

                "target_personas": [
                    "Sales Manager",
                    "Business Development Manager"
                ],

                "deliverables": [
                    "Proposal Generator",
                    "Document Templates"
                ],

                "use_cases": [
                    "Sales proposal creation",
                    "Solution proposal drafting",
                    "Quotation support",
                    "Bid and RFP responses"
                ],

                "tags": [
                    "automation",
                    "llm",
                    "rag",
                    "document_ai"
                ],

                "estimated_duration_weeks": 2
            },

            {
                "id": "technical_documentation_assistant",

                "name": "Technical Documentation Assistant",

                "category": "Document AI",

                "type": "catalog",

                "priority": "HIGH",

                "difficulty": "LOW",

                "roi": (
                    "Standardize and accelerate creation of "
                    "technical manuals and documentation."
                ),

                "target_personas": [
                    "Technical Writer",
                    "Product Engineer"
                ],

                "deliverables": [
                    "Documentation Assistant",
                    "Standardized Templates"
                ],

                "use_cases": [
                    "User manual creation",
                    "Maintenance guide drafting",
                    "Standard operating procedures",
                    "Product specification documents"
                ],

                "tags": [
                    "automation",
                    "llm",
                    "rag",
                    "document_ai"
                ],

                "estimated_duration_weeks": 3
            },

            {
                "id": "predictive_maintenance",

                "name": "Predictive Maintenance",

                "category": "Industrial AI",

                "type": "catalog",

                "priority": "HIGH",

                "difficulty": "MEDIUM",

                "roi": (
                    "Reduce unplanned machine downtime and "
                    "maintenance costs."
                ),

                "target_personas": [
                    "Maintenance Manager",
                    "Plant Manager"
                ],

                "deliverables": [
                    "Predictive Models",
                    "Monitoring Dashboards"
                ],

                "use_cases": [
                    "Equipment failure prediction",
                    "Maintenance scheduling",
                    "Spare parts planning",
                    "Condition-based monitoring"
                ],

                "tags": [
                    "automation",
                    "timeseries",
                    "ml",
                    "industrial_ai"
                ],

                "estimated_duration_weeks": 6
            },

            {
                "id": "ai_quality_inspection",

                "name": "AI Quality Inspection",

                "category": "Computer Vision",

                "type": "catalog",

                "priority": "HIGH",

                "difficulty": "MEDIUM",

                "roi": (
                    "Improve defect detection accuracy and "
                    "reduce manual inspection effort."
                ),

                "target_personas": [
                    "Quality Manager",
                    "Production Manager"
                ],

                "deliverables": [
                    "Inspection Models",
                    "Integration Workflows"
                ],

                "use_cases": [
                    "Defect detection on production lines",
                    "Visual inspection automation",
                    "Surface defect analysis",
                    "Assembly verification"
                ],

                "tags": [
                    "automation",
                    "vision",
                    "ml",
                    "computer_vision"
                ],

                "estimated_duration_weeks": 5
            }
        ],

        "generic_opportunities": [
            "Digital Twin",
            "Demand Forecasting",
            "Computer Vision",
            "Supply Chain Optimization"
        ]
    },

    "Retail": {

        "id": "retail",

        "name": "Retail",

        "description": (
            "Physical and online retail, ecommerce, "
            "consumer shopping experiences and merchandising."
        ),

        "keywords": [
            "retail",
            "ecommerce",
            "shopping",
            "fashion",
            "store",
            "marketplace"
        ],

        "pain_points": [
            "Product descriptions",
            "Customer support",
            "Cart abandonment",
            "Marketing campaigns",
            "Customer engagement"
        ],

        "services": [

            {
                "id": "ai_product_description_generator",

                "name": "AI Product Description Generator",

                "category": "Document AI",

                "type": "catalog",

                "priority": "HIGH",

                "difficulty": "LOW",

                "roi": (
                    "Accelerate product listing creation and "
                    "improve content consistency."
                ),

                "target_personas": [
                    "Ecommerce Manager",
                    "Category Manager"
                ],

                "deliverables": [
                    "Description Generator",
                    "Copywriting Templates"
                ],

                "use_cases": [
                    "Catalog listing creation",
                    "SEO-friendly product copy",
                    "Multi-language descriptions",
                    "Bulk product onboarding"
                ],

                "tags": [
                    "automation",
                    "llm",
                    "rag",
                    "document_ai"
                ],

                "estimated_duration_weeks": 2
            },

            {
                "id": "ai_shopping_assistant",

                "name": "AI Shopping Assistant",

                "category": "Conversational AI",

                "type": "catalog",

                "priority": "HIGH",

                "difficulty": "MEDIUM",

                "roi": (
                    "Increase conversion rates and improve "
                    "customer experience through guided shopping."
                ),

                "target_personas": [
                    "Customer Experience Lead",
                    "Ecommerce Product Manager"
                ],

                "deliverables": [
                    "Shopping Assistant Bot",
                    "Integration Flows"
                ],

                "use_cases": [
                    "Customer Support",
                    "Lead Qualification",
                    "Product Recommendation",
                    "Order Tracking"
                ],

                "tags": [
                    "automation",
                    "llm",
                    "chatbot",
                    "rag"
                ],

                "estimated_duration_weeks": 4
            },

            {
                "id": "marketing_content_generator",

                "name": "Marketing Content Generator",

                "category": "Document AI",

                "type": "catalog",

                "priority": "MEDIUM",

                "difficulty": "LOW",

                "roi": (
                    "Reduce time spent on campaign content "
                    "creation and testing."
                ),

                "target_personas": [
                    "Marketing Manager",
                    "Social Media Manager"
                ],

                "deliverables": [
                    "Content Generator",
                    "Campaign Templates"
                ],

                "use_cases": [
                    "Email campaign content",
                    "Social media posts",
                    "Ad copy generation",
                    "A/B test variants"
                ],

                "tags": [
                    "automation",
                    "llm",
                    "rag",
                    "document_ai"
                ],

                "estimated_duration_weeks": 3
            }
        ],

        "generic_opportunities": [
            "Recommendation Engine",
            "Customer Segmentation",
            "Visual Search"
        ]
    }
}