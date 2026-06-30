# candidate_scorer.py

class CandidateScorer:

    def score(self, candidate, features):

        score = 0.0

        signals = candidate["redrob_signals"]

        # --------------------------------------------------
        # Experience (15)
        # --------------------------------------------------

        exp = features["years_exp"]

        if 5 <= exp <= 9:
            score += 15
        elif 4 <= exp < 5 or 9 < exp <= 11:
            score += 12
        elif 2 <= exp < 4:
            score += 8
        else:
            score += 4

        # --------------------------------------------------
        # AI Skills (15)
        # --------------------------------------------------

        score += min(features["ai_skill_count"], 5) * 3

        # --------------------------------------------------
        # Advanced AI Skills (20)
        # --------------------------------------------------

        score += min(features["advanced_ai_skill_count"], 5) * 4

        # --------------------------------------------------
        # Job Title Match (10)
        # --------------------------------------------------

        if features["title_match"]:
            score += 10

        # --------------------------------------------------
        # NLP
        # --------------------------------------------------

        if features["has_nlp"]:
            score += 8

        # --------------------------------------------------
        # LLM
        # --------------------------------------------------

        if features["has_llm"]:
            score += 10

        # --------------------------------------------------
        # Search / Ranking
        # --------------------------------------------------

        if features["has_search"]:
            score += 15

        # --------------------------------------------------
        # Semantic Search
        # --------------------------------------------------

        if features["semantic_search"]:
            score += 10

        # --------------------------------------------------
        # Production ML
        # --------------------------------------------------

        if features["production_ml"]:
            score += 8

        # --------------------------------------------------
        # Consulting Penalty
        # --------------------------------------------------

        ratio = features["consulting_ratio"]

        if ratio > 0.8:
            score -= 10
        elif ratio > 0.5:
            score -= 6

        # --------------------------------------------------
        # Research Penalty
        # --------------------------------------------------

        if features["is_research"]:
            score -= 6

        # --------------------------------------------------
        # Computer Vision Only
        # --------------------------------------------------

        if features["has_cv"] and not features["has_nlp"]:
            score -= 5

        # ==================================================
        # Platform / Redrob Signals
        # ==================================================

        if features["open_to_work"]:
            score += 5

        score += signals["profile_completeness_score"] / 20

        score += features["response_rate"] * 8

        score += signals["interview_completion_rate"] * 8

        score += min(signals["saved_by_recruiters_30d"], 10)

        score += min(
            signals["search_appearance_30d"] / 100,
            5
        )

        github = signals["github_activity_score"]

        if github != -1:
            score += github / 10

        assessments = signals["skill_assessment_scores"]

        if assessments:
            score += (
                sum(assessments.values())
                / len(assessments)
            ) / 10

        # --------------------------------------------------
        # Notice Period
        # --------------------------------------------------

        notice = features["notice_days"]

        if notice <= 30:
         score += 8
        elif notice <= 60:
         score += 6
        elif notice <= 90:
         score += 3
        else:
         score += 1
        # --------------------------------------------------
        # Location
        # --------------------------------------------------

        if features["preferred_location"]:
            score += 5
        elif features["relocation"]:
            score += 3

        # --------------------------------------------------
        # Flexible Work Mode
        # --------------------------------------------------

        if signals["preferred_work_mode"] == "flexible":
            score += 2

        # --------------------------------------------------
        # Verified Profile
        # --------------------------------------------------

        if signals["verified_email"]:
            score += 1

        if signals["verified_phone"]:
            score += 1

        if signals["linkedin_connected"]:
            score += 1

        return round(score, 4)