# Sprints OnDance — Planejamento de Implementação

> Baseado no `docs/CHECKLIST.md`. Cada sprint tem duração de **2 semanas**.
> Conforme itens são implementados, atualizar o checklist.

---

## Sprint 1 (semanas 1-2) — Player + Formato das Aulas

> Sem player, a plataforma é só um catálogo. Este sprint entrega o CORE do produto.

- [x] Player de vídeo (play/pausa/avançar/voltar)
- [x] Continuar de onde parou (save/restore posição do vídeo)
- [x] Marcar aula como concluída
- [x] Formato das aulas: texto explicativo (campo no modelo Lesson)
- [x] Formato das aulas: materiais extras/PDF (campo no modelo Lesson)
- [x] Formato das aulas: exercícios/atividades (campo no modelo Lesson)
- [x] Página "Assistir aula" real (trocar placeholder)
- [x] Assistir aulas (trocar placeholder no perfil do aluno)
- [x] Fluxo de inscrição no catálogo (ExplorarPage → modal → AssistirPage)
- [x] MyCoursesPage com dados reais (lista de matrículas + progresso)

**Itens do checklist atendidos:** Seção 10, 11, 12

---

## Sprint 2 (semanas 3-4) — Progresso + Certificados + Recuperação de Senha

> Recompensa pelo engajamento. Recuperação de senha é UX crítico que ficou para trás.

- [x] Progresso do aluno — backend (UserCourse + LessonProgress)
- [x] Progresso do aluno — frontend (%) e aulas assistidas/total
- [x] Campo carga horária no modelo Course
- [x] API de certificados
- [ ] Geração automática de certificado ao concluir curso
- [ ] Download de certificado em PDF
- [ ] Compartilhar certificado
- [x] Perfil: exibir cursos iniciados
- [x] Perfil: exibir cursos concluídos
- [x] Perfil: exibir certificados
- [x] Área do aluno: cursos concluídos (trocar placeholder)
- [x] Área do aluno: certificados (trocar placeholder)
- [ ] Certificados no perfil do aluno (seção 7 do checklist)
- [ ] Recuperação de senha por email

**Itens do checklist atendidos:** Seção 6 (recuperação), 7 (perfil), 14, 15, 16, 17 (placeholders aluno)

---

## Sprint 3 (semanas 5-6) — Experiência do Aluno

> Melhorias standalone — filtros, home, dados reais nos placeholders.

- [x] Filtro por tipo de dança no catálogo
- [x] Filtro por nível no catálogo
- [x] Filtro por professor no catálogo
- [x] Filtro por duração no catálogo
- [x] Seção de professores na Home
- [x] Depoimentos de alunos na Home
- [ ] Recebe certificado ao concluir (check da visão do projeto)
- [x] Aprende no seu ritmo (check da visão — depende de progresso real)
- [ ] Emitir certificados (check do professor)

**Itens do checklist atendidos:** Seção 5 (home), 8 (filtros), 1 (visão)

---

## Sprint 4 (semanas 7-8) — Engajamento (Avaliação + Trilhas + Notificações)

> Mantém o aluno voltando e cria comunidade.

- [x] Modelo + API de avaliações (estrelas 1-5)
- [x] Avaliação por estrelas no frontend (1-5)
- [x] Modelo + API de comentários
- [x] Comentários escritos no frontend
- [x] Avaliações recebidas na área do professor
- [x] Trilha de conhecimento — modelo de prerequisitos no Course
- [x] Trilha de conhecimento — frontend (sequência Iniciante → Intermediário → Avançado)
- [x] Sugestão "Próximo curso recomendado"
- [x] Modelo + API de notificações
- [x] Bell de notificações com dados reais (trocar badge hardcoded)
- [x] Notificação: nova aula disponível
- [x] Notificação: novo curso lançado
- [x] Notificação: curso quase concluído
- [x] Email de notificação (nova aula, novo curso, quase concluído)
- [x] Pop-ups in-page ("Novo curso disponível!")
- [x] Pop-ups in-page ("Volte e continue seu curso")

**Itens do checklist atendidos:** Seção 13, 18 (avaliações), 19, 20, 21

---

## Sprint 5 (semanas 9-10) — Marketing (Leads + Campanhas + Analytics)

> Depende de ter usuários e dados reais fluindo.

- [x] Captação de leads (nome + email de visitantes não cadastrados)
- [x] Modelo + API de campanhas
- [x] Campanhas: email marketing
- [x] Campanhas: promoção de cursos
- [x] Campanhas: novos conteúdos
- [x] Admin: enviar campanhas (seção 3 do checklist)
- [x] Analytics real: número de usuários
- [x] Analytics real: cursos mais assistidos
- [x] Analytics real: tempo médio de aula
- [x] Analytics real: taxa de conclusão
- [x] Painel admin: estatísticas reais (trocar mock por dados da API)
- [x] Analisar dados (seção 3 do checklist — admin)
- [x] Administrar conteúdo (seção 3 do checklist — admin)
- [x] Admin: categorias (trocar placeholder)
- [x] Admin: analytics (trocar placeholder)
- [x] Admin: campanhas (trocar placeholder)
- [x] Admin: config (trocar placeholder)

**Itens do checklist atendidos:** Seção 22, 23, 24, 25 (estatísticas), 3 (admin)

---

## Sprint 6 (semanas 11-12) — Segurança + Polimento Final

> Fecha gaps e prepara para evolução.

- [ ] Proteção contra downloads ilegais de vídeos
- [x] Push notification (preparação infra para app futuro)
- [x] Professor: configurações (trocar placeholder)
- [x] Aluno: configurações (trocar placeholder)
- [x] Admin: configurações (trocar placeholder)
- [x] Professor: gestão de aulas (trocar placeholder)
- [x] Professor: ganhos/financeiro (trocar placeholder)
- [ ] Revisão geral de UX e responsividade
- [x] Revisão geral de acessibilidade
- [x] Testes end-to-end dos fluxos principais
- [x] Documentação final das APIs
- [ ] Preparação/marcações para fases futuras (marketplace, eventos, loja, festivais)

**Itens do checklist atendidos:** Seção 26 (segurança), 20 (push), 29 (futuras expansões)

---

## Resumo por Sprint

| Sprint | Foco | Semanas | Itens do Checklist |
|--------|------|---------|---------------------|
| 1 | Player + Formato das Aulas | 1-2 | 7 itens |
| 2 | Progresso + Certificados + Rec. Senha | 3-4 | 13 itens |
| 3 | Experiência do Aluno | 5-6 | 8 itens |
| 4 | Engajamento | 7-8 | 15 itens |
| 5 | Marketing | 9-10 | 17 itens |
| 6 | Segurança + Polimento | 11-12 | 12 itens |

**Total: 12 semanas (6 sprints) para cobrir todos os itens pendentes do checklist.**