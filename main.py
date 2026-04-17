import customtkinter as ctk
from tkinter import filedialog
import pandas as pd
from os import startfile

#interface
app = ctk.CTk()
app.title('xl')
screenw = app.winfo_screenwidth()
screenh = app.winfo_screenheight()
width = 500
height = 350
x = (screenw // 2) - (width // 2)
y = (screenh // 2) - (height // 2)
app.geometry(f"{width}x{height}+{x}+{y}")
title = ctk.CTkLabel(app, text="Preenchedor de Excel", font=("Arial", 24))
title.pack(pady=35)
arquivos = {"nomes": None, "idades": None, "cidades": None}

#carregar arquivos
def load_file(tipo, label):
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if path:
        arquivos[tipo] = path
        label.configure(text=f"{path.split('/')[-1]}")
#criar planilha
def preencher():
    if not all(arquivos.values()):
        status.configure(text="Selecione os 3 arquivos primeiro!")
        return
    
    try:
        with open(arquivos["nomes"], encoding="utf-8") as f:
            nomes = [l.strip() for l in f.readlines() if l.strip()]

        with open(arquivos["idades"]) as f:
            idades = [int(l.strip()) for l in f.readlines() if l.strip()]

        with open(arquivos["cidades"], encoding="utf-8") as f:
            cidades = [l.strip() for l in f.readlines() if l.strip()]

        # validação
        if not (len(nomes) == len(idades) == len(cidades)):
            status.configure(text="Os arquivos têm tamanhos diferentes!")
            return

        status.configure(text="Gerando arquivo Excel...")
        app.update()

        df = pd.DataFrame({
            "Nome": nomes,
            "Idade": idades,
            "Cidade": cidades
        })

        caminho = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            initialfile="planilha_preenchida.xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )

        if not caminho:
            status.configure(text="Operação cancelada.")
            return

        df.to_excel(caminho, index=False)
        startfile(caminho)

        status.configure(text=f"{len(nomes)} registros salvo com sucesso!")

    except Exception as e:
        status.configure(text=f"Erro: {str(e)}")

#botões
for tipo, texto in [("nomes", "Nomes"), ("idades", "Idades"), ("cidades", "Cidades")]:
    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(pady = 5)
    lbl = ctk.CTkLabel(frame, text="Nenhum arquivo", font=("Arial", 12), width=200)
    lbl.pack(side="right", padx=10)
    ctk.CTkButton(frame, text=f"Selecionar {texto}", width=150,
                  command=lambda t=tipo, l=lbl: load_file(t, l)).pack(side="left")

botao = ctk.CTkButton(app, text="Preencher Planilha", command=preencher,
                      font=("Arial", 14,"bold"), height=40)
                    
botao.pack(pady=20)

status = ctk.CTkLabel(app, text="", font=("Arial", 12))
status.pack()

app.mainloop()