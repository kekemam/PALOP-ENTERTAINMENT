# Auditoria de segurança — 23 de Agosto de 2026

Site institucional PALOP ENTERTAINMENT (estático, sem backend).
Âmbito: `index.html`, `vercel.json`, `img/`, `fonts/`.

## Resumo

Nenhuma vulnerabilidade explorável. Foram corrigidas duas questões de
privacidade/configuração e endurecida a resposta HTTP.

| # | Achado | Gravidade | Estado |
|---|---|---|---|
| 1 | Tipos de letra carregados do Google (IP dos visitantes exposto a terceiro) | Média (RGPD) | **Corrigido** |
| 2 | Sem cabeçalhos de segurança HTTP | Média | **Corrigido** |
| 3 | Comentário no código nomeava infraestrutura possível | Baixa | **Corrigido** |
| 4 | Email em texto simples (recolha por robôs de spam) | Informativo | Aceite |
| 5 | Formulário sem proteção anti-spam | Informativo | Não aplicável hoje |

## Testes de injeção — todos falharam (bom)

Executados no browser contra o site a correr:

- **`localStorage` envenenado.** `palop-lang` é a única coisa que o site
  guarda. Injetei `<img src=x onerror=…>` como valor e recarreguei: o código
  não encontra o idioma, recai em `pt` e nada executa.
- **Injeção pelos campos do formulário.** Submeti nome, assunto e mensagem com
  `"><script>alert(1)</script>`, `javascript:` e sequências `%0d%0a` (tentativa
  de injeção de cabeçalhos). O URL gerado mantém o prefixo fixo
  `https://wa.me/41787307866?text=` e todo o conteúdo passa por
  `encodeURIComponent` — nenhum caractere cru perigoso chega ao URL.
- **Reflexão no DOM.** O payload nunca aparece no DOM como HTML.

## Superfície de ataque

- **`innerHTML` em 3 sítios** (i18n, faixa rolante, corpo das fichas). Todos
  alimentados exclusivamente pelo objeto `T` escrito à mão no ficheiro. Nenhum
  dado do visitante, do URL ou do `localStorage` lá chega.
- **Sem backend, sem base de dados, sem sessões, sem autenticação.** Não há
  credenciais no repositório — confirmado por varredura.
- **Sem scripts de terceiros, sem iframes, sem service workers.**
- **Sem cookies.** O único armazenamento é `localStorage['palop-lang']`, que
  guarda `pt`, `en` ou `fr`. É estritamente funcional, não identifica ninguém e
  não exige aviso de consentimento.
- **Links externos** (Facebook, Instagram, WhatsApp) têm todos
  `rel="noopener"` — a página de destino não consegue manipular a de origem.
- **Imagens sem metadados EXIF** — verificado ficheiro a ficheiro. Não há
  coordenadas GPS nem identificação de equipamento.

## O que foi corrigido

### 1. Tipos de letra alojados no próprio site

Antes: 4 pedidos a `fonts.googleapis.com` e `fonts.gstatic.com` em cada visita,
o que entrega o IP de cada visitante à Google sem consentimento. Um tribunal
alemão (LG München, 2022) considerou esta prática uma violação do RGPD, e a
empresa é portuguesa com público europeu.

Agora: os 8 ficheiros `.woff2` (subconjuntos `latin` e `latin-ext`) estão em
`fonts/`. **Zero pedidos externos** — confirmado no browser. Cada visitante
carrega apenas os subconjuntos de que precisa (~95 KB em português).

Efeito colateral positivo: a Política de Privacidade afirma que o site não usa
serviços de terceiros. Antes disto, era discutível. Agora é literalmente verdade.

### 2. Cabeçalhos de segurança (`vercel.json`)

| Cabeçalho | Para quê |
|---|---|
| `Content-Security-Policy` | Bloqueia scripts, estilos e imagens de origens externas |
| `X-Frame-Options: DENY` + `frame-ancestors 'none'` | Impede que o site seja embebido noutro (clickjacking) |
| `X-Content-Type-Options: nosniff` | Impede o browser de adivinhar tipos de ficheiro |
| `Referrer-Policy` | Não revela o URL completo a sites externos |
| `Permissions-Policy` | Desliga câmara, microfone, localização e pagamentos |
| `Strict-Transport-Security` | Força HTTPS |

Nota honesta sobre a CSP: o CSS e o JavaScript estão embutidos no HTML, o que
obriga a `'unsafe-inline'`. Isso é menos rígido do que o ideal, mas continua a
bloquear o vetor principal — carregar código de um domínio externo. Uma CSP por
hash exigiria recalcular o hash a cada edição, o que num ficheiro único é uma
armadilha de manutenção.

### 3. Comentário no código

O comentário do `FORM_ENDPOINT` dava exemplos de serviços de backend. Foi
generalizado — não vale a pena anunciar a stack no código publicado.

## Aceite sem correção

- **Email visível.** `info@palopentertainment.com` aparece em texto simples e
  será recolhido por robôs de spam. Ofuscar prejudicaria quem quer copiar o
  endereço; o filtro de spam do servidor de email é o sítio certo para tratar
  disto.
- **Formulário sem CAPTCHA nem limite de envios.** Hoje não há endpoint: o
  botão abre o WhatsApp do próprio visitante, por isso não há nada para abusar.
  **Se ligar o `FORM_ENDPOINT` a um servidor, acrescente proteção anti-spam**
  (campo armadilha, limite por IP, ou o mecanismo do serviço escolhido).

## A rever antes de pôr no ar

- **Política de Privacidade e Termos** são um rascunho mínimo e honesto. Devem
  ser revistos por quem trata do RGPD da empresa.
- **Repositório público.** O código e as imagens ficam visíveis a qualquer
  pessoa — o mesmo que já acontece no site. Não há segredos, mas há fotografias
  de pessoas identificáveis, com o mesmo grau de exposição do site publicado.
