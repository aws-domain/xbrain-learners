"""
Bedrock Agent Client - Wrapper for invoking Bedrock Agent with tools
"""
import boto3
import json
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


class BedrockAgentClient:
    """
    Client for interacting with Bedrock Agent (L3 - with tools).

    ❓ PRACTICE QUESTION 1:
    So sánh BedrockClient (L1/L2) vs BedrockAgentClient (L3):
    - L1/L2: Gọi trực tiếp bedrock-runtime
    - L3: Gọi bedrock-agent-runtime với agent_id

    Tại sao cần agent_id? Agent làm gì khác với model invoke?
    """

    def __init__(self):
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        self.agent_id = os.getenv('BEDROCK_AGENT_ID')
        self.agent_alias_id = os.getenv('BEDROCK_AGENT_ALIAS_ID', 'TSTALIASID')

        if not self.agent_id:
            raise ValueError("BEDROCK_AGENT_ID environment variable is required for L3")

        self.client = boto3.client(
            'bedrock-agent-runtime',
            region_name=self.region
        )

    def invoke_agent(self, query: str, session_id: str = None, enable_trace: bool = False) -> Dict[str, Any]:
        """
        Invoke Bedrock Agent with a query.

        Args:
            query: User's question
            session_id: Session ID for conversation continuity (L4 will use this)
            enable_trace: If True, return detailed trace of agent actions

        Returns:
            Dict with answer, citations, and trace (if enabled)

        ❓ PRACTICE QUESTION 2:
        enable_trace=True cho phép bạn xem:
        - Agent reasoning steps
        - Tool calls made
        - KB retrievals
        - Final answer generation

        Khi nào nên enable trace?
        - Development/debugging?
        - Production monitoring?
        - User-facing responses?
        """
        if not session_id:
            import uuid
            session_id = str(uuid.uuid4())

        try:
            response = self.client.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.agent_alias_id,
                sessionId=session_id,
                inputText=query,
                enableTrace=enable_trace
            )

            # Parse streaming response
            answer_parts = []
            citations = []
            traces = []

            event_stream = response['completion']

            for event in event_stream:
                if 'chunk' in event:
                    chunk = event['chunk']
                    if 'bytes' in chunk:
                        text = chunk['bytes'].decode('utf-8')
                        answer_parts.append(text)

                if 'trace' in event and enable_trace:
                    traces.append(event['trace'])

            answer = ''.join(answer_parts)

            return {
                'answer': answer,
                'session_id': session_id,
                'citations': citations,
                'traces': traces if enable_trace else None
            }

        except Exception as e:
            print(f"Error invoking agent: {e}")
            return {
                'answer': f"Error: {str(e)}",
                'session_id': session_id,
                'citations': [],
                'traces': None
            }

    def parse_trace(self, traces: list) -> Dict[str, Any]:
        """
        Parse agent trace to extract useful debugging info.

        ❓ PRACTICE QUESTION 3:
        Agent trace chứa:
        - orchestrationTrace: Agent reasoning
        - preProcessingTrace: Input processing
        - postProcessingTrace: Output formatting

        Với câu hỏi "What is PaymentGW's current latency?",
        trace sẽ show agent:
        1. Nhận diện cần tool nào?
        2. Gọi tool với params gì?
        3. Nhận response như thế nào?
        4. Generate answer ra sao?
        """
        if not traces:
            return {}

        tool_calls = []
        kb_retrievals = []
        reasoning_steps = []

        for trace in traces:
            trace_data = trace.get('trace', {})

            # Extract tool invocations
            if 'orchestrationTrace' in trace_data:
                orch = trace_data['orchestrationTrace']
                if 'invocationInput' in orch:
                    tool_calls.append(orch['invocationInput'])
                if 'observation' in orch:
                    reasoning_steps.append(orch['observation'])

            # Extract KB retrievals
            if 'retrievalTrace' in trace_data:
                kb_retrievals.append(trace_data['retrievalTrace'])

        return {
            'tool_calls': tool_calls,
            'kb_retrievals': kb_retrievals,
            'reasoning_steps': reasoning_steps
        }


if __name__ == "__main__":
    """
    ❓ PRACTICE QUESTION 4:
    Test agent với các loại câu hỏi:

    1. KB-only question:
       "What is PaymentGW's authentication method?"
       → Agent không gọi tool, chỉ dùng KB

    2. Tool-only question:
       "What is PaymentGW's current latency?"
       → Agent gọi get_service_metrics

    3. KB + Tool question:
       "Is PaymentGW meeting its SLA?"
       → Agent gọi tool + retrieve từ KB + synthesize

    Observe trace để hiểu agent decision-making.
    """
    print("Testing Bedrock Agent Client...\n")

    try:
        client = BedrockAgentClient()

        # Test query
        query = "What is PaymentGW's current p99 latency?"
        print(f"Query: {query}\n")

        result = client.invoke_agent(query, enable_trace=True)

        print(f"Answer: {result['answer']}\n")

        if result['traces']:
            trace_info = client.parse_trace(result['traces'])
            print(f"Tool calls: {len(trace_info['tool_calls'])}")
            print(f"KB retrievals: {len(trace_info['kb_retrievals'])}")

        print("\n✓ Agent client working!")

    except ValueError as e:
        print(f"⚠️  {e}")
        print("\nTo use L3, you need to:")
        print("1. Create Bedrock Agent in AWS Console")
        print("2. Set BEDROCK_AGENT_ID in .env")
        print("3. Deploy Lambda functions for tools")
