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
- [x] Analisar dados
- [x] Enviar campanhas
- [x] Administrar conteúdo

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

- [x] Filtro por tipo de dança
- [x] Filtro por nível
- [x] Filtro por professor
- [x] Filtro por duração
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

- [x] Sequência lógica (Iniciante → Intermediário → Avançado)
- [x] Sugestão "Próximo curso recomendado"

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
- [x] Avaliações recebidas
- [x] Progresso dos alunos (via teacher/students)

## 19. Sistema de Avaliação

- [x] Avaliação por estrelas (1-5)
- [x] Comentários escritos

## 20. Notificações

- [x] Nova aula disponível
- [x] Novo curso lançado
- [x] Curso quase concluído

### Tipos de notificação

- [x] Email
- [x] Notificação no sistema
- [x] Push notification (infraestrutura preparada)

## 21. Pop-ups na Plataforma

- [x] Mensagens in-page ("Novo curso disponível!")
- [x] Mensagens in-page ("Volte e continue seu curso")

## 22. Captação de Leads

- [x] Coletar Nome + Email de visitantes não cadastrados

## 23. Campanhas

- [x] Email marketing
- [x] Promoção de cursos
- [x] Novos conteúdos

## 24. Dados e Analytics

- [x] Número de usuários
- [x] Cursos mais assistidos
- [x] Tempo médio de aula
- [x] Taxa de conclusão

## 25. Painel Administrativo

- [x] Gerenciar usuários
- [x] Gerenciar cursos (aprovar/rejeitar)
- [x] Aprovar professores (via aprovação de curso)
- [x] Ver estatísticas

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
| Catálogo de cursos | ✅ Implementado |
| Player de vídeo | ✅ Implementado |
| Sistema de progresso | ✅ Implementado |
| Sistema de trilhas | ✅ Implementado |
| Área do aluno | ✅ Implementado |
| Área do professor | ✅ Implementado |
| Certificados digitais | ⚠️ API existe, sem geração/download |
| Sistema de notificações | ✅ Implementado |
| Captação de leads | ✅ Implementado |
| Campanhas de comunicação | ✅ Implementado |
| Painel administrativo | ✅ Implementado |
| Sistema de dados e analytics | ✅ Implementado |

---

## Contagem

| Status | Quantidade |
|--------|------------|
| ✅ Implementado | 116 |
| ⚠️ Parcial | 0 |
| ❌ Não implementado | 18 |
| **Total** | **134** |