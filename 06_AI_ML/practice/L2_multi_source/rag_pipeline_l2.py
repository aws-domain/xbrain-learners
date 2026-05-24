"""
Enhanced RAG Pipeline for L2 - Multi-Source Reasoning
"""
from bedrock_client import BedrockClient
from typing import Dict, List, Any
from collections import defaultdict


class RAGPipelineL2:
    """
    Enhanced RAG pipeline with multi-document synthesis capabilities.

    Key improvements over L1:
    1. Higher default max_chunks (10 vs 5)
    2. Document grouping and conflict detection
    3. Enhanced prompt for synthesis
    4. Source citation tracking
    """

    def __init__(self, debug: bool = False):
        self.client = BedrockClient()
        self.debug = debug

    def retrieve(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """
        Retrieve with higher chunk count for multi-doc queries.

        ❓ PRACTICE QUESTION 1:
        L1 dùng max_results=5, L2 dùng max_results=10.
        Thử với max_results=15 hoặc 20.
        Có retrieve được nhiều unique documents hơn không?
        Hay chỉ thêm chunks từ cùng documents?
        """
        result = self.client.retrieve(query, max_results)

        if self.debug:
            # Group chunks by source document
            docs = defaultdict(list)
            for chunk in result['chunks']:
                doc_name = chunk['source'].split('/')[-1]
                docs[doc_name].append(chunk)

            print(f"\n{'='*60}")
            print(f"RETRIEVE: {query}")
            print(f"{'='*60}")
            print(f"Retrieved {len(result['chunks'])} chunks from {len(docs)} documents\n")

            for doc_name, chunks in docs.items():
                print(f"📄 {doc_name}: {len(chunks)} chunks")
                for i, chunk in enumerate(chunks, 1):
                    print(f"   Chunk {i}: score={chunk['score']:.3f}")
            print()

        return result

    def group_chunks_by_document(self, chunks: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Group chunks by source document for better organization.

        ❓ PRACTICE QUESTION 2:
        Tại sao cần group chunks by document?
        Hint: So sánh 2 cách present context:
        - Flat: chunk1, chunk2, chunk3...
        - Grouped: [Doc A: chunk1, chunk2], [Doc B: chunk3]
        Cách nào giúp LLM synthesize tốt hơn?
        """
        grouped = defaultdict(list)
        for chunk in chunks:
            doc_name = chunk['source'].split('/')[-1]
            grouped[doc_name].append(chunk)
        return dict(grouped)

    def detect_conflicts(self, grouped_chunks: Dict[str, List[Dict]]) -> List[str]:
        """
        Detect potential conflicts (e.g., v1 vs v2, archived vs active).

        ❓ PRACTICE QUESTION 3:
        Hàm này detect conflicts dựa trên filename patterns.
        Còn cách nào khác để detect conflicts?
        - Semantic similarity giữa chunks?
        - Metadata tags?
        - LLM-based conflict detection?
        """
        conflicts = []

        doc_names = list(grouped_chunks.keys())

        # Check for version conflicts
        for doc in doc_names:
            if 'v1' in doc.lower() or 'archived' in doc.lower():
                # Look for newer version
                base_name = doc.replace('_v1', '').replace('_archived', '')
                for other_doc in doc_names:
                    if other_doc != doc and base_name in other_doc:
                        conflicts.append(f"Version conflict: {doc} vs {other_doc}")

        return conflicts

    def construct_prompt_l2(self, query: str, chunks: List[Dict]) -> str:
        """
        Enhanced prompt construction for multi-document synthesis.

        ❓ PRACTICE QUESTION 4:
        So sánh L1 prompt vs L2 prompt.
        L2 prompt có thêm instructions gì?
        Thử remove từng instruction và xem impact.
        """
        # Enhanced system instruction for L2
        system = """You are GeekBrain AI Assistant with advanced reasoning capabilities.

CORE RULES:
1. Synthesize information across ALL provided documents
2. When documents conflict, prefer newer/active versions over archived
3. Cross-reference information to build complete answers
4. Cite specific documents when making claims
5. If information spans multiple documents, explain the connection

CONFLICT RESOLUTION:
- api_reference_v2.md supersedes api_reference_v1_archived.md
- Non-archived documents supersede archived ones
- Explicitly state when you're resolving a conflict

MULTI-DOCUMENT SYNTHESIS:
- Combine related information from different sources
- Show your reasoning chain (e.g., "According to X, ... and Y states that ...")
- Identify dependencies and relationships between entities

ANSWER FORMAT:
- Start with direct answer
- Provide supporting details from multiple sources
- End with source citations if relevant"""

        # Group chunks by document
        grouped = self.group_chunks_by_document(chunks)

        # Detect conflicts
        conflicts = self.detect_conflicts(grouped)

        # Build structured context
        context_parts = []

        if conflicts:
            context_parts.append("⚠️ CONFLICTS DETECTED:")
            for conflict in conflicts:
                context_parts.append(f"  - {conflict}")
            context_parts.append("")

        context_parts.append("DOCUMENTS:")
        for doc_name, doc_chunks in grouped.items():
            context_parts.append(f"\n[Document: {doc_name}]")
            for i, chunk in enumerate(doc_chunks, 1):
                context_parts.append(f"\nSection {i}:")
                context_parts.append(chunk['text'])

        context = "\n".join(context_parts)

        # Construct full prompt
        prompt = f"""{system}

{context}

QUESTION: {query}

ANSWER (synthesize across all documents):"""

        if self.debug:
            print(f"\n{'='*60}")
            print(f"PROMPT CONSTRUCTION (L2)")
            print(f"{'='*60}")
            print(f"Documents: {len(grouped)}")
            print(f"Total chunks: {len(chunks)}")
            print(f"Conflicts detected: {len(conflicts)}")
            print(f"Context length: {len(context)} chars")
            if conflicts:
                print(f"\nConflicts:")
                for c in conflicts:
                    print(f"  - {c}")
            print()

        return prompt

    def answer(self, query: str, max_chunks: int = 10) -> Dict[str, Any]:
        """
        Complete L2 RAG pipeline with multi-document synthesis.

        ❓ PRACTICE QUESTION 5:
        Test với câu L2-02:
        "If Team Commerce discovers a P1 bug at 21:00 Friday, can they deploy?"

        Cần 3 documents:
        1. deployment_policy.md
        2. incident_response_policy.md
        3. team_structure.md

        Check debug output:
        - Có retrieve đủ 3 docs không?
        - Nếu thiếu, tăng max_chunks lên bao nhiêu?
        """
        # Step 1: Retrieve
        retrieval_result = self.retrieve(query, max_chunks)
        chunks = retrieval_result['chunks']

        if not chunks:
            return {
                'query': query,
                'answer': "I couldn't find any relevant information in the knowledge base.",
                'chunks': [],
                'sources': [],
                'documents_used': 0
            }

        # Step 2: Construct enhanced prompt
        prompt = self.construct_prompt_l2(query, chunks)

        # Step 3: Generate answer
        answer = self.client.invoke_model(prompt, max_tokens=1500)  # More tokens for detailed answers

        if self.debug:
            print(f"\n{'='*60}")
            print(f"GENERATED ANSWER (L2)")
            print(f"{'='*60}")
            print(answer)
            print()

        # Extract metadata
        grouped = self.group_chunks_by_document(chunks)
        sources = list(grouped.keys())

        return {
            'query': query,
            'answer': answer,
            'chunks': chunks,
            'sources': sources,
            'documents_used': len(grouped),
            'num_chunks': len(chunks),
            'top_score': chunks[0]['score'] if chunks else 0.0,
            'conflicts_detected': len(self.detect_conflicts(grouped))
        }


if __name__ == "__main__":
    """
    ❓ PRACTICE QUESTION 6:
    Test L2 pipeline với các câu hỏi khác nhau:

    1. Single-doc question (L1 style):
       "What is PaymentGW's authentication method?"
       → L2 có overkill không?

    2. Multi-doc question (L2 style):
       "What is PaymentGW's API rate limit?"
       → Có detect conflict v1 vs v2 không?

    3. Cross-reference question:
       "Which services depend on AuthSvc?"
       → Có retrieve đủ docs không?
    """
    print("Testing L2 RAG Pipeline...\n")

    rag = RAGPipelineL2(debug=True)

    # Test with L2-01 (version conflict)
    test_query = "What is PaymentGW's API rate limit?"

    print(f"Question: {test_query}\n")
    result = rag.answer(test_query)

    print(f"\n{'='*60}")
    print("FINAL RESULT")
    print(f"{'='*60}")
    print(f"Answer: {result['answer']}")
    print(f"\nMetadata:")
    print(f"  Documents used: {result['documents_used']}")
    print(f"  Sources: {', '.join(result['sources'])}")
    print(f"  Conflicts detected: {result['conflicts_detected']}")
    print(f"  Top relevance: {result['top_score']:.3f}")
