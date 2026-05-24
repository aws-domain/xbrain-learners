"""
Test L5 Investigation Prompts - Goal-Directed Multi-Step Reasoning
"""
import json
from pathlib import Path
from bedrock_agent_client import BedrockAgentClient
import time


def load_l5_investigations():
    """Load L5 investigation prompts from questions/student/L5_investigation_prompts.json"""
    questions_path = Path(__file__).parent.parent.parent / "questions" / "student" / "L5_investigation_prompts.json"

    with open(questions_path, 'r') as f:
        data = json.load(f)

    return data['investigations']


def check_investigation_quality(investigation: dict, result: dict, debug: bool = False) -> dict:
    """
    Check investigation quality based on:
    1. Data sources used (KB, API, DB)
    2. Steps executed
    3. Findings completeness
    4. Recommendations quality

    ❓ PRACTICE QUESTION 1:
    L5 grading là subjective - không có single correct answer.
    Làm thế nào để automate grading?

    Approach 1: Checklist-based
    - ✓ Used monitoring API?
    - ✓ Used database?
    - ✓ Used KB?
    - ✓ Generated recommendations?

    Approach 2: LLM-as-judge
    - Gọi Claude để grade investigation quality
    - Provide rubric và expected findings
    - LLM returns score + feedback

    Approach 3: Hybrid
    - Checklist cho objective criteria
    - LLM cho subjective criteria (recommendation quality)

    Bạn chọn approach nào?
    """
    inv_id = investigation['id']
    prompt = investigation['prompt']
    expected_steps = investigation['expected_steps']
    expected_findings = investigation['expected_findings']
    data_sources_needed = investigation['data_sources_needed']

    answer = result['answer']
    traces = result.get('traces', [])

    # Parse traces to check what was done
    if traces:
        from bedrock_agent_client import BedrockAgentClient
        client = BedrockAgentClient()
        trace_info = client.parse_trace(traces)
        tools_used = len(trace_info['tool_calls']) > 0
        kb_used = len(trace_info['kb_retrievals']) > 0
    else:
        # Fallback: check answer content
        tools_used = any(keyword in answer.lower() for keyword in ['current', 'approximately', 'live', 'now'])
        kb_used = any(keyword in answer.lower() for keyword in ['policy', 'according to', 'document', 'postmortem'])

    # Check data sources coverage
    data_sources_used = []
    if tools_used:
        data_sources_used.append('monitoring_api' if 'monitoring_api' in data_sources_needed else 'database')
    if kb_used:
        data_sources_used.append('knowledge_base')

    sources_coverage = len(data_sources_used) / len(data_sources_needed) if data_sources_needed else 0

    # Check if answer contains key findings
    findings_keywords = expected_findings.lower().split()[:10]  # First 10 words as key terms
    findings_found = sum(1 for kw in findings_keywords if kw in answer.lower())
    findings_coverage = findings_found / len(findings_keywords) if findings_keywords else 0

    # Check if recommendations are present
    has_recommendations = any(keyword in answer.lower() for keyword in
                             ['recommend', 'should', 'suggest', 'action', 'improve', 'priority'])

    # Calculate overall score
    score = (
        sources_coverage * 0.3 +      # 30% - used required data sources
        findings_coverage * 0.4 +      # 40% - covered key findings
        (1.0 if has_recommendations else 0.0) * 0.3  # 30% - provided recommendations
    )

    if debug:
        print(f"\n  Grading breakdown:")
        print(f"    Data sources: {data_sources_used} / {data_sources_needed} ({sources_coverage:.1%})")
        print(f"    Findings coverage: {findings_coverage:.1%}")
        print(f"    Has recommendations: {has_recommendations}")
        print(f"    Overall score: {score:.2f}")

    return {
        'passed': score >= 0.6,
        'score': score,
        'sources_coverage': sources_coverage,
        'findings_coverage': findings_coverage,
        'has_recommendations': has_recommendations,
        'tools_used': tools_used,
        'kb_used': kb_used
    }


def run_tests(debug: bool = False):
    """
    Run all L5 investigation tests.

    ❓ PRACTICE QUESTION 2:
    L5 investigations mất nhiều thời gian (10-30s mỗi investigation).
    Với 5 investigations, total time ~1-2 minutes.

    Có thể parallel không?
    - Investigations độc lập → có thể parallel
    - Nhưng Bedrock Agent có rate limit
    - Trade-off: speed vs rate limit

    Trong production, làm thế nào handle long-running investigations?
    - Async processing?
    - Progress updates?
    - Timeout handling?
    """
    print("\n" + "="*60)
    print("  Testing L5 Investigations - Goal-Directed Reasoning")
    print("="*60 + "\n")

    # Load investigations
    investigations = load_l5_investigations()
    print(f"Loaded {len(investigations)} investigation prompts\n")

    # Initialize Agent client
    try:
        agent = BedrockAgentClient()
    except Exception as e:
        print(f"❌ Cannot initialize agent: {e}")
        print("\nPlease complete L3/L4 setup first.")
        return []

    # Track results
    results = []
    passed = 0
    failed = 0

    # Run each investigation
    for i, inv in enumerate(investigations, 1):
        inv_id = inv['id']
        prompt = inv['prompt']
        expected_steps = inv['expected_steps']
        data_sources = inv['data_sources_needed']

        print(f"[{i}/{len(investigations)}] {inv_id}")
        print(f"Prompt: {prompt[:80]}...")
        print(f"Expected steps: {len(expected_steps)}")
        print(f"Data sources: {', '.join(data_sources)}")

        # Run investigation
        print(f"  Running investigation (this may take 10-30 seconds)...")
        start_time = time.time()

        result = agent.invoke_agent(prompt, enable_trace=debug)
        answer = result['answer']

        elapsed = time.time() - start_time
        print(f"  Completed in {elapsed:.1f}s")

        # Check quality
        check = check_investigation_quality(inv, result, debug=debug)

        if check['passed']:
            print(f"  ✓ PASS (score: {check['score']:.2f})")
            passed += 1
            status = "PASS"
        else:
            print(f"  ✗ FAIL (score: {check['score']:.2f})")
            print(f"    Sources coverage: {check['sources_coverage']:.1%}")
            print(f"    Findings coverage: {check['findings_coverage']:.1%}")
            print(f"    Has recommendations: {check['has_recommendations']}")
            failed += 1
            status = "FAIL"

        results.append({
            'id': inv_id,
            'prompt': prompt,
            'answer': answer,
            'status': status,
            'score': check['score'],
            'elapsed_seconds': elapsed,
            'sources_coverage': check['sources_coverage'],
            'findings_coverage': check['findings_coverage'],
            'has_recommendations': check['has_recommendations'],
            'tools_used': check['tools_used'],
            'kb_used': check['kb_used']
        })

        print()

    # Print summary
    print("="*60)
    print(f"RESULTS: {passed}/{len(investigations)} investigations passed")
    print("="*60)

    # Detailed analysis
    if results:
        avg_score = sum(r['score'] for r in results) / len(results)
        avg_time = sum(r['elapsed_seconds'] for r in results) / len(results)
        tools_count = sum(1 for r in results if r['tools_used'])
        kb_count = sum(1 for r in results if r['kb_used'])
        recs_count = sum(1 for r in results if r['has_recommendations'])

        print(f"\nAnalysis:")
        print(f"  Average score: {avg_score:.2f}")
        print(f"  Average time: {avg_time:.1f}s")
        print(f"  Used tools: {tools_count}/{len(results)}")
        print(f"  Used KB: {kb_count}/{len(results)}")
        print(f"  Provided recommendations: {recs_count}/{len(results)}")

    if failed > 0:
        print(f"\n❌ {failed} investigations failed.")
        print("\nCommon L5 issues:")
        print("  • Incomplete investigation → Agent stops too early")
        print("  • Missing data sources → Not using tools or KB")
        print("  • Shallow findings → Not synthesizing across sources")
        print("  • Generic recommendations → Not specific/actionable")
        print("\nImprovement strategies:")
        print("  1. Improve agent instructions (be explicit about investigation depth)")
        print("  2. Add examples of good investigations in prompt")
        print("  3. Use structured output format for consistency")
        print("  4. Implement multi-pass synthesis (gather → analyze → recommend)")
    else:
        print(f"\n✓ All investigations passed! L5 implementation is excellent.\n")
        print("🎉 Congratulations! You've completed all 5 levels:")
        print("  ✅ L1 - RAG Basic")
        print("  ✅ L2 - Multi-Source Reasoning")
        print("  ✅ L3 - Tools Integration")
        print("  ✅ L4 - Conversation Memory")
        print("  ✅ L5 - Goal-Directed Investigation")
        print("\nYour GeekBrain AI chatbot is production-ready! 🚀")

    return results


def save_results(results, output_file: str = "l5_test_results.json"):
    """
    Save investigation test results.

    ❓ PRACTICE QUESTION 3:
    Analyze l5_test_results.json:
    1. Investigation nào mất nhiều thời gian nhất? Tại sao?
    2. Investigation nào có score thấp nhất? Missing gì?
    3. Pattern nào xuất hiện trong successful investigations?

    Use insights để improve agent instructions.
    """
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    """
    ❓ PRACTICE QUESTION 4:
    Final reflection - So sánh journey từ L1 → L5:

    | Metric | L1 | L5 | Growth |
    |--------|----|----|--------|
    | Complexity | Low | Very High | 10x |
    | Response time | 2-3s | 10-30s | 10x |
    | Code lines | ~200 | ~2000 | 10x |
    | AWS services | 2 | 6+ | 3x |
    | Capabilities | Basic Q&A | Full investigation | ∞ |

    Lessons learned:
    1. Start simple (L1) → iterate (L2-L5)
    2. Each level builds on previous
    3. Complexity grows exponentially
    4. But capabilities grow even faster

    Worth it? Absolutely! 🎉
    """
    import sys

    debug = '--debug' in sys.argv

    print("\n⚠️  Prerequisites check:")
    print("  1. L1-L4 setup complete?")
    print("  2. All AWS services running?")
    print("  3. Ready for long-running tests? (1-2 minutes)")
    print("\nPress Enter to continue or Ctrl+C to abort...")
    input()

    results = run_tests(debug=debug)

    if results:
        # Save results
        save_results(results)

        # Exit with appropriate code
        failed_count = sum(1 for r in results if r['status'] == 'FAIL')
        sys.exit(0 if failed_count == 0 else 1)
