import importlib.util
import sys

spec = importlib.util.spec_from_file_location("SpecialistAgent", "./nexus-specialist-template.py")
if spec is None or spec.loader is None:
    raise ImportError("Could not load SpecialistAgent from nexus-specialist-template.py")
module = importlib.util.module_from_spec(spec)
sys.modules["SpecialistAgent"] = module
spec.loader.exec_module(module)
SpecialistAgent = module.SpecialistAgent

class BuilderSpecialist(SpecialistAgent):
    def __init__(self, model_path=None):
        super().__init__(domain="construction", model_path=model_path)

    def process_query(self, aicl_message):
        # Construction-specific query processing (placeholder)
        return {"steps": ["Measure area", "Select materials", "Build frame", "Install decking"]}

    def generate_response(self, processed_query):
        # Generate a step-by-step guide (placeholder)
        return "Step-by-step guide to building a deck: " + ", ".join(processed_query["steps"]) 