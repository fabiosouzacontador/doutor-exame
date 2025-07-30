from flask import Flask, render_template, request
import os

app = Flask(__name__)

def get_valores_referencia(idade, sexo):
    ref = {}
    if idade < 18:
        ref["hemoglobina"] = {"nome": "Hemoglobina", "min": 11.5, "max": 15.5, "unidade": "g/dL"}
    elif sexo == "feminino":
        ref["hemoglobina"] = {"nome": "Hemoglobina", "min": 12.0, "max": 16.0, "unidade": "g/dL"}
    else:
        ref["hemoglobina"] = {"nome": "Hemoglobina", "min": 13.5, "max": 17.5, "unidade": "g/dL"}

    ref["colesterol"] = {"nome": "Colesterol total", "min": 0, "max": 199, "unidade": "mg/dL"}
    ref["glicemia"] = {"nome": "Glicemia em jejum", "min": 70, "max": 99, "unidade": "mg/dL"}

    if sexo == "feminino":
        ref["creatina"] = {"nome": "Creatinina", "min": 0.5, "max": 1.1, "unidade": "mg/dL"}
    else:
        ref["creatina"] = {"nome": "Creatinina", "min": 0.7, "max": 1.3, "unidade": "mg/dL"}

    ref["leucocitos"] = {"nome": "Leucócitos", "min": 4000, "max": 11000, "unidade": "/mm³"}
    ref["plaquetas"] = {"nome": "Plaquetas", "min": 150000, "max": 450000, "unidade": "/mm³"}

    return ref

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analise", methods=["POST"])
def analise():
    try:
        idade = int(request.form.get("idade"))
    except:
        idade = 30
    sexo = request.form.get("sexo", "masculino")
    VALORES_REFERENCIA = get_valores_referencia(idade, sexo)

    resultados = []
    alertas = []

    for campo, info in VALORES_REFERENCIA.items():
        valor_str = request.form.get(campo)
        if valor_str:
            try:
                valor = float(valor_str.replace(",", "."))
                status = "normal"
                if valor < info["min"]:
                    status = "baixo"
                    alertas.append(f"{info['nome']} baixo")
                elif valor > info["max"]:
                    status = "alto"
                    alertas.append(f"{info['nome']} alto")
                resultados.append({
                    "exame": info["nome"],
                    "valor": valor,
                    "unidade": info["unidade"],
                    "min": info["min"],
                    "max": info["max"],
                    "status": status
                })
            except:
                continue

    if not resultados:
        diagnostico = "Nenhum dado informado."
    elif len(alertas) == 0:
        diagnostico = "🔍 Nenhum desvio significativo foi identificado. Continue com acompanhamento médico regular."
    else:
        condicoes = ", ".join(alertas)
        diagnostico = f"🔍 Foram identificados os seguintes desvios: {condicoes}. Recomendamos avaliação com médico."

    return render_template("resultado.html", resultados=resultados, diagnostico=diagnostico)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)