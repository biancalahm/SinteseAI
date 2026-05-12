from langchain_elasticsearch import ElasticsearchStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
class VectorDBManager:
    def __init__(self, es_url="http://localhost:9200"):
        # 1. Este modelo só TRADUZ texto para números (Vetores)
        self.embeddings = OllamaEmbeddings(model="qwen3-embedding:0.6b") 
        self.es_url = es_url

    def _get_store(self, index_name):
        """Função privada para conectar a um índice específico."""
        return ElasticsearchStore(
            es_url=self.es_url,
            index_name=index_name,
            embedding=self.embeddings,
            strategy=ElasticsearchStore.ApproxRetrievalStrategy()
        )
    def recreate_index(self, index_name):

        store = self._get_store(index_name)

        if store.client.indices.exists(index=index_name):
            store.client.indices.delete(index=index_name)

        print(f"Índice {index_name} removido.")
    def insert_documents(self, index_name, chunks):
        """Insere pedaços de texto em um índice específico."""
        store = self._get_store(index_name)
        # add_documents é o método para acrescentar dados sem recriar o índice
        try:
            
            store.add_documents(documents=chunks) #LangChain utiliza a Bulk API do Elasticsearch para inserção eficiente
            print(f"Documentos inseridos no índice: {index_name}")
        except Exception as e:
            print(f"Erro ao inserir documentos no índice {index_name}: {e}") 
            if hasattr(e, "errors"):
                for erro in e.errors[:5]:
                    print(erro)
    
    def search(self, index_name, query, k=4):
        """Busca os pedaços mais relevantes em um índice."""
        store = self._get_store(index_name)
        result = store.similarity_search(query, k=k)
        return result
    
    def delete_all_documents(self, index_name):

        store = self._get_store(index_name)

        response = store.client.delete_by_query(
            index=index_name,
            body={
                "query": {
                    "match_all": {}
                }
            },
            refresh=True
        )

        print(f"Todos os documentos apagados de: {index_name}")
        print(response)