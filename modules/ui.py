import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# Importa os módulos criados
from . import utils
from . import ops

THUMB_W, THUMB_H = 280, 220

class BinImgOpsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Operações Lógicas e Aritméticas com Imagens")
        self.geometry("1200x760")
        self.minsize(1080, 680)

        self.root_dir = None
        self.images = []
        self.imgA_path = None
        self.imgB_path = None
        self.imgA_pil = None
        self.imgB_pil = None
        self.result_pil = None

        self.thresholdA = tk.IntVar(value=128)
        self.thresholdB = tk.IntVar(value=128)
        self.modo_var = tk.StringVar(value="logico")

        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Sidebar (painel esquerdo)
        sidebar = ttk.Frame(self, padding=8)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.columnconfigure(0, weight=1)
        sidebar.rowconfigure(3, weight=1) # Expande a Listbox

        ttk.Label(sidebar, text="Diretório raiz").grid(row=0, column=0, sticky="w")
        ttk.Button(sidebar, text="Escolher pasta…", command=self.pick_root).grid(row=1, column=0, sticky="ew", pady=(2, 8))
        ttk.Label(sidebar, text="Arquivos (selecione 1 ou 2)").grid(row=2, column=0, sticky="w")

        self.file_list = tk.Listbox(sidebar, selectmode=tk.EXTENDED, height=20)
        self.file_list.grid(row=3, column=0, sticky="nsew")
        self.file_list.bind("<<ListboxSelect>>", self.on_list_select)
        ttk.Button(sidebar, text="Recarregar", command=self.refresh_list).grid(row=4, column=0, sticky="ew", pady=(6, 0))

        # Main area (painel direito)
        main = ttk.Frame(self, padding=8)
        main.grid(row=0, column=1, sticky="nsew")
        for c in range(3): main.columnconfigure(c, weight=1)
        main.rowconfigure(1, weight=1)

        controls = self._build_controls_frame(main)
        controls.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 8))

        # Preview panels
        self.panelA = self._make_panel(main, "Imagem A (pré-processada)", 1, 0)
        self.panelB = self._make_panel(main, "Imagem B (pré-processada)", 1, 1)
        self.panelR = self._make_panel(main, "Resultado", 1, 2, include_save=True)

    def _build_controls_frame(self, parent):
        controls = ttk.Frame(parent)
        for i in range(4): controls.columnconfigure(i, weight=1)

        # Modo de Operação
        modo_frame = ttk.LabelFrame(controls, text="Modo de Operação")
        modo_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ttk.Radiobutton(modo_frame, text="Lógico (binário)", value="logico", variable=self.modo_var, command=self.update_previews).pack(anchor="w", padx=8, pady=4)
        ttk.Radiobutton(modo_frame, text="Aritmético (tons de cinza)", value="aritmetico", variable=self.modo_var, command=self.update_previews).pack(anchor="w", padx=8, pady=(0,8))

        # Sliders de Limiar
        thrA_frame = ttk.LabelFrame(controls, text="Limiar A")
        thrA_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 8))
        ttk.Scale(thrA_frame, from_=0, to=255, variable=self.thresholdA, command=lambda e: self.update_previews()).pack(fill="x", padx=8, pady=8)
        ttk.Label(thrA_frame, textvariable=self.thresholdA).pack(pady=(0,8))

        thrB_frame = ttk.LabelFrame(controls, text="Limiar B")
        thrB_frame.grid(row=0, column=2, sticky="nsew", padx=(0, 8))
        ttk.Scale(thrB_frame, from_=0, to=255, variable=self.thresholdB, command=lambda e: self.update_previews()).pack(fill="x", padx=8, pady=8)
        ttk.Label(thrB_frame, textvariable=self.thresholdB).pack(pady=(0,8))

        # Botões de Operação
        ops_frame = ttk.LabelFrame(controls, text="Operações")
        ops_frame.grid(row=0, column=3, rowspan=2, sticky="nsew")
        row1 = ttk.Frame(ops_frame); row1.pack(fill="x", expand=True, padx=8, pady=4)
        ttk.Button(row1, text="A + B", command=lambda: self.run_compute("add")).pack(side="left", expand=True, fill="x")
        ttk.Button(row1, text="A − B", command=lambda: self.run_compute("sub")).pack(side="left", expand=True, fill="x", padx=4)
        ttk.Button(row1, text="A × B", command=lambda: self.run_compute("mul")).pack(side="left", expand=True, fill="x")
        ttk.Button(row1, text="A ÷ B", command=lambda: self.run_compute("div")).pack(side="left", expand=True, fill="x", padx=4)

        row2 = ttk.Frame(ops_frame); row2.pack(fill="x", expand=True, padx=8, pady=4)
        ttk.Button(row2, text="A AND B", command=lambda: self.run_compute("and")).pack(side="left", expand=True, fill="x")
        ttk.Button(row2, text="A OR B", command=lambda: self.run_compute("or")).pack(side="left", expand=True, fill="x", padx=4)
        ttk.Button(row2, text="A XOR B", command=lambda: self.run_compute("xor")).pack(side="left", expand=True, fill="x")
        ttk.Button(row2, text="NOT A", command=lambda: self.run_compute("not")).pack(side="left", expand=True, fill="x", padx=4)

        # Botão de Reset
        ttk.Button(controls, text="Resetar limiares (128)", command=self.reset_thresholds).grid(row=1, column=0, columnspan=3, sticky="ew", pady=(6,0), padx=(0,8))
        
        return controls

    def _make_panel(self, parent, title, row, col, include_save=False):
        frame = ttk.LabelFrame(parent, text=title)
        frame.grid(row=row, column=col, sticky="nsew", padx=(0 if col == 0 else 8, 0))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        canvas = tk.Canvas(frame, width=THUMB_W, height=THUMB_H, bg="#f0f0f0")
        canvas.pack(expand=True, fill="both", padx=8, pady=8)

        info = ttk.Label(frame, text="—")
        info.pack(padx=8, pady=(0, 8))

        save_btn = None
        if include_save:
            save_btn = ttk.Button(frame, text="Salvar resultado…", command=self.save_result, state="disabled")
            save_btn.pack(padx=8, pady=(0, 8))

        return {"canvas": canvas, "info": info, "save": save_btn, "photo": None}

    def _render_to_panel(self, panel, img_pil, label_text):
        canvas: tk.Canvas = panel["canvas"]
        canvas.delete("all")
        if panel.get("save"): panel["save"].config(state="disabled")

        if img_pil is None:
            panel["info"].config(text="—")
            panel["photo"] = None
            return

        cw, ch = canvas.winfo_width() or THUMB_W, canvas.winfo_height() or THUMB_H
        img_disp = utils.fit_image(img_pil, (cw, ch))
        photo = ImageTk.PhotoImage(img_disp)
        panel["photo"] = photo # Keep reference
        canvas.create_image(cw // 2, ch // 2, image=photo)
        panel["info"].config(text=label_text)
        if panel.get("save"): panel["save"].config(state="normal")

    def pick_root(self):
        directory = filedialog.askdirectory(title="Escolher diretório raiz")
        if directory:
            self.root_dir = directory
            self.refresh_list()

    def refresh_list(self):
        self.images = utils.list_image_files(self.root_dir)
        self.file_list.delete(0, tk.END)
        for _, rel_path in self.images:
            self.file_list.insert(tk.END, rel_path)

    def on_list_select(self, event=None):
        sel_indices = self.file_list.curselection()
        self.imgA_path, self.imgB_path = None, None
        if len(sel_indices) >= 1:
            self.imgA_path = self.images[sel_indices[0]][0]
        if len(sel_indices) >= 2:
            self.imgB_path = self.images[sel_indices[1]][0]
        self.load_selected_images()

    def load_selected_images(self):
        try:
            self.imgA_pil = Image.open(self.imgA_path) if self.imgA_path else None
            self.imgB_pil = Image.open(self.imgB_path) if self.imgB_path else None
        except Exception as e:
            messagebox.showerror("Erro ao carregar imagem", str(e))
        self.update_previews()

    def update_previews(self):
        modo = self.modo_var.get()

        if self.imgA_pil:
            img_a_display = self.imgA_pil.convert("L")
            if modo == "logico":
                a_bin = utils.pil_to_bool_array(self.imgA_pil, self.thresholdA.get())
                img_a_display = utils.bool_array_to_pil(a_bin)
            self._render_to_panel(self.panelA, img_a_display, f"A: {os.path.basename(self.imgA_path)}")
        else:
            self._render_to_panel(self.panelA, None, "—")

        if self.imgB_pil:
            img_b_display = self.imgB_pil.convert("L")
            if modo == "logico":
                b_bin = utils.pil_to_bool_array(self.imgB_pil, self.thresholdB.get())
                img_b_display = utils.bool_array_to_pil(b_bin)
            self._render_to_panel(self.panelB, img_b_display, f"B: {os.path.basename(self.imgB_path)}")
        else:
            self._render_to_panel(self.panelB, None, "—")

        self._render_to_panel(self.panelR, self.result_pil, "Resultado")

    def reset_thresholds(self):
        self.thresholdA.set(128)
        self.thresholdB.set(128)
        self.update_previews()

    def run_compute(self, op: str):
        if not self.imgA_pil:
            messagebox.showwarning("Atenção", "Selecione pelo menos uma imagem (A).")
            return
        if op != "not" and not self.imgB_pil:
            messagebox.showwarning("Atenção", "Selecione duas imagens (A e B) para esta operação.")
            return

        self.result_pil = ops.perform_operation(
            op,
            self.imgA_pil,
            self.imgB_pil,
            self.thresholdA.get(),
            self.thresholdB.get(),
            self.modo_var.get()
        )

        if self.result_pil:
            self._render_to_panel(self.panelR, self.result_pil, "Resultado")
        else:
            messagebox.showerror("Erro", f"A operação '{op}' falhou ou não é válida para o modo atual.")

    def save_result(self):
        if not self.result_pil:
            messagebox.showinfo("Info", "Nenhum resultado para salvar.")
            return
        path = filedialog.asksaveasfilename(
            title="Salvar resultado",
            defaultextension=".png",
            filetypes=[("PNG", ".png"), ("JPEG", ".jpg .jpeg"), ("BMP", ".bmp")],
        )
        if path:
            try:
                self.result_pil.save(path)
                messagebox.showinfo("Sucesso", f"Arquivo salvo em: {path}")
            except Exception as e:
                messagebox.showerror("Erro ao salvar", str(e))