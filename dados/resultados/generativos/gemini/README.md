# Resultados – Gemini

Esta pasta é dedicada ao **armazenamento dos resultados obtidos com o modelo Gemini**.  
O conteúdo aqui serve como registro e referência para análises posteriores.

## Modelo Utilizado
- **Nome:** `gemini-2.5-flash`  
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
- O acesso foi feito via **Google Gemini API**.  
- O modelo foi configurado para **responder apenas com 0 ou 1**, de forma a viabilizar métricas quantitativas.  
- As execuções foram feitas em lotes para melhor controle de requisições.

## Documentação Oficial
📖 [Gemini API – Documentação](https://ai.google.dev/gemini-api/docs)
