from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from vector_db_manager import VectorDBManager
class PDFProcessor:
    def __init__(self, vector_manager, chunk_size=1000, chunk_overlap=200):
        # Configuramos as regras de fatiamento na inicialização
        self.db = vector_manager
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True
        )

    def process_pdf(self, file_path):
        """
        Carrega o PDF, divide em pedaços e retorna a lista de chunks.
        """
        if not file_path.endswith('.pdf'):
            raise ValueError("O arquivo fornecido não é um PDF.")
        print(f"Carregando arquivo: {file_path}")
        loader = PyPDFLoader(file_path)
        # Carrega as páginas originais
        documentos_inteiros = loader.load()
        # (chunks)
        chunks = self.text_splitter.split_documents(documentos_inteiros)
        print(f"Documento dividido em {len(chunks)} pedaços.")
        return chunks, len(documentos_inteiros)
    
    def insert(self, path_pdf, index_name):
        try:
            # Obter chunks do PDF
            chunks, total_paginas = self.process_pdf(path_pdf)
            # Insere no ElasticSearch (Embedding)
            self.db.recreate_index(index_name)  
            self.db.insert_documents(index_name, chunks)
            print(f" Índice: {index_name}")
            print(f" Páginas processadas: {total_paginas}")
            print(f" Chunks gerados: {len(chunks)}")
        except Exception as e:
            print(f"Erro no processo: {e}")