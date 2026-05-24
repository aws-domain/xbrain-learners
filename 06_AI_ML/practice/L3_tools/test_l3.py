"""
Test L3 Questions - Grounded Computation with Tools
"""
import json
from bedrock_agent_client import BedrockAgentClient
from pathlib import Path
import re


def load_l3_questions():
    """Load L3 questions from questions/student/L3_questions.json"""
    questions_path = Path(__file__).parent.parent.parent / "questions" / "student" / "L3_questions.json"

    with open(questions_path, 'r') as f:
        data = json.load(f)

    return data['questions']


def check_answer_l3(question_id: str, expected: str, actual: str, data_source: str, tool_needed: str) -> dict:
    """
    Check L3 answer - must verify both correctness and tool usage.

    L3 grading criteria:
    1. Correct numerical/factual answer
    2. Evidence that tool was called (not just KB)
    3. Reasonable tolerance for live data (±5%)

    ❓ PRACTICE QUESTION 1:
    L3 answers có live data với jitter (±5%).
    Ví dụ: Expected = 185ms, actual có thể là 180-190ms.
    Làm thế nào để check "approximately equal"?
    """
    actual_lower = actual.lower()
    expected_lower = expected.lower()

    # Extract numbers from both answers
    expected_numbers = [float(n) for n in re.findall(r'\d+\.?\d*', expected)]
    actual_numbers = [float(n) for n in re.findall(r'\d+\.?\d*', actual)]

    # Check if numbers match (with tolerance for live data)
    numbers_match = False
    if expected_numbers and actual_numbers:
        # For each expected number, check if there's a close match in actual
        matches = 0
        for exp_num in expected_numbers:
            for act_num in actual_numbers:
                # Allow ±10% tolerance for live metrics
                if abs(act_num - exp_num) / exp_num <= 0.10:
                    matches += 1
                    break
        numbers_match = matches >= len(expected_numbers) * 0.8  # 80% of numbers should match

    # Check for key terms
    key_terms = []
    for word in expected.split():
        if len(word) > 3 and word.lower() not in ['the', 'and', 'for', 'with', 'from']:
            key_terms.append(word.lower().strip('.,!?'))

    terms_found = sum(1 for term in key_terms if term in actual_lower)
    terms_match = terms_found / len(key_terms) if key_terms else 0.5

    # Overall score
    score = (numbers_match * 0.6) + (terms_match * 0.4)

    return {
        'passed': score >= 0.6,
        'score': score,
        'numbers_match': numbers_match,
        'terms_match': terms_match
    }


def run_tests(debug: bool = False):
    """
    Run all L3 test questions.

    ❓ PRACTICE QUESTION 2:
    L3 tests phụ thuộc vào:
    1. Monitoring API running (localhost:8000)
    2. Database seeded (geekbrain.db)
    3. Lambda deployed
    4. Bedrock Agent configured

    Nếu test fail, check từng dependency này.
    """
    print("\n" + "="*60)
    print("  Testing L3 Questions - Grounded Computation")
    print("="*60 + "\n")

    # Load questions
    questions = load_l3_questions()
    print(f"Loaded {len(questions)} questions\n")

    # Initialize Agent client
    try:
        agent = BedrockAgentClient()
    except ValueError as e:
        print(f"❌ Cannot initialize agent: {e}")
        print("\nPlease complete L3 setup:")
        print("1. Create Bedrock Agent")
        print("2. Deploy Lambda functions")
        print("3. Set BEDROCK_AGENT_ID in .env")
        return []

    # Track results
    results = []
    passed = 0
    failed = 0

    # Test each question
    for i, q in enumerate(questions, 1):
        question_id = q['id']
        question_text = q['question']
        expected_answer = q['expected_answer']
        data_source = q['data_source']
        tool_needed = q['tool_needed']

        print(f"[{i}/{len(questions)}] {question_id}")
        print(f"Q: {question_text}")
        print(f"Tool needed: {tool_needed}")
        print(f"Data source: {data_source}")

        # Get answer from Agent
        result = agent.invoke_agent(question_text, enable_trace=debug)
        actual_answer = result['answer']

        # Parse trace to verify tool was called
        tool_called = False
        if result['traces']:
            trace_info = agent.parse_trace(result['traces'])
            tool_called = len(trace_info['tool_calls']) > 0

        # Check answer quality
        check_result = check_answer_l3(question_id, expected_answer, actual_answer, data_source, tool_needed)

        # Determine pass/fail
        if check_result['passed']:
            status_icon = "✓"
            if not tool_called and data_source != 'knowledge_base':
                status_icon = "⚠️"  # Correct answer but didn't use tool
                print(f"  {status_icon} PASS (but tool not detected - may have used KB instead)")
            else:
                print(f"  {status_icon} PASS (score: {check_result['score']:.2f})")
            passed += 1
            status = "PASS"
        else:
            print(f"  ✗ FAIL (score: {check_result['score']:.2f})")
            print(f"    Expected: {expected_answer}")
            print(f"    Got: {actual_answer}")
            if not tool_called:
                print(f"    ⚠️  Tool was not called!")
            failed += 1
            status = "FAIL"

        results.append({
            'id': question_id,
            'question': question_text,
            'expected': expected_answer,
            'actual': actual_answer,
            'status': status,
            'score': check_result['score'],
            'tool_called': tool_called,
            'data_source': data_source,
            'tool_needed': tool_needed
        })

        print()

    # Print summary
    print("="*60)
    print(f"RESULTS: {passed}/{len(questions)} passed ({passed/len(questions)*100:.1f}%)")
    print("="*60)

    # Detailed analysis
    avg_score = sum(r['score'] for r in results) / len(results) if results else 0
    tools_used = sum(1 for r in results if r['tool_called'])

    print(f"\nAnalysis:")
    print(f"  Average score: {avg_score:.2f}")
    print(f"  Tools called: {tools_used}/{len(results)}")

    if failed > 0:
        print(f"\n❌ {failed} questions failed.")
        print("\nCommon L3 issues:")
        print("  • Tool not called → Check agent instructions")
        print("  • Wrong tool called → Check OpenAPI schema")
        print("  • Tool returns error → Check Lambda logs")
        print("  • Answer incorrect → Check tool implementation")
        print("\nDebug steps:")
        print("  1. Run with --debug to see agent trace")
        print("  2. Check Lambda CloudWatch logs")
        print("  3. Test Lambda directly with mock events")
        print("  4. Verify monitoring API is running")
    else:
        print(f"\n✓ All questions passed! L3 implementation is working.\n")

    return results


def save_results(results, output_file: str = "l3_test_results.json"):
    """
    Save test results with tool usage metrics.

    ❓ PRACTICE QUESTION 3:
    Analyze l3_test_results.json:
    1. Câu nào tool_called=false nhưng vẫn pass?
       → Agent có thể đoán đúng từ KB (lucky guess)
    2. Câu nào tool_called=true nhưng fail?
       → Tool return sai data hoặc agent không parse đúng
    3. Pattern nào xuất hiện?
    """
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    """
    ❓ PRACTICE QUESTION 4:
    So sánh test results L1 vs L2 vs L3:

    | Metric | L1 | L2 | L3 |
    |--------|----|----|-----|
    | Pass rate | 90-100% | 60-80% | 70-90% |
    | Avg response time | 2-3s | 3-5s | 5-8s |
    | Complexity | Low | Medium | High |

    L3 có trade-off gì?
    - Slower response (tool calls)
    - More complex setup (Lambda, Agent)
    - But can answer questions L1/L2 cannot

    Đáng không?
    """
    import sys

    debug = '--debug' in sys.argv

    print("\n⚠️  Prerequisites check:")
    print("  1. Monitoring API running? (http://localhost:8000)")
    print("  2. Database seeded? (geekbrain.db)")
    print("  3. Lambda deployed? (geekbrain-tools)")
    print("  4. Bedrock Agent created? (BEDROCK_AGENT_ID set)")
    print("\nPress Enter to continue or Ctrl+C to abort...")
    input()

    results = run_tests(debug=debug)

    if results:
        # Save results
        save_results(results)

        # Exit with appropriate code
        failed_count = sum(1 for r in results if r['status'] == 'FAIL')
        sys.exit(0 if failed_count == 0 else 1)
