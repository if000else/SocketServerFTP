import sys
from pathlib import Path
BASEDIR = Path(__file__).parent.parent
sys.path.append(str(BASEDIR))
from modules import main


if __name__ == "__main__":
    main.run()