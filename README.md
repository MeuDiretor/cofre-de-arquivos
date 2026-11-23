# Cofre de Arquivos

Implementei uma stack CloudFormation para armazenar arquivos em um bucket S3 privado. O template declara criptografia padrão, versionamento, bloqueio de acesso público e recusa de transporte sem HTTPS. O nome físico é gerado pelo CloudFormation.

## Estrutura

- `template.json`: bucket, política e saídas com nome e ARN.
- `verificar.py`: contrato local das proteções previstas neste projeto.
- `tests/test_contrato.py`: regressões para mudanças perigosas na configuração.
- [Decisões e operação](docs/decisoes.md).
- [Validação realizada](docs/validacao.md).

O parâmetro `Ambiente` aceita `desenvolvimento`, `homologacao` ou `producao` e serve como tag. Ele não conecta o projeto a nenhum ambiente existente.

## Verificar localmente

Python 3.10 ou posterior. Os testes e o verificador usam somente a biblioteca padrão. Execute a partir da raiz deste repositório:

```sh
python verificar.py
python -m unittest discover -s tests -v
```

Para conferir o esquema CloudFormation, crie um ambiente virtual e instale a ferramenta de desenvolvimento:

```sh
python -m venv .venv
```

Windows:

```powershell
.venv/Scripts/python.exe -m pip install -r requirements-dev.txt
.venv/Scripts/cfn-lint.exe template.json
```

Linux/macOS:

```sh
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/cfn-lint template.json
```

## Resultado e limites

Em 23/11/2026, executei nove testes locais com sucesso, o verificador de contrato e cfn-lint 1.61.0 sem apontamentos. Um controle negativo com status de versionamento inválido foi rejeitado com E3030.

Não implantei esta stack na AWS, não criei bucket e não executei testes de acesso remoto. A validação estática não prova permissões efetivas, comportamento de uma conta real nem disponibilidade do serviço. Os próximos passos de uma implantação futura estão documentados como roteiro, não como operações já realizadas.

Não há aplicação web, usuário IAM, chave de acesso, instância EC2 ou credencial neste repositório. A política só nega transporte inseguro; não concede acesso a arquivos. Um consumidor futuro precisará de autorização apropriada e restrita.

## Preservação e custos

`DeletionPolicy: Retain` e `UpdateReplacePolicy: Retain` preservam os recursos nas operações correspondentes do CloudFormation. Isso não impede que uma identidade autorizada remova objetos ou versões diretamente. Versionamento não equivale a backup independente ou armazenamento imutável.

Recursos retidos saem do gerenciamento da stack e podem continuar gerando custos. Uma futura implantação exige avaliar preços, permissões, integrações e retenção. Este projeto não executa deploy nem limpeza automaticamente.

## Referências

Consultadas em 23/11/2026:

- [Primeira stack e ciclo de criação](https://docs.aws.amazon.com/pt_br/AWSCloudFormation/latest/UserGuide/gettingstarted.walkthrough.html).
- [Recurso S3 Bucket](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-s3-bucket.html).
- [DeletionPolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-deletionpolicy.html).
- [UpdateReplacePolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-updatereplacepolicy.html).

Código e documentação próprios, sob licença MIT.
