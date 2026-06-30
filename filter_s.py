from filter_f import FeatureExtractor
from candidate_scorer import CandidateScorer


class HardFilter:

    NON_TECH = {
        "marketing manager",
        "sales executive",
        "hr manager",
        "accountant"
    }

    def __init__(self):

        self.extractor = FeatureExtractor()
        self.scorer = CandidateScorer()

    def filter(self, candidate):

        features = self.extractor.extract(candidate)

        profile = candidate.get("profile", {})
        title = profile.get("current_title", "").lower()

        # -------------------------------
        # Rule 1 : Experience
        # -------------------------------

        exp = features["years_exp"]

        if exp < 2:
            return False, "Too Little Experience"

        if exp > 15:
            return False, "Overqualified"

        # -------------------------------
        # Rule 2 : Non-Tech
        # -------------------------------

        if title in self.NON_TECH:
            return False, "Non Technical"

        # -------------------------------
        # Rule 3 : Consulting Only
        # -------------------------------

        if features["consulting_ratio"] >= 0.9:
            return False, "Consulting Only"

        # -------------------------------
        # Rule 4 : Research Only
        # -------------------------------

        if (
            features["is_research"]
            and
            not features["production_ml"]
        ):
            return False, "Research Only"

        # -------------------------------
        # Rule 5 : Pure Computer Vision
        # -------------------------------

        if (
            features["has_cv"]
            and
            not features["has_nlp"]
            and
            not features["has_llm"]
        ):
            return False, "Computer Vision Only"

        # -------------------------------
        # Rule 6 : Notice Period
        # -------------------------------

        if features["notice_days"] > 180:
            return False, "Very Long Notice"

        # -------------------------------
        # Rule 7 : Final Score
        # -------------------------------

        score = self.scorer.score(candidate, features)

        if score < 15:
            return False, "Low Score"

        return True, "Qualified"

    def filter_dataset(self, candidates):

        qualified = []
        rejected = []
        reason_count = {}

        for candidate in candidates:

            try:

                passed, reason = self.filter(candidate)

                if passed:
                    qualified.append(candidate)

                else:
                    reason_count[reason] = reason_count.get(reason, 0) + 1
                    candidate["reject_reason"] = reason
                    rejected.append(candidate)

            except Exception as e:

                reason = "Invalid Profile"

                reason_count[reason] = reason_count.get(reason, 0) + 1

                candidate["reject_reason"] = str(e)

                rejected.append(candidate)

        print("\nReject Summary")
        print("-" * 35)

        for reason, count in sorted(reason_count.items(), key=lambda x: -x[1]):
            print(f"{reason:<25} {count}")

        return qualified, rejected