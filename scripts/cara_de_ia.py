#!/usr/bin/env python3
"""Aponta num texto em português os tiques que costumam denunciar escrita de IA.

Não descobre quem escreveu o texto. Só mostra padrões, para você decidir o que reescrever.
Uso: python cara_de_ia.py texto.txt  (ou "-" para ler da entrada padrão)  [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

LETRA = "A-Za-zÀ-ÖØ-öø-ÿ"
PALAVRA = re.compile(rf"[{LETRA}0-9]+(?:-[{LETRA}0-9]+)*")


@dataclass
class Achado:
    linha: int
    regra: str
    trecho: str
    motivo: str
    troca: str
    peso: int


# (id, padrão, peso, motivo, o que fazer)
REGRAS: list[tuple[str, str, int, str, str]] = [
    # Contraste de revelação
    ("contraste", r"\bnão (?:é|são|foi|era) (?:apenas |só |somente |simplesmente |sobre )?[^.,;:!?\n]{1,50}[,;:—–-]\s*(?:é|são|foi|era|mas)\b", 3,
     "Contraste de revelação (\"não é X, é Y\"), o tique mais comum de IA.", "Diga direto o que a coisa é."),
    ("contraste", r"\bnão se trata (?:apenas |só |somente )?de\b", 3,
     "Contraste de revelação.", "Diga direto do que se trata."),
    ("contraste", r"\bnão (?:apenas|só|somente) [^.;:!?\n]{1,70}\b(?:mas|como) (?:também|ainda)\b", 2,
     "Fórmula \"não só X, mas também Y\".", "Separe em duas frases ou escolha a ideia mais forte."),
    ("contraste", r"\bmais do que (?:um|uma|apenas|só) [^.;:!?\n]{1,50},\s*(?:é|são)\b", 2,
     "Fórmula \"mais do que X, é Y\".", "Diga direto o que a coisa é."),
    ("lista_de_sem", r"\bsem [^.,;:!?\n]{1,30},\s*sem [^.,;:!?\n]{1,30}(?:,| e)\s*sem\b", 2,
     "Lista em cadência (\"sem X, sem Y, sem Z\").", "Fique com o item que mais importa."),
    # Abertura e fecho de assistente
    ("assistente", r"\b(?:ótima|excelente|boa) pergunta\b", 3, "Fala de assistente.", "Apague."),
    ("assistente", r"(?:^|\n)\s*(?:claro|com certeza|certamente)\s*[!,:]", 3, "Abertura de assistente.", "Comece pelo assunto."),
    ("assistente", r"\baqui está (?:o|a|um|uma)\b", 2, "Fala de assistente entregando texto.", "Apague."),
    ("assistente", r"\b(?:espero que (?:isso |isto )?ajude|se precisar de mais|fique à vontade para|estou à disposição)\b", 3,
     "Fecho de assistente.", "Apague."),
    # Expressões prontas
    ("clichê", r"\b(?:no|em um|num) mundo (?:de hoje|atual|cada vez mais|em constante)\b", 3, "Abertura genérica.", "Comece por um fato concreto."),
    ("clichê", r"\bno cenário (?:atual|de hoje)\b", 2, "Abertura genérica.", "Diga qual cenário, com um exemplo."),
    ("clichê", r"\bnos dias (?:de hoje|atuais)\b", 1, "Abertura genérica.", "Corte ou seja específico."),
    ("clichê", r"\b(?:vale|cabe) (?:ressaltar|destacar|lembrar|mencionar)\b", 2, "Enrolação antes da informação.", "Vá direto à informação."),
    ("clichê", r"\bé (?:importante|fundamental|essencial|crucial) (?:ressaltar|destacar|lembrar|notar|entender|compreender|mencionar)\b", 2,
     "Enrolação antes da informação.", "Vá direto à informação."),
    ("clichê", r"\b(?:vamos )?mergulh(?:ar|e|emos|amos) (?:fundo|de cabeça|neste|nesse|no|na)\b", 3, "Metáfora típica de IA.", "Diga o que vem a seguir."),
    ("clichê", r"\bsem mais delongas\b", 3, "Clichê.", "Apague."),
    ("clichê", r"\bdivisor de águas\b", 2, "Clichê.", "Mostre o que mudou, com um dado."),
    ("clichê", r"\b(?:a|uma) chave (?:para|do|da)\b", 1, "Metáfora batida.", "Nomeie a causa real."),
    ("clichê", r"\b(?:a verdade é que|a grande verdade|o segredo é)\b", 1, "Suspense vazio.", "Corte e diga logo."),
    ("clichê", r"\bé aqui que (?:entra|entram|a mágica)\b", 3, "Transição típica de IA.", "Corte a transição."),
    ("clichê", r"\b(?:em suma|em síntese|em última análise|em resumo|para concluir|em conclusão)\b", 2, "Fecho de redação escolar.", "Termine na ideia, sem anunciar o fim."),
    ("clichê", r"\bnão é exagero dizer\b", 2, "Enrolação antes da informação.", "Afirme ou corte."),
    ("clichê", r"\bdesempenha um papel\b", 2, "Expressão genérica traduzida do inglês.", "Diga o que a coisa faz."),
    ("clichê", r"\bcada vez mais (?:importante|relevante|essencial|comum)\b", 1, "Generalização sem prova.", "Use um número ou um exemplo."),
    # Palavras infladas
    ("palavra_inflada", r"\b(?:potencializ\w+|alavanc\w+|otimiz\w+|impulsion\w+|revolucion\w+|transformador\w*|inovador\w*|robust[oa]s?|holístic\w+|sinergi\w+|tapeçaria|desbloque\w+|disruptiv\w+|empoder\w+)\b", 1,
     "Palavra inflada, comum em texto de IA e de marketing.", "Troque por uma palavra simples ou por um resultado concreto."),
    ("palavra_inflada", r"\b(?:jornada|navegar pel[oa]s?|universo d[eoa]s?|ecossistema)\b", 1, "Metáfora inflada.", "Diga o assunto pelo nome."),
    # Gerúndio pendurado
    ("gerúndio_final", r",\s+(?:garantindo|permitindo|proporcionando|transformando|tornando|reforçando|destacando|oferecendo|possibilitando|contribuindo|promovendo|ajudando|criando)\b[^.!?\n]*[.!?]", 2,
     "Frase que termina com um gerúndio acrescentando importância.", "Corte o final ou faça dele uma frase própria."),
    # Pergunta e resposta falsa
    ("pergunta_falsa", rf"(?:^|(?<=[.!?\n])\s*)(?:[{LETRA}]+\s+){{0,3}}[{LETRA}]+\?\s+[A-ZÀ-Ú][^.!?\n]{{0,60}}[.!]", 2,
     "Pergunta curta respondida logo depois (\"O resultado? Mais vendas.\").", "Afirme direto."),
]

REGRAS_COMPILADAS = [(i, re.compile(p, re.IGNORECASE), peso, m, t) for i, p, peso, m, t in REGRAS]
# Pergunta falsa depende da letra maiúscula, então não pode ignorar a caixa.
REGRAS_COMPILADAS = [
    (i, re.compile(rx.pattern) if i == "pergunta_falsa" else rx, peso, m, t)
    for i, rx, peso, m, t in REGRAS_COMPILADAS
]

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


def _linha_de(texto: str, pos: int) -> int:
    return texto.count("\n", 0, pos) + 1


def _resumo(trecho: str, limite: int = 90) -> str:
    trecho = " ".join(trecho.split())
    return trecho if len(trecho) <= limite else trecho[: limite - 1] + "…"


def _frases(texto: str) -> list[str]:
    partes = re.split(r"(?<=[.!?])\s+|\n+", texto)
    return [p.strip() for p in partes if len(PALAVRA.findall(p)) >= 2]


def _estruturais(texto: str, palavras: int) -> list[Achado]:
    achados: list[Achado] = []

    frases = _frases(texto)
    if len(frases) >= 6:
        tamanhos = [len(PALAVRA.findall(f)) for f in frases]
        media = statistics.mean(tamanhos)
        if media and statistics.pstdev(tamanhos) / media < 0.25:
            achados.append(Achado(1, "ritmo_igual", f"{len(frases)} frases, quase todas com cerca de {round(media)} palavras",
                                  "Frases do mesmo tamanho deixam o texto monótono.",
                                  "Misture frases bem curtas com frases mais longas.", 2))

    trios = list(re.finditer(rf"\b[{LETRA}-]+,\s+[{LETRA}-]+\s+e\s+[{LETRA}-]+\b", texto))
    if len(trios) >= 3:
        achados.append(Achado(_linha_de(texto, trios[0].start()), "lista_de_três",
                              f"{len(trios)} listas de três itens, como \"{_resumo(trios[0].group(), 40)}\"",
                              "Trios repetidos soam automáticos.", "Deixe alguns com um ou dois itens.", 2))

    travessoes = texto.count("—")
    if travessoes >= 3 and travessoes / max(palavras, 1) > 1 / 60:
        achados.append(Achado(_linha_de(texto, texto.index("—")), "travessão", f"{travessoes} travessões",
                              "Excesso de travessões é uma marca conhecida de IA.",
                              "Troque a maioria por ponto ou vírgula.", 2))

    linhas = texto.splitlines()
    negrito = [n for n, l in enumerate(linhas, 1) if re.match(r"\s*(?:[-*•]|\d+\.)\s+\*\*[^*]+\*\*", l)]
    if len(negrito) >= 3:
        achados.append(Achado(negrito[0], "marcador_com_negrito", f"{len(negrito)} marcadores que começam em negrito",
                              "Formato padrão de resposta de assistente.", "Escreva em parágrafo, se o texto for corrido.", 2))

    enfeitados = [n for n, l in enumerate(linhas, 1)
                  if EMOJI.search(l[:6]) and (l.lstrip().startswith(("-", "*", "•", "#")) or len(l) < 80)]
    if len(enfeitados) >= 3:
        achados.append(Achado(enfeitados[0], "emoji_de_enfeite", f"{len(enfeitados)} linhas abertas com emoji",
                              "Emoji como marcador é padrão de texto gerado.", "Deixe só onde ele acrescenta algo.", 1))
    return achados


def analisar(texto: str) -> dict:
    palavras = len(PALAVRA.findall(texto))
    achados: list[Achado] = []
    ocupado: list[tuple[int, int]] = []

    for regra, rx, peso, motivo, troca in REGRAS_COMPILADAS:
        for m in rx.finditer(texto):
            ini, fim = m.span()
            if any(ini < f and fim > i for i, f in ocupado):
                continue
            ocupado.append((ini, fim))
            # O início pode ter casado a quebra de linha anterior.
            inicio_real = ini + len(m.group()) - len(m.group().lstrip())
            achados.append(Achado(_linha_de(texto, inicio_real), regra, _resumo(m.group()), motivo, troca, peso))

    achados.extend(_estruturais(texto, palavras))
    achados.sort(key=lambda a: (a.linha, a.regra))

    pontos = sum(a.peso for a in achados)
    # 12 pontos a cada 100 palavras já é um texto tomado por tiques.
    base = max(palavras, 60)
    nota = min(100, round(pontos / base * 100 * 100 / 12))

    if palavras < 30:
        veredito = "Texto curto demais para uma nota confiável"
    elif nota >= 60:
        veredito = "Muita cara de IA"
    elif nota >= 25:
        veredito = "Alguns tiques de IA"
    else:
        veredito = "Poucos tiques de IA"

    return {"nota": nota, "veredito": veredito, "palavras": palavras, "achados": [asdict(a) for a in achados]}


def formatar(r: dict) -> str:
    saida = [f"Cara de IA: {r['nota']}/100 · {r['veredito']} · {r['palavras']} palavras", ""]
    if not r["achados"]:
        saida.append("Nenhum tique encontrado.")
    for a in r["achados"]:
        saida += [f"Linha {a['linha']} · {a['regra']}", f"  \"{a['trecho']}\"", f"  Por quê: {a['motivo']}", f"  O que fazer: {a['troca']}", ""]
    saida.append("A nota mede tiques no texto. Ela não prova quem escreveu.")
    return "\n".join(saida).rstrip()


def ler(caminho: str) -> str:
    if caminho == "-":
        return sys.stdin.read()
    dados = Path(caminho).read_bytes()
    try:
        return dados.decode("utf-8-sig")
    except UnicodeDecodeError:
        return dados.decode("cp1252")


def main(argv: list[str] | None = None) -> int:
    for fluxo in (sys.stdout, sys.stderr, sys.stdin):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Aponta os tiques de IA num texto em português.")
    p.add_argument("arquivo", help='arquivo de texto, ou "-" para a entrada padrão')
    p.add_argument("--json", action="store_true", help="saída em JSON")
    a = p.parse_args(argv)
    try:
        texto = ler(a.arquivo)
    except OSError as erro:
        print(f"Não consegui abrir {a.arquivo}: {erro.strerror}", file=sys.stderr)
        return 2
    r = analisar(texto)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else formatar(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
