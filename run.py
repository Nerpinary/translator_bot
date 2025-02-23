import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.main import main

if __name__ == '__main__':
    main() 