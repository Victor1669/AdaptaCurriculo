import csv
import json

from .config import DATA_DIR

CSV_PADRAO = {
    "niveis.csv": {
        "campos": ["nivel"],
        "linhas": [
            {"nivel": "Júnior"},
            {"nivel": "Pleno"},
            {"nivel": "Sênior"},
            {"nivel": "Estágio"},
        ],
    },
    "combinacoes.csv": {
        "campos": ["cargo", "categoria", "objetivo", "suporte", "categorias_tech"],
        "linhas": [
            {
                "cargo": "Desenvolvedor",
                "categoria": "Frontend",
                "objetivo": "Busco oportunidade como Desenvolvedor Front-End para aplicar conhecimentos em React.js, TypeScript e interfaces modernas, contribuindo com código limpo, performance e boa experiência do usuário.",
                "suporte": "false",
                "categorias_tech": "WEB|INFRA",
            },
            {
                "cargo": "Desenvolvedor",
                "categoria": "Mobile",
                "objetivo": "Busco oportunidade como Desenvolvedor Mobile para aplicar conhecimentos em React Native e Flutter, desenvolvendo aplicativos performáticos e com boa experiência do usuário.",
                "suporte": "false",
                "categorias_tech": "MOBILE|BANCO|INFRA",
            },
            {
                "cargo": "Desenvolvedor",
                "categoria": "Full-Stack",
                "objetivo": "Busco oportunidade como Desenvolvedor Full-Stack para atuar no ciclo completo de desenvolvimento, do front-end ao back-end, com foco em qualidade de código e entrega de valor.",
                "suporte": "false",
                "categorias_tech": "WEB|JAVA|BANCO|INFRA",
            },
            {
                "cargo": "Desenvolvedor",
                "categoria": "Desktop",
                "objetivo": "Busco oportunidade como Desenvolvedor Desktop para aplicar conhecimentos em Java e C#, desenvolvendo sistemas robustos e de fácil manutenção.",
                "suporte": "false",
                "categorias_tech": "DESKTOP|BANCO|INFRA",
            },
            {
                "cargo": "Analista de Suporte",
                "categoria": "Suporte",
                "objetivo": "Busco oportunidade na área de Suporte e TI para aplicar conhecimentos em manutenção de computadores, Pacote Office e resolução de problemas técnicos.",
                "suporte": "true",
                "categorias_tech": "SUPORTE|INFRA",
            },
        ],
    },
    "cursos.csv": {
        "campos": ["titulo", "categorias", "data"],
        "linhas": [
            {
                "titulo": "Informática Completa 2.0 – CEBRAC Cursos | Word, Excel, PowerPoint, Windows",
                "categorias": "SUPORTE",
                "data": "Jun 2023 – Jun 2024",
            },
            {
                "titulo": "General English – Education First | Inglês Intermediário",
                "categorias": "TODOS",
                "data": "Fev 2024 – Nov 2024",
            },
            {
                "titulo": "The Ultimate React Course 2025: React, Next.js, Redux & More - Udemy | React.js, Tailwind, Next.js, Supabase, Git, GitHub",
                "categorias": "WEB",
                "data": "Dez 2024 – Jan 2025",
            },
            {
                "titulo": "Suporte Técnico (Voluntário) – ETEC de Embu | Manutenção de computadores",
                "categorias": "SUPORTE",
                "data": "Fev 2026 – Mar 2026",
            },
        ],
    },
    "projetos.csv": {
        "campos": ["nome", "descricao", "categorias", "link"],
        "linhas": [
            {
                "nome": "PiggyXp (projeto em grupo)",
                "descricao": "App mobile de educação financeira desenvolvido em equipe para o TCC. React Native + TypeScript no front-end; Node.js, Express e MySQL para dados dos usuários e MongoDB para dados de conteúdo teórico no back-end.",
                "categorias": "MOBILE|BANCO|WEB",
                "link": "github.com/Victor1669/PiggyXp-FrontEnd",
            },
            {
                "nome": "Livraria ETEC (projeto pessoal)",
                "descricao": "Sistema desktop de gerenciamento de biblioteca. Java/Swing no front-end, MySQL integrado via JDBC.",
                "categorias": "DESKTOP|BANCO|JAVA",
                "link": "github.com/Victor1669/livraria-etec-java",
            },
        ],
    },
}


def carregar_csv(nome):
    caminho = DATA_DIR / nome
    with open(caminho, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def carregar_json(nome):
    caminho = DATA_DIR / nome
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def carregar_config():
    return carregar_json("config.json")


def categorias_tech_config():
    cfg = carregar_config()
    if "categorias_tech" not in cfg:
        raise ValueError("Campo 'categorias_tech' não encontrado no config.json")
    return cfg["categorias_tech"]


def salvar_csv(nome, campos, linhas):
    DATA_DIR.mkdir(exist_ok=True)
    caminho = DATA_DIR / nome
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(linhas)


def sincronizar_categorias_tech():
    mapa = categorias_tech_config()
    linhas = [
        {"categoria": nome, "tecnologias": ",".join(techs)}
        for nome, techs in mapa.items()
    ]
    salvar_csv("categorias_tech.csv", ["categoria", "tecnologias"], linhas)


def garantir_csvs():
    """Cria CSVs padrão se ainda não existirem (primeira execução)."""
    DATA_DIR.mkdir(exist_ok=True)
    criados = []
    for nome, dados in CSV_PADRAO.items():
        if not (DATA_DIR / nome).exists():
            salvar_csv(nome, dados["campos"], dados["linhas"])
            criados.append(nome)
    existia = (DATA_DIR / "categorias_tech.csv").exists()
    sincronizar_categorias_tech()
    if not existia:
        criados.append("categorias_tech.csv")
    return criados


def resetar_csvs():
    """Recria todos os CSVs com os dados padrão."""
    DATA_DIR.mkdir(exist_ok=True)
    for nome, dados in CSV_PADRAO.items():
        salvar_csv(nome, dados["campos"], dados["linhas"])
    sincronizar_categorias_tech()
    return list(CSV_PADRAO.keys()) + ["categorias_tech.csv"]


def separar_categorias(texto):
    return [x.strip() for x in texto.split("|") if x.strip()]


def obter_tecnologias(categorias_tech_str):
    mapa = categorias_tech_config()
    categorias = separar_categorias(categorias_tech_str)
    indefinidas = [cat for cat in categorias if cat not in mapa]
    if indefinidas:
        raise ValueError(
            "Categorias de tecnologia não definidas no config.json: "
            + ", ".join(indefinidas)
        )

    techs = []
    for cat in categorias:
        for t in mapa[cat]:
            if t not in techs:
                techs.append(t)
    return techs


def formatar_techs(techs):
    return " • ".join(techs)


def filtrar_cursos(categorias_selecionadas, suporte):
    cursos = carregar_csv("cursos.csv")
    resultado = []
    cats_set = set(categorias_selecionadas)

    for c in cursos:
        cats_curso = separar_categorias(c["categorias"])
        if "TODOS" in cats_curso:
            resultado.append(c)
            continue
        if suporte and "SUPORTE" in cats_curso:
            resultado.append(c)
            continue
        if any(cat in cats_set for cat in cats_curso):
            resultado.append(c)
    return resultado


def filtrar_projetos(categorias_selecionadas):
    projetos = carregar_csv("projetos.csv")
    cats_set = set(categorias_selecionadas)
    resultado = []
    for p in projetos:
        cats_proj = separar_categorias(p["categorias"])
        if any(cat in cats_set for cat in cats_proj):
            resultado.append(p)
    return resultado
