import json
import csv
from openpyxl import Workbook
from validator import CandidateValidator

from filter_s import HardFilter

def load_candidates(file_path):
    candidates = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line:
                candidates.append(json.loads(line))

    return candidates


def generate_reason(features):

    reasons = []

    if features["title_match"]:
        reasons.append("Relevant AI/ML Role")

    if features["has_llm"]:
        reasons.append("LLM")

    if features["has_nlp"]:
        reasons.append("NLP")

    if features["semantic_search"]:
        reasons.append("Semantic Search")

    if features["has_search"]:
        reasons.append("Retrieval/Search")

    if features["production_ml"]:
        reasons.append("Production ML")

    if features["advanced_ai_skill_count"] >= 3:
        reasons.append("Strong AI Stack")

    reasons.append(f'{features["years_exp"]:.1f} Years Experience')

    return ", ".join(reasons)


def main():

    # -------------------------------
    # Load Dataset
    # -------------------------------

    candidates = load_candidates("candidates.jsonl")

    print(f"\nLoaded {len(candidates)} candidates.")

    # -------------------------------
    # Hard Filter
    # -------------------------------
    validator = CandidateValidator()
    valid_candidates = []
    invalid_candidates = []
    for candidate in candidates:

        ok, reason = validator.validate(candidate)

        if ok:
            valid_candidates.append(candidate)
        else:
            candidate["reject_reason"] = reason
            invalid_candidates.append(candidate)

    print(f"Passed Validation : {len(valid_candidates)}")
    print(f"Failed Validation : {len(invalid_candidates)}")
    
    
    
    
    
    hf = HardFilter()

    qualified, rejected = hf.filter_dataset(valid_candidates)

    print(f"Qualified : {len(qualified)}")
    print(f"Rejected  : {len(rejected)}")

    # -------------------------------
    # Candidate Scoring
    # -------------------------------

    scored = []

    for candidate in qualified:

        features = hf.extractor.extract(candidate)

        score = hf.scorer.score(candidate, features)

        reason = generate_reason(features)

        scored.append({
            "candidate_id": candidate["candidate_id"],
            "score": score,
            "reason": reason,
            "candidate": candidate
        })

    # -------------------------------
    # Sort
    # -------------------------------

    

    # -------------------------------
    # Top 100
    # -------------------------------
    max_score = max(item["score"] for item in scored)
    min_score = min(item["score"] for item in scored)

    for item in scored:

     if max_score == min_score:
         item["normalized_score"] = 1.0
     else:
         item["normalized_score"] = round(
             (item["score"] - min_score) /
             (max_score - min_score),
             4
         )
    scored.sort(
    key=lambda x: (-round(x["normalized_score"], 4), x["candidate_id"])
)
    top_candidates = scored[:100]

    print(f"\nTop Candidates : {len(top_candidates)}")

    # -------------------------------
    # Save JSONL
    # -------------------------------

    with open(
        "top_candidates.jsonl",
        "w",
        encoding="utf-8"
    ) as f:

        for item in top_candidates:

            f.write(json.dumps(item["candidate"]))

            f.write("\n")

    print("Saved top_candidates.jsonl")

    # -------------------------------
    # Save CSV
    # -------------------------------

    with open(
        "DevFusion.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "candidate_id",
            "rank", 
            "score",
            "reasoning"
        ])

        for rank, item in enumerate(top_candidates, start=1):

            writer.writerow([
                item["candidate_id"],
                rank,  
                f"{item["normalized_score"]:.4f}",
                item["reason"]
            ])

    print("Saved DevFusion.csv")

    # -------------------------------
    # Save Excel
    # -------------------------------

    wb = Workbook()

    ws = wb.active

    ws.title = "Top Candidates"

    ws.append([
        "candidate_id",
        "rank",
        "score",
        "reasoning"
    ])

    for rank, item in enumerate(top_candidates, start=1):

        ws.append([
            item["candidate_id"],
            rank,
            f"{item["normalized_score"]:.4f}",
            item["reason"]
        ])

    wb.save("DevFusion.xlsx")

    print("Saved DevFusion.xlsx")

    # -------------------------------
    # Top 10 Preview
    # -------------------------------

    print("\nTop 10 Candidates\n")

    
    for rank, item in enumerate(top_candidates[:10], start=1):
     print(
        rank,
        item["candidate_id"],
        f"{item['normalized_score']:.4f}"
    )
#for rank, item in enumerate(top_candidates[:10], start=1):

     #   print(
      #      f"{rank:2d}. "
       #     f"{item['candidate_id']} | "
        #     f"{item['score']:.4f}"
        #)


if __name__ == "__main__":
    main()