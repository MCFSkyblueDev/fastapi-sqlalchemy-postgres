import pkgutil
import importlib
from app.config.database import Base  # Import Base to attach models

# Dynamically import all models in the models directory
def import_models():
    package_path = __path__  # Path to models/
    package_name = __name__  # "app.models"

    for _, module_name, _ in pkgutil.iter_modules(package_path):
        importlib.import_module(f"{package_name}.{module_name}")

import_models()

# __all__ = Base.__subclasses__() 