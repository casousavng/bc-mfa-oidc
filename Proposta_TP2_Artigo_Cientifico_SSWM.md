# Proposta de Artigo Científico: TP2 — Investigação Aplicada em SSWM

**Unidade Curricular:** Segurança em Sistemas Web e Mobile  
**Curso:** Mestrado em Engenharia Informática — Especialização em Cibersegurança  
**Instituição:** ISPGAYA  
**Ponderação:** 50% da Nota Final  
**Data Limite de Entrega:** 15 de Janeiro de 2027  
**Formato Esperado:** Artigo Científico Formal (Template IEEE / Conferência)  

---

## 1. Tema Proposto

> **Título Provisório:** *Arquitetura de Autenticação Cognitiva Cega para Aplicações Web e Mobile em Terminais Não Confiáveis com Suporte OIDC*  
> *(Blind Cognitive Multi-Factor Authentication Architecture for Untrusted Web and Mobile Endpoints under OpenID Connect)*

---

## 2. Enquadramento e Continuidade Metodológica

Este trabalho materializa a transição direta entre o estudo crítico de incidentes de roubo de credenciais/sessão realizado no **TP1** e a fundamentação formal da **Tese de Mestrado**.

```
[TP1: O Problema Empírico]
Incidente de quebra de MFA / Infostealers / Interceção de credenciais em endpoints não confiáveis.
                                    │
                                    ▼
[TP2: A Solução & Artigo Científico]
Proposta de arquitetura de Autenticação Cognitiva Cega:
• Desacoplamento entre o ecrã do terminal e a computação mental do segredo.
• Integração formal com OpenID Connect / OAuth 2.0 através das claims 'amr' e 'acr' (RFC 8176).
• Avaliação preliminar de latência, usabilidade e vetores de ataque mitigados.
                                    │
                                    ▼
[TESE DE MESTRADO: A Validação Abrangente]
Dissertação completa com protótipo funcional, testes empíricos de utilizadores, análise de usabilidade (SUS score) e parcerias com laboratórios de investigação.
```

---

## 3. Estrutura Canónica do Artigo (IEEE Format)

1. **Abstract & Index Terms:** Resumo conciso do problema de exfiltração em endpoints não confiáveis, arquitetura proposta e resultados de avaliação.
2. **I. Introduction:** Contextualização do trabalho em ecossistemas Web e Mobile, fraquezas de abordagens atuais (FIDO2 exigindo hardware próprio, SMS-OTP vulnerável) e objetivos.
3. **II. Related Work & Threat Landscape:** Revisão da literatura científica (ScienceDirect, ACM Digital Library, IEEE) sobre MFA cognitivo, shoulder surfing e ataques AitM.
4. **III. System Architecture & Authentication Flow:**
   * Modelação do protocolo e troca de mensagens.
   * Geração criptográfica do desafio dinâmico no servidor de identidade (IdP).
   * Processamento cognitivo pelo utilizador humano.
   * Integração com normas OIDC / OAuth 2.0 (RFC 8176).
5. **IV. Security & Threat Analysis:** Análise formal contra vetores MITRE ATT&CK (Keyloggers, Screen Grabbers, SIM Swapping, Evilginx AitM).
6. **V. Usability & Overhead Considerations:** Discussão da carga cognitiva, taxa de erro (False Reject Rate) e compensações de usabilidade (UX).
7. **VI. Conclusion & Future Work:** Fecho do estudo e projeção dos testes laboratoriais para a dissertação de mestrado.
8. **References:** Corpus bibliográfico formal de alto impacto (Q1/Q2).

---

## 4. Cronograma de Execução do TP2

| Data Limite | Tarefa | Estado |
| :--- | :--- | :--- |
| **01/Dez/2026** | Validação do tema formal e estrutura do artigo com o docente | Planeado |
| **15/Dez/2026** | Consolidação do estado da arte e corpus bibliográfico IEEE/ACM | Planeado |
| **28/Dez/2026** | Modelação formal da arquitetura e fluxogramas OIDC/MFA | Planeado |
| **08/Jan/2027** | Redação completa do artigo em template LaTeX/IEEE | Planeado |
| **15/Jan/2027** | **Submissão final do Trabalho de Investigação (50%)** | Marco Crítico |
