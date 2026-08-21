import streamlit as st

from laundry_care import LaundryCareWorkflow


st.set_page_config(
    page_title="Laundry Care Agent",
    page_icon="🧺",
    layout="centered",
)


@st.cache_resource
def get_workflow() -> LaundryCareWorkflow:
    return LaundryCareWorkflow()


workflow = get_workflow()

st.title("🧺 Laundry Care Agent")
st.caption(
    "Functional Python prototype demonstrating guardrails, routing, specialist agents, "
    "structured outputs and final-response synthesis."
)

st.info(
    "This is an educational portfolio prototype. Always check the garment care label "
    "before making a real-world laundry decision."
)

example = st.selectbox(
    "Try an example",
    [
        "Write my own request",
        "White wool jumper with a wine stain",
        "Dark polyester shirt with a grease stain",
        "Blue denim jeans with a coffee stain",
        "Out-of-scope request",
    ],
)

examples = {
    "White wool jumper with a wine stain": "How should I wash a white wool jumper with a wine stain?",
    "Dark polyester shirt with a grease stain": "How should I wash a dark polyester shirt with a grease stain?",
    "Blue denim jeans with a coffee stain": "How should I wash blue denim jeans with a coffee stain?",
    "Out-of-scope request": "What is the capital of France?",
}

initial_value = examples.get(example, "")

with st.form("laundry_request_form"):
    user_input = st.text_area(
        "Describe the garment and the problem",
        value=initial_value,
        placeholder="Example: How should I wash a white wool jumper with a wine stain?",
        height=120,
    )
    submitted = st.form_submit_button("Analyse request", use_container_width=True)

if submitted:
    result = workflow.run(user_input)

    st.subheader("Result")

    if result.status == "completed":
        st.success(result.final_response)
    elif result.status == "clarification":
        st.warning(result.final_response)
    else:
        st.error(result.final_response)

    with st.expander("View agent execution trace"):
        st.json(result.trace)

st.divider()

with st.expander("How the workflow works"):
    st.markdown(
        """
1. **Guardrails** validate the request.
2. **Laundry Request Classifier** decides whether it belongs to the supported domain.
3. **Fabric Agent** identifies material-related constraints.
4. **Color Agent** adds colour-protection rules.
5. **Stain Agent** adds stain-treatment guidance.
6. **Final Instruction Agent** combines the specialist outputs into one response.
7. Out-of-scope requests are routed to the **Clarification Agent**.
        """
    )

st.caption(
    "Current implementation: deterministic, rule-based Python workflow. "
    "No external LLM API or paid service is required."
)
