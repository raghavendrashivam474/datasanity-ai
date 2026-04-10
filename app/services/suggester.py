import pandas as pd
from rapidfuzz import process, fuzz
from typing import List, Dict, Optional

# Extended medicine dictionary
MEDICINE_DICTIONARY = [
    "paracetamol", "crocin", "dolo", "calpol",
    "amoxicillin", "augmentin", "azithromycin", "zithromax",
    "ibuprofen", "brufen", "advil",
    "aspirin", "disprin",
    "metformin", "glucophage",
    "cetirizine", "zyrtec", "alerid",
    "omeprazole", "prilosec",
    "atorvastatin", "lipitor",
    "amlodipine", "norvasc",
    "losartan", "cozaar",
    "metoprolol", "betaloc",
    "ciprofloxacin", "cifran", "ciplox",
    "doxycycline", "doxt",
    "prednisone", "prednisolone",
    "gabapentin", "neurontin",
    "hydrochlorothiazide", "hctz",
    "lisinopril", "prinivil",
    "simvastatin", "zocor",
    "pantoprazole", "protonix",
    "ranitidine", "zantac",
    "diclofenac", "voltaren", "voveran",
    "naproxen", "naprosyn",
    "tramadol", "ultram",
    "montelukast", "singulair",
    "levothyroxine", "synthroid",
    "insulin", "humulin", "novolin",
    "glimepiride", "amaryl",
    "metronidazole", "flagyl",
    "clarithromycin", "biaxin",
    "salbutamol", "albuterol", "ventolin",
    "furosemide", "lasix",
    "warfarin", "coumadin",
    "clopidogrel", "plavix",
    "alprazolam", "xanax",
    "diazepam", "valium",
    "lorazepam", "ativan",
    "sertraline", "zoloft",
    "fluoxetine", "prozac",
    "amitriptyline", "elavil",
    "fexofenadine", "allegra",
    "loratadine", "claritin",
    "diphenhydramine", "benadryl",
    "chlorpheniramine", "chlor-trimeton"
]


def find_closest_match(
    value: str,
    dictionary: List[str],
    threshold: int = 75
) -> Optional[Dict]:
    """
    Find the closest match for a value in the dictionary.
    """
    if not value or not isinstance(value, str):
        return None

    value_clean = value.strip().lower()

    # Exact match — no fix needed
    if value_clean in dictionary:
        return None

    result = process.extractOne(
        value_clean,
        dictionary,
        scorer=fuzz.ratio,
        score_cutoff=threshold
    )

    if result:
        match, score, _ = result
        return {
            "suggested": str(match),
            "confidence": round(score / 100, 2),
            "method": "fuzzy_match"
        }

    return None


def run_typo_fixes(
    df: pd.DataFrame,
    logs: List[Dict]
) -> pd.DataFrame:
    """
    Check medicine name columns for typos.
    """
    name_columns = [
        col for col in df.columns
        if 'name' in col.lower()
        or 'medicine' in col.lower()
        or 'drug' in col.lower()
        or 'product' in col.lower()
    ]

    for col in name_columns:
        for idx in df.index:
            val = df.at[idx, col]

            if not isinstance(val, str) or pd.isna(val):
                continue

            match = find_closest_match(
                val, MEDICINE_DICTIONARY
            )

            if match:
                old_val = val
                df.at[idx, col] = match["suggested"]
                logs.append({
                    "row": int(idx + 2),
                    "column": str(col),
                    "old": str(old_val),
                    "new": str(match["suggested"]),
                    "confidence": str(match["confidence"]),
                    "action": "typo_fix",
                    "reason": f"Fuzzy matched to '{match['suggested']}' "
                              f"(confidence: {match['confidence']})"
                })

    return df