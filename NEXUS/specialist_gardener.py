import importlib.util
import sys

spec = importlib.util.spec_from_file_location("SpecialistAgent", "./nexus-specialist-template.py")
if spec is None or spec.loader is None:
    raise ImportError("Could not load SpecialistAgent from nexus-specialist-template.py")
module = importlib.util.module_from_spec(spec)
sys.modules["SpecialistAgent"] = module
spec.loader.exec_module(module)
SpecialistAgent = module.SpecialistAgent

class GardenerSpecialist(SpecialistAgent):
    def __init__(self, model_path=None):
        super().__init__(domain="horticulture", model_path=model_path)

    def process_query(self, aicl_message):
        # Gardening-specific query processing (placeholder)
        return {"advice": "Water your plants in the morning and use mulch to retain moisture."}

    def generate_response(self, processed_query):
        # Generate gardening advice (placeholder)
        return f"Gardening tip: {processed_query['advice']}" 