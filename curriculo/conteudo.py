from .dados import carregar_config

_cfg = carregar_config()

NOME = _cfg["nome"]
CONTATO = _cfg["contato"]
RESUMO = _cfg["resumo"]
IDIOMAS = _cfg["idiomas"]
SUPORTE_TI = _cfg["suporte_ti"]
CATEGORIAS_TECH = _cfg["categorias_tech"]
FORMACAO = _cfg["formacao"]
EXPERIENCIAS = _cfg["experiencias"]
