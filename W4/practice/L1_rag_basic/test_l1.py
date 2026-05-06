"""
Test L1 Questions - Automated testing with expected answers
"""
import json
from rag_pipeline import RAGPipeline
from pathlib import Path


def load_l1_questions():
    """
    Load L1 questions from questions/student/L1_questions.json

    ❓ PRACTICE QUESTION 1:
    Mở file L1_questions.json và đọc structure.
    Mỗi question có những fields gì?
    Field nào quan trọng nhất để verify answer?
    """
    questions_path = Path(__file__).parent.parent.parent / "questions" / "student" / "L1_questions.json"

    with open(questions_path, 'r') as f:
        data = json.load(f)

    return data['questions']


def check_answer(question_id: str, expected: str, actual: str, grading_notes: str) -> bool:
    """
    Check if actual answer matches expected answer.

    This is a simple keyword-based check. In production, you'd use:
    - Semantic similarity (embeddings)
    - LLM-as-judge
    - Exact string matching for numbers/dates

    ❓ PRACTICE QUESTION 2:
    Hàm này chỉ check keyword matching (case-insensitive).
    Nếu expected = "1000 requests per minute" nhưng actual = "1000 rpm",
    test sẽ pass hay fail? Làm thế nào để improve?
    """
    import re

    # Normalize: lowercase, remove commas (e.g. 1,000 → 1000), strip punctuation
    expected_norm = expected.lower().replace(',', '').strip()
    actual_norm = actual.lower().replace(',', '').strip().rstrip('.')

    # Direct containment check: either answer contains expected or vice versa
    if expected_norm in actual_norm or actual_norm in expected_norm:
        return True

    # Keyword-based fallback
    numbers = re.findall(r'\d+', expected_norm)
    skip_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or'}
    words = expected_norm.split()
    important_words = [w.strip('.,!?()') for w in words if w not in skip_words and len(w) > 1]
    key_terms = numbers + important_words[:5]

    if not key_terms:
        return True

    matches = sum(1 for term in key_terms if term in actual_norm)
    return matches / len(key_terms) >= 0.7


def run_tests(debug: bool = False):
    """
    Run all L1 test questions.

    ❓ PRACTICE QUESTION 3:
    Chạy test với debug=True và debug=False.
    Khi nào nên dùng debug mode?
    """
    print("\n" + "="*60)
    print("  Testing L1 Questions - Single-Fact Retrieval")
    print("="*60 + "\n")

    # Load questions
    questions = load_l1_questions()
    print(f"Loaded {len(questions)} questions\n")

    # Initialize RAG pipeline
    rag = RAGPipeline(debug=debug)

    # Track results
    results = []
    passed = 0
    failed = 0

    # Test each question
    for i, q in enumerate(questions, 1):
        question_id = q['id']
        question_text = q['question']
        expected_answer = q['expected_answer']
        source_doc = q['source_document']
        grading_notes = q.get('grading_notes', '')

        print(f"[{i}/{len(questions)}] {question_id}: {question_text}")

        # Get answer from RAG
        result = rag.answer(question_text, max_chunks=5)
        actual_answer = result['answer']

        # Check if answer is correct
        is_correct = check_answer(question_id, expected_answer, actual_answer, grading_notes)

        # Check if correct source was retrieved
        source_retrieved = any(source_doc in src for src in result['sources'])

        if is_correct and source_retrieved:
            print(f"  ✓ PASS")
            passed += 1
            status = "PASS"
        else:
            print(f"  ✗ FAIL")
            if not is_correct:
                print(f"    Expected: {expected_answer}")
                print(f"    Got: {actual_answer}")
            if not source_retrieved:
                print(f"    Expected source: {source_doc}")
                print(f"    Retrieved: {', '.join(result['sources'])}")
            failed += 1
            status = "FAIL"

        results.append({
            'id': question_id,
            'question': question_text,
            'expected': expected_answer,
            'actual': actual_answer,
            'status': status,
            'sources': result['sources'],
            'score': result['top_score']
        })

        print()

    # Print summary
    print("="*60)
    print(f"RESULTS: {passed}/{len(questions)} passed ({passed/len(questions)*100:.1f}%)")
    print("="*60)

    if failed > 0:
        print(f"\n❌ {failed} questions failed. Review the output above for details.\n")
        print("Common issues:")
        print("  • Wrong source retrieved → Check KB sync status")
        print("  • Answer format mismatch → Improve prompt instructions")
        print("  • Missing key information → Increase max_chunks")
    else:
        print(f"\n✓ All questions passed! L1 implementation is working correctly.\n")

    return results


def save_results(results, output_file: str = "l1_test_results.json"):
    """
    Save test results to JSON file for analysis.

    ❓ PRACTICE QUESTION 4:
    Sau khi chạy test, mở file l1_test_results.json.
    Tìm question có score thấp nhất.
    Tại sao score thấp? Có cần improve query phrasing không?
    """
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    """
    ❓ PRACTICE QUESTION 5:
    Chạy test nhiều lần (3-5 lần).
    Kết quả có consistent không?
    Nếu có câu đôi khi pass, đôi khi fail → nguyên nhân là gì?
    (Hint: xem lại temperature setting trong bedrock_client.py)
    """
    import sys

    debug = '--debug' in sys.argv

    results = run_tests(debug=debug)

    # Save results
    save_results(results)

    # Exit with appropriate code
    failed_count = sum(1 for r in results if r['status'] == 'FAIL')
    sys.exit(0 if failed_count == 0 else 1)
