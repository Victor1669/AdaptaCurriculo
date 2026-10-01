import os

from .dados import carregar_csv, garantir_csvs, resetar_csvs, salvar_csv
from .gerador import gerar_docx


def limpar():
    os.system("clear" if os.name != "nt" else "cls")


def escolher_opcao(titulo, opcoes):
    while True:
        print(f"\n{titulo}")
        print("-" * 40)
        for i, op in enumerate(opcoes, 1):
            print(f"  {i}. {op}")
        print("  0. Voltar")
        escolha = input("\nEscolha: ").strip()
        if escolha == "0":
            return None
        if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
            return opcoes[int(escolha) - 1]
        print("Opção inválida.")


def ler_multilinha():
    """Lê várias linhas e une num parágrafo. Linha vazia finaliza."""
    print("(Escreva o texto; Enter numa linha vazia finaliza. Linhas serão unidas.)")
    while True:
        linhas = []
        while True:
            linha = input()
            if linha == "":
                break
            linhas.append(linha.strip())
        texto = " ".join(part for part in linhas if part).strip()
        if not texto:
            return ""
        print(f"\nTexto final:\n{texto}\n")
        resp = input("Confirmar? (S/n/refazer): ").strip().lower()
        if resp in ("", "s", "sim"):
            return texto
        if resp in ("n", "nao", "não"):
            return ""
        print("Digite novamente:\n")


def listar_categorias(cats):
    for i, c in enumerate(cats, 1):
        print(f"  {i}. {c['categoria']}")


def converter_numeros(nums, cats):
    selecionadas = []
    for n in nums:
        if n.isdigit() and 1 <= int(n) <= len(cats):
            selecionadas.append(cats[int(n) - 1]["categoria"])
    return selecionadas


def menu_gerar():
    limpar()
    print("=== GERAR CURRÍCULO ===\n")

    combinacoes = carregar_csv("combinacoes.csv")
    cargos = sorted(set(c["cargo"] for c in combinacoes))

    cargo = escolher_opcao("Escolha o Cargo:", cargos)
    if not cargo:
        return

    cats_do_cargo = sorted(set(c["categoria"] for c in combinacoes if c["cargo"] == cargo))
    categoria = escolher_opcao(f"Escolha a Categoria para '{cargo}':", cats_do_cargo)
    if not categoria:
        return

    niveis = [n["nivel"] for n in carregar_csv("niveis.csv")]
    nivel = escolher_opcao("Escolha o Nível:", niveis)
    if not nivel:
        return

    comb = next(c for c in combinacoes if c["cargo"] == cargo and c["categoria"] == categoria)
    suporte_default = comb["suporte"].lower() == "true"

    print(f"\nSuporte de TI pré-definido: {'Sim' if suporte_default else 'Não'}")
    resp = input("Deseja alterar? (s/N): ").strip().lower()
    if resp == "s":
        suporte = input("Incluir Suporte de TI? (s/N): ").strip().lower() == "s"
    else:
        suporte = suporte_default

    print("\nGerando currículo...")
    try:
        caminho = gerar_docx(
            cargo=cargo,
            categoria=categoria,
            nivel=nivel,
            objetivo=comb["objetivo"],
            suporte=suporte,
            categorias_tech=comb["categorias_tech"],
        )
    except ValueError as e:
        print(f"\nErro: {e}")
        input("\nPressione Enter para continuar...")
        return
    print("\nCurrículo gerado com sucesso!")
    print(f"Arquivo: {caminho}")
    input("\nPressione Enter para continuar...")


def menu_adicionar_combinacao():
    limpar()
    print("=== ADICIONAR COMBINAÇÃO (Cargo + Categoria) ===\n")

    cargo = input("Cargo (ex: Desenvolvedor): ").strip()
    if not cargo:
        return

    categoria = input("Categoria (ex: Frontend): ").strip()
    if not categoria:
        return

    print("\nObjetivo profissional (pode ser longo, pressione Enter duas vezes para terminar):")
    objetivo = ler_multilinha()
    if not objetivo:
        print("Objetivo não pode ser vazio.")
        input("Enter para voltar...")
        return

    suporte = input("Suporte de TI padrão? (s/N): ").strip().lower() == "s"

    print("\nCategorias de tecnologia disponíveis:")
    cats = carregar_csv("categorias_tech.csv")
    listar_categorias(cats)
    print("Digite os números separados por espaço (ex: 1 6):")
    selecionadas = converter_numeros(input("> ").strip().split(), cats)
    if not selecionadas:
        print("Nenhuma categoria selecionada.")
        input("Enter para voltar...")
        return

    combinacoes = carregar_csv("combinacoes.csv")
    combinacoes.append({
        "cargo": cargo,
        "categoria": categoria,
        "objetivo": objetivo,
        "suporte": "true" if suporte else "false",
        "categorias_tech": "|".join(selecionadas),
    })
    salvar_csv("combinacoes.csv", ["cargo", "categoria", "objetivo", "suporte", "categorias_tech"], combinacoes)
    print("\nCombinação adicionada com sucesso!")
    input("Enter para continuar...")


def menu_adicionar_curso():
    limpar()
    print("=== ADICIONAR CURSO ===\n")

    titulo = input("Título completo do curso: ").strip()
    if not titulo:
        return

    print("\nCategorias (digite números separados por espaço, ou 0 para TODOS):")
    cats = carregar_csv("categorias_tech.csv")
    listar_categorias(cats)
    print("  0. TODOS")
    nums = input("> ").strip().split()
    if "0" in nums:
        categorias = "TODOS"
    else:
        selecionadas = converter_numeros(nums, cats)
        categorias = "|".join(selecionadas) if selecionadas else "TODOS"

    data = input("Data (ex: Jan 2025 – Mar 2025): ").strip()

    cursos = carregar_csv("cursos.csv")
    cursos.append({"titulo": titulo, "categorias": categorias, "data": data})
    salvar_csv("cursos.csv", ["titulo", "categorias", "data"], cursos)
    print("\nCurso adicionado!")
    input("Enter para continuar...")


def menu_adicionar_projeto():
    limpar()
    print("=== ADICIONAR PROJETO ===\n")

    nome = input("Nome do projeto: ").strip()
    if not nome:
        return

    print("Descrição (Enter duas vezes para terminar):")
    descricao = ler_multilinha()

    print("\nCategorias de tecnologia:")
    cats = carregar_csv("categorias_tech.csv")
    listar_categorias(cats)
    selecionadas = converter_numeros(input("Números separados por espaço: ").strip().split(), cats)

    link = input("Link GitHub: ").strip()

    projetos = carregar_csv("projetos.csv")
    projetos.append({
        "nome": nome,
        "descricao": descricao,
        "categorias": "|".join(selecionadas),
        "link": link,
    })
    salvar_csv("projetos.csv", ["nome", "descricao", "categorias", "link"], projetos)
    print("\nProjeto adicionado!")
    input("Enter para continuar...")


def menu_resetar_csvs():
    limpar()
    print("=== RESETAR CSVs ===\n")
    print("Isso vai sobrescrever todos os CSVs em data/")
    print("com os valores padrão do sistema.\n")
    resp = input("Confirmar reset? (s/N): ").strip().lower()
    if resp != "s":
        print("Cancelado.")
        input("Enter para continuar...")
        return
    arquivos = resetar_csvs()
    print("\nCSVs resetados:")
    for nome in arquivos:
        print(f"  - {nome}")
    input("\nEnter para continuar...")


def menu_principal():
    criados = garantir_csvs()
    if criados:
        print("Primeira execução: CSVs padrão criados em data/")
        for nome in criados:
            print(f"  - {nome}")
        input("\nEnter para continuar...")

    while True:
        limpar()
        print("=" * 45)
        print("  ADAPTADOR DE CURRÍCULO")
        print("=" * 45)
        print()
        print("  1. Gerar currículo")
        print("  2. Adicionar combinação (Cargo + Categoria)")
        print("  3. Adicionar curso")
        print("  4. Adicionar projeto")
        print("  5. Resetar CSVs (dados padrão)")
        print("  0. Sair")
        print()
        op = input("Escolha: ").strip()

        if op == "1":
            menu_gerar()
        elif op == "2":
            menu_adicionar_combinacao()
        elif op == "3":
            menu_adicionar_curso()
        elif op == "4":
            menu_adicionar_projeto()
        elif op == "5":
            menu_resetar_csvs()
        elif op == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")
            input("Enter...")
