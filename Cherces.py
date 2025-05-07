import customtkinter as ctk
from tkinter import filedialog, messagebox
from instagrapi import Client
import schedule
import threading
import time

cl = Client()
postagens = []

# Função de login
def login_instagram():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    try:
        cl.login(usuario, senha)
        messagebox.showinfo("Login", "Login realizado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao logar: {e}")

# Adicionar postagem
def adicionar_postagem():
    imagem = filedialog.askopenfilename(title="Selecione a imagem")
    legenda = entry_legenda.get()
    hora = entry_hora.get()

    if imagem and legenda and hora:
        postagens.append({"imagem": imagem, "legenda": legenda, "hora": hora})
        listbox_postagens.insert("end", f"{hora} - {legenda}")
        schedule.every().day.at(hora).do(postar, len(postagens) - 1)
        entry_legenda.delete(0, 'end')
        entry_hora.delete(0, 'end')
    else:
        messagebox.showwarning("Campos vazios", "Preencha todos os campos.")

# Remover postagem
def remover_postagem():
    selecionado = listbox_postagens.curselection()
    if selecionado:
        index = selecionado[0]
        listbox_postagens.delete(index)
        del postagens[index]
    else:
        messagebox.showwarning("Aviso", "Selecione uma postagem para remover.")

# Postar no Instagram
def postar(index):
    try:
        postagem = postagens[index]
        cl.photo_upload(postagem["imagem"], postagem["legenda"])
        print(f"Postado: {postagem['legenda']}")
    except Exception as e:
        print(f"Erro ao postar: {e}")

# Iniciar o agendamento
def iniciar_agendamento():
    def loop():
        while True:
            schedule.run_pending()
            time.sleep(30)
    threading.Thread(target=loop, daemon=True).start()
    messagebox.showinfo("Agendador", "Agendamento iniciado!")

# Configuração da janela principal
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Agendador de Postagens")
app.geometry("500x600")

# Login
frame_login = ctk.CTkFrame(app)
frame_login.pack(pady=10, padx=10, fill="x")

entry_usuario = ctk.CTkEntry(frame_login, placeholder_text="Usuário do Instagram")
entry_usuario.pack(pady=5, padx=10, fill="x")

entry_senha = ctk.CTkEntry(frame_login, placeholder_text="Senha", show="*")
entry_senha.pack(pady=5, padx=10, fill="x")

btn_login = ctk.CTkButton(frame_login, text="Login", command=login_instagram)
btn_login.pack(pady=10)

# Postagem
frame_postagem = ctk.CTkFrame(app)
frame_postagem.pack(pady=10, padx=10, fill="x")

entry_legenda = ctk.CTkEntry(frame_postagem, placeholder_text="Legenda")
entry_legenda.pack(pady=5, padx=10, fill="x")

entry_hora = ctk.CTkEntry(frame_postagem, placeholder_text="Horário (HH:MM)")
entry_hora.pack(pady=5, padx=10, fill="x")

btn_adicionar = ctk.CTkButton(frame_postagem, text="Adicionar Imagem e Agendar", command=adicionar_postagem)
btn_adicionar.pack(pady=10)

# Lista de postagens
listbox_frame = ctk.CTkFrame(app)
listbox_frame.pack(pady=10, padx=10, fill="both", expand=True)


import tkinter as tk  # adicione isso no topo do código

listbox_postagens = tk.Listbox(listbox_frame, height=10, font=("Arial", 12))
listbox_postagens.pack(pady=5, padx=10, fill="both", expand=True)


btn_remover = ctk.CTkButton(app, text="Remover Selecionada", command=remover_postagem)
btn_remover.pack(pady=5)

btn_iniciar = ctk.CTkButton(app, text="Iniciar Agendamento", command=iniciar_agendamento)
btn_iniciar.pack(pady=10)

app.mainloop()
