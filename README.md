# PALOP ENTERTAINMENT — website institucional

Site estático de ficheiro único (`index.html`): CSS, HTML e JS vanilla, sem build,
sem dependências. Basta abrir o ficheiro ou publicar a pasta.

## Estrutura

```
palop/
├── index.html     ← o site completo (~108 KB)
├── img/           ← imagens em WebP (~1,4 MB carregados pela página)
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

Os slots ainda por preencher estão comentados no topo do `<style>` (bloco
«SLOTS DE IMAGEM») — enquanto não tiverem fotografia, os cartões usam
composições gráficas de fallback que continuam a ler bem:

Todos os slots estão preenchidos. Se houver imagens melhores para algum
cartão, basta trocar o ficheiro em `img/` mantendo o nome.

Nas imagens de campanha (Turismo, Jobs, Agência, PALOP TV) foi recortada
apenas a zona de imagem, deixando de fora os títulos e o logótipo já impressos
no cartaz — de outro modo apareceriam dois títulos sobrepostos no mesmo
cartão. No PALOP Jobs, as duas colunas de pessoas foram justapostas para
eliminar a coluna central de ícones e texto; no PALOP TV usou-se a zona dos
arcos e do mapa, sem o lettering do canal.

O enquadramento de cada cartão é controlado por classes no `index.html`:
`.top` (topo da imagem), `.low` (base), `.right` e `.face`. Para reenquadrar,
altere a `background-position` da classe respetiva no `<style>`.

Formatos sugeridos: hero 2400×1400 · retratos 1200×1600 · cartões 1400×1000.
Guardar em WebP a ~80 % de qualidade.

## 2. Formulário de contacto

O botão **«Enviar pelo WhatsApp»** valida os campos e abre o WhatsApp
(`wa.me/351962215940`) com a mensagem já composta:

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

Qualquer alojamento estático serve. Com a Vercel:

```bash
npx vercel --prod
```

(a partir desta pasta; não há passo de build)

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
