import streamlit as st

from freestream import footer

st.set_page_config(
    page_title="FreeStream: Chatbots for specific use-cases", page_icon="🏡"
)

st.title("FreeStream")
st.header(":green[_Chatbots, tuned for specific use-cases_]", divider="red")
# Project Overview
st.subheader(":blue[What is FreeStream?]")
# Show footer
st.markdown(footer, unsafe_allow_html=True)


st.write(
    """
    FreeStream is a collection of chatbots that are tuned for specific use-cases.
    """
)
st.divider()
st.subheader("What tools are currently available?")
st.write(
    """
    ### :blue[RAGbot]:
    
    :orange[*RAGbot searches files you upload for answers to your questions.*]
    
    The first chatbot made for FreeStream was RAGbot. It's great for asking specific questions about long policy documents, summarizing the contents of an article, or synthesizing knowledge from multiple sources, such as legal or scientific documents. You may to upload however many PDFs, Word documents, or plain text files you'd like. You can then pose specific questions directly related to the content of your documents.
    """
)

with st.expander(label=":violet[RAGbot workflow:]", expanded=False):
    st.markdown(
        """
        1. Upload Documents:  Upload your documents to RAGbot.
        
        2. Document Splitting:  RAGbot splits your documents into chunks for further processing.
        
        3. Embedding Generation:  The chunks of text are turned into vector embeddings, which basically means the data is standardized into numerical representations.
        
        4. Retriever Creation and Indexing:  The vector embeddings are sorted into a vector database using FAISS.
        
        5. Context Retrieval: Upon being asked a question, the retriever returns the relevant context from the vector database.
        
        6. Context Relevance Validation:  To safeguard against errors, the system only generates a response if the retrieved context is sufficiently relevant to aide the AI's response.
        
        7. Question Answering:  The system meticulously answers your question, drawing knowledge exclusively from the retrieved content.
        """
    )


st.write(
    """
    ### :blue[Curie]:
    
    :orange[*This base chatbot is a more general purpose version of RAGbot. It's quicker and more focused on the user due to its system prompt and the lack of a retriever.*]
    
    Curie is perfect for venting your thoughts, getting constructive feedback on something you wrote, helping you make sense of things. Plus you don't have to upload any files. It's great for stuffing context into your questions when you use the Claude Haiku model. Specifically, it's been told to actively assist users in comprehending reality using their curiousity and critical thinking skills. It has a tendency to nudge you towards answers rather than giving them away, which is great for learning.
    """
)

with st.expander(label=":violet[System Prompt:]", expanded=False):
    st.markdown(
        """
        *You are a friendly AI chatbot designed to assist users in comprehending reality, exploring their curiosity, and practicing critical thinking skills. Your role is to guide users towards the right answers by providing thoughtful, well-reasoned responses. When faced with a question, decompose the problem into smaller, manageable parts and reason through each step systematically. This approach will help you provide comprehensive and accurate answers. Remember, your goal is to enhance learning and understanding, so only provide direct advice when explicitly asked to do so. Always strive to provide responses that are relevant, accurate, and contextually appropriate.*
        """
    )

st.write(
    """
    ### :blue[InfoNexus]:
    
    :orange[*The InfoNexus is an agent-based chatbot that thinks in cycles in order to accomplish answer a user's query.*]
    
    In the typical chatbot pages, your AI assistant would perform a set of actions in a linear fashion, one time through. InfoNexus is different because it operates off of a predefined workflow, which allows it to work in cycles, meaning it can decide what to do based on its available set of tools.
    
    For now, it only has the Tavily Search API, which is a "search engine built specifically for AI agents (LLMs), delivering real-time, accurate, and factual results at speed." This chatbot is a work in progress, and currently non-conversational, which means it can only answer questions in a single-shot fashion, and cannot remember previous queries.
    """
)
with st.expander(label=":violet['Agent' description:]", expanded=False):
    st.markdown("""
        The AI assistant is therefore an "Agent" because it decides when to use a tool based on its ability to answer the user appropriately. This agent is then operated as a "State machine" in the sense that the underlying large language model changes the contents of the "state" based on the output of a node. Think of nodes as points in the AI's workflow.
        """
    )
    
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

