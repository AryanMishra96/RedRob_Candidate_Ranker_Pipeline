from datetime import datetime


class CandidateValidator:

    def validate(self, candidate):

        profile = candidate["profile"]
        signals = candidate["redrob_signals"]

        # ---------------------------------------
        # 1. Signup Date <= Last Active
        # ---------------------------------------

        signup = datetime.strptime(
            signals["signup_date"], "%Y-%m-%d"
        )

        active = datetime.strptime(
            signals["last_active_date"], "%Y-%m-%d"
        )

        if signup > active:
            return False, "Signup After Last Active"

        # ---------------------------------------
        # 2. Salary Range
        # ---------------------------------------

        salary = signals["expected_salary_range_inr_lpa"]

        if salary["min"] > salary["max"]:
            return False, "Invalid Salary Range"

        # ---------------------------------------
        # 3. Expert Skill with Zero Duration
        # ---------------------------------------

        for skill in candidate["skills"]:

            if (
                skill["proficiency"] == "expert"
                and skill.get("duration_months", 0) == 0
            ):
                return False, "Expert Skill With Zero Duration"

        # ---------------------------------------
        # 4. Job Duration Validation
        # ---------------------------------------

        for job in candidate["career_history"]:

            start = datetime.strptime(
                job["start_date"], "%Y-%m-%d"
            )

            if job["is_current"] or job["end_date"] is None:
                end = datetime.today()
            else:
                end = datetime.strptime(
                    job["end_date"], "%Y-%m-%d"
                )

            actual_months = (
                (end.year - start.year) * 12
                + (end.month - start.month)
            )

            if abs(actual_months - job["duration_months"]) > 6:
                return False, "Job Duration Mismatch"

        # ---------------------------------------
        # 5. Graduation vs Experience
        # ---------------------------------------

        if candidate["education"]:

            graduation_year = max(
                edu["end_year"]
                for edu in candidate["education"]
            )

            max_possible_exp = datetime.today().year - graduation_year

            if (
                profile["years_of_experience"]
                > max_possible_exp + 3
            ):
                return False, "Experience Mismatch"

        return True, "Valid"