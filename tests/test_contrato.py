import copy
import json
from pathlib import Path
import unittest

from verificar import verificar


class ContratoTests(unittest.TestCase):
    def setUp(self):
        self.base = json.loads((Path(__file__).resolve().parents[1] / "template.json").read_text(encoding="utf-8"))

    def test_template_atende_contrato_e_nao_muda_entrada(self):
        original = copy.deepcopy(self.base)
        self.assertEqual(verificar(self.base), [])
        self.assertEqual(self.base, original)

    def test_cada_bloqueio_publico_e_obrigatorio(self):
        for nome in self.base["Resources"]["Arquivos"]["Properties"]["PublicAccessBlockConfiguration"]:
            with self.subTest(nome=nome):
                alterado = copy.deepcopy(self.base)
                alterado["Resources"]["Arquivos"]["Properties"]["PublicAccessBlockConfiguration"][nome] = False
                self.assertTrue(verificar(alterado))

    def test_http_nao_pode_virar_permissao_ou_https_negado(self):
        for atributo, valor in (("Effect", "Allow"), ("Condition", {"Bool": {"aws:SecureTransport": "true"}})):
            with self.subTest(atributo=atributo):
                alterado = copy.deepcopy(self.base)
                alterado["Resources"]["TransporteSeguro"]["Properties"]["PolicyDocument"]["Statement"][0][atributo] = valor
                self.assertTrue(verificar(alterado))

    def test_negacao_precisa_cobrir_bucket_e_objetos(self):
        for indice in (0, 1):
            with self.subTest(indice=indice):
                alterado = copy.deepcopy(self.base)
                del alterado["Resources"]["TransporteSeguro"]["Properties"]["PolicyDocument"]["Statement"][0]["Resource"][indice]
                self.assertTrue(verificar(alterado))

    def test_exclusao_e_substituicao_preservam_recursos(self):
        for nome in ("Arquivos", "TransporteSeguro"):
            for atributo in ("DeletionPolicy", "UpdateReplacePolicy"):
                with self.subTest(nome=nome, atributo=atributo):
                    alterado = copy.deepcopy(self.base)
                    alterado["Resources"][nome][atributo] = "Delete"
                    self.assertTrue(verificar(alterado))

    def test_sem_criptografia_ou_versionamento_rejeitado(self):
        for campo in ("BucketEncryption", "VersioningConfiguration", "OwnershipControls"):
            with self.subTest(campo=campo):
                alterado = copy.deepcopy(self.base)
                del alterado["Resources"]["Arquivos"]["Properties"][campo]
                self.assertTrue(verificar(alterado))

    def test_politica_nao_pode_proteger_outro_bucket(self):
        self.base["Resources"]["TransporteSeguro"]["Properties"]["Bucket"] = "outro-bucket"
        self.assertTrue(verificar(self.base))

    def test_nome_global_fixo_rejeitado(self):
        self.base["Resources"]["Arquivos"]["Properties"]["BucketName"] = "nome-fixo"
        self.assertTrue(verificar(self.base))

    def test_recurso_adicional_exige_revisao(self):
        self.base["Resources"]["Extra"] = {"Type": "AWS::EC2::Instance"}
        self.assertTrue(verificar(self.base))


if __name__ == "__main__":
    unittest.main()
