import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import tempfile
import pandas as pd
import base64
import json
from htmlTemplates import css, bot_template, user_template

# Configuración de idioma (puedes añadir más idiomas fácilmente)
TEXTS = {
    "es": {
        "title": "Chatea con tus documentos 📚",
        "question_placeholder": "Haz una pregunta sobre tu documento:",
        "sidebar_title": "Tus documentos",
        "upload_text": "Carga tus archivos (PDF, TXT, CSV)",
        "process_button": "Procesar",
        "processing_text": "Procesando documentos...",
        "success_message": "¡Documentos procesados correctamente!",
        "error_message": "Por favor, sube al menos un documento.",
        "no_docs_message": "Por favor, procesa documentos antes de hacer preguntas.",
        "summarize_button": "Generar Resumen",
        "summarizing_text": "Generando resumen...",
        "summary_success": "¡Resumen generado correctamente!",
        "summary_title": "Resumen del documento",
        "extract_button": "Extraer Datos Estructurados",
        "extracting_text": "Extrayendo datos...",
        "extract_success": "¡Datos extraídos correctamente!",
        "extract_title": "Datos Estructurados Extraídos",
        "clear_data_button": "Borrar datos estructurados",
        "tab1": "Chatea con documentos 📚",
        "tab2": "Chatea con texto ✏️",
        "tab3": "Datos estructurados 📊",
        "ask_text": "Haz una pregunta sobre el texto:",
        "structured_data_info": "Procesa un documento y haz clic en 'Extraer Datos Estructurados' para ver información estructurada aquí.",
        "delete_success": "Datos estructurados borrados.",
        "download_summary": "Descargar resumen",
        "download_structured": "Descargar datos estructurados",
        "download_chat": "Descargar historial de chat",
        "search_placeholder": "Buscar en el documento...",
        "search_results": "Resultados de búsqueda",
        "clear_session": "Limpiar todo",
        "session_cleared": "Sesión reiniciada.",
        "help_title": "¿Cómo funciona la aplicación?",
        "help_content": "- Sube uno o varios documentos en PDF, TXT o CSV.\n- Haz preguntas sobre el contenido en el chat.\n- Extrae resúmenes o datos estructurados automáticamente.\n- Descarga los resultados para usarlos donde quieras."
    },
    "en": {
        "title": "Chat with your documents 📚",
        "question_placeholder": "Ask a question about your documents:",
        "sidebar_title": "Your documents",
        "upload_text": "Upload your files (PDF, TXT, CSV)",
        "process_button": "Process",
        "processing_text": "Processing documents...",
        "success_message": "Documents processed successfully!",
        "error_message": "Please upload at least one document.",
        "no_docs_message": "Please process documents before asking questions.",
        "summarize_button": "Generate Summary",
        "summarizing_text": "Generating summary...",
        "summary_success": "Summary generated successfully!",
        "summary_title": "Document Summary",
        "extract_button": "Extract Structured Data",
        "extracting_text": "Extracting data...",
        "extract_success": "Data extracted successfully!",
        "extract_title": "Extracted Structured Data",
        "clear_data_button": "Clear structured data",
        "tab1": "Chat with documents 📚",
        "tab2": "Chat with text ✏️",
        "tab3": "Structured data 📊",
        "ask_text": "Ask a question about the text:",
        "structured_data_info": "Process a document and click 'Extract Structured Data' to see structured information here.",
        "delete_success": "Structured data cleared.",
        "download_summary": "Download summary",
        "download_structured": "Download structured data",
        "download_chat": "Download chat history",
        "search_placeholder": "Search in document...",
        "search_results": "Search results",
        "clear_session": "Clear all",
        "session_cleared": "Session cleared.",
        "help_title": "How does the app work?",
        "help_content": "- Upload one or more documents (PDF, TXT, CSV).\n- Ask questions about the content in the chat.\n- Automatically extract summaries or structured data.\n- Download results for your own use."
    }
}

class Person(BaseModel):
    name: str = Field(description="Nombre completo de la persona")
    role: Optional[str] = Field(description="Rol o cargo de la persona")

class Date(BaseModel):
    date: str = Field(description="Fecha en formato DD/MM/YYYY o similar")
    context: str = Field(description="Contexto o evento relacionado con la fecha")

class Figure(BaseModel):
    value: str = Field(description="Valor numérico")
    unit: Optional[str] = Field(description="Unidad (€, %, etc.)")
    description: str = Field(description="Descripción o contexto de la cifra")

class StructuredData(BaseModel):
    people: List[Person] = Field(description="Lista de personas mencionadas")
    dates: List[Date] = Field(description="Lista de fechas importantes")
    figures: List[Figure] = Field(description="Lista de cifras o valores numéricos importantes")
    tables: List[str] = Field(description="Representaciones textuales de tablas encontradas")

def procesar_archivo(uploaded_file):
    text = ""
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name
    try:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PdfReader(temp_path)
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif uploaded_file.type == "text/plain":
            with open(temp_path, "r", encoding="utf-8") as f:
                text = f.read()
        elif uploaded_file.type == "text/csv":
            df = pd.read_csv(temp_path)
            text = df.to_string(index=False)
    except Exception as e:
        st.error(f"Error procesando {uploaded_file.name}: {str(e)}")
    finally:
        os.unlink(temp_path)
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1200,
        chunk_overlap=100,
        length_function=len
    )
    return text_splitter.split_text(text)

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', 
        return_messages=True
    )
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )

def summarize_document(text_chunks):
    llm = ChatOpenAI()
    docs = [Document(page_content=chunk) for chunk in text_chunks]
    chain = load_summarize_chain(llm, chain_type="stuff")
    return chain.run(docs)

def extract_structured_data(text_chunks):
    llm = ChatOpenAI(temperature=0)
    parser = PydanticOutputParser(pydantic_object=StructuredData)
    prompt_template = PromptTemplate(
        template="""Extrae la siguiente información estructurada del texto a continuación:
        1. Personas mencionadas (nombres y roles)
        2. Fechas importantes con su contexto
        3. Cifras o valores numéricos importantes
        4. Tablas (si existen, represéntalas como texto)
        
        Texto: {text}
        
        {format_instructions}
        """,
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    full_text = " ".join(text_chunks)
    if len(full_text) > 10000:
        full_text = full_text[:10000]
    prompt = prompt_template.format(text=full_text)
    output = llm.predict(prompt)
    try:
        structured_data = parser.parse(output)
        return structured_data
    except Exception as e:
        st.error(f"Error al parsear los datos: {str(e)}")
        return None

def handle_userinput(user_question, lang):
    if st.session_state.conversation is None:
        st.warning(TEXTS[lang]["no_docs_message"])
        return
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    for message in reversed(st.session_state.chat_history):
        content = getattr(message, 'content', str(message))
        if message.__class__.__name__ == "HumanMessage":
            st.markdown(user_template.replace("{{MSG}}", content), unsafe_allow_html=True)
        else:
            st.markdown(bot_template.replace("{{MSG}}", content), unsafe_allow_html=True)

def display_structured_data(data, lang):
    if not data:
        return
    if data.people:
        st.subheader("📋 " + ("Personas mencionadas" if lang=="es" else "People mentioned"))
        for person in data.people:
            st.markdown(f"**{person.name}**")
            if person.role:
                st.markdown(f"*{ 'Rol' if lang=='es' else 'Role' }:* {person.role}")
            st.markdown("---")
    if data.dates:
        st.subheader("📅 " + ("Fechas importantes" if lang=="es" else "Important dates"))
        for date in data.dates:
            st.markdown(f"**{date.date}**")
            st.markdown(f"*{ 'Contexto' if lang=='es' else 'Context' }:* {date.context}")
            st.markdown("---")
    if data.figures:
        st.subheader("🔢 " + ("Cifras importantes" if lang=="es" else "Key figures"))
        for figure in data.figures:
            value_with_unit = f"{figure.value}"
            if figure.unit:
                value_with_unit += f" {figure.unit}"
            st.markdown(f"**{value_with_unit}**")
            st.markdown(f"*{ 'Descripción' if lang=='es' else 'Description' }:* {figure.description}")
            st.markdown("---")
    if data.tables:
        st.subheader("📊 " + ("Tablas encontradas" if lang=="es" else "Tables found"))
        for i, table in enumerate(data.tables):
            with st.expander(f"Tabla {i+1}" if lang=="es" else f"Table {i+1}", expanded=False):
                try:
                    df = pd.read_csv(pd.compat.StringIO(table))
                    st.dataframe(df)
                except Exception:
                    st.text(table)

def download_button(label, data, file_name, mime):
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:{mime};base64,{b64}" download="{file_name}">{label}</a>'
    st.markdown(href, unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(
        page_title="Asistente Documental de Iberdrola",
        page_icon="📄",
        layout="wide"
    )
    st.markdown(css, unsafe_allow_html=True)
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Logo_Iberdrola_%282023%29.svg/768px-Logo_Iberdrola_%282023%29.svg.png",
        width=180,
    )

    # Selector de idioma en la barra lateral
    with st.sidebar:
        st.markdown("### 🌐 Idioma / Language")
        language = st.radio(
            "Selecciona el idioma / Select language",
            options=["es", "en"],
            format_func=lambda x: "Español" if x == "es" else "English",
            index=0 if "language" not in st.session_state else ["es", "en"].index(st.session_state["language"]),
            key="sidebar_language"
        )
        st.session_state["language"] = language

        st.markdown("### ⚙️ Opciones")
        if st.button(TEXTS[language]["clear_session"]):
            for key in ["conversation", "text_chunks", "summary", "structured_data", "chat_history"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.success(TEXTS[language]["session_cleared"])

        with st.expander(TEXTS[language]["help_title"]):
            st.markdown(TEXTS[language]["help_content"])

    lang = st.session_state["language"]

    # Inicializar variables de sesión
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "text_chunks" not in st.session_state:
        st.session_state.text_chunks = None
    if "summary" not in st.session_state:
        st.session_state.summary = None
    if "structured_data" not in st.session_state:
        st.session_state.structured_data = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Pestañas
    tab1, tab2, tab3 = st.tabs([TEXTS[lang]["tab1"], TEXTS[lang]["tab2"], TEXTS[lang]["tab3"]])

    with tab1:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.header(TEXTS[lang]["title"])
            if st.session_state.summary:
                with st.expander(TEXTS[lang]["summary_title"], expanded=True):
                    st.write(st.session_state.summary)
                    download_button(TEXTS[lang]["download_summary"], st.session_state.summary, "resumen.txt", "text/plain")
            user_question = st.text_input(TEXTS[lang]["question_placeholder"], key="tab1_question")
            if user_question:
                handle_userinput(user_question, lang)
            if st.session_state.chat_history:
                chat_json = json.dumps([getattr(m, 'content', str(m)) for m in st.session_state.chat_history], ensure_ascii=False, indent=2)
                download_button(TEXTS[lang]["download_chat"], chat_json, "historial_chat.json", "application/json")
        with col2:
            st.markdown("### 🔎 " + TEXTS[lang]["search_placeholder"])
            search_term = st.text_input(TEXTS[lang]["search_placeholder"], key="search_term")
            if search_term and st.session_state.text_chunks:
                results = [chunk for chunk in st.session_state.text_chunks if search_term.lower() in chunk.lower()]
                st.markdown(f"**{TEXTS[lang]['search_results']}:**")
                for res in results:
                    st.write(res)

    with tab2:
        st.header(TEXTS[lang]["tab2"])
        raw_text = st.text_area(TEXTS[lang]["ask_text"], height=200, key="tab2_textarea")
        if st.button(TEXTS[lang]["process_button"], key="tab2_process"):
            if raw_text:
                with st.spinner(TEXTS[lang]["processing_text"]):
                    text_chunks = get_text_chunks(raw_text)
                    st.session_state.text_chunks = text_chunks
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                st.success(TEXTS[lang]["success_message"])
        user_question_text = st.text_input(TEXTS[lang]["ask_text"], key="tab2_question")
        if user_question_text:
            handle_userinput(user_question_text, lang)

    with tab3:
        st.header(TEXTS[lang]["tab3"])
        if st.session_state.structured_data:
            if st.button(TEXTS[lang]["clear_data_button"], key="tab3_clear"):
                st.session_state.structured_data = None
                st.success(TEXTS[lang]["delete_success"])
            display_structured_data(st.session_state.structured_data, lang)
            download_button(TEXTS[lang]["download_structured"], st.session_state.structured_data.json(indent=2, ensure_ascii=False), "datos_estructurados.json", "application/json")
        else:
            st.info(TEXTS[lang]["structured_data_info"])

    # Panel lateral
    with st.sidebar:
        st.subheader(TEXTS[lang]["sidebar_title"])
        uploaded_files = st.file_uploader(
            TEXTS[lang]["upload_text"],
            accept_multiple_files=True,
            type=["pdf", "txt", "csv"],
            key="sidebar_uploader"
        )
        if st.button(TEXTS[lang]["process_button"], key="sidebar_process"):
            if uploaded_files:
                with st.spinner(TEXTS[lang]["processing_text"]):
                    raw_text = ""
                    for file in uploaded_files:
                        raw_text += procesar_archivo(file)
                    text_chunks = get_text_chunks(raw_text)
                    st.session_state.text_chunks = text_chunks
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                st.success(TEXTS[lang]["success_message"])
            else:
                st.error(TEXTS[lang]["error_message"])
        if st.session_state.conversation:
            cols = st.columns(2)
            with cols[0]:
                if st.button(TEXTS[lang]["summarize_button"], key="sidebar_summarize"):
                    with st.spinner(TEXTS[lang]["summarizing_text"]):
                        summary = summarize_document(st.session_state.text_chunks)
                        st.session_state.summary = summary
                    st.success(TEXTS[lang]["summary_success"])
            with cols[1]:
                if st.button(TEXTS[lang]["extract_button"], key="sidebar_extract"):
                    with st.spinner(TEXTS[lang]["extracting_text"]):
                        structured_data = extract_structured_data(st.session_state.text_chunks)
                        st.session_state.structured_data = structured_data
                    st.success(TEXTS[lang]["extract_success"])

if __name__ == '__main__':
    main()