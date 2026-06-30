import re


class FeatureExtractor:

    CONSULTING_COMPANIES = {
        "tcs", "infosys", "wipro", "accenture",
        "capgemini", "mindtree", "cognizant",
        "hcl", "tech mahindra", "ltimindtree"
    }

    RESEARCH_WORDS = {
        "research",
        "research scientist",
        "publication",
        "published",
        "conference",
        "journal",
        "phd",
        "thesis",
        "paper"
    }

    NLP_WORDS = {
        "nlp",
        "bert",
        "transformer",
        "tokenization",
        "retrieval",
        "rag",
        "embedding",
        "vector database",
        "llm",
        "langchain",
        "llamaindex"
    }

    SEARCH_WORDS = {
        "search",
        "ranking",
        "recommendation",
        "retrieval",
        "matching",
        "semantic search"
    }

    CV_WORDS = {
        "computer vision",
        "opencv",
        "yolo",
        "segmentation",
        "detection",
        "image classification"
    }

    TITLE_WORDS = {
        "machine learning engineer",
        "ml engineer",
        "ai engineer",
        "applied ml engineer",
        "applied ml",
        "search engineer",
        "recommendation systems engineer",
        "recommendation engineer",
        "data scientist"
    }

    ADVANCED_AI_SKILLS = {
        "sentence transformers",
        "sentence-transformers",
        "pinecone",
        "qdrant",
        "weaviate",
        "milvus",
        "faiss",
        "vector search",
        "semantic search",
        "information retrieval",
        "learning to rank",
        "elasticsearch",
        "rag",
        "llm",
        "lora",
        "qlora"
    }

    PREFERRED_LOCATIONS = {
        "noida",
        "delhi",
        "gurgaon",
        "gurugram",
        "pune",
        "bangalore",
        "bengaluru"
    }

    def extract(self, candidate):

        profile = candidate["profile"]
        history = candidate["career_history"]
        skills = candidate["skills"]

        text = " ".join([
            profile.get("headline", ""),
            profile.get("summary", ""),
            *[job.get("title", "") for job in history],
            *[job.get("description", "") for job in history],
            *[skill.get("name", "") for skill in skills]
        ]).lower()

        features = {}

        # ---------------------------------------------------
        # Experience
        # ---------------------------------------------------

        features["years_exp"] = profile.get("years_of_experience", 0)

        # ---------------------------------------------------
        # Consulting Background
        # ---------------------------------------------------

        consulting = 0

        for job in history:
            company = job.get("company", "").lower()

            if any(c in company for c in self.CONSULTING_COMPANIES):
                consulting += 1

        features["consulting_ratio"] = (
            consulting / len(history)
            if history else 0
        )

        # ---------------------------------------------------
        # Research
        # ---------------------------------------------------

        features["is_research"] = any(
            word in text
            for word in self.RESEARCH_WORDS
        )

        # ---------------------------------------------------
        # NLP
        # ---------------------------------------------------

        features["has_nlp"] = any(
            word in text
            for word in self.NLP_WORDS
        )

        # ---------------------------------------------------
        # Search / Ranking
        # ---------------------------------------------------

        features["has_search"] = any(
            word in text
            for word in self.SEARCH_WORDS
        )

        # ---------------------------------------------------
        # Computer Vision
        # ---------------------------------------------------

        features["has_cv"] = any(
            word in text
            for word in self.CV_WORDS
        )

        # ---------------------------------------------------
        # Production ML
        # ---------------------------------------------------

        production_keywords = [
            "production",
            "deployed",
            "serving",
            "pipeline",
            "inference"
        ]

        features["production_ml"] = any(
            k in text
            for k in production_keywords
        )

        # ---------------------------------------------------
        # LLM
        # ---------------------------------------------------

        features["has_llm"] = any(
            word in text
            for word in [
                "llm",
                "gpt",
                "rag",
                "langchain",
                "llama",
                "fine tuning",
                "fine-tuning"
            ]
        )

        # ---------------------------------------------------
        # Basic AI Skill Count
        # ---------------------------------------------------

        ai_skills = {
            "python",
            "pytorch",
            "tensorflow",
            "sklearn",
            "huggingface",
            "llm",
            "rag",
            "bert",
            "transformer"
        }

        features["ai_skill_count"] = sum(
            skill.get("name", "").lower() in ai_skills
            for skill in skills
        )

        # ---------------------------------------------------
        # Advanced AI Skill Count
        # ---------------------------------------------------

        features["advanced_ai_skill_count"] = sum(
            skill.get("name", "").lower() in self.ADVANCED_AI_SKILLS
            for skill in skills
        )

        # ---------------------------------------------------
        # Job Title Match
        # ---------------------------------------------------

        features["title_match"] = any(
            word in text
            for word in self.TITLE_WORDS
        )

        # ---------------------------------------------------
        # Semantic Search Experience
        # ---------------------------------------------------

        features["semantic_search"] = any(
            word in text
            for word in self.ADVANCED_AI_SKILLS
        )

        # ---------------------------------------------------
        # Notice Period
        # ---------------------------------------------------

        signals = candidate["redrob_signals"]
        notice = signals["notice_period_days"]

        
        features["notice_days"] = notice

        features["response_rate"] = signals["recruiter_response_rate"]

        features["open_to_work"] = signals["open_to_work_flag"]

        features["relocation"] = signals["willing_to_relocate"]

        # ---------------------------------------------------
        # Location
        # ---------------------------------------------------

        location = profile.get("location", "").lower()

        features["preferred_location"] = any(
            city in location
            for city in self.PREFERRED_LOCATIONS
        )


        # ---------------------------------------------------
        # Recruiter Behaviour
        # ---------------------------------------------------

        return features