# Validação realizada

Data: 23/11/2026. Ambiente local: Windows, Python 3.14, cfn-lint 1.61.0 instalado em ambiente virtual isolado. Nenhuma credencial AWS foi utilizada.

| Verificação | Resultado observado | Limite |
|---|---|---|
| `python verificar.py` | Saída `Contrato local verificado.`, código 0 | Confere as proteções específicas deste template, não toda configuração CloudFormation possível |
| `python -m unittest discover -s tests -v` | Nove testes aprovados, 0,006 s | Análise local de documentos e mutações, sem autorizar requisições reais |
| `cfn-lint template.json` | Código 0, sem apontamentos | Esquemas e regras da versão instalada, sem implantação |
| Controle negativo do cfn-lint | `VersioningConfiguration.Status=Invalid` rejeitado com E3030, código 2 | Cópia temporária, removida após a conferência; template original preservado |

Os nove testes incluem subcasos que desativam cada bloqueio público, trocam a negação por permissão, invertem o contexto de HTTPS, removem o ARN do bucket ou dos objetos, alteram cada política de preservação, removem criptografia/versionamento/propriedade, mudam o destino da política, fixam um nome global e acrescentam um recurso fora do escopo. O contrato acusa essas alterações e preserva o documento recebido.

O contrato espera o formato deste projeto. Não é ferramenta genérica para entrada arbitrária nem substitui cfn-lint, revisão de política ou testes remotos. Nenhum resultado foi apresentado como deploy, teste de conectividade ou garantia de segurança absoluta.
