from llm import Llm
class SearchReport:
    def __init__(self, vector_manager):
        """
        Recebe uma instância do VectorDBManager já configurada. 
        Pré configura o LLM (Llama 3.1) para uso.
        """
        self.llm = Llm(model="llama3.1") 
        self.db = vector_manager
        

    def checklist_analysis(self,index_name , question):
        """
        Executar a lógica de pergunta e resposta (RAG).
        """
        print(f" Analisando: '{question}' no índice [{index_name}]...")
        
        try:           
            #ask_question contém a busca e o prompt que melhora a resposta para o usuário 
            result = self.llm.ask_question(index_name, question,db_manager=self.db)
            return result
        except Exception as e:
            return {
                "question": f"Erro ao processar análise: {str(e)}",
                "pages": "N/A"
            }

    def print_result(self, question, result):
        """
        Exibe o resultado da análise.
        """
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        BOLD = '\033[1m'
        YELLOW = '\033[93m'
        ENDC = '\033[0m'

       

        print(f"\n{HEADER}{'='*80}{ENDC}")
        print(f"{BOLD} DOCUMENTO ANALISADO:{ENDC} {YELLOW}{result['document_name']}{ENDC}")
        print(f"{BOLD} PERGUNTA:{ENDC} {OKBLUE}{question}{ENDC}")
        print(f"{HEADER}{'-'*80}{ENDC}")
            
        print(f"{BOLD} RESPOSTA GERADA COM BASE NO DOCUMENTO:{ENDC}")
        print(f"{result['answer']}") 
        
        print(f"{HEADER}{'-'*80}{ENDC}")
        print(f"{BOLD} LOCALIZAÇÃO NO PDF (PÁGINAS):{ENDC} {OKGREEN}{result['pages']}{ENDC}")
        print(f"{HEADER}{'='*80}{ENDC}\n")
            