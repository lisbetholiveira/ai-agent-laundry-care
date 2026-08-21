import unittest

from laundry_care import LaundryCareWorkflow


class LaundryCareWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = LaundryCareWorkflow()

    def test_white_wool_wine_example(self) -> None:
        result = self.workflow.run("How should I wash a white wool jumper with a wine stain?")

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.trace["fabric_agent"]["fabric"], "wool")
        self.assertEqual(result.trace["color_agent"]["color_group"], "white")
        self.assertEqual(result.trace["stain_agent"]["stain"], "wine")
        self.assertIn("cold", result.final_response.lower())
        self.assertIn("care label", result.final_response.lower())

    def test_out_of_scope_request_routes_to_clarification(self) -> None:
        result = self.workflow.run("What is the capital of France?")

        self.assertEqual(result.status, "clarification")
        self.assertEqual(result.trace["route"], "clarification")

    def test_empty_request_is_rejected(self) -> None:
        result = self.workflow.run("   ")

        self.assertEqual(result.status, "rejected")
        self.assertFalse(result.trace["guardrails"]["allowed"])

    def test_synthetic_dark_grease_flow(self) -> None:
        result = self.workflow.run("Dark polyester shirt with a grease stain")

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.trace["fabric_agent"]["fabric"], "synthetic")
        self.assertEqual(result.trace["color_agent"]["color_group"], "dark")
        self.assertEqual(result.trace["stain_agent"]["stain"], "grease")


if __name__ == "__main__":
    unittest.main()
