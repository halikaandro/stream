import streamlit as st

from freestream import footer

st.set_page_config(
    page_title="FreeStream: Unlimited Access to AI Tools", page_icon="🏡"
)

st.title("FreeStream")
st.header(":green[_Unlimited Access to AI Tools_]", divider="red")
# Project Overview
st.subheader(":blue[What is FreeStream?]")
# Show footer
st.markdown(footer, unsafe_allow_html=True)


st.write(
    """
    AI tools often seem complex or even intimidating, but FreeStream aims to change that. This project is about making AI accessible and understandable, showing how it can solve real-world problems in your daily life.
    """
)
st.divider()
st.subheader("What tools are currently available?")
st.write(
    """
    ### :blue[RAGbot]:
    
    :orange[*RAGbot can answer your questions directly from the documents you provide.*]
    
    This system empowers you to upload PDFs, Word documents, or plain text files. You can then pose specific questions directly related to the content of your documents.  Inspired by AlphaCodium's flow engineering techniques, it works as follows:
    """
)

with st.expander(label="RAGbot Guardrails for Text Generation", expanded=False):
    st.markdown(
        """
        1) Documentation Ingestion:  A long-context LLM carefully processes your uploaded documentation.

        2) Question Answering:  The system meticulously answers your question, drawing knowledge exclusively from the provided documents.

        3) Context Relevance Validation:  To safeguard against errors, the system only generates a response if the retrieved context is sufficiently relevant to aide the AI's response.
        """
    )


st.write(
    """
    ### :blue[Chatbot]:
    
    :orange[*This base Chatbot is a more general purpose version of RAGbot. It allows you to have a conversation with your choice of drop-in LLM without having to upload any files.*]
    
    Chatbot is perfect for venting your thoughts, getting constructive feedback on something you wrote, helping you make sense of things. Specifically, it's been told to actively assist users in comprehending reality using their curiousity and critical thinking skills. It has a tendency to nudge you towards answers rather than giving them away, which is great for learning. Read the system prompt:
    """
)

with st.expander(label="Chatbot Prompt", expanded=False):
    st.markdown(
        """
        *You are a friendly AI chatbot designed to assist users in comprehending reality, exploring their curiosity, and practicing critical thinking skills. Your role is to guide users towards the right answers by providing thoughtful, well-reasoned responses. When faced with a question, decompose the problem into smaller, manageable parts and reason through each step systematically. This approach will help you provide comprehensive and accurate answers. Remember, your goal is to enhance learning and understanding, so only provide direct advice when explicitly asked to do so. Always strive to provide responses that are relevant, accurate, and contextually appropriate.*
        """
    )

st.write(
    """
    ### :blue[Tool Executor]:
    
    :orange[*The Tool Executor is a chatbot that thinks in cycles in order to accomplish answer a user's query.*]
    
    In the typical chatbot pages, your AI assistant would perform a set of actions in a linear fashion, one time through. Tool Executor is different because it operates off of a predefined workflow, which allows it to work in cycles, meaning it can decide to try different things until it is confident it has the right answer.
    
    The AI assistant is therefore an "Agent" because it decides when to use a tool based on its ability to answer the user appropriately. This agent is then operated as a "State machine" in the sense that the underlying large language model changes the contents of the "state" based on the output of a node. Think of nodes as points in the AI's workflow.
    """
)
# spot to put the workflow diagram
# will use Miro
    
st.write(
    """
    ### :blue[Real-ESRGAN]:
    
    :orange[An image upscaler trained on "pure synthetic data." ]
    
    Real-ESRGAN usually powers image upscaling on those websites with free microservices that limit usage before asking for payment or sign up. We'll never do that here. Normally, Real-ESRGAN is capable of upscaling to arbitrary values, however due to the lack of GPU support on Streamlit Community Cloud, the application may crash if you try upscaling too large of an image or too large of a scale factor.
    """
)

st.divider()

st.markdown(
    """
    #### References
    
    * **[Run This App On Your Own Computer](https://github.com/Daethyra/FreeStream/blob/streamlit/README.md#installation)**
    * **[LLM Service Provider Privacy Policies](https://github.com/Daethyra/FreeStream/blob/streamlit/README.md#privacy-policy)**
    * **[FreeStream's GitHub Repository](https://github.com/Daethyra/FreeStream)**    
    """
)

st.divider()

