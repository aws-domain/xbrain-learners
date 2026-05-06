"""
GeekBrain AI Chatbot - Interactive CLI
"""
from rag_pipeline import RAGPipeline
import sys


def print_banner():
    """Print chatbot banner."""
    print("\n" + "="*60)
    print("  GeekBrain AI Chatbot - L1 (RAG Basic)")
    print("="*60)
    print("\nI can answer questions about GeekBrain's:")
    print("  • Services (PaymentGW, AuthSvc, OrderSvc, etc.)")
    print("  • Policies (deployment, security, SLA)")
    print("  • Team structure and ownership")
    print("  • API documentation")
    print("  • Incident postmortems")
    print("\nType 'quit' or 'exit' to end the conversation")
    print("Type 'debug on' to see retrieval details")
    print("Type 'debug off' to hide details")
    print("="*60 + "\n")


def main():
    """
    Main chatbot loop.

    ❓ PRACTICE QUESTION 1:
    Thử hỏi chatbot các câu hỏi sau và quan sát kết quả:
    1. "What is PaymentGW?" (general question)
    2. "What is the API rate limit?" (missing context - which service?)
    3. "Tell me about the March 5 incident" (specific event)

    Câu nào chatbot trả lời tốt nhất? Tại sao?
    """
    print_banner()

    # Initialize RAG pipeline
    rag = RAGPipeline(debug=False)

    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋\n")
                break

            if user_input.lower() == 'debug on':
                rag.debug = True
                print("✓ Debug mode enabled\n")
                continue

            if user_input.lower() == 'debug off':
                rag.debug = False
                print("✓ Debug mode disabled\n")
                continue

            # Process question
            result = rag.answer(user_input)

            # Print answer
            print(f"\nBot: {result['answer']}")

            # Print metadata (if not in debug mode, debug mode already prints this)
            if not rag.debug:
                print(f"\n📚 Sources: {', '.join(result['sources'])}")
                print(f"🎯 Relevance: {result['top_score']:.2f}")

            print()

        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            if '--debug' in sys.argv:
                import traceback
                traceback.print_exc()


if __name__ == "__main__":
    """
    ❓ PRACTICE QUESTION 2:
    Sau khi test chatbot với các câu hỏi L1, thử những câu này:

    1. "Which service had the highest cost in March 2026?"
       → Chatbot có trả lời được không? Tại sao?
       (Hint: Đây là câu L3 - cần tool, không có trong docs)

    2. "What is PaymentGW's API rate limit?" (L1-01)
       → So sánh answer với expected_answer trong L1_questions.json
       → Có match không?

    3. "If Team Commerce discovers a P1 bug at 21:00 Friday, can they deploy?"
       → Đây là câu L2 - cần synthesize từ nhiều docs
       → L1 pipeline có handle được không?
    """
    main()
