# Elasticsearch + RAG - Análise de Documentos - Estudo aplicado

Um projeto simples de busca e análise inteligente de documentos PDF utilizando **Elasticsearch** para armazenamento vetorial combinado com **LLMs** (Large Language Models) para geração de respostas contextualmente relevantes.

## Objetivo Principal

Implementar um sistema simples de **Retrieval Augmented Generation (RAG)** que permite:

- **Carregamento e processamento** de arquivos PDF
- **Busca semântica** em vetores de texto (embeddings)
- **Geração de respostas inteligentes** usando LLMs local (Llama 3.1)
- **Análise contextual** de documentos com referência às páginas de origem

O sistema é ideal para análise de relatórios financeiros, documentações técnicas ou qualquer corpus de texto que necessite busca semântica e respostas baseadas em contexto.

Utilizado como exemplo: Relatório de Estabilidade Financeira Volume 24 | N.1| Abril 2025 ISSN 2176-8102

Exemplo de resultado: ![1778624551708](images/README/1778624551708.png)

## Estrutura do Projeto

```
elastic_search/
├── main.py                      # Ponto de entrada do projeto
├── llm.py                       # Integração com o modelo Llama 3.1
├── vector_db_manager.py         # Gerenciador do Elasticsearch
├── search.py                    # Interface de busca e análise
├── load_file.py                 # Processador de arquivos PDF
├── docker-compose.yml           # Configuração da infraestrutura
├── requirements.txt             # Dependências Python
├── data/                        # Dados de entrada
│   └── dummy_data.json
├── docs/                        # Diretório para PDFs
│   └── relatorio.pdf            # Exemplo de documento
├── estudos/                     # Notebooks de aprendizado
│   ├── 04_create_index.ipynb
│   ├── 05_field_data_types.ipynb
│   ├── ...
│   └── 20_ingest_processors.ipynb
└
```

### Componentes Principais:


| Arquivo                  | Descrição                                                           |
| ------------------------ | --------------------------------------------------------------------- |
| **main.py**              | Orquestra o fluxo: carrega PDF, processa, busca e analisa             |
| **llm.py**               | Classe`Llm` - integração com Ollama (Llama 3.1)                     |
| **vector_db_manager.py** | Classe`VectorDBManager` - gerencia índices e buscas no Elasticsearch |
| **search.py**            | Classe`SearchReport` - interface de RAG (busca + LLM)                 |
| **load_file.py**         | Classe`PDFProcessor` - carrega e divide PDFs em chunks                |
| **estudos/**             | Notebooks Jupyter com tutoriais de Elasticsearch                      |

### Pré-requisitos

- Python 3.8+
- Docker e Docker Compose
- Ollama instalado localmente (para rodar os LLMs)

### Clonar/Acessar o Repositório

```bash

```

### Criar e Ativar Ambiente Virtual

```bash
# Criar ambiente
python3 -m venv venv

# Ativar (Linux/Mac)
source venv/bin/activate

```

### Instalar Dependências Python

```bash
pip install -r requirements.txt
```

**Dependências instaladas:**

```
langchain-core==0.x.x              # Base do LangChain
langchain-ollama==0.x.x            # Integração com Ollama
langchain-elasticsearch==0.x.x     # Conexão Elasticsearch
elasticsearch==8.x.x              # Cliente oficial
pypdf==4.x.x                       # Leitura de PDFs
langchain-community==0.x.x         # Loaders (PyPDFLoader)
langchain-text-splitters==0.x.x    # Divisor de texto
```

### Iniciar Infraestrutura (Docker)

```bash
# Inicia Elasticsearch 8.17.0 e Kibana 8.17.0
docker-compose up -d

# Verificar status
docker-compose ps

# Parar
docker-compose down
```

**Endpoints disponíveis:**

- Elasticsearch: `http://localhost:9200`
- Kibana: `http://localhost:5601`

### Configurar e Rodar Ollama

```bash
# Instalar e rodar Ollama (em outro terminal)
# Baixar modelos necessários
ollama pull llama3.1          # LLM para perguntas e respostas
ollama pull qwen3-embedding:0.6b  # Embedding para vetorização

# Ollama roda por padrão em http://localhost:11434
```

## Principais Modelos Utilizados

### LLMs (Large Language Models)


| Modelo                     | Função                                        | Provedor | Config                 |
| -------------------------- | ----------------------------------------------- | -------- | ---------------------- |
| **Llama 3.1**              | Análise de documentos e geração de respostas | Ollama   | `llama3.1`             |
| **Qwen3 Embedding** (0.6B) | Conversão de texto em vetores (embeddings)     | Ollama   | `qwen3-embedding:0.6b` |

### Backend de Dados


| Tecnologia        | Função                                  | Versão |
| ----------------- | ----------------------------------------- | ------- |
| **Elasticsearch** | Armazenamento vetorial e busca semântica | 8.17.0  |
| **Kibana**        | Interface para visualizar índices        | 8.17.0  |

### Frameworks/Bibliotecas


| Biblioteca                         | Função                                |
| ---------------------------------- | --------------------------------------- |
| **LangChain**                      | Orquestração de fluxo LLM + retrieval |
| **PyPDF**                          | Carregamento de documentos PDF          |
| **RecursiveCharacterTextSplitter** | Divisão inteligente de texto em chunks |
| **ElasticsearchStore**             | Integração de busca vetorial          |


### Exemplo Básico: Análise de Documento

```python
from load_file import PDFProcessor
from vector_db_manager import VectorDBManager
from search import SearchReport

# 1. Conectar ao Elasticsearch
db_manager = VectorDBManager(es_url="http://localhost:9200")

# 2. Processar e inserir PDF (comentado para evitar sobrescrita)
# processor = PDFProcessor(vector_manager=db_manager, chunk_size=512, chunk_overlap=200)
# processor.insert("docs/relatorio.pdf", index_name="contabilidade_index")

# 3. Criar interface de busca
search = SearchReport(db_manager)

# 4. Fazer pergunta
question = "Qual a relevancia do pix?"
result = search.checklist_analysis("contabilidade_index", question)

# 5. Exibir resultado
search.print_result(question, result)
```

**Resultado esperado:**

```
================================================================================
DOCUMENTO ANALISADO: relatorio.pdf
PERGUNTA: Qual a relevancia do pix?
--------
RESPOSTA GERADA COM BASE NO DOCUMENTO:
[Resposta do Llama 3.1 com contexto do documento]
--------
LOCALIZAÇÃO NO PDF (PÁGINAS): 2, 5, 12
```

### Fluxo de Processamento RAG

```
1. PDF Carregado
   ↓
2. Dividido em Chunks (512 tokens com overlap 200)
   ↓
3. Chunks Vetorizados com Qwen3 Embedding
   ↓
4. Armazenados no Elasticsearch (índice)
   ↓
5. Pergunta do usuário
   ↓
6. Busca Semântica (top-5 chunks similares)
   ↓
7. Contexto + Pergunta → Llama 3.1
   ↓
8. Resposta Gerada com Referências de Páginas
```

## Configurações Principais

### VectorDBManager

```python
.env
ELASTIC_SEARCH_URL
```

### PDFProcessor

```python
processor = PDFProcessor(
    vector_manager=db_manager,
    chunk_size=512,      # Tamanho dos pedaços de texto
    chunk_overlap=200    # Sobreposição entre chunks
)
```

### LLM (Llama 3.1)

```python
llm = Llm(model='llama3.1')  # Temperature=0 (respostas determinísticas)
```

## Recursos Adicionais

### Notebooks de Aprendizado (pasta `estudos/`)

- `04_create_index.ipynb` - Criação de índices no Elasticsearch
- `15_dense_vector_field_type.ipynb` - Tipos de campos vetoriais
- `17_knn_search.ipynb` - Busca por vizinhos mais próximos (KNN)
- `chatbot.ipynb` - Implementação de chatbot com RAG
- E mais 16 notebooks cobrindo toda a stack!


## Troubleshooting


| Problema                           | Solução                                                 |
| ---------------------------------- | --------------------------------------------------------- |
| **Elasticsearch não conecta**     | Verificar:`docker-compose ps` e `http://localhost:9200`   |
| **Ollama não encontrado**         | Instalar Ollama e rodar:`ollama serve` em outro terminal  |
| **Erro de importação LangChain** | Reinstalar:`pip install -r requirements.txt --upgrade`    |
| **Índice não criado**            | Usar:`processor.insert(path, index_name)` antes de buscar |

### Notas

Este projeto é um estudo prático de:

- Elasticsearch (busca vetorial)
- LLMs com Ollama (inferência local)
- Padrão RAG (Retrieval Augmented Generation)
- LangChain (orquestração)

Desenvolvido como material educacional para análise de documentos inteligente.

**Última atualização:** May 2026
**Autor:** Bianca Lahm - Estudos - Elastic Search
**Status:**  Funcional com documentação completa
