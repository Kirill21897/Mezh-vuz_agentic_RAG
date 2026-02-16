import pandas as pd
import logging
from pathlib import Path
from src.core.config import RAW_DATA_DIR

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, raw_data_dir: Path = RAW_DATA_DIR):
        self.raw_data_dir = raw_data_dir

    def load_csv_safely(self, file_path: Path) -> pd.DataFrame:
        """Loads CSV with automatic encoding detection"""
        encodings = ['utf-8', 'cp1251', 'latin1']
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                logger.info(f"✓ Loaded {file_path.name}: {len(df)} rows")
                return df
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Could not read {file_path.name}")

    def load_universities(self) -> pd.DataFrame:
        path = self.raw_data_dir / "universities.csv"
        if not path.exists():
            raise FileNotFoundError(f"Universities file not found: {path}")
        
        df = self.load_csv_safely(path)
        # Type casting
        if "university_id" in df.columns:
             df["university_id"] = df["university_id"].astype(int)
        if "is_active" in df.columns:
             df["is_active"] = df["is_active"].astype(bool)
        return df

    def load_programs(self) -> pd.DataFrame:
        path = self.raw_data_dir / "programs.csv"
        if not path.exists():
            raise FileNotFoundError(f"Programs file not found: {path}")
            
        df = self.load_csv_safely(path)
        # Type casting
        if "university_id" in df.columns:
             df["university_id"] = df["university_id"].astype(int)
        if "is_active" in df.columns:
             df["is_active"] = df["is_active"].astype(bool)
        return df

    def get_merged_active_programs(self) -> pd.DataFrame:
        """Returns a merged DataFrame of active programs and active universities."""
        univ_df = self.load_universities()
        prog_df = self.load_programs()

        # Merge
        merged = prog_df.merge(univ_df, on="university_id", how="inner", suffixes=("_prog", "_univ"))

        # Filter active
        # Check if columns exist before filtering, to be safe
        if "is_active_prog" in merged.columns and "is_active_univ" in merged.columns:
            active = merged[(merged["is_active_prog"]) & (merged["is_active_univ"])]
            return active
        else:
            logger.warning("Could not filter by is_active columns. Returning merged data.")
            return merged
