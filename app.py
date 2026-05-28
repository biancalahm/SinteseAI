# main.py
from rag_agent import RAG
from langchain_core.messages import HumanMessage, AIMessage
from load_file import PDFProcessor
from vector_db_manager import VectorDBManager
from search import SearchReport 
from support.constants import Constants as const

db_manager = VectorDBManager(es_url=const.ELASTIC_SEARCH_URL)
# Supondo que você obtenha o retriever do seu db_manager atual
index_name = const.INDEX_NAME 
meu_retriever = db_manager.get_retriever(index_name, 5)

agente = RAG(retriever=meu_retriever)
historico_chat = []

print("Bem-vindo ao Chat para extração de informações em documentos. Digite 'sair' para encerrar.")

while True:
    pergunta_usuario = input("\nVocê: ")
    if pergunta_usuario.lower() == 'sair':
        break

    # Passamos a pergunta E o histórico
    resultado = agente.ask_question(pergunta_usuario, historico_chat)
    
    print(f"\nIA: {resultado['answer']}")
    print(f"[Fonte: {resultado['document_name']} | Páginas: {resultado['pages']}]")


    historico_chat.extend([
        HumanMessage(content=pergunta_usuario),
        AIMessage(content=resultado['answer'])
    ])