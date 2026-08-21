from .agents import (
    ClarificationAgent,
    ColorAgent,
    FabricAgent,
    FinalInstructionAgent,
    Guardrails,
    LaundryRequestClassifier,
    StainAgent,
    serialise_analysis,
)
from .models import WorkflowResult


class LaundryCareWorkflow:
    """Sequential orchestration matching the project architecture."""

    def __init__(self) -> None:
        self.guardrails = Guardrails()
        self.classifier = LaundryRequestClassifier()
        self.fabric_agent = FabricAgent()
        self.color_agent = ColorAgent()
        self.stain_agent = StainAgent()
        self.final_agent = FinalInstructionAgent()
        self.clarification_agent = ClarificationAgent()

    def run(self, user_input: str) -> WorkflowResult:
        allowed, message = self.guardrails.validate(user_input)
        trace = {"input": user_input, "guardrails": {"allowed": allowed, "message": message}}

        if not allowed:
            return WorkflowResult(status="rejected", final_response=message, trace=trace)

        in_scope = self.classifier.classify(user_input)
        trace["classifier"] = {"laundry_care": in_scope}

        if not in_scope:
            response = self.clarification_agent.respond()
            trace["route"] = "clarification"
            return WorkflowResult(status="clarification", final_response=response, trace=trace)

        fabric = self.fabric_agent.analyse(user_input)
        color = self.color_agent.analyse(user_input, fabric)
        stain = self.stain_agent.analyse(user_input, fabric)

        trace["route"] = "laundry-care"
        trace["fabric_agent"] = serialise_analysis(fabric)
        trace["color_agent"] = serialise_analysis(color)
        trace["stain_agent"] = serialise_analysis(stain)

        final_response = self.final_agent.synthesise(fabric, color, stain)
        trace["final_instruction_agent"] = {"response": final_response}

        return WorkflowResult(status="completed", final_response=final_response, trace=trace)
