<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0B0A09,100:D97757&height=170&section=header&text=Cara%20de%20IA&fontSize=50&fontColor=F3EDE6&fontAlignY=36&desc=Ache%20os%20tiques%20de%20IA%20no%20seu%20texto%20%C2%B7%20gr%C3%A1tis%20da%20F%C3%A1brica%20de%20Canais&descAlignY=58&descSize=16" width="100%" alt="Cara de IA" />

<a href="https://sparks-gamesstudio.github.io/fabrica-de-canais/"><img src="https://sparks-gamesstudio.github.io/fabrica-de-canais/marca/simbolo-1024.png" width="84" alt="Fábrica de Canais" /></a>

**Aponta, linha por linha, o que faz o seu texto em português soar como IA e diz o que fazer em cada trecho.**

<p>
  <img src="https://img.shields.io/badge/gr%C3%A1tis-0B0A09?style=for-the-badge" alt="Grátis" />
  <img src="https://img.shields.io/badge/em%20portugu%C3%AAs-F3EDE6?style=for-the-badge" alt="Em português" />
  <img src="https://img.shields.io/badge/100%25%20offline-D97757?style=for-the-badge" alt="100% offline" />
  <img src="https://img.shields.io/badge/s%C3%B3%20Python-0B0A09?style=for-the-badge&logo=python&logoColor=white" alt="Só Python" />
</p>

<p>
  <a href="#instalacao"><img src="https://img.shields.io/badge/%E2%AC%87%EF%B8%8F%20Como%20instalar-D97757?style=for-the-badge" alt="Como instalar" /></a>
  <a href="https://sparks-gamesstudio.github.io/fabrica-de-canais/github.html"><img src="https://img.shields.io/badge/Mais%20projetos%20gr%C3%A1tis-0B0A09?style=for-the-badge&logo=github&logoColor=D97757" alt="Mais projetos grátis" /></a>
  <img src="https://img.shields.io/github/stars/sparks-gamesstudio/cara-de-ia?style=for-the-badge&color=D97757&label=%E2%AD%90" alt="Estrelas" />
</p>

</div>

## 👋 O Rebite explica

<img align="right" src="https://raw.githubusercontent.com/sparks-gamesstudio/sparks-gamesstudio/main/assets/rebite/acenar.jpg" width="170" alt="Rebite, o mascote da Fábrica de Canais" />

> Você pede um roteiro para a IA e vem aquele "não é apenas uma tendência, é uma necessidade". Aqui eu marco esses tiques, explico o problema e digo o que fazer. A decisão de mudar continua sendo sua.

<br clear="right" />

## 🔍 Como fica

```text
Cara de IA: 100/100 · Muita cara de IA · 90 palavras

Linha 1 · clichê
  "No mundo de hoje"
  Por quê: Abertura genérica.
  O que fazer: Comece por um fato concreto.

Linha 5 · pergunta_falsa
  "O resultado? Mais tempo livre."
  Por quê: Pergunta curta respondida logo depois.
  O que fazer: Afirme direto.
```

## 🧩 O que ele procura

| Tique | Exemplo |
|---|---|
| Contraste de revelação | "não é sobre dinheiro, é sobre liberdade" |
| Clichê | "no mundo de hoje", "vamos mergulhar fundo", "divisor de águas" |
| Fala de assistente | "ótima pergunta", "espero que isso ajude" |
| Gerúndio pendurado | "..., garantindo mais agilidade" |
| Pergunta falsa | "O resultado? Mais vendas." |
| Cadência | "sem X, sem Y e sem Z", trios em sequência, frases do mesmo tamanho |
| Formato | excesso de travessões, marcadores em negrito, emoji de enfeite |
| Palavra inflada | "potencializar", "alavancar", "jornada" |

<a id="instalacao"></a>

## ⬇️ Como instalar

Precisa do Python 3.10 ou mais novo. Não há pacotes para instalar.

**Sozinho, sem IA:**

```bash
git clone https://github.com/sparks-gamesstudio/cara-de-ia.git
```

```bash
python cara-de-ia/scripts/cara_de_ia.py meu-texto.txt
```

**Como skill do Claude Code, para ele também reescrever os trechos:**

```bash
git clone https://github.com/sparks-gamesstudio/cara-de-ia.git $HOME/.claude/skills/cara-de-ia
```

Depois, peça `/cara-de-ia` e cole o texto.

<table>
<tr>
<td width="110"><img src="https://raw.githubusercontent.com/sparks-gamesstudio/sparks-gamesstudio/main/assets/rebite/pensar.jpg" width="90" alt="Rebite pensando" /></td>
<td>

**Aviso honesto:** isto não é um detector de IA. Ele procura padrões em uma lista feita à mão, e gente de verdade também escreve assim. A nota não prova quem escreveu, então não use para acusar ninguém. Um texto de IA bem revisado pode tirar nota baixa, e a precisão não foi medida em um conjunto grande de textos.

</td>
</tr>
</table>

## 🔒 Seus dados

O script roda no seu computador e não faz nenhuma chamada de rede. Na versão skill, o texto passa pelo Claude Code, como qualquer texto que você envia a ele.

## 🧪 Para quem quer mexer

```bash
python -m unittest discover -s tests -v
```

As regras ficam na lista `REGRAS`, em `scripts/cara_de_ia.py`. Para sugerir um tique novo, abra uma issue com um exemplo.

---

<div align="center">

<a href="https://sparks-gamesstudio.github.io/fabrica-de-canais/"><img src="https://sparks-gamesstudio.github.io/fabrica-de-canais/marca/simbolo-1024.png" width="56" alt="Fábrica de Canais" /></a>

Feito pela **[Fábrica de Canais](https://sparks-gamesstudio.github.io/fabrica-de-canais/)**, skills de Claude Code para canais de vídeo no piloto automático.

<a href="https://instagram.com/afabricadecanais"><img src="https://img.shields.io/badge/@afabricadecanais-E4405F?style=flat-square&logo=instagram&logoColor=white" alt="Instagram" /></a>
<a href="https://github.com/sparks-gamesstudio"><img src="https://img.shields.io/badge/mais%20projetos-0B0A09?style=flat-square&logo=github&logoColor=D97757" alt="Mais projetos" /></a>

<sub>Licença MIT · use, modifique e compartilhe. Se ajudou, deixa uma ⭐</sub>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:D97757,100:0B0A09&height=90&section=footer" width="100%" alt="" />

</div>
