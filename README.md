# Projeto adapta currículo

Este projeto possui o propósito de configurar e adaptar facilmente seu currículo sem precisar gastar tokens de suas IAs, nem de mudar o estilo visual deles

## Público alvo

Profissionais da área de TI que estão cansados de ATS e que buscam facilitar a personalização do currículo

## Inicialização

Abra o terminal e execute nessa ordem:

### Dar permissão de execução
`chmod +x ./curriculo.sh`

### Ativa o ambiente python
`source venv/bin/activate`

### Executa o programa
`./curriculo.sh`

## Formatação

A formatação é configurada em `curriculo/config.py`, você aplica suas preferências para personalizar o currículo

## Currículos gerados

Eles são gerados na pasta `saidas/`

## Dados

Os CSVs são gerados automaticamente, você poderá adicionar combinações para o tipo necessário.

Caso algum deles for apagado, outro CSV será criado para manter o sistema funcional

## Configurações

As configurações em data/config.json possuem esta estrutura:

```

{
  "nome": "NOME",
  "contato": "LINHA COM SEUS CONTATOS",
  "resumo": "COLOQUE SEU RESUMO", // Coloque seus idiomas
  "idiomas": ["Inglês avançado", "Espanhol básico"],
  "suporte_ti": "Manutenção de computadores • Pacote Office", // Coloque se quiser
  "categorias_tech": { // Ex:
    "WEB": ["HTML", "CSS", "JavaScript", "TypeScript", "Node.js", "React.js", "Next.js"],
    },
  "formacao": [
    { // Ex:
      "titulo": "Escola Teste — Ensino Médio",
      "periodo": "Fev 2021 – Nov 2024 — Concluído"
    },
  ],
  "experiencias": [
    {
      "titulo": "Desenvolvedor – Empresa",
      "periodo": "Jun 2026 – Ago 2026 – Remoto",
      "bullets": [
        "Responsável Desenvolver",
        "Entrega completa do sistema, do início ao fim do contrato, trabalhando de forma independente.",
      ]
    },
  ]
}


```

## Cursos e Projetos

Poderão ser criados utilizando a CLI