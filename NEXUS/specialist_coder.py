import importlib.util
import sys

spec = importlib.util.spec_from_file_location("SpecialistAgent", "./nexus-specialist-template.py")
if spec is None or spec.loader is None:
    raise ImportError("Could not load SpecialistAgent from nexus-specialist-template.py")
module = importlib.util.module_from_spec(spec)
sys.modules["SpecialistAgent"] = module
spec.loader.exec_module(module)
SpecialistAgent = module.SpecialistAgent

class CoderSpecialist(SpecialistAgent):
    def __init__(self, model_path=None):
        super().__init__(domain="programming", model_path=model_path)

    def process_query(self, aicl_message):
        # Programming-specific query processing (placeholder)
        return {"code": "print('Hello, World!')"}

    def generate_response(self, processed_query):
        # Generate code response (placeholder)
        return f"Here is your code: {processed_query['code']}" 