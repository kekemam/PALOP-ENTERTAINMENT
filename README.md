# PALOP ENTERTAINMENT — website institucional

Site estático de ficheiro único (`index.html`): CSS, HTML e JS vanilla, sem build,
sem dependências. Basta abrir o ficheiro ou publicar a pasta.

## Estrutura

```
palop/
├── index.html     ← o site completo (~114 KB)
├── 404.html       ← página de erro, com o mesmo aspecto do site
├── robots.txt · sitemap.xml · site.webmanifest
├── apple-touch-icon.png
├── vercel.json    ← cabeçalhos de segurança e cache
├── img/           ← imagens em WebP (~1,4 MB carregados pela página)
├── ferramentas/   ← foto.py, prepara uma imagem para o site
└── README.md
```

## 1. Imagens

Todas as imagens do site estão em **WebP** (~1,4 MB no total, contra 2,4 MB
em JPEG). Os ficheiros `.jpg`/`.png` originais ficaram em `img/` como rede de
segurança — nada no site lhes toca. Para os apagar:

```bash
cd img && find . -maxdepth 1 \( -name '*.png' -o \( -name '*.jpg' -not -name 'og.jpg' \) \) -delete
```

A `og.jpg` é a única excepção e tem de se manter em JPEG: nem todos os
leitores de Open Graph das redes sociais interpretam WebP.

As imagens do folheto e do roll-up já estão recortadas, otimizadas e ligadas ao
site (pasta `img/`):

| Ficheiro | Onde aparece | Origem |
|---|---|---|
| `rosto.webp` | painel do ecrã de abertura | arte de capa do folheto |
| `direcao.webp` | «Quem Somos» | fotografia de dois convidados junto ao roll-up |
| `verdades.webp` | cartão Irmãos Verdades | photocall com o cartaz do lançamento |
| `cartaz-te-amo.webp` | secção «Destaque musical» | cartaz do lançamento, recortado do photocall |
| `multidao.webp` | cartão PALOP Festival | fotografia de multidão do folheto |
| `turismo.webp` | cartão Turismo | campanha «Seu portal para o melhor do turismo PALOP» |
| `jobs.webp` | cartão PALOP Jobs | campanha «Oportunidades de Carreira» |
| `agencia.webp` | cartão Agência de Artistas | campanha «PALOP Agência de Artistas» |
| `miss-palop.webp` | cartão Miss PALOP | grande final e coroação |
| `palop-tv.webp` | cartão PALOP TV | ecrã do canal (zona dos arcos) |
| `equipa.webp` | fundo da secção final (CTA) | equipa no photocall |
| `carlos-uissa.webp` | secção do CEO | retrato no photocall |
| `folheto-1.webp`, `folheto-2.webp` | secção «Folheto institucional» + lightbox | páginas do folheto |
| `logo-palop.webp` | header e footer | logótipo, com fundo tornado transparente |
| `og.jpg` | partilhas em redes sociais | recorte da arte de capa |
| `evento.webp` | *(não usado)* — alternativa para «Quem Somos» | roll-up sozinho num evento |

Todos os slots estão preenchidos.

### Trocar uma fotografia

Há uma ferramenta que corta, redimensiona e converte para WebP com o nome
certo — não é preciso saber que tamanho leva cada sítio:

```bash
python3 ferramentas/foto.py ~/Desktop/nova-foto.jpg ceo --foco cima
```

`python3 ferramentas/foto.py --lista` mostra os sítios disponíveis (`hero`,
`sobre`, `ceo`, `verdades`, `cartaz`, `festival`, `miss`, `tv`, `agencia`,
`turismo`, `jobs`, `equipa`, `og`). O `--foco` decide o que fica de fora
quando a foto é mais alta do que o sítio: `cima` guarda a cabeça, `baixo`
guarda os pés, `centro` é o que acontece por omissão.

Depois é publicar:

```bash
git add img && git commit -m "Nova foto: ceo" && git push
```

A Vercel republica em cerca de 30 segundos.

**O recorte é automático, não é inteligente.** A ferramenta corta pelo
centro — se o motivo estiver a um canto, ou se quiser um retrato apertado
a partir de uma foto de corpo inteiro, corte primeiro no telemóvel e só
depois passe pela ferramenta. Ela avisa quando o original é mais pequeno
do que o necessário e a foto vai sair menos nítida.

**Não substitua ficheiros à mão em `img/`.** Um JPEG com o nome `.webp`
não aparece no site: o servidor anuncia-o como WebP e o browser recusa-o,
por causa dos cabeçalhos de segurança. A ferramenta trata da conversão.

## 2. Abertura com o logótipo

Ao entrar no site aparece o logótipo sobre fundo preto durante **1,75
segundos**, com três ondas a irradiar, e depois desvanece. É feito com o
logótipo que já existe — não há vídeo nem peso acrescentado.

Só aparece quando faz sentido:

- **uma vez por sessão** (guardado em `sessionStorage`); quem navega pelo
  site ou volta atrás não a vê outra vez;
- **nunca** para quem tem «reduzir movimento» ligado no sistema;
- **nunca** quando o endereço já aponta para uma secção (`…#projetos`),
  porque essa pessoa sabe onde quer ir.

Sai a qualquer momento com o botão «Saltar», um clique, uma tecla, a roda
do rato ou um toque no ecrã. Se o JavaScript falhar, fica escondida e o
site abre normalmente.

Para mudar a duração, procure `setTimeout(fim,1750)` no `index.html`.
Para a desligar de vez, apague o bloco `<div id="intro">` e o `<script>`
que vem logo a seguir.

## 2. Agenda e notícias

A secção «Agenda» é alimentada por uma lista no `<script>` do `index.html`.
Procure `const AGENDA=[`.

```js
{ data:   '2027-03-14',              // AAAA-MM-DD, obrigatório
  tipo:   'evento',                  // 'evento' | 'noticia'
  titulo: 'Nome do evento',          // texto, ou {pt:'…',en:'…',fr:'…'}
  texto:  'Descrição curta.',        // idem, opcional
  local:  'Lisboa ao Vivo, Lisboa',  // opcional
  link:   'https://…',               // opcional
  cartaz: 'cartaz-do-evento.webp' }  // opcional, ficheiro em img/
```

O `cartaz` mostra uma miniatura ao lado do texto que abre em tamanho real
ao ser clicada. Para preparar a imagem a partir do cartaz original:

```bash
python3 -c "
from PIL import Image
im=Image.open('/caminho/do/cartaz.jpg').convert('RGB')
im.thumbnail((900,2700), Image.LANCZOS)
im.save('img/cartaz-do-evento.webp','WEBP',quality=80,method=6)"
```

- **A secção aparece e desaparece sozinha.** Com a lista vazia, tanto a
  secção como o link no menu ficam escondidos — o site nunca mostra um
  espaço em branco nem uma agenda vazia.
- O que estiver no futuro aparece primeiro, marcado **«Próximo»**, por
  ordem de proximidade. O resto fica abaixo, marcado «Realizado» ou
  «Notícia», do mais recente para o mais antigo.
- As datas são formatadas na língua activa (24 de junho / 24 June /
  24 juin) sem trabalho adicional.
- Nos campos de texto pode pôr uma string simples, que serve para as três
  línguas, ou um objeto `{pt,en,fr}` se quiser traduzir.

Neste momento tem **três entradas**: dois espectáculos de Setembro de 2026
(Chito Kaharam em Faro e o Show de Independência da Guiné-Bissau em
Quarteira) e o lançamento dos Irmãos Verdades de 2022, no arquivo. Todos
saíram de cartazes fornecidos — nada foi inventado.

## 2. Formulário de contacto

O botão **«Enviar pelo WhatsApp»** valida os campos e abre o WhatsApp
(`wa.me/41787307866`) com a mensagem já composta:

```
*Assunto*

Nome: …
Email: …
Telefone: …
Empresa/Organização: …

<mensagem>

_Enviado pelo site palopentertainment.com_
```

Funciona em telemóvel (app) e em desktop (WhatsApp Web ou app). **Falta sempre
o último passo: a pessoa tem de carregar em enviar dentro do WhatsApp.** O
texto de confirmação diz isso explicitamente, para o site não afirmar que
enviou quando pode não ter enviado.

O número está na constante `WA_NUMBER` no `<script>`.

### Passar para envio por servidor

Preencha `FORM_ENDPOINT` com um URL que aceite POST em JSON (Formspree,
Supabase, API própria) e o WhatsApp deixa de ser usado:

```js
const FORM_ENDPOINT='https://...';
```

O corpo enviado é `{nome, email, telefone, organizacao, assunto, mensagem,
idioma}`. Em caso de sucesso o formulário é limpo; em caso de falha mostra o
erro **e preserva o que a pessoa escreveu**. Se fizer esta mudança, altere
também o rótulo do botão (chave `f7` nas três línguas), que hoje diz
«Enviar pelo WhatsApp».

> **Atenção à CSP.** O `vercel.json` tem `connect-src 'self'`, o que bloqueia
> pedidos para domínios externos. Se o `FORM_ENDPOINT` apontar para fora do
> site (Formspree, por exemplo), acrescente esse domínio ao `connect-src`,
> senão o envio falha silenciosamente no browser.



## 3. Idiomas

Português (pt-PT) é o idioma principal. Inglês e Francês estão completos e
disponíveis no seletor PT/EN/FR do cabeçalho — a escolha fica guardada no
`localStorage` e, na primeira visita, segue o idioma do navegador.

São **187 chaves** por idioma, sem lacunas. Além do texto visível, mudam com o
idioma: o `<title>`, a `meta description`, o `lang` do `<html>`, os
`aria-label` (navegação, menu, botões de fechar), os `alt` das imagens do
folheto, os nomes dos países na secção Portugal × PALOP e as palavras da faixa
rolante.

Três formas de marcar conteúdo traduzível:

| Atributo | O que traduz |
|---|---|
| `data-i="chave"` | o texto do elemento (aceita HTML no valor) |
| `data-ia="chave"` | o `aria-label` |
| `data-ialt="chave"` | o `alt` |

Para acrescentar strings novas: marque o elemento e acrescente a chave aos três
objetos `T.pt`, `T.en` e `T.fr`. **Atenção:** se o elemento tiver filhos (um
ícone, por exemplo), o filho tem de ficar *fora* do elemento com `data-i` — o
i18n substitui o conteúdo todo.

Não são traduzidos, de propósito: nomes próprios e de marca (PALOP Festival,
Miss PALOP, PALOP TV, PALOP Jobs, Carlos Uissa, Irmãos Verdades, «Te Amo»), a
morada postal (tem de se manter em português para o correio e o GPS), números,
datas e contactos.

## 4. Publicar

Já está no ar: **https://palop-entertainment.vercel.app**

O projeto Vercel `palop-entertainment` está ligado ao repositório
`kekemam/PALOP-ENTERTAINMENT`. **Cada push para `main` faz deploy automático**
— não há passo de build.

Os commits têm de ter como autor `mampassarofficial@gmail.com`, senão a Vercel
ignora-os.

Para publicar a partir desta pasta sem passar pelo GitHub:

```bash
npx vercel --prod
```

### Domínio palopentertainment.com

Já está registado no projeto Vercel e a propriedade está verificada. O que
falta é **um passo no GoDaddy**, que é quem gere o DNS
(`ns63/ns64.domaincontrol.com`).

Hoje o domínio ainda aponta para o Wix, que devolve erro — não há site nenhum a
funcionar lá, por isso a mudança não deita nada abaixo.

Alterar apenas estes dois registos:

| Tipo | Nome | Valor actual (Wix) | Valor novo |
|---|---|---|---|
| A | `@` | `185.230.63.107` | `76.76.21.21` |
| CNAME | `www` | `pointing.wixdns.net` | `cname.vercel-dns.com` |

**Não tocar em mais nada.** O email da empresa está no Microsoft 365 e depende
de registos que vivem no mesmo painel:

- `MX` → `palopentertainment-com.mail.protection.outlook.com`
- `TXT` → `v=spf1 include:secureserver.net -all` e o de verificação da Microsoft
- `CNAME autodiscover` → `autodiscover.outlook.com`

Apagar ou trocar qualquer um destes deixa a empresa sem email.

A raiz redireciona para `www` (308), porque é o endereço impresso no folheto e
o que está no `canonical` do site. O certificado HTTPS é emitido pela Vercel
automaticamente, poucos minutos depois de o DNS propagar.

## Por confirmar

- **Redes confirmadas:** Facebook `facebook.com/palop.entertainment`,
  Instagram `@palop.entertainment` e `@palopjobs` (recrutamento). O
  `@palopjobs` aparece nos contactos, no rodapé e dentro da ficha do projeto
  PALOP Jobs. As três estão no `sameAs` do JSON-LD.
- **LinkedIn, X/Twitter e YouTube foram removidos** do site por não terem
  URL confirmado. Para os repor, acrescente um `<a>` a cada bloco
  `.socials` (contactos e rodapé) com o mesmo formato dos existentes.
- Textos de «Política de Privacidade» e «Termos e Condições» — são um rascunho
  mínimo e honesto (formulário de contacto, propriedade dos conteúdos). Devem
  ser revistos por quem trata do RGPD da empresa.
- **Resolução das imagens.** As fotografias de evento estão em boa resolução.
  Os recortes do folheto (`rosto`, `multidao`) vêm de uma digitalização a
  1600 px, por isso ficam mais suaves se forem ampliados.
- **Identificação das pessoas.** Só o Carlos Uissa está identificado (secção do
  CEO). As restantes pessoas nas fotografias de evento não têm legenda, porque
  essa informação não foi fornecida — as legendas ficam em `.media .cap`.
- Os quatro números da secção «Quem Somos» (5 países · 7 áreas · 2 continentes ·
  1 língua) derivam do conteúdo do folheto — não há dados de audiência,
  faturação ou público a apresentar.
