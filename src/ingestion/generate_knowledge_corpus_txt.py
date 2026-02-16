import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.core.data_loader import DataLoader
from src.core.formatter import format_program_doc
from src.core.config import PROCESSED_DATA_DIR

def main():
    print("Loading data...")
    loader = DataLoader()
    
    try:
        active_programs = loader.get_merged_active_programs()
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    print(f"Found {len(active_programs)} active programs.")

    documents = []
    for _, row in active_programs.iterrows():
        doc = format_program_doc(row)
        documents.append(doc)

    output_path = PROCESSED_DATA_DIR / "knowledge_corpus.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        for i, doc in enumerate(documents, 1):
            f.write(f"[Программа {i}]\n{doc}\n\n")

    print(f"Successfully created {len(documents)} documents.")
    print(f"File: {output_path}")

if __name__ == "__main__":
    main()
