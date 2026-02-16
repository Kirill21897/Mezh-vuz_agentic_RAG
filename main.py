import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.rag.agent import RAGAgent

def main():
    print("Initializing Agentic RAG...")
    try:
        agent = RAGAgent()
    except Exception as e:
        print(f"Error initializing agent: {e}")
        return

    print("\n" + "="*50)
    print("Welcome to the Academic Exchange RAG Agent!")
    print("Ask me about exchange programs, universities, or requirements.")
    print("Type 'exit' or 'quit' to stop.")
    print("="*50 + "\n")

    while True:
        try:
            query = input("You: ")
            if query.lower() in ['exit', 'quit', 'выход']:
                break
            
            if not query.strip():
                continue

            response = agent.process_query(query)
            print("\nAgent:")
            print(response.answer)
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError processing query: {e}")

if __name__ == "__main__":
    main()
