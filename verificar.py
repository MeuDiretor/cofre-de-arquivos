"""Contrato local das protecoes deste template; nao faz chamadas AWS."""
import json
from pathlib import Path


def verificar(template):
    problemas = []
    recursos = template.get("Resources", {})
    bucket = recursos.get("Arquivos", {})
    props = bucket.get("Properties", {})
    if bucket.get("Type") != "AWS::S3::Bucket":
        problemas.append("Recurso Arquivos deve ser um bucket S3.")
    bloqueios = props.get("PublicAccessBlockConfiguration", {})
    for chave in ("BlockPublicAcls", "BlockPublicPolicy", "IgnorePublicAcls", "RestrictPublicBuckets"):
        if bloqueios.get(chave) is not True:
            problemas.append(f"Bloqueio publico ausente: {chave}.")
    if props.get("OwnershipControls") != {"Rules": [{"ObjectOwnership": "BucketOwnerEnforced"}]}:
        problemas.append("ACLs devem permanecer desabilitadas.")
    if props.get("VersioningConfiguration", {}).get("Status") != "Enabled":
        problemas.append("Versionamento deve estar habilitado.")
    regras = props.get("BucketEncryption", {}).get("ServerSideEncryptionConfiguration", [])
    if not any(r.get("ServerSideEncryptionByDefault", {}).get("SSEAlgorithm") == "AES256" for r in regras):
        problemas.append("Criptografia SSE-S3 explicita ausente.")
    if "BucketName" in props:
        problemas.append("O nome fisico deve ser gerado, sem identificador global fixo.")
    for nome in ("Arquivos", "TransporteSeguro"):
        for atributo in ("DeletionPolicy", "UpdateReplacePolicy"):
            if recursos.get(nome, {}).get(atributo) != "Retain":
                problemas.append(f"Preservacao ausente: {nome}.{atributo}.")
    politica = recursos.get("TransporteSeguro", {})
    if politica.get("Type") != "AWS::S3::BucketPolicy" or politica.get("Properties", {}).get("Bucket") != {"Ref": "Arquivos"}:
        problemas.append("Politica deve apontar ao bucket da stack.")
    declaracoes = politica.get("Properties", {}).get("PolicyDocument", {}).get("Statement", [])
    esperado = {
        "Effect": "Deny", "Principal": "*", "Action": "s3:*",
        "Resource": [{"Fn::GetAtt": ["Arquivos", "Arn"]}, {"Fn::Sub": "${Arquivos.Arn}/*"}],
        "Condition": {"Bool": {"aws:SecureTransport": "false"}},
    }
    if not any(all(d.get(k) == v for k, v in esperado.items()) for d in declaracoes):
        problemas.append("Negacao de transporte inseguro deve abranger bucket e objetos.")
    if any(d.get("Effect") == "Allow" for d in declaracoes):
        problemas.append("Este contrato nao concede acesso pela politica do bucket.")
    if set(recursos) != {"Arquivos", "TransporteSeguro"}:
        problemas.append("Recursos adicionais exigem nova revisao de escopo e custos.")
    return problemas


if __name__ == "__main__":
    arquivo = Path(__file__).with_name("template.json")
    resultado = verificar(json.loads(arquivo.read_text(encoding="utf-8")))
    print("\n".join(resultado) if resultado else "Contrato local verificado.")
    raise SystemExit(bool(resultado))
