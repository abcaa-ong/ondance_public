# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Sobre o projeto

**OnDance** é uma plataforma digital da ABCAA (Associação Beneficente e Cultural Amor em Ação) para gerenciar avaliações de coreografias em festivais de dança: registro de notas de jurados em tempo real, cálculo automático de médias, organização de rankings e disponibilização de resultados.

## Comandos

> O stack ainda não foi definido. Quando for configurado, adicione aqui os comandos reais de build, lint e testes. Por enquanto, os comandos esperados são:

```bash
npm install      # Instalar dependências
npm run dev      # Rodar localmente
```

## Arquitetura

O projeto está em fase inicial (greenfield) — apenas documentação foi commitada. A estrutura de pastas planejada é:

```
ondance/
├── public/     # Arquivos estáticos
├── src/        # Código-fonte
└── docs/       # Documentação técnica
```

## Fluxo de contribuição

**Branches** seguem o padrão `tipo/descricao-curta`:
- `feat/` — nova funcionalidade
- `fix/` — correção de bug
- `docs/` — documentação
- `refactor/` — refatoração
- `test/` — testes

**Commits** no formato `tipo: descrição curta no imperativo` (ex: `feat: adiciona formulário de cadastro`).

**PRs** são abertos para `main` e precisam de aprovação do líder do squad. Referencie sempre a Issue com `Closes #NNN`.
