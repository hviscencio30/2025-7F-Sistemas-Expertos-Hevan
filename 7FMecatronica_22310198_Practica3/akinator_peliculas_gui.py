# -*- coding: utf-8 -*-
"""
Akinator de Películas — GUI con botones Sí/No (tkinter)
Autor: Hevan Jesús Viscencio López (proyecto)
Descripción:
- Carga el árbol desde JSON externo (--data base_peliculas.json).
- Ventana única con estilo "película": título, pregunta grande, botones Sí/No.
- Confirmación de película en hojas. Si falla, aprende (pop-ups) y persiste al JSON.
- Botón Salir y botón Jugar de nuevo.

Requisitos: Python 3.8+ (tkinter viene incluido).
"""
import json
import os
import sys
from typing import Dict, Any, List, Tuple, Optional

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# ---------------- Utilidades de archivo ----------------
def load_tree(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        # base mínima si no hay archivo
        return {
            "question": "¿Es una película animada?",
            "yes": {"movie": "Toy Story"},
            "no": {
                "question": "¿Es anterior al año 2000?",
                "yes": {"movie": "Titanic"},
                "no": {"movie": "Inception"}
            }
        }
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tree(path: str, tree: Dict[str, Any]) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)

def is_leaf(node: Dict[str, Any]) -> bool:
    return "movie" in node and isinstance(node["movie"], str)

# ---------------- GUI ----------------
class AkinatorGUI(tk.Tk):
    def __init__(self, data_path: str):
        super().__init__()
        self.title("🎬 Akinator de Películas")
        self.geometry("720x460")
        self.minsize(640, 420)

        # “Look” tipo cartel/cinema
        self.bg = "#0b0d14"      # azul noche
        self.fg = "#f1f3f9"      # blanco suave
        self.accent = "#e50914"  # rojo cine
        self.dim = "#9aa4b2"

        self.configure(bg=self.bg)
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Cinema.TFrame", background=self.bg)
        style.configure("Cinema.TLabel", background=self.bg, foreground=self.fg, font=("Bahnschrift", 12))
        style.configure("CinemaTitle.TLabel", background=self.bg, foreground=self.fg, font=("Bahnschrift", 16, "bold"))
        style.configure("CinemaQ.TLabel", background=self.bg, foreground=self.fg, font=("Bahnschrift", 18, "bold"), wraplength=560, anchor="center", justify="center")
        style.configure("CinemaSub.TLabel", background=self.bg, foreground=self.dim, font=("Bahnschrift", 10))
        style.configure("Cinema.TButton", font=("Bahnschrift", 12, "bold"), padding=10)
        style.map("Cinema.TButton",
                  background=[("active", self.accent)],
                  foreground=[("active", "white")])

        top = ttk.Frame(self, style="Cinema.TFrame")
        top.pack(fill="x", padx=20, pady=(18, 6))

        self.title_lbl = ttk.Label(top, text="Akinator de Películas", style="CinemaTitle.TLabel")
        self.title_lbl.pack(side="left")
        self.path_lbl = ttk.Label(top, text="base: —", style="CinemaSub.TLabel")
        self.path_lbl.pack(side="right")

        mid = ttk.Frame(self, style="Cinema.TFrame")
        mid.pack(fill="both", expand=True, padx=20, pady=10)

        self.q_lbl = ttk.Label(mid, text="Piensa en una película…", style="CinemaQ.TLabel")
        self.q_lbl.pack(expand=True)

        btns = ttk.Frame(self, style="Cinema.TFrame")
        btns.pack(pady=(6, 14))

        self.btn_yes = ttk.Button(btns, text="Sí", style="Cinema.TButton", command=self.on_yes)
        self.btn_no  = ttk.Button(btns, text="No", style="Cinema.TButton", command=self.on_no)
        self.btn_yes.grid(row=0, column=0, padx=10)
        self.btn_no.grid(row=0, column=1, padx=10)

        bottom = ttk.Frame(self, style="Cinema.TFrame")
        bottom.pack(fill="x", padx=20, pady=(0, 12))
        self.info_lbl = ttk.Label(bottom, text="Piensa en una película. Responde a las preguntas.", style="CinemaSub.TLabel")
        self.info_lbl.pack(side="left")

        self.btn_again = ttk.Button(bottom, text="Jugar de nuevo", style="Cinema.TButton", command=self.restart)
        self.btn_exit  = ttk.Button(bottom, text="Salir", style="Cinema.TButton", command=self.destroy)
        self.btn_exit.pack(side="right")
        self.btn_again.pack(side="right", padx=8)

        # Estado del juego
        self.data_path = data_path
        self.path_lbl.config(text=f"base: {os.path.basename(self.data_path)}")
        self.tree: Dict[str, Any] = load_tree(self.data_path)
        self.stack: List[Tuple[Dict[str, Any], Optional[str]]] = []  # (nodo, came_from_key)
        self.current: Dict[str, Any] = self.tree

        # Inicio
        self.show_current()

    # ---------- Lógica ----------
    def show_current(self):
        """Muestra la pregunta o confirmación de película."""
        if is_leaf(self.current):
            self.q_lbl.config(text=f"¿Estabas pensando en «{self.current['movie']}»?")
            self.info_lbl.config(text="Confirma con Sí/No. Si no, me enseñarás una nueva película.")
        else:
            self.q_lbl.config(text=self.current["question"])
            self.info_lbl.config(text="Responde Sí o No para continuar…")

    def on_yes(self):
        if is_leaf(self.current):
            # Adivinó
            messagebox.showinfo("¡Adivinada!", "🎉 ¡Bien! Lo adiviné.")
            self.ask_play_again()
            return
        # Avanzar por rama 'yes'
        self.stack.append((self.current, "yes"))
        self.current = self.current["yes"]
        self.show_current()

    def on_no(self):
        if is_leaf(self.current):
            # Aprender nueva película
            self.learn_new_movie(self.current)
            return
        # Avanzar por rama 'no'
        self.stack.append((self.current, "no"))
        self.current = self.current["no"]
        self.show_current()

    def learn_new_movie(self, wrong_leaf: Dict[str, Any]):
        """Popup para aprender: pide película, pregunta diferenciadora y respuesta correcta."""
        titulo = simpledialog.askstring(
            "No acerté 😅",
            "¿Qué película era?\n(Ej.: «Titanes del Pacífico»)",
            parent=self
        )
        if not titulo:
            # Cancelado
            self.info_lbl.config(text="Aprendizaje cancelado. Puedes seguir jugando o salir.")
            return

        pregunta = simpledialog.askstring(
            "Enséñame",
            f"Dime una pregunta SÍ/NO que distinga «{titulo}» de «{wrong_leaf['movie']}».\n"
            "Debe terminar con ‘?’",
            parent=self
        )
        if not pregunta:
            self.info_lbl.config(text="Aprendizaje cancelado. Puedes seguir jugando o salir.")
            return
        if not pregunta.endswith("?"):
            pregunta += "?"

        resp_si = messagebox.askyesno("Para la nueva película",
                                      f"Para «{titulo}», ¿la respuesta a:\n\n{pregunta}\n\nes SÍ?")
        # Construir nuevo nodo
        new_leaf = {"movie": titulo}
        old_leaf = wrong_leaf
        new_node = {"question": pregunta,
                    "yes": new_leaf if resp_si else old_leaf,
                    "no":  old_leaf if resp_si else new_leaf}

        # Reemplazar en el árbol
        if not self.stack:
            # La raíz era hoja (caso raro)
            self.tree = new_node
            self.current = self.tree
        else:
            parent, key = self.stack[-1]
            parent[key] = new_node
            self.current = parent[key]

        # Guardar
        try:
            save_tree(self.data_path, self.tree)
            messagebox.showinfo("Guardado", f"💾 Base de conocimiento actualizada en {os.path.basename(self.data_path)}.")
        except Exception as e:
            messagebox.showwarning("Aviso", f"No pude guardar cambios: {e}")

        self.show_current()

    def ask_play_again(self):
        again = messagebox.askyesno("¿Jugar otra vez?", "¿Quieres jugar otra vez?")
        if again:
            self.restart()
        else:
            self.destroy()

    def restart(self):
        """Reinicia al inicio del árbol sin perder lo aprendido."""
        self.tree = load_tree(self.data_path)  # recarga por si el archivo cambió
        self.current = self.tree
        self.stack.clear()
        self.show_current()
        self.info_lbl.config(text="Nueva partida. Piensa en otra película.")

# ---------------- Main ----------------
def main():
    data_path = "base_peliculas.json"
    args = sys.argv[1:]
    if "--data" in args:
        try:
            i = args.index("--data")
            data_path = args[i + 1]
        except Exception:
            print("Uso: python akinator_peliculas_gui.py --data RUTA_JSON")
            return
    app = AkinatorGUI(data_path)
    app.mainloop()

if __name__ == "__main__":
    main()
