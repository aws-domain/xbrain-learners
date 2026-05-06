"""
Test L2 Questions - Multi-Source Reasoning
"""
import json
from rag_pipeline_l2 import RAGPipelineL2
from pathlib import Path


def load_l2_questions():
    """Load L2 questions from questions/student/L2_questions.json"""
    questions_path = Path(__file__).parent.parent.parent / "questions" / "student" / "L2_questions.json"

    with open(questions_path, 'r') as f:
        data = json.load(f)

    return data['questions']


def check_answer_l2(question_id: str, expected: str, actual: str, reasoning_required: str) -> dict:
    """
    Check L2 answer - more sophisticated than L1.

    L2 answers require:
    1. Correct factual content
    2. Evidence of synthesis/reasoning
    3. Conflict resolution (if applicable)

    ❓ PRACTICE QUESTION 1:
    L2 grading khó hơn L1 vì cần check reasoning, không chỉ facts.
    Làm thế nào để automate việc check "synthesis quality"?
    - Keyword matching?
    - Check if multiple sources cited?
    - LLM-as-judge?
    """
    actual_lower = actual.lower()
    expected_lower = expected.lower()

    # Extract key facts from expected answer
    import re

    # Check for numbers
    expected_numbers = set(re.findall(r'\d+', expected))
    actual_numbers = set(re.findall(r'\d+', actual))
    numbers_match = len(expected_numbers & actual_numbers) / len(expected_numbers) if expected_numbers else 1.0

    # Check for key entities (names, services, etc.)
    # Extract capitalized words and important terms
    key_entities = []
    for word in expected.split():
        if word[0].isupper() or word.lower() in ['p1', 'p2', 'sla', 'api', 'jwt']:
            key_entities.append(word.lower().strip('.,!?'))

    entities_found = sum(1 for entity in key_entities if entity in actual_lower)
    entities_match = entities_found / len(key_entities) if key_entities else 0.5

    # Check for synthesis indicators
    synthesis_keywords = ['according to', 'based on', 'combines', 'both', 'however', 'but',
                          'supersedes', 'overrides', 'depends on', 'requires']
    has_synthesis = any(kw in actual_lower for kw in synthesis_keywords)

    # Overall score
    factual_score = (numbers_match + entities_match) / 2
    synthesis_bonus = 0.1 if has_synthesis else 0

    total_score = factual_score + synthesis_bonus

    return {
        'passed': total_score >= 0.6,
        'score': total_score,
        'numbers_match': numbers_match,
        'entities_match': entities_match,
        'has_synthesis': has_synthesis
    }


def run_tests(debug: bool = False):
    """
    Run all L2 test questions.

    ❓ PRACTICE QUESTION 2:
    L2 questions khó hơn L1. Expected pass rate:
    - L1: 90-100%
    - L2: 60-80%

    Nếu pass rate < 60%, debug:
    1. Check max_chunks - có đủ không?
    2. Check prompt - có instruct synthesis không?
    3. Check retrieved docs - có đủ required docs không?
    """
    print("\n" + "="*60)
    print("  Testing L2 Questions - Multi-Source Reasoning")
    print("="*60 + "\n")

    # Load questions
    questions = load_l2_questions()
    print(f"Loaded {len(questions)} questions\n")

    # Initialize RAG pipeline
    rag = RAGPipelineL2(debug=debug)

    # Track results
    results = []
    passed = 0
    failed = 0

    # Test each question
    for i, q in enumerate(questions, 1):
        question_id = q['id']
        question_text = q['question']
        expected_answer = q['expected_answer']
        source_docs = q['source_documents']
        reasoning_required = q['reasoning_required']

        print(f"[{i}/{len(questions)}] {question_id}")
        print(f"Q: {question_text}")
        print(f"Required docs: {', '.join(source_docs)}")

        # Get answer from RAG
        result = rag.answer(question_text, max_chunks=12)  # Higher for L2
        actual_answer = result['answer']

        # Check answer quality
        check_result = check_answer_l2(question_id, expected_answer, actual_answer, reasoning_required)

        # Check if required sources were retrieved
        sources_retrieved = sum(1 for doc in source_docs if any(doc in src for src in result['sources']))
        sources_coverage = sources_retrieved / len(source_docs)

        # Determine pass/fail
        if check_result['passed'] and sources_coverage >= 0.5:  # At least 50% of required docs
            print(f"  ✓ PASS (score: {check_result['score']:.2f}, docs: {sources_retrieved}/{len(source_docs)})")
            passed += 1
            status = "PASS"
        else:
            print(f"  ✗ FAIL (score: {check_result['score']:.2f}, docs: {sources_retrieved}/{len(source_docs)})")
            print(f"    Expected: {expected_answer[:100]}...")
            print(f"    Got: {actual_answer[:100]}...")
            if sources_coverage < 0.5:
                missing_docs = [doc for doc in source_docs if not any(doc in src for src in result['sources'])]
                print(f"    Missing docs: {', '.join(missing_docs)}")
            failed += 1
            status = "FAIL"

        results.append({
            'id': question_id,
            'question': question_text,
            'expected': expected_answer,
            'actual': actual_answer,
            'status': status,
            'score': check_result['score'],
            'sources': result['sources'],
            'required_docs': source_docs,
            'sources_coverage': sources_coverage,
            'has_synthesis': check_result['has_synthesis'],
            'conflicts_detected': result['conflicts_detected']
        })

        print()

    # Print summary
    print("="*60)
    print(f"RESULTS: {passed}/{len(questions)} passed ({passed/len(questions)*100:.1f}%)")
    print("="*60)

    # Detailed analysis
    avg_score = sum(r['score'] for r in results) / len(results)
    synthesis_count = sum(1 for r in results if r['has_synthesis'])

    print(f"\nAnalysis:")
    print(f"  Average score: {avg_score:.2f}")
    print(f"  Answers with synthesis: {synthesis_count}/{len(results)}")
    print(f"  Average docs coverage: {sum(r['sources_coverage'] for r in results)/len(results):.1%}")

    if failed > 0:
        print(f"\n❌ {failed} questions failed.")
        print("\nCommon L2 issues:")
        print("  • Insufficient chunks → Increase max_chunks to 12-15")
        print("  • Missing synthesis → Improve prompt instructions")
        print("  • Conflict not resolved → Add explicit conflict resolution rules")
        print("  • Wrong docs retrieved → Improve query phrasing or add metadata filters")
    else:
        print(f"\n✓ All questions passed! L2 implementation is excellent.\n")

    return results


def save_results(results, output_file: str = "l2_test_results.json"):
    """
    Save test results with detailed metrics.

    ❓ PRACTICE QUESTION 3:
    Mở l2_test_results.json và analyze:
    1. Question nào có score thấp nhất?
    2. Question nào missing nhiều required docs nhất?
    3. Question nào không có synthesis indicators?

    Với mỗi issue, plan cách fix.
    """
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    """
    ❓ PRACTICE QUESTION 4:
    So sánh L1 vs L2 test results:

    Metrics to compare:
    1. Pass rate: L1 vs L2
    2. Average response time: L1 vs L2
    3. Average chunks used: L1 vs L2
    4. Average documents used: L1 vs L2

    L2 có đáng với complexity tăng lên không?
    """
    import sys

    debug = '--debug' in sys.argv

    results = run_tests(debug=debug)

    # Save results
    save_results(results)

    # Exit with appropriate code
    failed_count = sum(1 for r in results if r['status'] == 'FAIL')
    sys.exit(0 if failed_count == 0 else 1)
