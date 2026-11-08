# 99freelas (Brasil, português)

## Coleta
Automática: `coletar.py` lê a listagem pública (`/projects`, liberada no robots.txt; termos sem cláusula sobre robôs). A listagem não mostra o orçamento.

Config (`plataformas.99freelas`):
- `subcategorias`: `categoria/subcategoria`, copiadas da URL do site depois de filtrar;
- `paginas`;
- `premium`: false = conta gratuita.

## Regras
- Proibido informar contato (e-mail, telefone, WhatsApp) ou link externo no perfil e nas propostas.
- Conta gratuita: nas primeiras **24 h** depois da publicação, só premium propõe. Status do projeto: `abre AAAA-MM-DD HH:MM` (publicação + 24 h).
- Cada proposta gasta **1 conexão**.

## Formulário da proposta
- **Sua oferta:** valor líquido para você, em R$.
- **Oferta final:** o que o cliente vê = oferta × 1,25 (taxa de 25%; conferir no formulário).
- **Duração estimada:** em dias.
- **Detalhes:** até **3000 caracteres**, em português.
