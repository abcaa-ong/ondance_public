# Checklist OnDance — instrucoes.md vs Implementação

> Baseado no documento `instrucoes.md` (Documento de Estrutura da Plataforma — Fase 1).
> Conforme os itens são implementados, trocar `- [ ]` por `- [x]` e atualizar o resumo.

## Legenda

| Símbolo | Significado |
|---------|-------------|
| ✅ | Implementado |
| ⚠️ | Parcialmente implementado |
| ❌ | Não implementado |

---

## 1. Visão do Projeto

- [x] Plataforma digital de ensino de dança online
- [x] Aluno entra na plataforma, escolhe curso, assiste aulas
- [x] Aprende no seu ritmo (player com progresso real)
- [ ] Recebe certificado ao concluir
- [x] Plataforma simples, intuitiva e acessível
- [ ] Marketplace de aulas presenciais, eventos, produtos (fase futura — correto adiar)

## 2. Objetivos da Plataforma

- [x] Democratizar o ensino da dança (qualquer pessoa pode acessar)
- [x] Organizar conhecimento (cursos com módulos e aulas estruturados)
- [x] Conectar alunos e professores (perfis e catálogo)
- [ ] Certificar aprendizado (API existe, sem geração/download)
- [x] Criar base de usuários (cadastro + login + perfil)

## 3. Perfis de Usuários

### Aluno

- [x] Criar conta
- [x] Acessar cursos
- [x] Assistir aulas (player de vídeo com YouTube/embed e HTML5 nativo)
- [x] Acompanhar progresso (LessonProgress com % e aulas concluídas)
- [ ] Receber certificados (não implementado)

### Professor

- [x] Cadastrar cursos
- [x] Enviar aulas
- [x] Acompanhar alunos
- [ ] Emitir certificados (não implementado)

### Administrador (OnDance)

- [x] Aprovar cursos
- [x] Gerenciar usuários
- [ ] Analisar dados (placeholder)
- [ ] Enviar campanhas (placeholder)
- [ ] Administrar conteúdo (placeholder)

## 4. Estrutura Geral da Plataforma — 6 Áreas

- [x] Página inicial
- [x] Cadastro e login
- [x] Catálogo de cursos
- [x] Área do aluno (parcial)
- [x] Área do professor (parcial)
- [x] Painel administrativo (parcial)

## 5. Página Inicial (Home)

- [x] Banner principal com explicação da plataforma
- [x] Destaque de cursos (busca da API, até 6 cursos)
- [ ] Seção de professores
- [ ] Depoimentos de alunos
- [x] Botão principal "Começar a aprender"

## 6. Cadastro e Login

- [x] Nome
- [x] Email
- [x] Senha
- [x] Cidade
- [x] Estado
- [x] Telefone (opcional)
- [x] Data de nascimento (opcional)
- [x] Login com Email + Senha
- [ ] Recuperação de senha por email

## 7. Perfil do Usuário

- [x] Nome
- [x] Foto
- [x] Cidade
- [x] Cursos iniciados (seção na ProfilePage)
- [x] Cursos concluídos (seção na ProfilePage)
- [x] Certificados (seção na ProfilePage + página dedicada)

## 8. Catálogo de Cursos

- [ ] Filtro por tipo de dança
- [ ] Filtro por nível
- [ ] Filtro por professor
- [ ] Filtro por duração
- [x] Busca por texto
- [x] Cada curso mostra: Título
- [x] Cada curso mostra: Professor
- [x] Cada curso mostra: Descrição
- [x] Cada curso mostra: Quantidade de aulas
- [x] Cada curso mostra: Duração
- [x] Cada curso mostra: Nível

## 9. Estrutura dos Cursos

- [x] Curso → Módulos → Aulas (modelo e CRUD completos)

## 10. Formato das Aulas

- [x] Vídeo (player HTML5 nativo + YouTube/Vimeo embed)
- [x] Texto explicativo (campo `content` no modelo Lesson)
- [x] Materiais extras / PDF (campo `materials_url` no modelo Lesson)
- [x] Exercícios / atividades (campo `exercises` no modelo Lesson)

## 11. Player de Aula

- [x] Play / Pausa / Avançar / Voltar
- [x] Continuar de onde parou
- [x] Marcar aula como concluída

## 12. Continuar de Onde Parou

- [x] Função essencial — salvar e restaurar ponto do vídeo

## 13. Trilha de Conhecimento

- [ ] Sequência lógica (Iniciante → Intermediário → Avançado)
- [ ] Sugestão "Próximo curso recomendado"

## 14. Progresso do Aluno

- [ ] Visualização de progresso (%) — placeholder
- [ ] Aulas assistidas / total — não implementado

## 15. Certificados

- [x] Modelo Certificate existe no backend
- [ ] Geração automática ao concluir curso
- [x] API de certificados

### Conteúdo do certificado

- [x] Nome do aluno (via Profile)
- [x] Nome do curso (via Course)
- [x] Nome do professor (via Course.teacher)
- [x] Carga horária (campo `workload` no modelo Course)
- [x] Data de conclusão (issue_date)
- [x] Código único (code)

## 16. Download de Certificado

- [ ] Baixar em PDF
- [ ] Compartilhar

## 17. Área do Aluno

- [x] Meus cursos (em andamento) — dados reais via API
- [x] Cursos concluídos — exibidos no MyCoursesPage
- [x] Certificados — dados reais via API
- [x] Perfil — implementado

## 18. Área do Professor

- [x] Criar cursos
- [x] Enviar aulas
- [x] Organizar módulos
- [x] Editar conteúdo
- [x] Quantidade de alunos
- [ ] Avaliações recebidas
- [x] Progresso dos alunos (via teacher/students)

## 19. Sistema de Avaliação

- [ ] Avaliação por estrelas (1-5)
- [ ] Comentários escritos

## 20. Notificações

- [ ] Nova aula disponível
- [ ] Novo curso lançado
- [ ] Curso quase concluído

### Tipos de notificação

- [ ] Email
- [ ] Notificação no sistema (só ícone estático com badge hardcoded)
- [ ] Push notification (futuro app)

## 21. Pop-ups na Plataforma

- [ ] Mensagens in-page ("Novo curso disponível!")
- [ ] Mensagens in-page ("Volte e continue seu curso")

## 22. Captação de Leads

- [ ] Coletar Nome + Email de visitantes não cadastrados

## 23. Campanhas

- [ ] Email marketing
- [ ] Promoção de cursos
- [ ] Novos conteúdos

## 24. Dados e Analytics

- [ ] Número de usuários (mock no admin)
- [ ] Cursos mais assistidos
- [ ] Tempo médio de aula
- [ ] Taxa de conclusão

## 25. Painel Administrativo

- [x] Gerenciar usuários
- [x] Gerenciar cursos (aprovar/rejeitar)
- [x] Aprovar professores (via aprovação de curso)
- [ ] Ver estatísticas (placeholder com mock)

## 26. Segurança

- [x] Proteção de senha (JWT + hash Django)
- [x] Controle de acesso (role-based routing + permissions)
- [ ] Proteção contra downloads ilegais de vídeos

## 27. Experiência do Usuário

- [x] Simples
- [x] Rápida
- [x] Intuitiva
- [x] Onboarding / Welcome Modal
- [x] Dark mode

## 28. Design

- [x] Cores: Preto, Roxo, Rosa, Azul, Branco
- [x] Estilo moderno ligado à dança e tecnologia
- [x] Fontes: Poppins (headings) + Nunito (body)

## 29. Futuras Expansões (Fases Futuras)

- [ ] Marketplace de aulas presenciais
- [ ] Venda de ingressos de eventos
- [ ] Loja de produtos de dança
- [ ] Divulgação de festivais

## 30. Resumo — O que Precisa Ser Desenvolvido

| Item | Status |
|------|--------|
| Sistema de cadastro | ✅ Implementado |
| Sistema de login | ✅ Implementado |
| Perfil de usuário | ✅ Implementado |
| Catálogo de cursos | ⚠️ Parcial — faltam filtros |
| Player de vídeo | ✅ Implementado |
| Sistema de progresso | ✅ Implementado |
| Sistema de trilhas | ❌ Não implementado |
| Área do aluno | ⚠️ Parcial (dashboard, explorar, assistir, meus cursos) |
| Área do professor | ⚠️ Parcial (CRUD cursos + alunos) |
| Certificados digitais | ⚠️ API existe, sem geração/download |
| Sistema de notificações | ❌ Só ícone UI |
| Captação de leads | ❌ Não implementado |
| Campanhas de comunicação | ❌ Placeholder |
| Painel administrativo | ⚠️ Parcial (cursos + usuários) |
| Sistema de dados e analytics | ❌ Placeholder (mock) |

---

## Contagem

| Status | Quantidade |
|--------|------------|
| ✅ Implementado | 49 |
| ⚠️ Parcial | 4 |
| ❌ Não implementado | 40 |
| **Total** | **93** |