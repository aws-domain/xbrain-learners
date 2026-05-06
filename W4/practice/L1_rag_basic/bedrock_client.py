"""
Bedrock Client - Wrapper for AWS Bedrock API calls
"""
import boto3
import json
import os
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()


class BedrockClient:
    """
    Wrapper class for interacting with AWS Bedrock services.
    Handles both Knowledge Base retrieval and model invocation.
    """

    def __init__(self):
        """
        Initialize Bedrock clients.

        ❓ PRACTICE QUESTION 1:
        Tại sao cần 2 clients riêng biệt (bedrock-agent-runtime và bedrock-runtime)?
        Hint: Xem lại course "Bedrock Getting Started" - phần Architecture
        """
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        self.kb_id = os.getenv('KNOWLEDGE_BASE_ID')
        self.model_id = os.getenv('MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')

        # Client for Knowledge Base operations
        self.bedrock_agent_client = boto3.client(
            'bedrock-agent-runtime',
            region_name=self.region
        )

        # Client for model invocation
        self.bedrock_runtime_client = boto3.client(
            'bedrock-runtime',
            region_name=self.region
        )

    def retrieve(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Retrieve relevant chunks from Knowledge Base.

        Args:
            query: User's question
            max_results: Maximum number of chunks to retrieve

        Returns:
            Dict containing retrieved chunks with scores and metadata

        ❓ PRACTICE QUESTION 2:
        Thử thay đổi max_results từ 5 → 10 → 20.
        Response time thay đổi như thế nào? Tại sao?
        """
        try:
            response = self.bedrock_agent_client.retrieve(
                knowledgeBaseId=self.kb_id,
                retrievalQuery={
                    'text': query
                },
                retrievalConfiguration={
                    'vectorSearchConfiguration': {
                        'numberOfResults': max_results
                    }
                }
            )

            # Parse response into cleaner format
            chunks = []
            for result in response.get('retrievalResults', []):
                chunks.append({
                    'text': result['content']['text'],
                    'score': result['score'],
                    'source': result['location']['s3Location']['uri'],
                    'metadata': result.get('metadata', {})
                })

            return {
                'chunks': chunks,
                'query': query
            }

        except Exception as e:
            print(f"Error retrieving from KB: {e}")
            return {'chunks': [], 'query': query}

    def invoke_model(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Invoke Claude model to generate answer.

        Args:
            prompt: Complete prompt (system + context + question)
            max_tokens: Maximum tokens in response

        Returns:
            Generated answer text

        ❓ PRACTICE QUESTION 3:
        Trong course "Foundation Models", bạn học về token limits.
        Claude 3 Sonnet có context window là bao nhiêu tokens?
        Với 5 chunks (mỗi chunk ~300 tokens), còn bao nhiêu tokens cho conversation?
        """
        try:
            # Construct request body for Claude
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.0
            })

            response = self.bedrock_runtime_client.invoke_model(
                modelId=self.model_id,
                body=body
            )

            # Parse response
            response_body = json.loads(response['body'].read())
            answer = response_body['content'][0]['text']

            return answer

        except Exception as e:
            print(f"Error invoking model: {e}")
            return f"Error generating answer: {str(e)}"

    def retrieve_and_generate(self, query: str) -> Dict[str, Any]:
        """
        Convenience method: Retrieve + Generate in one call.
        Uses Bedrock's built-in RetrieveAndGenerate API.

        ❓ PRACTICE QUESTION 4:
        So sánh method này với việc gọi retrieve() rồi invoke_model() riêng.
        Ưu điểm và nhược điểm của mỗi approach?
        """
        try:
            response = self.bedrock_agent_client.retrieve_and_generate(
                input={
                    'text': query
                },
                retrieveAndGenerateConfiguration={
                    'type': 'KNOWLEDGE_BASE',
                    'knowledgeBaseConfiguration': {
                        'knowledgeBaseId': self.kb_id,
                        'modelArn': f'arn:aws:bedrock:{self.region}::foundation-model/{self.model_id}'
                    }
                }
            )

            return {
                'answer': response['output']['text'],
                'citations': response.get('citations', [])
            }

        except Exception as e:
            print(f"Error in retrieve_and_generate: {e}")
            return {'answer': f"Error: {str(e)}", 'citations': []}


if __name__ == "__main__":
    # Quick test
    client = BedrockClient()

    # Test retrieve
    print("Testing retrieve...")
    result = client.retrieve("What is PaymentGW's API rate limit?")
    print(f"Retrieved {len(result['chunks'])} chunks")
    if result['chunks']:
        print(f"Top chunk score: {result['chunks'][0]['score']:.3f}")
        print(f"Source: {result['chunks'][0]['source']}")

    # Test invoke_model
    print("\nTesting invoke_model...")
    prompt = "Answer in one sentence: What is 2+2?"
    answer = client.invoke_model(prompt)
    print(f"Answer: {answer}")

    print("\n✓ Bedrock client initialized successfully!")
