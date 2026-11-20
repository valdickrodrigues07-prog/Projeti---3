import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk


DATA_DIR = Path(__file__).resolve().parent
FILES = {
    "administradores": DATA_DIR / "admin.txt",
    "alunos": DATA_DIR / "alunos.txt",
    "cursos": DATA_DIR / "cursos.txt",
}


class SistemaGestao:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão de Alunos")
        self.root.geometry("900x600")
        self.root.minsize(760, 500)

        self.administradores = self._ler_arquivo(
            FILES["administradores"], 2
        )
        self.alunos = self._ler_arquivo(FILES["alunos"], 3)
        self.cursos = self._ler_arquivo(FILES["cursos"], 2)

        self._configurar_estilo()
        if self.administradores:
            self._mostrar_login()
        else:
            self._mostrar_cadastro_inicial()

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

    def _configurar_estilo(self):
        estilo = ttk.Style()
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("TFrame", background="#f3f5f8")
        estilo.configure("TLabel", background="#f3f5f8", foreground="#172033")
        estilo.configure("Title.TLabel", font=("Segoe UI", 21, "bold"))
        estilo.configure("Subtitle.TLabel", font=("Segoe UI", 10), foreground="#64748b")
        estilo.configure("TButton", padding=(10, 7))
        estilo.configure("Treeview", rowheight=29, font=("Segoe UI", 10))
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _mostrar_login(self):
        self._mostrar_formulario_acesso("Entrar no sistema", "Entrar")

    def _mostrar_cadastro_inicial(self):
        self._mostrar_formulario_acesso(
            "Crie o primeiro administrador", "Criar administrador", inicial=True
        )

    def _mostrar_formulario_acesso(self, titulo, texto_botao, inicial=False):
        self._limpar_tela()
        tela = ttk.Frame(self.root, padding=32)
        tela.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(tela, text="GESTÃO ESCOLAR", style="Subtitle.TLabel").pack(
            anchor="w", pady=(0, 5)
        )
        ttk.Label(tela, text=titulo, style="Title.TLabel").pack(
            anchor="w", pady=(0, 20)
        )

        ttk.Label(tela, text="Usuário").pack(anchor="w")
        usuario = ttk.Entry(tela, width=38)
        usuario.pack(fill="x", pady=(5, 14))
        ttk.Label(tela, text="Senha").pack(anchor="w")
        senha = ttk.Entry(tela, width=38, show="•")
        senha.pack(fill="x", pady=(5, 20))

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
                    self._mostrar_principal()
            elif (nome, chave) in self.administradores:
                self._mostrar_principal()
            else:
                messagebox.showerror("Acesso negado", "Usuário ou senha incorretos.")
                senha.delete(0, tk.END)

        ttk.Button(tela, text=texto_botao, command=enviar).pack(fill="x")
        senha.bind("<Return>", enviar)
        usuario.focus_set()

    def _mostrar_principal(self):
        self._limpar_tela()
        principal = ttk.Frame(self.root, padding=24)
        principal.pack(fill="both", expand=True)

        cabecalho = ttk.Frame(principal)
        cabecalho.pack(fill="x", pady=(0, 18))
        ttk.Label(
            cabecalho, text="Gestão de alunos e cursos", style="Title.TLabel"
        ).pack(side="left")
        ttk.Button(
            cabecalho, text="Carregar dados", command=self._carregar_dados
        ).pack(side="right", padx=(8, 0))
        ttk.Button(
            cabecalho, text="Salvar dados", command=self._salvar_e_notificar
        ).pack(side="right")

        self.abas = ttk.Notebook(principal)
        self.abas.pack(fill="both", expand=True)
        self._criar_aba_alunos()
        self._criar_aba_cursos()
        self._criar_aba_administradores()

    def _criar_tabela(self, pai, colunas, titulos, larguras):
        container = ttk.Frame(pai, padding=14)
        container.pack(fill="both", expand=True)
        tabela = ttk.Treeview(container, columns=colunas, show="headings")
        for coluna, titulo, largura in zip(colunas, titulos, larguras):
            tabela.heading(coluna, text=titulo)
            tabela.column(coluna, width=largura, anchor="w")
        barra = ttk.Scrollbar(container, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=barra.set)
        tabela.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return tabela

    def _criar_aba_alunos(self):
        aba = ttk.Frame(self.abas)
        self.abas.add(aba, text="Alunos")
        comandos = ttk.Frame(aba, padding=(14, 14, 14, 0))
        comandos.pack(fill="x")
        ttk.Label(comandos, text="Pesquisar:").pack(side="left", padx=(0, 8))
        self.pesquisa_aluno = ttk.Entry(comandos)
        self.pesquisa_aluno.pack(side="left", fill="x", expand=True)
        self.pesquisa_aluno.bind("<KeyRelease>", lambda _e: self._atualizar_alunos())
        ttk.Button(comandos, text="Cadastrar aluno", command=self._formulario_aluno).pack(
            side="left", padx=(10, 0)
        )
        ttk.Button(
            comandos, text="Excluir selecionado", command=self._excluir_aluno
        ).pack(side="left", padx=(8, 0))
        self.tabela_alunos = self._criar_tabela(
            aba, ("nome", "idade", "curso"), ("Nome", "Idade", "Curso"), (300, 90, 300)
        )
        self._atualizar_alunos()

    def _criar_aba_cursos(self):
        aba = ttk.Frame(self.abas)
        self.abas.add(aba, text="Cursos")
        comandos = ttk.Frame(aba, padding=(14, 14, 14, 0))
        comandos.pack(fill="x")
        ttk.Button(comandos, text="Cadastrar curso", command=self._formulario_curso).pack(
            side="left"
        )
        ttk.Button(
            comandos, text="Excluir selecionado", command=self._excluir_curso
        ).pack(side="left", padx=8)
        self.tabela_cursos = self._criar_tabela(
            aba, ("nome", "duracao"), ("Curso", "Duração"), (420, 220)
        )
        self._atualizar_cursos()

    def _criar_aba_administradores(self):
        aba = ttk.Frame(self.abas)
        self.abas.add(aba, text="Administradores")
        comandos = ttk.Frame(aba, padding=(14, 14, 14, 0))
        comandos.pack(fill="x")
        ttk.Button(
            comandos,
            text="Cadastrar administrador",
            command=self._formulario_administrador,
        ).pack(side="left")
        ttk.Button(
            comandos,
            text="Excluir selecionado",
            command=self._excluir_administrador,
        ).pack(side="left", padx=8)
        self.tabela_administradores = self._criar_tabela(
            aba, ("usuario",), ("Usuário",), (420,)
        )
        self._atualizar_administradores()

    def _preencher_tabela(self, tabela, registros, filtro=None):
        tabela.delete(*tabela.get_children())
        for registro in registros:
            if filtro and not filtro(registro):
                continue
            tabela.insert("", "end", values=registro)

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
            self.tabela_administradores, [(usuario,) for usuario, _ in self.administradores]
        )

    def _abrir_formulario(self, titulo, campos, ao_salvar):
        janela = tk.Toplevel(self.root)
        janela.title(titulo)
        janela.resizable(False, False)
        janela.transient(self.root)
        janela.grab_set()
        quadro = ttk.Frame(janela, padding=20)
        quadro.pack(fill="both", expand=True)
        entradas = {}
        for linha, (chave, rotulo, segredo) in enumerate(campos):
            ttk.Label(quadro, text=rotulo).grid(
                row=linha, column=0, sticky="w", pady=6, padx=(0, 12)
            )
            entrada = ttk.Entry(quadro, width=34, show="•" if segredo else "")
            entrada.grid(row=linha, column=1, sticky="ew", pady=6)
            entradas[chave] = entrada

        def salvar():
            valores = {chave: campo.get().strip() for chave, campo in entradas.items()}
            if any(not valor for valor in valores.values()):
                messagebox.showwarning(
                    "Campos obrigatórios", "Preencha todos os campos.", parent=janela
                )
                return
            if ao_salvar(valores):
                janela.destroy()

        ttk.Button(quadro, text="Salvar", command=salvar).grid(
            row=len(campos), column=0, columnspan=2, sticky="ew", pady=(14, 0)
        )
        quadro.columnconfigure(1, weight=1)
        next(iter(entradas.values())).focus_set()

    def _formulario_aluno(self):
        def salvar(valores):
            try:
                idade = int(valores["idade"])
                if idade <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning(
                    "Idade inválida", "Informe uma idade inteira maior que zero."
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
        def salvar(valores):
            self.cursos.append((valores["nome"], valores["duracao"]))
            self._atualizar_cursos()
            return self._salvar_dados()

        self._abrir_formulario(
            "Cadastrar curso",
            [("nome", "Nome do curso", False), ("duracao", "Duração", False)],
            salvar,
        )

    def _formulario_administrador(self):
        def salvar(valores):
            if any(usuario.casefold() == valores["usuario"].casefold()
                   for usuario, _ in self.administradores):
                messagebox.showwarning(
                    "Usuário existente", "Já existe um administrador com esse usuário."
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

    def _excluir_registro(self, tabela, registros, atualizar, descricao, chave):
        selecionados = tabela.selection()
        if not selecionados:
            messagebox.showinfo("Selecione um registro", f"Selecione {descricao} para excluir.")
            return
        valores = tabela.item(selecionados[0], "values")
        if not messagebox.askyesno(
            "Confirmar exclusão", f"Deseja excluir {descricao} '{valores[0]}'?"
        ):
            return
        indice = next(
            (i for i, registro in enumerate(registros) if chave(registro) == tuple(valores)),
            None,
        )
        if indice is not None:
            registros.pop(indice)
            atualizar()
            self._salvar_dados()

    def _excluir_aluno(self):
        self._excluir_registro(
            self.tabela_alunos,
            self.alunos,
            self._atualizar_alunos,
            "o aluno",
            lambda aluno: tuple(map(str, aluno)),
        )

    def _excluir_curso(self):
        self._excluir_registro(
            self.tabela_cursos,
            self.cursos,
            self._atualizar_cursos,
            "o curso",
            lambda curso: tuple(map(str, curso)),
        )

    def _excluir_administrador(self):
        if len(self.administradores) <= 1:
            messagebox.showwarning(
                "Operação não permitida", "O sistema precisa manter ao menos um administrador."
            )
            return
        self._excluir_registro(
            self.tabela_administradores,
            self.administradores,
            self._atualizar_administradores,
            "o administrador",
            lambda administrador: (administrador[0],),
        )

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
