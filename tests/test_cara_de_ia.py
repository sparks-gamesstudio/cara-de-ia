import json
import subprocess
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from cara_de_ia import analisar  # noqa: E402

COM_CARA = (RAIZ / "exemplos" / "com-cara-de-ia.txt").read_text(encoding="utf-8")
SEM_CARA = (RAIZ / "exemplos" / "sem-cara-de-ia.txt").read_text(encoding="utf-8")


def regras(texto):
    return {a["regra"] for a in analisar(texto)["achados"]}


class Exemplos(unittest.TestCase):
    def test_texto_com_tiques_tira_nota_alta(self):
        self.assertGreaterEqual(analisar(COM_CARA)["nota"], 60)

    def test_texto_direto_tira_nota_baixa(self):
        r = analisar(SEM_CARA)
        self.assertLess(r["nota"], 25, r["achados"])


class Regras(unittest.TestCase):
    def test_contraste(self):
        self.assertIn("contraste", regras("Isso não é sobre dinheiro, é sobre liberdade."))
        self.assertIn("contraste", regras("Ele não só canta, mas também dança muito bem."))

    def test_negacao_comum_nao_vira_contraste(self):
        self.assertNotIn("contraste", regras("O carro não é novo. Comprei em 2019 e paguei à vista."))

    def test_assistente(self):
        self.assertIn("assistente", regras("Claro! Vou explicar como funciona."))
        self.assertIn("assistente", regras("Espero que isso ajude no seu projeto."))

    def test_pergunta_falsa(self):
        self.assertIn("pergunta_falsa", regras("Testamos tudo. O resultado? Mais vendas."))

    def test_pergunta_de_verdade_longa_nao_conta(self):
        self.assertNotIn("pergunta_falsa", regras("Você lembra quando foi a última vez que abriu aquele aplicativo no celular? Eu não."))

    def test_gerundio_final(self):
        self.assertIn("gerúndio_final", regras("A ferramenta foi atualizada, garantindo mais agilidade para todos."))

    def test_lista_de_sem(self):
        self.assertIn("lista_de_sem", regras("Funciona sem cadastro, sem cartão e sem instalar nada."))

    def test_listas_de_tres_so_contam_quando_repetem(self):
        self.assertNotIn("lista_de_três", regras("Comprei pão, leite e café."))
        self.assertIn("lista_de_três", regras("Pão, leite e café. Sol, areia e mar. Rápido, fácil e barato."))

    def test_ritmo_igual(self):
        frase = "Esta frase tem sempre seis palavras. "
        self.assertIn("ritmo_igual", regras(frase * 7))

    def test_achado_aponta_a_linha_certa(self):
        r = analisar("Primeira linha normal.\n\nSem mais delongas, vamos lá.")
        self.assertEqual(r["achados"][0]["linha"], 3)


class Bordas(unittest.TestCase):
    def test_texto_vazio(self):
        r = analisar("")
        self.assertEqual(r["nota"], 0)
        self.assertEqual(r["achados"], [])

    def test_texto_curto_avisa(self):
        self.assertIn("curto", analisar("Sem mais delongas.")["veredito"])


class Linha(unittest.TestCase):
    def rodar(self, *args, entrada=None):
        return subprocess.run([sys.executable, str(RAIZ / "scripts" / "cara_de_ia.py"), *args],
                              capture_output=True, input=entrada, encoding="utf-8")

    def test_json(self):
        p = self.rodar(str(RAIZ / "exemplos" / "com-cara-de-ia.txt"), "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertGreaterEqual(json.loads(p.stdout)["nota"], 60)

    def test_entrada_padrao_com_acento(self):
        p = self.rodar("-", entrada="É aqui que entra a mágica, garantindo ação.")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("É aqui que entra", p.stdout)

    def test_arquivo_inexistente(self):
        p = self.rodar("nao-existe.txt")
        self.assertEqual(p.returncode, 2)
        self.assertNotIn("Traceback", p.stderr)


if __name__ == "__main__":
    unittest.main()
