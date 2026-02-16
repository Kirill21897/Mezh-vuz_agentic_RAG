import sys
import logging
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.core.data_loader import DataLoader
from src.core.formatter import generate_universities_section_md, generate_programs_section_md, generate_metadata_section_md
from src.core.config import PROCESSED_DATA_DIR, LOG_FORMAT

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

def main():
    logger.info("Generating knowledge corpus (Markdown) for RAG...")
    
    loader = DataLoader()
    
    try:
        universities_df = loader.load_universities()
        programs_df = loader.load_programs()
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return

    markdown_parts = []
    
    # Header
    markdown_parts.append("# База знаний: Университеты и Образовательные программы\n")
    markdown_parts.append("*Автоматически сгенерированный корпус для RAG системы*\n")
    
    # Sections
    if universities_df is not None:
        markdown_parts.append(generate_universities_section_md(universities_df))
    
    if programs_df is not None:
        markdown_parts.append(generate_programs_section_md(programs_df))
    
    # Metadata
    markdown_parts.append(generate_metadata_section_md())
    
    # Save
    knowledge_corpus = "\n".join(markdown_parts)
    output_file = PROCESSED_DATA_DIR / "knowledge_corpus.md"
    output_file.write_text(knowledge_corpus, encoding="utf-8")
    
    logger.info("="*60)
    logger.info(f" Done!")
    logger.info(f" File: {output_file.name}")
    logger.info(f" Size: {len(knowledge_corpus):,} chars")
    logger.info(f" Path: {output_file.absolute()}")
    logger.info("="*60)

if __name__ == "__main__":
    main()
