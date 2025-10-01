# Resultados – Cohere

Esta pasta é dedicada ao **armazenamento dos resultados obtidos com o modelo da Cohere**.  
O conteúdo aqui serve como registro e referência para análises posteriores.

## Modelo Utilizado
- **Nome:** `command-a-03-2025`  
- **Tipo:** LLM (Large Language Model)  
- **Finalidade:** Classificação de discurso de ódio em português a partir de diferentes estratégias de prompting (zero-shot, one-shot e few-shot).  

## Estrutura dos Resultados
- Arquivos `.csv` contendo as saídas do modelo para cada configuração de prompt.  
- Cada arquivo armazena:
  - Texto original
  - Saída processada pelo modelo
  - Saída bruta retornada pela API
  - Labels de referência (quando aplicável)

## Observações Importantes
- O acesso foi feito via **Cohere Chat API**.  
- Com a **Trial Key**, há limite de **10 requisições por minuto**.  
- Para execuções maiores, recomenda-se utilizar uma **Production Key**.

## Documentação Oficial
📖 [Cohere Chat API – Documentação](https://docs.cohere.com/v2/docs/chat-api)
