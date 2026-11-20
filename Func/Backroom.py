g_Lista_Alunos = []
g_Lista_Cursos = []
g_Lista_Login = []

def opcoes(x):
    if x == 0:
        print("\nCadastro de Administrador:\n")
        usuario = input("Insira o nome do administrador:\n")
        senha = input("Insira a senha do administrador:\n")
        print(f"Nome do Administrador: {usuario}\nSenha: {senha}\n")
        g_Lista_Login.append((usuario, senha))
        print("\nAdministrador cadastrado com sucesso!\n")
    if x == 1:
        print("\nCadastro de Aluno:\n")
        nome = input("Insira o nome do aluno:\n")
        idade = int(input("Insira a idade do aluno:\n"))
        curso = input("Insira o curso do aluno:\n")
        print(f"Nome: {nome}\nIdade: {idade}\nCurso: {curso}\n" )
        g_Lista_Alunos.append((nome, idade, curso))
        print("\nAluno cadastrado com sucesso!\n")

    elif x == 2:
        print("\nListagem de Alunos:\n")
        if not g_Lista_Alunos:
            print("\nNenhum aluno cadastrado.\n")
        else:
            for nome, idade, curso in g_Lista_Alunos:
                print(f"Nome: {nome}\nIdade: {idade}\nCurso: {curso}\n")
    elif x == 3:
        print("\nExclusão de Aluno:\n")
        nome_exclusao = input("Insira o nome do aluno a ser excluído:\n")
        encontrado = False
        for i, (nome, idade, curso) in enumerate(g_Lista_Alunos):
            if nome.lower() == nome_exclusao.lower():
                g_Lista_Alunos.pop(i)
                print("\nAluno excluído com sucesso!\n")
                encontrado = True
                break
        if not encontrado:
            print("\nAluno não encontrado.\n")
    elif x == 4:
        print("\nCadastro de Curso:\n")
        nome_curso = input("Insira o nome do curso:\n")
        duracao = input("Insira a duração do curso:\n")
        print(f"Nome do Curso: {nome_curso}\nDuração: {duracao}\n")
        g_Lista_Cursos.append((nome_curso, duracao))
        print("\nCurso cadastrado com sucesso!\n")
    elif x == 5:
        print("\nListagem de Cursos:\n")
        if not g_Lista_Cursos:
            print("\nNenhum curso cadastrado.\n")
        else:
            for nome_curso, duracao in g_Lista_Cursos:
                print(f"Nome do Curso: {nome_curso}\nDuração: {duracao}\n")
    elif x == 6:
        print("\nExclusão de Curso:\n")
        nome_exclusao_curso = input("Insira o nome do curso a ser excluído:\n")
        encontrado = False
        for i, (nome_curso, duracao) in enumerate(g_Lista_Cursos):
            if nome_curso.lower() == nome_exclusao_curso.lower():
                g_Lista_Cursos.pop(i)
                print("\nCurso excluído com sucesso!\n")
                encontrado = True
                break
        if not encontrado:
            print("\nCurso não encontrado.\n")
    elif x == 7:
        print("\nPesquisa de Alunos:\n")
        nome_pesquisa = input("Insira o nome do aluno a ser pesquisado:\n")
        encontrado = False
        for nome, idade, curso in g_Lista_Alunos:
            if nome.lower() == nome_pesquisa.lower():
                print(f"Nome: {nome}\nIdade: {idade}\nCurso: {curso}\n")
                encontrado = True
                break
        if not encontrado:
            print("\nAluno não encontrado.\n")
    elif x == 8:
        print("\nSaindo do sistema. Até logo!\n")
        exit()
    if x > 10 or x < 0:
        print("\nOpção inválida. Por favor, insira um número válido.")
    if x == 9:
        print("\nSalvando dados...\n")
        with open("admin.txt", "w") as f:
            for usuario, senha in g_Lista_Login:
                f.write(f"{usuario},{senha}\n")
        with open("alunos.txt", "w") as f:
            for nome, idade, curso in g_Lista_Alunos:
                f.write(f"{nome},{idade},{curso}\n")
        with open("cursos.txt", "w") as f:
            for nome_curso, duracao in g_Lista_Cursos:
                f.write(f"{nome_curso},{duracao}\n")
        print("\nDados salvos com sucesso!\n")
    if x == 10:
        print("\nCarregando dados...\n")
        try:
            with open("admin.txt", "r") as f:
                g_Lista_Login.clear()
                for line in f:
                    admin_data = line.rstrip("\r\n").split(",", 1)
                    if len(admin_data) == 2:
                        g_Lista_Login.append((admin_data[0], admin_data[1]))
            with open("alunos.txt", "r") as f:
                g_Lista_Alunos.clear()
                for line in f:
                    nome, idade, curso = line.strip().split(",")
                    g_Lista_Alunos.append((nome, int(idade), curso))
            with open("cursos.txt", "r") as f:
                g_Lista_Cursos.clear()
                for line in f:
                    nome_curso, duracao = line.strip().split(",")
                    g_Lista_Cursos.append((nome_curso, duracao))
            print("\nDados carregados com sucesso!\n")
        except FileNotFoundError:
            print("\nArquivos de dados não encontrados. Nenhum dado foi carregado.\n")
