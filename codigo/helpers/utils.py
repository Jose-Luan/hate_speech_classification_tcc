import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import os
import re
import time

def save_metrics_and_plots(results, y_true, y_pred, output_dir, model_name):
    """
    Salva métricas globais, matriz de confusão e relatório de classificação.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Salvar métricas globais
    results_df = pd.DataFrame([results])
    results_df.to_csv(f"{output_dir}/metrics.csv", index=False)

    # Matriz de Confusão
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Não Ódio (0)", "Ódio (1)"],
        yticklabels=["Não Ódio (0)", "Ódio (1)"]
    )
    plt.xlabel("Predção")
    plt.ylabel("Real")
    plt.title(f"Matriz de Confusão - {model_name}")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/confusion_matrix.png")
    plt.close()

    # Classification Report
    report = classification_report(
        y_true,
        y_pred,
        target_names=["Não Ódio (0)", "Ódio (1)"],
        digits=4
    )
    with open(f"{output_dir}/classification_report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n✅ Resultados salvos em '{output_dir}'")

def classificar_texto(model, texto, prompt_template):
    """
    Classifica um lote de textos com base em um modelo e um template de prompt.
    """
    prompt = prompt_template
    for idx, txt in enumerate(texto, 1):
        prompt += f"{idx}. {txt}\n"
    prompt += (
        "\nResponda SOMENTE com 0 ou 1, um por linha, na mesma ordem dos textos fornecidos.\n"
        "Não explique, não justifique, não adicione nada além dos números."
    )

    if hasattr(model, "generate_content"):  # Para o modelo Gemini
        resposta = model.generate_content(prompt)
        resposta_texto = resposta.text.strip()
    elif hasattr(model, "chat"):  # Para o modelo Cohere
        res = model.chat(
            model="command-a-03-2025",
            messages=[{"content": prompt, "role": "user"}],
            max_tokens=200,
            temperature=0.3
        )
        resposta_texto = "".join([c.text for c in res.message.content if hasattr(c, "text")]).strip()
    else:
        raise ValueError("Modelo não suportado.")

    return resposta_texto, resposta_texto

def parse_saida(saida, expected_len):
    """
    Processa a saída do modelo para capturar apenas os valores 0 e 1.
    """
    matches = re.findall(r"\b[01]\b", saida)
    if len(matches) == expected_len:
        return matches
    else:
        return matches + [None] * (expected_len - len(matches))

def processar_lotes(df_final, model, prompt_template, prompt_name, batch_size=20, sleep_time=2):
    """
    Processa lotes de textos para classificação e atualiza o DataFrame com os resultados.
    """
    df_final = df_final
    df_final[prompt_name] = None
    df_final[f'{prompt_name}_raw'] = None
    
    print(f"classificação com: {prompt_name}")

    for i in range(0, len(df_final), batch_size):
        try:
            lote = df_final.iloc[i:i+batch_size]["text"].tolist()
            saida, raw_saida = classificar_texto(model, lote, prompt_template)

            resultados = parse_saida(saida, len(lote))
            raw_resultados = raw_saida.split("\n")

            for j, res in enumerate(resultados):
                idx = i + j
                if idx < len(df_final):
                    if res in ["0", "1"]:
                        df_final.at[idx, prompt_name] = int(res)
                    else:
                        df_final.at[idx, prompt_name] = None
                    df_final.at[idx, f'{prompt_name}_raw'] = (
                        raw_resultados[j] if j < len(raw_resultados) else None
                    )

            time.sleep(sleep_time)

        except Exception as e:
            print(f"Erro no batch {i}–{i+batch_size} para {prompt_name}: {e}")
            time.sleep(15)

    return df_final

def plot_confusion(y_true, y_pred, titulo, path, output_dir):
    cm = confusion_matrix(y_true, y_pred, labels=[0,1])
    plt.figure(figsize=(5,4))
    sns.heatmap(
                cm, 
                annot=True, 
                fmt="d", 
                cmap="Blues",
                xticklabels=["Não ódio (0)", "Ódio (1)"],
                yticklabels=["Não ódio (0)", "Ódio (1)"]
    )
    plt.xlabel("Predição")
    plt.ylabel("Real")
    plt.title(titulo)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/confusion_matrix.png")
    plt.show()
    plt.close()

    report = classification_report(y_true, y_pred, target_names=["Não ódio (0)", "Ódio (1)"])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(report)

    print("\nRelatório de Classificação:")
    print(report)