---
name: cara-de-ia
description: Aponta num texto em português os tiques que denunciam escrita de IA (contraste "não é X, é Y", clichês, gerúndio pendurado, trios, travessões) e reescreve só os trechos marcados, sem inventar nada. Use quando pedirem "tira a cara de IA", "isso parece IA?", "deixa mais humano" ou ao revisar roteiro, legenda, post ou e-mail.
---

# Cara de IA

`<skill>` é a pasta desta skill.

1. Salve o texto em um arquivo temporário, se ele veio colado na conversa, e rode:
   ```
   python <skill>/scripts/cara_de_ia.py <arquivo>
   ```
2. Mostre a nota e os achados mais importantes, em poucas linhas.
3. Se a pessoa pediu para reescrever, ou pediu para tirar a cara de IA, reescreva **só os trechos marcados**:
   - mantenha todos os fatos, números, nomes e a voz de quem escreveu;
   - não acrescente exemplo, dado ou opinião. Onde faltar um detalhe concreto, deixe `[coloque aqui um exemplo seu]`;
   - não troque um tique por outro.
4. Rode o script de novo na versão reescrita e mostre a nota antes e depois.

Sempre deixe claro: a nota mede tiques no texto e não prova quem escreveu. Nunca use a nota para acusar alguém de usar IA.
