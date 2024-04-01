# FreeStream

Try out different AI tools.

***TLDR***:
- A Streamlit multi-page application
- AI chatbots for different scenarios:
  - RAGbot - Have an AI generate text based on what you upload
    - Your uploaded files are deleted upon exit
  - Chatbot - Work with a general purpose AI assistant
- All conversation content is traced via LangSmith for developer evaluation
- No sign-ups required

## Table of Contents

- [Quickstart](#quickstart)
  - [Installation](#installation)
- [Description](#description)
  - [Vocabulary](#important-vocabulary)
  - [Current Functionality](#what-can-freestream-do-for-me-currently)
- [Functional Requirements](#functional-requirements)
- [Non-Functional Requirements](#non-functional-requirements)
- [Roadmap](#roadmap)
  - [Thinking Out Loud](#thinking-out-loud) 
  - [Future Functionality Plans](#future-functionality-plans)
- [License](./LICENSE)
- [LLM Providers' Privacy Policies](#llm-providers-privacy-policies)

## Quickstart

This app is hosted via Streamlit Community Cloud, [here](https://freestream.streamlit.app/ "Current Version: 4.0.1")

### Installation

This project uses `poetry` for dependency management because that's what Streamlit Community Cloud uses to deploy the project.

Install it with:
```bash
pip install -U pip && pip install -U poetry
```

Then, install the project's dependencies in a virtual environment using poetry. 

Run:

```bash
poetry install
```

You will need to set all required secrets, which require their own respective accounts.
Make a copy of "template.secrets.toml" and rename it to "secrets.toml" in the root of the project. Fill out each field in the file.

**Need API Keys?**
| **API Platform** | **Link** |
| ---- | ---------- |
| Claude | https://console.anthropic.com/ |
| Google | https://aistudio.google.com/app/apikey |
| Langchain | https://smith.langchain.com/ |
| OpenAI | https://platform.openai.com/api-keys |

You can then start the development server with hot reloading by running:

```bash
poetry run streamlit run ./freestream/🏡_Home.py
```

---

## Description
I originally created this project as a chatbot for law and medical professionals, but I quickly realized a more flexible system would benefit everyone.

#### **Important Vocabulary**

*In order of importance, specific to our learning.*
| **Vocab** | **Definition** |
| ---- | ---------- |
| [Large Language Model](https://en.wikipedia.org/wiki/Large_language_model "Wikipedia: Large language model") | A model that can generate text. |
| [RAG](https://arxiv.org/abs/2005.11401 "Arxiv: 2005.11401") | Retrieval Augmented Generation |
| [C-RAG](https://arxiv.org/abs/2401.15884 "Arxiv: 2401.15884") | Corrective-Retrieval Augmented Generation |
| [Self-RAG](https://arxiv.org/abs/2310.11511 "Arxiv: 2310.11511") | Self-reflective Retrieval Augmented Generation |

### What can FreeStream do for me, currently?

FreeStream functions as a multi-page Streamlit web application, which means it's running on typical web technologies like JavaScript but its actually built using Python. 

There are "bot" pages where you can interact with an LLM of your choosing, for example, GPT-4 or Claude Opus. These pages have vastly different prompt engineering techniques being applied, so you may specifically find the prompts in the code interesting even if you aren't a programmer. The first bot page was "RAGbot," which allows you to upload a file (or files) and ask it questions.

For now, the only non-"bot" page is [*Real-ESRGAN*](./freestream/pages/3_🖼️_Real-ESRGAN.py "Python code"), an image upscaler trained on "pure synthetic data" that can upscale to arbitrary ratios in GPU-supported environments.

#### Functional Requirements

The application **MUST**...
1. Provide a user interface for chatting with the latest large language models.
2. Leverage advanced prompt engineering techniques.
3. Provide a range of chatbot pages, differentiated by their prompt engineering.
4. Let the user "drop-in" their choice of LLM at any time during a conversation.
5. Allow users to perform image upscaling (PDF, JPEG, PNG) without limits.

#### Non-Functional Requirements

The application **SHOULD**...
1. Aim for 24/7 availability.
2. Prioritize ease of navigation
3. Feature a visually appealing seamless interface.
4. Empower non-technical users reactive AI.
5. Let users generate tasks based on their speech

# Roadmap

## Thinking Out Loud
The next bot pages I'd like to make are an AgentExecutor and an advanced state machine using LangGraph. For the AgentExecutor, users could have a general purpose assistant that's more robust than "Chatbot". And for the state machine, I could implement corrective RAG for the first time, or maybe do something like RAPTOR or ColBERT.

### Future Functionality Plans

- [x] Create an RAG chatbot
- [x] Create a general purpose AI chatbot
- [x] Add Gemini-Pro to the model list
- [x] Add Anthropic's Claude 3 model family
- [x] Add AI decision making
  - [ ] Implement Corrective-RAG OR Reflective-RAG
- [x] Turn into a Multi-Page Application (MPA)
  - [x] (Homepage) Add a welcome screen with...
    - [x] a description of the project
    - [x] privacy policy
  - [x] (Page) Migrate RAG SPA code
    - [x] Add "Temperature" slider
  - [x] (Page) Add "Image Upscaler"
    - [x] Multi-file upload
    - [x] File type detection
  - [x] (Page) Real-ESRGAN Image Upscaler
    - [x] Review HuggingFace Spaces's as a potential solution
  - [ ] (Page) Add a "Task Transcriber"
    - [ ] Transcribes microphone input
    - [ ] Use LLM to identify each and every task while grouping some to avoid redundance
    - [ ] Generates text within a predefined task template, for each task identified

---

# [License](./LICENSE)

# LLM Providers' Privacy Policies

- [OpenAI Privacy Policy](https://openai.com/policies/privacy-policy)
- [Google](https://transparency.google/our-policies/privacy-policy-terms-of-service/ "Was unable to find a privacy policy specific to Google AI Studio.")
- [Anthropic](https://support.anthropic.com/en/articles/7996866-how-long-do-you-store-personal-data "Support forum response that may suddenly be obsoleted.")
- [Streamlit](https://streamlit.io/privacy-policy/)

## Additional References

| **Reference** | **Description** |
| ---- | ---------- |
| [ColBERT](https://arxiv.org/abs/2004.12832 "Arxiv: 2004.12832") | Efficient BERT-Based Document Search |
| [RAPTOR](https://arxiv.org/abs/2401.18059 "Arxiv: 2401.18059") | Recursive Abstractive Processing for Tree-Organized Retrieval |