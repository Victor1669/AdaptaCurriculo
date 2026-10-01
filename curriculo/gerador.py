from docx import Document

from .config import OUTPUT_DIR
from .dados import obter_tecnologias, separar_categorias
from .formatacao import configurar_documento
from .secoes import (
    add_cabecalho,
    add_conhecimentos,
    add_cursos,
    add_experiencia,
    add_formacao,
    add_objetivo,
    add_projetos,
    add_resumo,
)


def gerar_docx(cargo, categoria, nivel, objetivo, suporte, categorias_tech):
    OUTPUT_DIR.mkdir(exist_ok=True)

    techs = obter_tecnologias(categorias_tech)
    categorias_lista = separar_categorias(categorias_tech)

    doc = Document()
    configurar_documento(doc)

    add_cabecalho(doc)
    add_objetivo(doc, cargo, categoria, nivel, objetivo)
    add_conhecimentos(doc, techs, suporte)
    add_resumo(doc)
    add_formacao(doc)
    add_experiencia(doc)
    add_cursos(doc, categorias_lista, suporte)
    add_projetos(doc, categorias_lista)

    nome_arquivo = f"Curriculo_{cargo}_{categoria}_{nivel}.docx".replace(" ", "_")
    caminho = OUTPUT_DIR / nome_arquivo
    doc.save(caminho)
    return caminho
