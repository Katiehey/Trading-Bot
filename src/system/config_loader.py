import yaml
import os
from dotenv import load_dotenv

class Config:
    """Loads YAML configuration and provides typed accessors; reads API keys from the environment."""

    def __init__(self, path="config/config.yaml"):
        """Load config from path and populate environment variables from .env."""
        load_dotenv()
        with open(path, "r") as f:
            self.cfg = yaml.safe_load(f)

    def get(self, section, key=None):
        """Return a section dict or a specific key value from the loaded YAML."""
        if key:
            return self.cfg[section][key]
        return self.cfg[section]

    def api_keys(self):
        return {
            "apiKey": os.getenv("TEST_API_KEY"),
            "secret": os.getenv("TEST_SECRET")
        }
