import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document


st.set_page_config(page_title="BNS Legal Assistant", layout="wide")
st.title("Bharatiya Nyaya Sanhita (BNS) Legal Assistant")
st.caption("Offline AI System | Replacing IPC with BNS 2023 | 100% Privacy Preserved")


@st.cache_resource
def load_db():
    embeddings = HuggingFaceEmbeddings(model_name="./my_offline_model")
    db = Chroma(persist_directory="./bns_vector_db", embedding_function=embeddings)
    return db

db = load_db()


system_prompt = (
    "You are an expert Indian Legal Advisor specialized in the Bharatiya Nyaya Sanhita (BNS) 2023. "
    "Use the following pieces of retrieved context to answer the question. "
    "If you don't know the answer, say that you don't know. "
    "\n\n"
    "RULES:\n"
    "1. Identify the specific BNS Section numbers relevant to the crime.\n"
    "2. Classify the offense as COGNIZABLE (Police can arrest) or NON-COGNIZABLE if possible.\n"
    "3. State the PUNISHMENT clearly.\n"
    "\n\n"
    "CONTEXT FROM BNS DATABASE:\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


llm = ChatOllama(model="mistral")


col1, col2 = st.columns([1, 1])

with col1:
    st.info("Describe the Incident")
    user_query = st.text_area("Enter details", placeholder="e.g., My neighbor threatened to hit me...", height=150)
    analyze_btn = st.button("Analyze Incident (Offline)")

with col2:
    if analyze_btn and user_query:
        with st.spinner("Searching BNS Sections..."):
            try:
                docs = db.similarity_search(user_query, k=3)
                
                context_text = "\n\n".join([doc.page_content for doc in docs])
                
                formatted_prompt = prompt.format_messages(context=context_text, input=user_query)
                
                response = llm.invoke(formatted_prompt)
                
                st.success("Legal Analysis")
                st.markdown(response.content)

                st.warning("Source Sections (Evidence)")
                for doc in docs:
                    section_id = doc.metadata.get('Section', 'Unknown')
                    offense_name = doc.metadata.get('Section _name', 'N/A')
                    
                    with st.expander(f"Section {section_id}: {offense_name}"):
                        st.write(doc.page_content)
            
            except Exception as e:
                st.error(f"Error: {e}")


st.sidebar.markdown("### System Status")
st.sidebar.success("Database: Connected (Local)")
st.sidebar.success("Model: Mistral (Offline)")
st.sidebar.info("Data Source: Official BNS Gazette 2023")