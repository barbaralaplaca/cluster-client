from pathlib import Path

import dotenv

dotenv.load_dotenv(dotenv_path=f"{Path(__file__).parent.parent}/.env.test", override=True)
