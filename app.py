from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

ARQUIVO = "produtos.json"


def ler_produtos():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return []


def salvar_produtos(produtos):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(produtos, arquivo, ensure_ascii=False, indent=4)


@app.route("/")
def inicio():
    produtos = ler_produtos()
    return render_template("index.html", produtos=produtos)


@app.route("/adicionar", methods=["POST"])
def adicionar():
    produtos = ler_produtos()

    novo_produto = {
        "id": len(produtos) + 1,
        "nome": request.form["nome"],
        "categoria": request.form["categoria"],
        "quantidade": float(request.form["quantidade"]),
        "preco": float(request.form["preco"]),
        "tipo_preco": request.form["tipo_preco"]
    }

    produtos.append(novo_produto)
    salvar_produtos(produtos)
    return redirect("/")


@app.route("/excluir/<int:id>")
def excluir(id):
    produtos = ler_produtos()
    produtos = [p for p in produtos if p["id"] != id]
    salvar_produtos(produtos)
    return redirect("/")


# 🚀 PARTE IMPORTANTE PARA RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
