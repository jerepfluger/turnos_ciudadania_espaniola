import os
import sys

from dotenv import load_dotenv
from dynaconf import Dynaconf

ALLOWED_ENVS = ['DEV', "BETA", 'PROD']
ENVIRONMENT = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ALLOWED_ENVS else 'DEV'

config_files = ['config.yaml']
if ENVIRONMENT == 'BETA':
    config_files.append('config-BETA.yaml')
if ENVIRONMENT == 'PROD':
    config_files.append('config-PROD.yaml')

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv('.env')
settings = Dynaconf(
    settings_files=config_files,
    envvar_prefix=False,
)


def expand_env_vars(obj):
    """Recursively expands environment variables in strings."""
    if isinstance(obj, dict):
        return {k: expand_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [expand_env_vars(v) for v in obj]
    elif isinstance(obj, str):
        return os.path.expanduser(os.path.expandvars(obj))
    return obj  # Return as is if it's not a string, dict, or list


# Expand all settings
expanded_settings = expand_env_vars(settings.as_dict())

# Update Dynaconf settings with expanded values
settings.update(expanded_settings)
