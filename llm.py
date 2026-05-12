from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

class Llm:
    def __init__(self, model='llama3.1'):
    
        self.llm = ChatOllama(model=model, temperature=0) 

    def ask_question(self, index_name, question, db_manager):
        
            docs = db_manager.search(index_name, question, k=5)
            
         
            context = "\n\n".join([d.page_content for d in docs])
            pages = sorted(list(set([str(d.metadata.get('page', '?')) for d in docs])))
            doc_name = docs[0].metadata.get('source', 'Desconhecido').split('/')[-1]
        
            template = """
            Você é um analista experiente do mercado financeiro. Use os trechos do documento abaixo para responder à pergunta para leigos no tema.
            Se a informação não estiver no texto, diga que não encontrou.
            
            Trechos do documento:
            {context}
            
            Pergunta: {question} 
            
            Resposta:
            """
            
            prompt = ChatPromptTemplate.from_template(template)
            
            # 4. EXECUÇÃO: O Llama 3.1 lê o contexto e responde
            chain = prompt | self.llm
            resposta = chain.invoke({"context": context, "question": question})

            return {
                "answer": resposta.content,
                "pages": ", ".join(pages),
                "document_name": doc_name
            }