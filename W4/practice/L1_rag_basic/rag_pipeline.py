"""
RAG Pipeline - Core logic for Retrieval-Augmented Generation
"""
from bedrock_client import BedrockClient
from typing import Dict, List, Any


class RAGPipeline:
    """
    Implements the RAG (Retrieval-Augmented Generation) pipeline.

    Pipeline flow:
    1. User question → Retrieve relevant chunks from KB
    2. Construct prompt with context
    3. Generate answer using LLM
    """

    def __init__(self, debug: bool = False):
        """
        Initialize RAG pipeline.

        Args:
            debug: If True, print intermediate steps

        ❓ PRACTICE QUESTION 1:
        Trong course "Integrating AI into Your Apps", bạn học về RAG pattern.
        Tại sao cần retrieve trước rồi mới generate?
        Tại sao không để LLM trả lời trực tiếp từ training data?
        """
        self.client = BedrockClient()
        self.debug = debug

    def retrieve(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Step 1: Retrieve relevant chunks from Knowledge Base.

        ❓ PRACTICE QUESTION 2:
        Thử query: "What is PaymentGW's API rate limit?"
        - Nếu retrieve được chunk từ api_reference_v1_archived.md (500 rpm)
        - Và chunk từ api_reference_v2.md (1000 rpm)
        Chunk nào sẽ có score cao hơn? Tại sao?
        """
        result = self.client.retrieve(query, max_results)

        if self.debug:
            print(f"\n{'='*60}")
            print(f"RETRIEVE: {query}")
            print(f"{'='*60}")
            print(f"Retrieved {len(result['chunks'])} chunks\n")

            for i, chunk in enumerate(result['chunks'], 1):
                print(f"Chunk {i}:")
                print(f"  Score: {chunk['score']:.3f}")
                print(f"  Source: {chunk['source'].split('/')[-1]}")
                print(f"  Text: {chunk['text'][:150]}...")
                print()

        return result

    def construct_prompt(self, query: str, chunks: List[Dict]) -> str:
        """
        Step 2: Construct prompt with retrieved context.

        Prompt structure:
        - System instruction
        - Retrieved context (chunks)
        - User question

        ❓ PRACTICE QUESTION 3:
        Thử thay đổi system instruction để LLM:
        - Luôn cite source document
        - Trả lời ngắn gọn (1-2 câu)
        - Nói "I don't know" nếu không tìm thấy trong context
        Cách nào hiệu quả nhất?
        """
        # System instruction
        system = """You are GeekBrain AI Assistant. Answer questions based ONLY on the provided context.

Rules:
1. Answer with a single short sentence or phrase - no markdown, no bold, no bullet points
2. Do NOT cite sources or add explanations
3. If the answer is NOT in the context, say "I don't have that information in the knowledge base"
4. Be precise with numbers, dates, and technical details
5. Prefer CURRENT/active documents over ARCHIVED ones"""

        # Build context from chunks
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            source_file = chunk['source'].split('/')[-1]
            context_parts.append(f"[Document {i}: {source_file}]\n{chunk['text']}")

        context = "\n\n".join(context_parts)

        # Construct full prompt
        prompt = f"""{system}

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""

        if self.debug:
            print(f"\n{'='*60}")
            print(f"PROMPT CONSTRUCTION")
            print(f"{'='*60}")
            print(f"Context length: {len(context)} chars")
            print(f"Number of chunks: {len(chunks)}")
            print(f"\nFull prompt:\n{prompt[:500]}...\n")

        return prompt

    def generate(self, prompt: str) -> str:
        """
        Step 3: Generate answer using Claude.

        ❓ PRACTICE QUESTION 4:
        Trong bedrock_client.py, temperature được set = 0.0.
        Thử thay đổi thành 0.5 hoặc 1.0.
        Answer có thay đổi không? Tại sao?
        (Hint: xem lại course "Foundation Models" - phần Temperature)
        """
        answer = self.client.invoke_model(prompt)

        if self.debug:
            print(f"\n{'='*60}")
            print(f"GENERATED ANSWER")
            print(f"{'='*60}")
            print(answer)
            print()

        return answer

    def answer(self, query: str, max_chunks: int = 5) -> Dict[str, Any]:
        """
        Complete RAG pipeline: Retrieve → Construct → Generate.

        Args:
            query: User's question
            max_chunks: Number of chunks to retrieve

        Returns:
            Dict with answer, chunks, and metadata
        """
        # Step 1: Retrieve
        retrieval_result = self.retrieve(query, max_chunks)
        chunks = retrieval_result['chunks']

        if not chunks:
            return {
                'query': query,
                'answer': "I couldn't find any relevant information in the knowledge base.",
                'chunks': [],
                'sources': []
            }

        # Step 2: Construct prompt
        prompt = self.construct_prompt(query, chunks)

        # Step 3: Generate answer
        answer = self.generate(prompt)

        # Extract sources
        sources = list(set([chunk['source'].split('/')[-1] for chunk in chunks]))

        return {
            'query': query,
            'answer': answer,
            'chunks': chunks,
            'sources': sources,
            'num_chunks': len(chunks),
            'top_score': chunks[0]['score'] if chunks else 0.0
        }

    def answer_simple(self, query: str) -> str:
        """
        Simplified version using Bedrock's RetrieveAndGenerate API.

        ❓ PRACTICE QUESTION 5:
        So sánh answer() vs answer_simple():
        - Cái nào cho bạn control nhiều hơn?
        - Cái nào dễ debug hơn?
        - Cái nào nhanh hơn?
        Khi nào nên dùng cái nào?
        """
        result = self.client.retrieve_and_generate(query)
        return result['answer']


if __name__ == "__main__":
    # Test RAG pipeline
    print("Testing RAG Pipeline...\n")

    rag = RAGPipeline(debug=True)

    # Test question from L1
    test_query = "What is the current API rate limit for PaymentGW?"

    print(f"Question: {test_query}\n")
    result = rag.answer(test_query)

    print(f"\n{'='*60}")
    print("FINAL RESULT")
    print(f"{'='*60}")
    print(f"Answer: {result['answer']}")
    print(f"Sources: {', '.join(result['sources'])}")
    print(f"Chunks used: {result['num_chunks']}")
    print(f"Top relevance score: {result['top_score']:.3f}")
