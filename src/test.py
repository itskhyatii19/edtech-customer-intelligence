import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.pipelines.predict_pipeline import run_pipeline

result = run_pipeline()
print(result)