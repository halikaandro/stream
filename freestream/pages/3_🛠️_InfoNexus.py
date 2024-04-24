import json
import operator
import os
from typing import Annotated, Sequence, TypedDict

import streamlit as st
from langchain import hub
from langchain.agents import load_tools
from langchain.memory import ConversationBufferMemory
from langchain.tools.retriever import create_retriever_tool
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_message_histories import \
    StreamlitChatMessageHistory
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import BaseMessage, FunctionMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai import ChatOpenAI, OpenAI
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from pages import RetrieveDocuments, StreamHandler, footer

# Initialize LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "FreeStream-v4.0.0"
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets.LANGCHAIN.LANGCHAIN_ENDPOINT
os.environ["LANGCHAIN_API_KEY"] = st.secrets.LANGCHAIN.LANGCHAIN_API_KEY
os.environ["TAVILY_API_KEY"] = st.secrets.TAVILY.TAVILY_API_KEY

# Set up page config
st.set_page_config(page_title="FreeStream: InfoNexus", page_icon="🛠️")

st.title("🛠️ InfoNexus")
st.subheader(":green[Leverages Tavily Web Search to Answer Questions.]")
st.caption(":violet[Powered by GPT-3.5-Turbo]")
st.divider()
# Show footer
st.markdown(footer, unsafe_allow_html=True)

# Add temperature header
temperature_header = st.sidebar.markdown(
    """
    ## Temperature Slider
    """
)
# Add the sidebar temperature slider
temperature_slider = st.sidebar.slider(
    label=""":orange[Set LLM Temperature]. The :blue[lower] the temperature, the :blue[less] random the model will be. The :blue[higher] the temperature, the :blue[more] random the model will be.""",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.05,
    key="llm_temperature",
)

# Set our Agent's Chat Model
model = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=temperature_slider,
    openai_api_key=st.secrets.OPENAI.openai_api_key,
    streaming=True,
)

# Set a model for tools
# Requires an 'LLM' not 'Chat Model'
toollm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=temperature_slider,
    openai_api_key=st.secrets.OPENAI.openai_api_key,
    streaming=True,
)

# Instantiate tools
tavily_search = TavilySearchResults()
toolbox = [tavily_search]
toolbox = toolbox + load_tools(tool_names=["llm-math"], llm=toollm)

prompt = hub.pull("daethyra/openai-tools-agent")

# Instantiate the tool executor
tool_executor = ToolExecutor(toolbox)

# Convert the tools to OpenAI functions
functions = [convert_to_openai_function(t) for t in toolbox]
model = model.bind_functions(functions)


class AgentState(TypedDict):
    """
    A TypedDict representing the state of an agent in the FreeStream application.

    This class is used to define the structure of the agent's state, which includes
    a sequence of messages exchanged between the agent and the user. The messages are annotated
    with an operator function, specifically `operator.add`, which is used to aggregate
    the messages in the sequence.

    Attributes:
        messages (Annotated[Sequence[BaseMessage], operator.add]): A sequence of BaseMessage
            instances representing the conversation history between the agent and the user. The
            `Annotated` type hint is used to specify that the `operator.add` function
            should be used to aggregate the messages in this sequence.
    """

    messages: Annotated[Sequence[BaseMessage], operator.add]


# Define the function that determines whether to continue or not
def should_continue(state):
    """
    Determines whether the agent should continue processing based on the last message in the state.

    This function checks the last message in the agent's state to determine if there is a function call.
    If there is no function call in the last message, it returns "end", indicating that the agent should stop processing.
    If there is a function call, it returns "continue", indicating that the agent should continue processing.

    Args:
        state (AgentState): The current state of the agent, which includes a sequence of messages.

    Returns:
        str: "end" if there is no function call in the last message, "continue" otherwise.
    """
    messages = state["messages"]
    last_message = messages[-1]
    # If there is no function call, then we finish
    if "function_call" not in last_message.additional_kwargs:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


# Define the function that calls the model
def call_model(state):
    """
    Invokes the model with the current state's messages and returns the model's response.

    This function retrieves the messages from the agent's state and invokes the model with these messages.
    The response from the model is then wrapped in a dictionary with the key "messages" and returned.
    This response will be added to the existing list of messages in the agent's state.

    Args:
        state (AgentState): The current state of the agent, which includes a sequence of messages.

    Returns:
        dict: A dictionary containing the model's response wrapped in a list under the key "messages".
    """
    messages = state["messages"]
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


# Define the function to execute tools
def call_tool(state):
    """
    Executes a specified tool based on the last message in the state and returns the tool's response.

    This function extracts the tool name and input from the last message in the agent's state.
    It then constructs a ToolInvocation object and invokes the tool using the tool_executor.
    The response from the tool is wrapped in a FunctionMessage and returned in a dictionary
    under the key "messages". This response will be added to the existing list of messages in the agent's state.

    Args:
        state (AgentState): The current state of the agent, which includes a sequence of messages.

    Returns:
        dict: A dictionary containing the tool's response wrapped in a FunctionMessage under the key "messages".
    """
    messages = state["messages"]
    # Based on the continue condition
    # we know the last message involves a function call
    last_message = messages[-1]
    # We construct an ToolInvocation from the function_call
    action = ToolInvocation(
        tool=last_message.additional_kwargs["function_call"]["name"],
        tool_input=json.loads(
            last_message.additional_kwargs["function_call"]["arguments"]
        ),
    )
    # We call the tool_executor and get back a response
    response = tool_executor.invoke(action)
    # We use the response to create a FunctionMessage
    function_message = FunctionMessage(content=str(response), name=action.tool)
    # We return a list, because this will get added to the existing list
    return {"messages": [function_message]}


# Define a new graph
workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.set_entry_point("agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
    # Finally we pass in a mapping.
    # The keys are strings, and the values are other nodes.
    # END is a special node marking that the graph should finish.
    # What will happen is we will call `should_continue`, and then the output of that
    # will be matched against the keys in this mapping.
    # Based on which one it matches, that node will then be called.
    {
        # If `tools`, then we call the tool node.
        "continue": "action",
        # Otherwise we finish.
        "end": END,
    },
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("action", "agent")

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
app = workflow.compile()

# Setup memory for contextual conversation
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(
    memory_key="chat_history", chat_memory=msgs, return_messages=True
)
from langchain.memory import ChatMessageHistory
memory = ChatMessageHistory(session_id="test-session")
agent_with_chat_history = RunnableWithMessageHistory(
    app,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# Button to clear conversation history
if st.sidebar.button("Clear message history"):
    msgs.clear()

# Display coversation history window
avatars = {"human": "user", "ai": "assistant"}
for msg in msgs.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

output_container = st.empty()

# Display user input field and enter button
if user_query := st.chat_input(placeholder="Ask me anything!"):
    st.chat_message("user").write(user_query)
    
    # Display assistant response
    with st.chat_message("assistant"):
        user_query = {"messages": [HumanMessage(content=user_query)]}
        for output in agent_with_chat_history.stream(user_query, config={"configurable": {"session_id": "placeholder_id"}}):
            # stream() yields dictionaries with output keyed by node name
            for key, value in output.items():
                if key.upper() == "ACTION":
                    with st.expander(label=f"EXECUTING \"{key.upper()}\"", expanded=False):
                        content = value['messages'][0].content
                        st.markdown(content)
                else:
                    content = value['messages'][0].content
                    st.markdown(f"""`Output from \"{key.upper()}\":`\n\n""" + content)
                    # I really don't like this `app`. I'd rather use implement something compatible with `StreamlitCallbackhandler`
            st.markdown("\n---\n")
    st.success("Done thinking.", icon="✅")
