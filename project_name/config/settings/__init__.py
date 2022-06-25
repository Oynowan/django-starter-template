import environ
from .base import *

env = environ.Env()
env.read_env()

if env.str('ENV_VAR', default=None) == "dev":
    from .dev import *
else:
    from .prod import *
