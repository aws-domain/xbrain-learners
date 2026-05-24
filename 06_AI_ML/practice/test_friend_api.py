"""
Test friend's n8n API against question files.
Usage:
    python test_friend_api.py             # L1
    python test_friend_api.py --level 2   # L2
    python test_friend_api.py --level 3   # L3
"""
import json
import re
import sys
import time
import requests
from pathlib import Path

API_URL = "http://drive.duckq1linux.id.vn/webhook/3a1ded89-75d5-41d3-8e0d-9b0df7632422?brid=YWdncwGE6hFBvaRgR_FkZHT1Pjog"
QUESTIONS_DIR = Path(__file__).parent.parent / "questions" / "student"
SKIP_WORDS = {"the","a","an","is","are","was","were","in","on","at","to","for","of","and","or","its","that","both","must","just","also","than","from","with","but"}


def ask(question: str) -> str:
    try:
        response = requests.post(API_URL, json={"chatInput": question}, timeout=30)
        data = response.json()
        return data.get("output", data.get("answer", str(data)))
    except Exception as e:
        return f"ERROR: {e}"


def extract_numbers(text: str):
    # Normalize: remove commas, dollar signs
    text = text.replace(",", "").replace("$", "")
    return [float(n) for n in re.findall(r"\d+\.?\d*", text)]


def numbers_match(expected: str, actual: str, tolerance: float = 0.10) -> bool:
    exp_nums = extract_numbers(expected)
    if not exp_nums:
        return True
    act_nums = extract_numbers(actual)
    if not act_nums:
        return False
    matched = 0
    for en in exp_nums:
        for an in act_nums:
            if en == 0:
                if an == 0:
                    matched += 1
                    break
            elif abs(an - en) / en <= tolerance:
                matched += 1
                break
    return matched >= len(exp_nums) * 0.8


def keywords_match(source_text: str, actual: str, threshold: float = 0.7) -> bool:
    actual_norm = actual.lower().replace(",", "")
    words = [w.strip(".,!?()$%") for w in source_text.lower().split()
             if len(w) > 1 and w.strip(".,!?()$%") not in SKIP_WORDS]
    if not words:
        return True
    matches = sum(1 for w in words if w in actual_norm)
    return matches / len(words) >= threshold


def check_l1(q: dict, actual: str) -> bool:
    expected = q["expected_answer"]
    actual_norm = actual.lower().replace(",", "").strip()
    expected_norm = expected.lower().replace(",", "").strip()

    if expected_norm in actual_norm or actual_norm in expected_norm:
        return True
    return numbers_match(expected, actual) and keywords_match(expected, actual)


def check_l2(q: dict, actual: str) -> bool:
    # L2: dùng grading_notes làm tiêu chí chính (chứa "Must X, Y, Z")
    grading = q.get("grading_notes", "")
    expected = q["expected_answer"]

    # Check grading_notes keywords (threshold thấp vì câu dài)
    grading_ok = keywords_match(grading, actual, threshold=0.5)
    # Check expected_answer keywords
    expected_ok = keywords_match(expected, actual, threshold=0.5)

    return grading_ok and expected_ok


def check_l3(q: dict, actual: str) -> bool:
    expected = q["expected_answer"]
    grading = q.get("grading_notes", "")

    # Số liệu phải khớp (±10% cho live data)
    if not numbers_match(expected, actual, tolerance=0.10):
        return False

    # Check grading notes keywords
    return keywords_match(grading, actual, threshold=0.5)


def run_level(level: int):
    file_map = {1: "L1_questions.json", 2: "L2_questions.json", 3: "L3_questions.json"}
    check_fn = {1: check_l1, 2: check_l2, 3: check_l3}

    path = QUESTIONS_DIR / file_map[level]
    questions = json.loads(path.read_text())["questions"]

    print(f"\n{'='*60}")
    print(f"  Testing L{level} — {len(questions)} questions")
    print(f"{'='*60}\n")

    passed = 0
    for i, q in enumerate(questions, 1):
        print(f"[{i}/{len(questions)}] {q['id']}: {q['question']}")
        actual = ask(q["question"])
        ok = check_fn[level](q, actual)

        if ok:
            print(f"  ✓ PASS")
            passed += 1
        else:
            print(f"  ✗ FAIL")
            print(f"    Expected: {q['expected_answer']}")
            print(f"    Got:      {actual[:300]}")
        print()
        time.sleep(0.5)

    print(f"{'='*60}")
    print(f"RESULTS: {passed}/{len(questions)} passed ({passed/len(questions)*100:.1f}%)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    level = 1
    if "--level" in sys.argv:
        level = int(sys.argv[sys.argv.index("--level") + 1])
    run_level(level)
