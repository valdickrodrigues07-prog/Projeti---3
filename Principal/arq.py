import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk


DATA_DIR = Path(__file__).resolve().parent
FILES = {
    "administradores": DATA_DIR / "admin.txt",
    "alunos": DATA_DIR / "alunos.txt",
    "cursos": DATA_DIR / "cursos.txt",
}

# ───────────────────────── Tema Tech Teach ─────────────────────────
COR = {
    "bg": "#070B16",
    "painel": "#0C1326",
    "card": "#121B33",
    "zebra": "#0F1730",
    "borda": "#1E2A4A",
    "texto": "#E8EEFB",
    "muted": "#7F8DB0",
    "ciano": "#22D3EE",
    "violeta": "#8B5CF6",
    "verde": "#34D399",
    "perigo": "#F43F5E",
}
FONTE = "Segoe UI"
MONO = "Consolas"


def misturar(c1, c2, t):
    """Mistura duas cores hex (#rrggbb) — usado nos brilhos do painel."""
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(x + (y - x) * t) for x, y in zip(a, b))


class Botao(tk.Label):
    ESTILOS = {
        "primario": ("#22D3EE", "#67E8F9", "#04111F", "#04111F"),
        "fantasma": ("#121B33", "#1E2A4A", "#E8EEFB", "#FFFFFF"),
        "perigo": ("#2A1022", "#F43F5E", "#FB7185", "#FFFFFF"),
    }

    def __init__(self, pai, texto, comando, estilo="primario", **opcoes):
        self.cores = self.ESTILOS[estilo]
        super().__init__(
            pai,
            text=texto,
            bg=self.cores[0],
            fg=self.cores[2],
            font=(FONTE, 10, "bold"),
            padx=16,
            pady=9,
            cursor="hand2",
            **opcoes,
        )
        self.bind("<Enter>", lambda _e: self.config(bg=self.cores[1], fg=self.cores[3]))
        self.bind("<Leave>", lambda _e: self.config(bg=self.cores[0], fg=self.cores[2]))
        self.bind("<Button-1>", lambda _e: comando())


class Campo(tk.Frame):
    """Campo de texto escuro com borda que brilha em ciano ao focar."""

    def __init__(self, pai, segredo=False, largura=30, icone=None):
        super().__init__(pai, bg=COR["borda"], padx=1, pady=1)
        interno = tk.Frame(self, bg=COR["card"])
        interno.pack(fill="x")
        if icone:
            tk.Label(
                interno, text=icone, bg=COR["card"], fg=COR["ciano"], font=(MONO, 11, "bold")
            ).pack(side="left", padx=(12, 0))
        self.entrada = tk.Entry(
            interno,
            width=largura,
            show="•" if segredo else "",
            bg=COR["card"],
            fg=COR["texto"],
            insertbackground=COR["ciano"],
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=(FONTE, 11),
        )
        self.entrada.pack(side="left", fill="x", expand=True, ipady=9, padx=12)
        self.entrada.bind("<FocusIn>", lambda _e: self.config(bg=COR["ciano"]))
        self.entrada.bind("<FocusOut>", lambda _e: self.config(bg=COR["borda"]))

    def get(self):
        return self.entrada.get()

    def limpar(self):
        self.entrada.delete(0, tk.END)

    def focar(self):
        self.entrada.focus_set()

    def vincular(self, evento, funcao):
        self.entrada.bind(evento, funcao, add="+")


class CardStat(tk.Frame):
    def __init__(self, pai, rotulo, cor):
        super().__init__(
            pai, bg=COR["card"], highlightbackground=COR["borda"], highlightthickness=1
        )
        tk.Frame(self, bg=cor, width=3).pack(side="left", fill="y")
        corpo = tk.Frame(self, bg=COR["card"])
        corpo.pack(side="left", padx=16, pady=12)
        tk.Label(
            corpo, text=rotulo.upper(), font=(MONO, 9, "bold"), fg=COR["muted"], bg=COR["card"]
        ).pack(anchor="w")
        self.valor = tk.Label(
            corpo, text="0", font=(FONTE, 24, "bold"), fg=COR["texto"], bg=COR["card"]
        )
        self.valor.pack(anchor="w")

    def definir(self, numero):
        self.valor.config(text=str(numero))


class ItemNav(tk.Frame):
    def __init__(self, pai, icone, texto, comando):
        super().__init__(pai, bg=COR["painel"], cursor="hand2")
        self.ativo = False
        self.barra = tk.Frame(self, bg=COR["painel"], width=3)
        self.barra.pack(side="left", fill="y")
        self.rotulo = tk.Label(
            self,
            text=f"{icone}   {texto}",
            font=(FONTE, 11),
            anchor="w",
            padx=18,
            pady=13,
            bg=COR["painel"],
            fg=COR["muted"],
            cursor="hand2",
        )
        self.rotulo.pack(side="left", fill="x", expand=True)
        for widget in (self, self.rotulo):
            widget.bind("<Button-1>", lambda _e: comando())
            widget.bind("<Enter>", lambda _e: self._pintar(True))
            widget.bind("<Leave>", lambda _e: self._pintar(False))

    def definir_ativo(self, ativo):
        self.ativo = ativo
        self._pintar(False)

    def _pintar(self, hover):
        if self.ativo:
            bg, fg, barra = COR["card"], COR["texto"], COR["ciano"]
        elif hover:
            bg, fg, barra = "#101930", COR["texto"], COR["painel"]
        else:
            bg, fg, barra = COR["painel"], COR["muted"], COR["painel"]
        self.config(bg=bg)
        self.rotulo.config(bg=bg, fg=fg)
        self.barra.config(bg=barra)


class PainelMarca(tk.Canvas):
    """Painel lateral da tela de login: grade, brilhos neon e trilhas de circuito."""

    def __init__(self, pai):
        super().__init__(pai, bg=COR["bg"], highlightthickness=0)
        self.bind("<Configure>", self._desenhar)

    def _desenhar(self, _evento=None):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 50 or h < 50:
            return
        bg = COR["bg"]

        for cx, cy, raio_max, cor in (
            (w * 0.85, h * 0.12, 330, COR["violeta"]),
            (w * 0.05, h * 0.95, 300, COR["ciano"]),
        ):
            for i in range(14, 0, -1):
                raio = raio_max * i / 14
                intensidade = (1 - i / 14) ** 1.6 * 0.30
                self.create_oval(
                    cx - raio, cy - raio, cx + raio, cy + raio,
                    fill=misturar(bg, cor, intensidade), outline="",
                )

        grade = misturar(bg, "#FFFFFF", 0.05)
        for x in range(0, w, 44):
            self.create_line(x, 0, x, h, fill=grade)
        for y in range(0, h, 44):
            self.create_line(0, y, w, y, fill=grade)

        trilhas = (
            ((0.00, 0.72), (0.22, 0.72), (0.28, 0.78), (0.55, 0.78)),
            ((0.00, 0.82), (0.12, 0.82), (0.18, 0.88), (0.40, 0.88)),
            ((0.64, 1.00), (0.64, 0.92), (0.72, 0.84), (1.00, 0.84)),
        )
        for trilha in trilhas:
            pontos = [(x * w, y * h) for x, y in trilha]
            self.create_line(
                *[c for p in pontos for c in p], fill=misturar(bg, COR["ciano"], 0.5), width=2
            )
            x, y = pontos[-1]
            self.create_oval(x - 4, y - 4, x + 4, y + 4, outline=COR["ciano"], fill=bg, width=2)

        y0 = h * 0.22
        self.create_text(56, y0, text="</>", anchor="w", font=(MONO, 34, "bold"), fill=COR["ciano"])
        self.create_text(
            56, y0 + 62, text="TECH TEACH", anchor="w", font=(FONTE, 38, "bold"), fill=COR["texto"]
        )
        self.create_line(58, y0 + 100, 148, y0 + 100, width=3, fill=COR["violeta"])
        self.create_text(
            56, y0 + 122, text="Gestão inteligente de alunos,\ncursos e acessos.",
            anchor="nw", font=(FONTE, 14), fill=COR["muted"],
        )
        self.create_text(
            56, y0 + 205, text="[ alunos ]  [ cursos ]  [ admins ]",
            anchor="w", font=(MONO, 11), fill=misturar(bg, COR["ciano"], 0.8),
        )
        self.create_oval(56, h - 44, 66, h - 34, fill=COR["verde"], outline="")
        self.create_text(
            76, h - 39, text="SISTEMA ONLINE  //  v2.0",
            anchor="w", font=(MONO, 10), fill=COR["muted"],
        )


# ───────────────────────── Aplicação ─────────────────────────
class SistemaGestao:
    TITULOS = {
        "alunos": ("Alunos", "// gerencie matrículas e cursos"),
        "cursos": ("Cursos", "// catálogo de cursos e durações"),
        "admins": ("Administradores", "// controle de acessos ao sistema"),
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Tech Teach • Sistema de Gestão de Alunos")
        self.root.configure(bg=COR["bg"])
        self.root.minsize(940, 620)
        self._centralizar(self.root, 1120, 700)

        self.administradores = self._ler_arquivo(FILES["administradores"], 2)
        self.alunos = self._ler_arquivo(FILES["alunos"], 3)
        self.cursos = self._ler_arquivo(FILES["cursos"], 2)
        self.usuario_atual = ""

        self._configurar_estilo()
        if self.administradores:
            self._mostrar_login()
        else:
            self._mostrar_cadastro_inicial()
        self._barra_escura()

    # ── Dados (lógica original preservada) ──
    @staticmethod
    def _ler_arquivo(caminho, quantidade_campos):
        registros = []
        if not caminho.exists():
            return registros

        with caminho.open("r", encoding="utf-8") as arquivo:
            for numero, linha in enumerate(arquivo, start=1):
                campos = linha.rstrip("\r\n").split(",")
                if len(campos) != quantidade_campos:
                    raise ValueError(
                        f"Formato inválido em {caminho.name}, linha {numero}."
                    )
                if quantidade_campos == 3:
                    try:
                        campos[1] = int(campos[1])
                    except ValueError as erro:
                        raise ValueError(
                            f"Idade inválida em {caminho.name}, linha {numero}."
                        ) from erro
                registros.append(tuple(campos))
        return registros

    def _salvar_dados(self):
        conteudos = {
            "administradores": self.administradores,
            "alunos": self.alunos,
            "cursos": self.cursos,
        }
        try:
            for chave, registros in conteudos.items():
                with FILES[chave].open("w", encoding="utf-8") as arquivo:
                    for registro in registros:
                        arquivo.write(",".join(map(str, registro)) + "\n")
        except OSError as erro:
            messagebox.showerror(
                "Erro ao salvar", f"Não foi possível salvar os dados:\n{erro}"
            )
            return False
        return True

    # ── Utilidades visuais ──
    def _barra_escura(self):
        """Barra de título escura no Windows 10/11 (ignorado em outros sistemas)."""
        try:
            import ctypes

            self.root.update()
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 20, ctypes.byref(ctypes.c_int(1)), 4
            )
        except Exception:
            pass

    @staticmethod
    def _centralizar(janela, largura=None, altura=None, pai=None):
        janela.update_idletasks()
        largura = largura or janela.winfo_reqwidth()
        altura = altura or janela.winfo_reqheight()
        if pai is not None:
            x = pai.winfo_rootx() + (pai.winfo_width() - largura) // 2
            y = pai.winfo_rooty() + (pai.winfo_height() - altura) // 2
        else:
            x = (janela.winfo_screenwidth() - largura) // 2
            y = (janela.winfo_screenheight() - altura) // 2
        janela.geometry(f"{largura}x{altura}+{max(x, 0)}+{max(y, 0)}")

    def _configurar_estilo(self):
        estilo = ttk.Style()
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure(
            "Tech.Treeview",
            background=COR["card"],
            fieldbackground=COR["card"],
            foreground=COR["texto"],
            rowheight=40,
            borderwidth=0,
            font=(FONTE, 10),
        )
        estilo.layout("Tech.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        estilo.map(
            "Tech.Treeview",
            background=[("selected", "#16365A")],
            foreground=[("selected", "#FFFFFF")],
        )
        estilo.configure(
            "Tech.Treeview.Heading",
            background=COR["painel"],
            foreground=COR["ciano"],
            font=(MONO, 10, "bold"),
            relief="flat",
            borderwidth=0,
            padding=(12, 11),
        )
        estilo.map("Tech.Treeview.Heading", background=[("active", COR["painel"])])
        estilo.configure(
            "Tech.Vertical.TScrollbar",
            background=COR["borda"],
            troughcolor=COR["card"],
            bordercolor=COR["card"],
            arrowcolor=COR["muted"],
            lightcolor=COR["borda"],
            darkcolor=COR["borda"],
            relief="flat",
            gripcount=0,
        )
        estilo.map("Tech.Vertical.TScrollbar", background=[("active", "#2B3B66")])

    def _limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ── Login ──
    def _mostrar_login(self):
        self._mostrar_formulario_acesso("Entrar no sistema", "Entrar")

    def _mostrar_cadastro_inicial(self):
        self._mostrar_formulario_acesso(
            "Crie o primeiro administrador", "Criar administrador", inicial=True
        )

    def _mostrar_formulario_acesso(self, titulo, texto_botao, inicial=False):
        self._limpar_tela()
        PainelMarca(self.root).pack(side="left", fill="both", expand=True)

        lado = tk.Frame(self.root, bg=COR["painel"], width=460)
        lado.pack(side="right", fill="y")
        lado.pack_propagate(False)
        tk.Frame(lado, bg=COR["borda"], width=1).pack(side="left", fill="y")

        form = tk.Frame(lado, bg=COR["painel"])
        form.place(relx=0.5, rely=0.5, anchor="center", width=340)

        tk.Label(
            form,
            text="// PRIMEIRO ACESSO" if inicial else "// ACESSO RESTRITO",
            font=(MONO, 10, "bold"), fg=COR["ciano"], bg=COR["painel"],
        ).pack(anchor="w")
        tk.Label(
            form, text=titulo, font=(FONTE, 22, "bold"), fg=COR["texto"],
            bg=COR["painel"], wraplength=340, justify="left",
        ).pack(anchor="w", pady=(6, 4))
        tk.Label(
            form, text="Use as credenciais de administrador.",
            font=(FONTE, 10), fg=COR["muted"], bg=COR["painel"],
        ).pack(anchor="w", pady=(0, 26))

        tk.Label(
            form, text="USUÁRIO", font=(MONO, 9, "bold"), fg=COR["muted"], bg=COR["painel"]
        ).pack(anchor="w")
        usuario = Campo(form, icone="@")
        usuario.pack(fill="x", pady=(5, 16))
        tk.Label(
            form, text="SENHA", font=(MONO, 9, "bold"), fg=COR["muted"], bg=COR["painel"]
        ).pack(anchor="w")
        senha = Campo(form, segredo=True, icone="#")
        senha.pack(fill="x", pady=(5, 24))

        def enviar(_evento=None):
            nome = usuario.get().strip()
            chave = senha.get()
            if not nome or not chave:
                messagebox.showwarning(
                    "Campos obrigatórios", "Informe o usuário e a senha."
                )
                return

            if inicial:
                self.administradores.append((nome, chave))
                if self._salvar_dados():
                    self.usuario_atual = nome
                    self._mostrar_principal()
            elif (nome, chave) in self.administradores:
                self.usuario_atual = nome
                self._mostrar_principal()
            else:
                messagebox.showerror("Acesso negado", "Usuário ou senha incorretos.")
                senha.limpar()

        Botao(form, texto_botao, enviar).pack(fill="x")
        usuario.vincular("<Return>", enviar)
        senha.vincular("<Return>", enviar)
        usuario.focar()

    # ── Tela principal ──
    def _mostrar_principal(self):
        self._limpar_tela()

        lateral = tk.Frame(self.root, bg=COR["painel"], width=240)
        lateral.pack(side="left", fill="y")
        lateral.pack_propagate(False)
        tk.Frame(self.root, bg=COR["borda"], width=1).pack(side="left", fill="y")

        marca = tk.Frame(lateral, bg=COR["painel"])
        marca.pack(fill="x", padx=22, pady=(26, 30))
        tk.Label(
            marca, text="</>", font=(MONO, 18, "bold"), fg=COR["ciano"], bg=COR["painel"]
        ).pack(side="left")
        tk.Label(
            marca, text=" TECH TEACH", font=(FONTE, 14, "bold"), fg=COR["texto"], bg=COR["painel"]
        ).pack(side="left")

        tk.Label(
            lateral, text="// MENU", font=(MONO, 9, "bold"), fg=COR["muted"], bg=COR["painel"]
        ).pack(anchor="w", padx=22, pady=(0, 8))

        self.navegacao = {}
        for chave, icone, nome in (
            ("alunos", "◉", "Alunos"),
            ("cursos", "▤", "Cursos"),
            ("admins", "◆", "Administradores"),
        ):
            item = ItemNav(lateral, icone, nome, lambda c=chave: self._ir_para(c))
            item.pack(fill="x")
            self.navegacao[chave] = item

        rodape = tk.Frame(lateral, bg=COR["painel"])
        rodape.pack(side="bottom", fill="x", padx=18, pady=20)
        tk.Label(
            rodape, text="● ONLINE", font=(MONO, 9, "bold"), fg=COR["verde"], bg=COR["painel"]
        ).pack(anchor="w")
        tk.Label(
            rodape, text=self.usuario_atual or "admin", font=(FONTE, 11, "bold"),
            fg=COR["texto"], bg=COR["painel"],
        ).pack(anchor="w", pady=(2, 0))
        Botao(rodape, "Sair", self._mostrar_login, "fantasma").pack(fill="x", pady=(12, 0))

        conteudo = tk.Frame(self.root, bg=COR["bg"])
        conteudo.pack(side="left", fill="both", expand=True)

        cabecalho = tk.Frame(conteudo, bg=COR["bg"])
        cabecalho.pack(fill="x", padx=28, pady=(26, 18))
        titulos = tk.Frame(cabecalho, bg=COR["bg"])
        titulos.pack(side="left")
        self.titulo_pagina = tk.Label(
            titulos, font=(FONTE, 22, "bold"), fg=COR["texto"], bg=COR["bg"]
        )
        self.titulo_pagina.pack(anchor="w")
        self.subtitulo_pagina = tk.Label(
            titulos, font=(MONO, 10), fg=COR["muted"], bg=COR["bg"]
        )
        self.subtitulo_pagina.pack(anchor="w")
        Botao(cabecalho, "Salvar dados", self._salvar_e_notificar).pack(side="right")
        Botao(cabecalho, "Carregar dados", self._carregar_dados, "fantasma").pack(
            side="right", padx=(0, 10)
        )

        estatisticas = tk.Frame(conteudo, bg=COR["bg"])
        estatisticas.pack(fill="x", padx=28, pady=(0, 18))
        self.stats = {}
        for i, (chave, rotulo, cor) in enumerate(
            (
                ("alunos", "Alunos", COR["ciano"]),
                ("cursos", "Cursos", COR["violeta"]),
                ("admins", "Administradores", COR["verde"]),
            )
        ):
            card = CardStat(estatisticas, rotulo, cor)
            card.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 14, 0))
            estatisticas.columnconfigure(i, weight=1, uniform="stat")
            self.stats[chave] = card

        area = tk.Frame(conteudo, bg=COR["bg"])
        area.pack(fill="both", expand=True, padx=28, pady=(0, 26))
        self.paginas = {}
        self._criar_aba_alunos(area)
        self._criar_aba_cursos(area)
        self._criar_aba_administradores(area)
        self._ir_para("alunos")

    def _ir_para(self, chave):
        for pagina in self.paginas.values():
            pagina.pack_forget()
        self.paginas[chave].pack(fill="both", expand=True)
        for nome, item in self.navegacao.items():
            item.definir_ativo(nome == chave)
        titulo, subtitulo = self.TITULOS[chave]
        self.titulo_pagina.config(text=titulo)
        self.subtitulo_pagina.config(text=subtitulo)

    def _atualizar_stats(self):
        if not getattr(self, "stats", None):
            return
        self.stats["alunos"].definir(len(self.alunos))
        self.stats["cursos"].definir(len(self.cursos))
        self.stats["admins"].definir(len(self.administradores))

    # ── Tabelas ──
    def _nova_pagina(self, pai, chave):
        pagina = tk.Frame(pai, bg=COR["bg"])
        self.paginas[chave] = pagina
        barra = tk.Frame(pagina, bg=COR["bg"])
        barra.pack(fill="x")
        return pagina, barra

    def _criar_tabela(self, pai, colunas, titulos, larguras, mensagem_vazia):
        moldura = tk.Frame(
            pai, bg=COR["card"], highlightbackground=COR["borda"], highlightthickness=1
        )
        moldura.pack(fill="both", expand=True, pady=(16, 0))
        tabela = ttk.Treeview(
            moldura, columns=colunas, show="headings", style="Tech.Treeview", selectmode="browse"
        )
        for coluna, titulo, largura in zip(colunas, titulos, larguras):
            tabela.heading(coluna, text=titulo.upper(), anchor="w")
            tabela.column(coluna, width=largura, anchor="w")
        barra = ttk.Scrollbar(
            moldura, orient="vertical", command=tabela.yview, style="Tech.Vertical.TScrollbar"
        )
        tabela.configure(yscrollcommand=barra.set)
        tabela.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        tabela.tag_configure("par", background=COR["card"])
        tabela.tag_configure("impar", background=COR["zebra"])
        tabela.vazio = tk.Label(
            moldura, text=mensagem_vazia, font=(MONO, 11), fg=COR["muted"], bg=COR["card"]
        )
        return tabela

    def _criar_aba_alunos(self, pai):
        pagina, comandos = self._nova_pagina(pai, "alunos")
        self.pesquisa_aluno = Campo(comandos, icone=">", largura=32)
        self.pesquisa_aluno.pack(side="left")
        self.pesquisa_aluno.vincular("<KeyRelease>", lambda _e: self._atualizar_alunos())
        Botao(comandos, "Excluir selecionado", self._excluir_aluno, "perigo").pack(side="right")
        Botao(comandos, "+  Cadastrar aluno", self._formulario_aluno).pack(
            side="right", padx=(0, 10)
        )
        self.tabela_alunos = self._criar_tabela(
            pagina, ("nome", "idade", "curso"), ("Nome", "Idade", "Curso"),
            (320, 90, 320), "// nenhum aluno encontrado",
        )
        self._atualizar_alunos()

    def _criar_aba_cursos(self, pai):
        pagina, comandos = self._nova_pagina(pai, "cursos")
        Botao(comandos, "Excluir selecionado", self._excluir_curso, "perigo").pack(side="right")
        Botao(comandos, "+  Cadastrar curso", self._formulario_curso).pack(
            side="right", padx=(0, 10)
        )
        self.tabela_cursos = self._criar_tabela(
            pagina, ("nome", "duracao"), ("Curso", "Duração"),
            (440, 220), "// nenhum curso cadastrado",
        )
        self._atualizar_cursos()

    def _criar_aba_administradores(self, pai):
        pagina, comandos = self._nova_pagina(pai, "admins")
        Botao(comandos, "Excluir selecionado", self._excluir_administrador, "perigo").pack(
            side="right"
        )
        Botao(comandos, "+  Cadastrar administrador", self._formulario_administrador).pack(
            side="right", padx=(0, 10)
        )
        self.tabela_administradores = self._criar_tabela(
            pagina, ("usuario",), ("Usuário",), (440,), "// nenhum administrador"
        )
        self._atualizar_administradores()

    def _preencher_tabela(self, tabela, registros, filtro=None):
        tabela.delete(*tabela.get_children())
        exibidos = 0
        for indice, registro in enumerate(registros):
            if filtro and not filtro(registro):
                continue
            tag = "par" if exibidos % 2 == 0 else "impar"
            # o iid guarda a posição real na lista, para excluir com segurança
            tabela.insert("", "end", iid=str(indice), values=registro, tags=(tag,))
            exibidos += 1
        if exibidos:
            tabela.vazio.place_forget()
        else:
            tabela.vazio.place(relx=0.5, rely=0.55, anchor="center")
        self._atualizar_stats()

    def _atualizar_alunos(self):
        consulta = self.pesquisa_aluno.get().strip().casefold()
        self._preencher_tabela(
            self.tabela_alunos,
            self.alunos,
            lambda aluno: consulta in aluno[0].casefold()
            or consulta in aluno[2].casefold(),
        )

    def _atualizar_cursos(self):
        self._preencher_tabela(self.tabela_cursos, self.cursos)

    def _atualizar_administradores(self):
        self._preencher_tabela(
            self.tabela_administradores,
            [(usuario,) for usuario, _ in self.administradores],
        )

    # ── Formulários ──
    def _abrir_formulario(self, titulo, campos, ao_salvar):
        janela = tk.Toplevel(self.root)
        janela.title(titulo)
        janela.configure(bg=COR["painel"])
        janela.resizable(False, False)
        janela.transient(self.root)

        quadro = tk.Frame(janela, bg=COR["painel"], padx=30, pady=28)
        quadro.pack(fill="both", expand=True)
        tk.Label(
            quadro, text="// NOVO REGISTRO", font=(MONO, 9, "bold"),
            fg=COR["ciano"], bg=COR["painel"],
        ).pack(anchor="w")
        tk.Label(
            quadro, text=titulo, font=(FONTE, 18, "bold"), fg=COR["texto"], bg=COR["painel"]
        ).pack(anchor="w", pady=(4, 20))

        entradas = {}
        for chave, rotulo, segredo in campos:
            tk.Label(
                quadro, text=rotulo.upper(), font=(MONO, 9, "bold"),
                fg=COR["muted"], bg=COR["painel"],
            ).pack(anchor="w")
            campo = Campo(quadro, segredo=segredo, largura=36)
            campo.pack(fill="x", pady=(5, 16))
            entradas[chave] = campo

        def salvar(_evento=None):
            valores = {chave: campo.get().strip() for chave, campo in entradas.items()}
            if any(not valor for valor in valores.values()):
                messagebox.showwarning(
                    "Campos obrigatórios", "Preencha todos os campos.", parent=janela
                )
                return
            if ao_salvar(valores, janela):
                janela.destroy()

        botoes = tk.Frame(quadro, bg=COR["painel"])
        botoes.pack(fill="x", pady=(6, 0))
        Botao(botoes, "Salvar", salvar).pack(side="right")
        Botao(botoes, "Cancelar", janela.destroy, "fantasma").pack(side="right", padx=(0, 10))

        janela.bind("<Return>", salvar)
        janela.bind("<Escape>", lambda _e: janela.destroy())
        self._centralizar(janela, pai=self.root)
        janela.wait_visibility()
        janela.grab_set()
        next(iter(entradas.values())).focar()

    def _formulario_aluno(self):
        def salvar(valores, janela):
            try:
                idade = int(valores["idade"])
                if idade <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning(
                    "Idade inválida",
                    "Informe uma idade inteira maior que zero.",
                    parent=janela,
                )
                return False
            self.alunos.append((valores["nome"], idade, valores["curso"]))
            self._atualizar_alunos()
            return self._salvar_dados()

        self._abrir_formulario(
            "Cadastrar aluno",
            [
                ("nome", "Nome", False),
                ("idade", "Idade", False),
                ("curso", "Curso", False),
            ],
            salvar,
        )

    def _formulario_curso(self):
        def salvar(valores, janela):
            self.cursos.append((valores["nome"], valores["duracao"]))
            self._atualizar_cursos()
            return self._salvar_dados()

        self._abrir_formulario(
            "Cadastrar curso",
            [("nome", "Nome do curso", False), ("duracao", "Duração", False)],
            salvar,
        )

    def _formulario_administrador(self):
        def salvar(valores, janela):
            if any(
                usuario.casefold() == valores["usuario"].casefold()
                for usuario, _ in self.administradores
            ):
                messagebox.showwarning(
                    "Usuário existente",
                    "Já existe um administrador com esse usuário.",
                    parent=janela,
                )
                return False
            self.administradores.append((valores["usuario"], valores["senha"]))
            self._atualizar_administradores()
            return self._salvar_dados()

        self._abrir_formulario(
            "Cadastrar administrador",
            [("usuario", "Usuário", False), ("senha", "Senha", True)],
            salvar,
        )

    # ── Exclusão ──
    def _excluir_registro(self, tabela, registros, atualizar, descricao):
        selecionados = tabela.selection()
        if not selecionados:
            messagebox.showinfo(
                "Selecione um registro", f"Selecione {descricao} para excluir."
            )
            return
        indice = int(selecionados[0])
        registro = registros[indice]
        if not messagebox.askyesno(
            "Confirmar exclusão", f"Deseja excluir {descricao} '{registro[0]}'?"
        ):
            return
        registros.pop(indice)
        atualizar()
        self._salvar_dados()

    def _excluir_aluno(self):
        self._excluir_registro(
            self.tabela_alunos, self.alunos, self._atualizar_alunos, "o aluno"
        )

    def _excluir_curso(self):
        self._excluir_registro(
            self.tabela_cursos, self.cursos, self._atualizar_cursos, "o curso"
        )

    def _excluir_administrador(self):
        if len(self.administradores) <= 1:
            messagebox.showwarning(
                "Operação não permitida",
                "O sistema precisa manter ao menos um administrador.",
            )
            return
        self._excluir_registro(
            self.tabela_administradores,
            self.administradores,
            self._atualizar_administradores,
            "o administrador",
        )

    # ── Carregar / salvar ──
    def _carregar_dados(self):
        try:
            self.administradores = self._ler_arquivo(FILES["administradores"], 2)
            self.alunos = self._ler_arquivo(FILES["alunos"], 3)
            self.cursos = self._ler_arquivo(FILES["cursos"], 2)
        except (OSError, ValueError) as erro:
            messagebox.showerror("Erro ao carregar", str(erro))
            return
        self._atualizar_alunos()
        self._atualizar_cursos()
        self._atualizar_administradores()
        messagebox.showinfo("Dados carregados", "Os dados foram carregados com sucesso.")

    def _salvar_e_notificar(self):
        if self._salvar_dados():
            messagebox.showinfo("Dados salvos", "Os dados foram salvos com sucesso.")


def main():
    root = tk.Tk()
    try:
        SistemaGestao(root)
    except (OSError, ValueError) as erro:
        messagebox.showerror("Erro ao abrir dados", str(erro))
        root.destroy()
        return
    root.mainloop()


if __name__ == "__main__":
    main()