import os
from dotenv import load_dotenv

# Imports do Core e Ollama (LangChain v1)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

# Imports das correntes que agora vivem no langchain-classic
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from support.constants import Constants as const
load_dotenv()

class RAG:
    def __init__(self, retriever):
        """
        Inicializa o modelo e monta a estrutura lógica do Chat uma única vez.
        
        :param retriever: O objeto retriever vindo do seu db_manager (ElasticSearch).
        """
        self.llm = ChatOllama(
            model=const.OLLAMA_MODEL, 
            temperature=0, 
            streaming=True
        )
        self.retriever = retriever
        
        # Construímos a chain no momento em que a classe é instanciada
        self.rag_chain = self._build_prediction_pipeline()

    def _build_prediction_pipeline(self):
        """
        Monta a arquitetura interna do RAG Conversacional.
        """
        # 1. Prompt de Contextualização da Pergunta
        contextualize_q_system_prompt = (
            "Dado o histórico de chat e a última pergunta do usuário, que pode fazer "
            "referência ao contexto anterior, formule uma pergunta independente que possa "
            "ser compreendida sem o histórico. NÃO responda à pergunta, apenas reformule-a "
            "se necessário, ou retorne-a como está."
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        # Cria o Retriever Inteligente (que lê histórico antes de buscar no banco)
        history_aware_retriever = create_history_aware_retriever(
            self.llm, self.retriever, contextualize_q_prompt
        )

        # 2. Prompt de Resposta Final (Seu prompt original adaptado para o formato de mensagens)
        qa_system_prompt = (
            "Você é um analista experiente do mercado financeiro. Use os trechos do "
            "documento abaixo para responder à pergunta para leigos no tema.\n"
            "Se a informação não estiver no texto, diga que não encontrou.\n\n"
            "CONTEXTO:\n{context}\n\n"
            "INSTRUÇÕES DE RESPOSTA::\n"
            "1. Se o documento comprovar a conformidade, inicie com 'CONFORME'.\n"
            "2. Se houver falta de dados, responda 'NÃO ENCONTRADO'.\n"
            "3. Cite o parágrafo ou página de referência."
        )
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        # Cria a corrente que junta os documentos e os joga no prompt de QA
        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)

        # 3. Une o Retriever Inteligente com a Corrente de Resposta
        return create_retrieval_chain(history_aware_retriever, question_answer_chain)

    def ask_question(self, question: str, chat_history: list):
        """
        Executa a pergunta do usuário considerando o histórico da conversa.
        
        :param question: A nova pergunta (ex: "Qual a norma citada na página 10?")
        :param chat_history: Lista contendo o histórico de interações da sessão
        """
        # Executa todo o pipeline do RAG de forma automática
        resposta = self.rag_chain.invoke({
            "input": question,
            "chat_history": chat_history
        })
        #print(f"Resposta do RAG: {resposta}")
        # Recuperação de metadados dos documentos coletados na busca do ElasticSearch
        docs = resposta.get("context", [])
        pages = sorted(list(set([str(d.metadata.get('page', '?')) for d in docs])))
        doc_name = docs[0].metadata.get('source', 'Desconhecido').split('/')[-1] if docs else "N/A"

        # Métricas de consumo de tokens (mantido do seu original)
        metadados_iniciais = resposta.get("response_metadata", {})
        token_usage = metadados_iniciais.get("token_usage") or {}
        
        print(f"--- Estatísticas da Auditoria ---")
        print(f"Tokens gastos na pergunta: {token_usage.get('prompt_tokens', 'N/A')}")
        print(f"Tokens gastos na resposta: {token_usage.get('completion_tokens', 'N/A')}")
        print(f"Total de tokens: {token_usage.get('total_tokens', 'N/A')}")

        return {
            "answer": resposta["answer"],
            "pages": ", ".join(pages),
            "document_name": doc_name
        }