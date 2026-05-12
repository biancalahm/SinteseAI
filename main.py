from load_file import PDFProcessor
from vector_db_manager import VectorDBManager
from search import SearchReport 


if __name__ == "__main__":
    # Define os parâmetros e roda o projeto
    arquivo = "docs/relatorio.pdf"
    index_name = "contabilidade_index"
    db_manager = VectorDBManager(es_url="http://localhost:9200")
    #processor = PDFProcessor(vector_manager=db_manager, chunk_size=512, chunk_overlap=200)
    # a funcao abaixo remove o existente e insere um novo (apenas para testes)
    #processor.insert(arquivo, index_name)
    search = SearchReport(db_manager)
    question = "Qual a relevancia do pix ?"
    result= search.checklist_analysis(index_name, question)
    search.print_result(question, result)