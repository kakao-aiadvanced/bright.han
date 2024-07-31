from pprint import pprint
from typing import List

import streamlit as st
from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph
from typing_extensions import TypedDict

from agent import web_search, retrieve, grade_documents, generate, decide_to_generate, \
    grade_generation_v_documents_and_question


## State
class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents
    """

    question: str
    generation: str
    web_search: str
    documents: List[str]


def addNode(workflow: StateGraph):
    # Define the nodes
    workflow.add_node("websearch", web_search)  # web search
    workflow.add_node("retrieve", retrieve)  # retrieve
    workflow.add_node("generate", generate)  # generatae
    workflow.add_node("relevance_checker", grade_documents)  # grade documents


def buildGraph(workflow: StateGraph) -> CompiledGraph:
    # Build graph
    workflow.set_entry_point("retrieve")

    workflow.add_edge("retrieve", "relevance_checker")
    workflow.add_conditional_edges(
        "relevance_checker",
        decide_to_generate,
        {
            "websearch": "websearch",
            "generate": "generate",
        },
    )
    workflow.add_edge("websearch", "relevance_checker")
    workflow.add_conditional_edges(
        "generate",
        grade_generation_v_documents_and_question,
        {
            "not supported": "generate",
            "useful": END,
            "not useful": "generate",
        },
    )

    return workflow.compile()


def runStreamlit(inputs):
    st.title("Research Assistant powered by OpenAI")
    input_topic = st.text_input(
        ":female-scientist: Enter a topic",
        value=inputs,
    )
    generate_report = st.button("Generate Report")
    if generate_report:
        with st.spinner("Generating Report"):
            inputs = {"question": input_topic}
            for output in app.stream(inputs):
                for key, value in output.items():
                    print(f"Finished running: {key}:")
            final_report = value["generation"]
            st.markdown(final_report)
    st.sidebar.markdown("---")
    if st.sidebar.button("Restart"):
        st.session_state.clear()
        st.experimental_rerun()


def PrintAsCommand(inputs):
    question = {"question": inputs}
    for output in app.stream(question):
        for key, value in output.items():
            pprint(f"Finished running: {key}:")
    pprint(value["generation"])


if __name__ == '__main__':
    workflow = StateGraph(GraphState)
    addNode(workflow)
    app = buildGraph(workflow)

    PrintAsCommand("What is telsa???")

    # ----------------------------------------------------------------------
    # Streamlit 앱 UI
    # runStreamlit("What is telsa???")
