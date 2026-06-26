# MVP OnDance — Escopo Mínimo Viável

> O loop mínimo que funciona de ponta a ponta:
> **Cadastro → Explorar cursos → Assistir aulas → Acompanhar progresso → Receber certificado**

**Duração: 4 semanas (2 sprints)**

---

## O que entra no MVP

### Sprint MVP-1 (semanas 1-2) — Player + Formato das Aulas

- [x] Player de vídeo (play/pausa/avançar/voltar)
- [x] Continuar de onde parou (save/restore posição do vídeo)
- [x] Marcar aula como concluída
- [x] Campo texto explicativo no modelo Lesson
- [x] Página "Assistir aula" real (trocar placeholder)
- [x] Assistir aulas (trocar placeholder no perfil do aluno)
- [x] Fluxo de inscrição no catálogo (ExplorarPage → modal → AssistirPage)
- [x] MyCoursesPage com dados reais (lista de matrículas + progresso)

### Sprint MVP-2 (semanas 3-4) — Progresso + Certificados + Recuperação de Senha

- [x] Progresso do aluno — backend (UserCourse + LessonProgress)
- [x] Progresso do aluno — frontend (%) e aulas assistidas/total
- [ ] Campo carga horária no modelo Course
- [ ] API de certificados
- [ ] Geração automática de certificado ao concluir curso
- [ ] Download de certificado em PDF
- [ ] Perfil: exibir cursos iniciados
- [ ] Perfil: exibir cursos concluídos
- [ ] Perfil: exibir certificados
- [ ] Área do aluno: cursos concluídos (trocar placeholder)
- [ ] Área do aluno: certificados (trocar placeholder)
- [ ] Recuperação de senha por email

---

## O que NÃO entra no MVP (pós-MVP)

| Funcionalidade | Sprint original | Razão para adiar |
|---|---|---|
| Filtros avançados no catálogo | 3 | Busca por texto já funciona |
| Seção de professores na Home | 3 | Nice-to-have |
| Depoimentos de alunos na Home | 3 | Nice-to-have |
| Materiais extras/PDF na aula | 1 | Vídeo já entrega valor |
| Exercícios/atividades na aula | 1 | Nice-to-have |
| Compartilhar certificado | 2 | Download PDF já resolve |
| Avaliação por estrelas + comentários | 4 | Engajamento |
| Trilha de conhecimento | 4 | Engajamento |
| Sugestão "Próximo curso recomendado" | 4 | Engajamento |
| Notificações (email, sistema, push) | 4 | Engajamento |
| Pop-ups in-page | 4 | Engajamento |
| Captação de leads | 5 | Crescimento |
| Campanhas | 5 | Crescimento |
| Analytics real | 5 | Crescimento |
| Painel admin: estatísticas reais | 5 | Operacional |
| Proteção contra downloads ilegais de vídeos | 6 | Segurança |
| Push notification | 6 | Futuro app |

---

## Critério de pronto do MVP

O MVP está pronto quando um aluno consegue:

1. Criar conta e fazer login
2. Recuperar a senha se esquecer
3. Navegar pelo catálogo de cursos
4. Inscrever-se em um curso
5. Assistir às aulas de vídeo
6. Sair e continuar de onde parou
7. Ver seu progresso (% e aulas concluídas)
8. Concluir o curso e receber o certificado em PDF
9. Ver seus cursos e certificados no perfil