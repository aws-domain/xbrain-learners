"""
Test L4 Conversation Scripts - Multi-Turn with Memory
"""
import json
import uuid
from pathlib import Path
from dynamodb_client import DynamoDBClient
from bedrock_agent_client import BedrockAgentClient


def load_l4_conversations():
    """Load L4 conversation scripts from questions/student/L4_conversation_scripts.json"""
    questions_path = Path(__file__).parent.parent.parent / "questions" / "student" / "L4_conversation_scripts.json"

    with open(questions_path, 'r') as f:
        data = json.load(f)

    return data['conversations']


def check_turn_answer(expected: str, actual: str) -> dict:
    """
    Check if turn answer is correct.

    ❓ PRACTICE QUESTION 1:
    L4 grading phức tạp hơn L1/L2/L3 vì:
    - Turn 1 có thể đúng nhưng Turn 2 sai (do memory fail)
    - Cần check cả conversation flow, không chỉ individual answers

    Làm thế nào để grade conversation quality?
    """
    import re

    actual_lower = actual.lower()
    expected_lower = expected.lower()

    # Extract key terms
    expected_numbers = set(re.findall(r'\d+', expected))
    actual_numbers = set(re.findall(r'\d+', actual))

    # Check number overlap
    if expected_numbers:
        numbers_match = len(expected_numbers & actual_numbers) / len(expected_numbers)
    else:
        numbers_match = 0.5

    # Check key terms
    key_terms = [w.lower().strip('.,!?') for w in expected.split()
                 if len(w) > 3 and w.lower() not in ['the', 'and', 'for', 'with', 'that', 'this']]

    terms_found = sum(1 for term in key_terms if term in actual_lower)
    terms_match = terms_found / len(key_terms) if key_terms else 0.5

    score = (numbers_match * 0.5) + (terms_match * 0.5)

    return {
        'passed': score >= 0.5,
        'score': score
    }


def run_conversation_test(conversation: dict, agent: BedrockAgentClient, db: DynamoDBClient, debug: bool = False):
    """
    Run a single conversation script.

    ❓ PRACTICE QUESTION 2:
    Conversation test khác với single-turn test:
    - Phải maintain session_id across turns
    - Turn N phụ thuộc vào Turn N-1
    - Nếu Turn 1 fail, Turn 2+ cũng fail

    Có nên stop test ngay khi 1 turn fail không?
    """
    conv_id = conversation['id']
    title = conversation['title']
    turns = conversation['turns']

    print(f"\n{'='*60}")
    print(f"Conversation {conv_id}: {title}")
    print(f"{'='*60}\n")

    # Create new session for this conversation
    session_id = str(uuid.uuid4())
    db.create_session(session_id, user_id='test-user')

    results = []
    all_passed = True

    for turn_data in turns:
        turn_num = turn_data['turn']
        user_msg = turn_data['user']
        expected = turn_data['expected_answer']
        requires = turn_data['requires']

        print(f"Turn {turn_num}:")
        print(f"  User: {user_msg}")
        print(f"  Requires: {requires}")

        # Invoke agent with session context
        result = agent.invoke_agent(user_msg, session_id=session_id, enable_trace=debug)
        actual = result['answer']

        print(f"  Bot: {actual[:100]}...")

        # Check answer
        check = check_turn_answer(expected, actual)

        if check['passed']:
            print(f"  ✓ PASS (score: {check['score']:.2f})")
            status = "PASS"
        else:
            print(f"  ✗ FAIL (score: {check['score']:.2f})")
            print(f"    Expected: {expected[:100]}...")
            all_passed = False
            status = "FAIL"

        # Store turn in DynamoDB (for memory)
        # Note: In production, agent should do this automatically
        # For testing, we manually store to verify memory works
        db.add_turn(
            session_id=session_id,
            turn_number=turn_num,
            user_message=user_msg,
            bot_response=actual,
            entities=[],  # Would extract from actual in production
            tools=[]
        )

        results.append({
            'turn': turn_num,
            'user': user_msg,
            'expected': expected,
            'actual': actual,
            'status': status,
            'score': check['score']
        })

        print()

    return {
        'conversation_id': conv_id,
        'title': title,
        'session_id': session_id,
        'passed': all_passed,
        'turns': results
    }


def run_tests(debug: bool = False):
    """
    Run all L4 conversation tests.

    ❓ PRACTICE QUESTION 3:
    L4 test phụ thuộc vào:
    1. L3 setup (Agent, Lambda, Tools)
    2. DynamoDB tables created
    3. Agent có session management enabled

    Nếu test fail, check dependencies theo thứ tự này.
    """
    print("\n" + "="*60)
    print("  Testing L4 Conversations - Memory & Continuity")
    print("="*60 + "\n")

    # Load conversations
    conversations = load_l4_conversations()
    print(f"Loaded {len(conversations)} conversation scripts\n")

    # Initialize clients
    try:
        agent = BedrockAgentClient()
        db = DynamoDBClient()
    except Exception as e:
        print(f"❌ Cannot initialize clients: {e}")
        print("\nPlease complete L4 setup:")
        print("1. Complete L3 setup (Agent, Lambda)")
        print("2. Create DynamoDB tables")
        print("3. Update Lambda IAM role for DynamoDB access")
        return []

    # Run each conversation
    results = []
    passed_count = 0
    failed_count = 0

    for conv in conversations:
        result = run_conversation_test(conv, agent, db, debug=debug)
        results.append(result)

        if result['passed']:
            passed_count += 1
        else:
            failed_count += 1

    # Print summary
    print("\n" + "="*60)
    print(f"RESULTS: {passed_count}/{len(conversations)} conversations passed")
    print("="*60)

    # Detailed analysis
    total_turns = sum(len(r['turns']) for r in results)
    passed_turns = sum(1 for r in results for t in r['turns'] if t['status'] == 'PASS')

    print(f"\nTurn-level analysis:")
    print(f"  Total turns: {total_turns}")
    print(f"  Passed turns: {passed_turns}/{total_turns} ({passed_turns/total_turns*100:.1f}%)")

    if failed_count > 0:
        print(f"\n❌ {failed_count} conversations failed.")
        print("\nCommon L4 issues:")
        print("  • Turn 1 pass but Turn 2 fail → Memory not working")
        print("  • Pronouns not resolved → Entity tracking issue")
        print("  • Context lost after 3+ turns → History not loaded")
        print("\nDebug steps:")
        print("  1. Check DynamoDB tables have data")
        print("  2. Verify agent session management enabled")
        print("  3. Check conversation history retrieval")
        print("  4. Test with --debug to see agent trace")
    else:
        print(f"\n✓ All conversations passed! L4 implementation is excellent.\n")

    return results


def save_results(results, output_file: str = "l4_test_results.json"):
    """
    Save conversation test results.

    ❓ PRACTICE QUESTION 4:
    Analyze l4_test_results.json:
    1. Conversation nào có Turn 1 pass nhưng Turn 2+ fail?
       → Memory issue
    2. Conversation nào tất cả turns đều fail?
       → Fundamental issue (tools, KB)
    3. Pattern nào xuất hiện?
    """
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    """
    ❓ PRACTICE QUESTION 5:
    So sánh test complexity L1 → L2 → L3 → L4:

    | Level | Test Type | Dependencies | Difficulty |
    |-------|-----------|--------------|------------|
    | L1 | Single Q&A | KB only | Easy |
    | L2 | Multi-doc Q&A | KB only | Medium |
    | L3 | Q&A + Tools | KB + API + DB + Lambda | Hard |
    | L4 | Multi-turn conversation | L3 + DynamoDB + Session | Very Hard |

    L4 là hardest vì:
    - Phụ thuộc vào tất cả L1/L2/L3
    - Thêm session management
    - Thêm memory/entity tracking
    - Test phải run sequentially (không parallel được)

    Có cách nào simplify L4 testing không?
    """
    import sys

    debug = '--debug' in sys.argv

    print("\n⚠️  Prerequisites check:")
    print("  1. L3 setup complete? (Agent, Lambda, Tools)")
    print("  2. DynamoDB tables created? (sessions, conversations)")
    print("  3. Lambda has DynamoDB permissions?")
    print("\nPress Enter to continue or Ctrl+C to abort...")
    input()

    results = run_tests(debug=debug)

    if results:
        # Save results
        save_results(results)

        # Exit with appropriate code
        failed_count = sum(1 for r in results if not r['passed'])
        sys.exit(0 if failed_count == 0 else 1)
