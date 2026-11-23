# Decisões e roteiro operacional

## Escopo

O recurso central é armazenamento de arquivos, sem depender de AMI, VPC padrão, porta pública ou chave SSH. O bucket não recebe nome global fixo. `Ref` associa a política ao bucket; `Fn::GetAtt` e `Fn::Sub` constroem os ARNs sem IDs de conta fixos.

Mantive os quatro controles de bloqueio de acesso público e `BucketOwnerEnforced`, desabilitando ACLs. A criptografia padrão usa SSE-S3 (`AES256`); não cria chave KMS. Uma opção de criptografia padrão não substitui revisão de todas as políticas e solicitações que um consumidor poderá usar.

A política nega operações S3 com `aws:SecureTransport=false`, cobrindo bucket e objetos. Não contém `Allow`. Isso não é um simulador de autorização IAM: permissões de identidade, SCPs, endpoints, outras políticas e contexto da requisição precisam de revisão numa implantação real. Integrações com serviços AWS também precisam de revisão específica do contexto de transporte; nenhuma foi configurada neste projeto.

## Preservação

Versionamento ajuda a recuperar sobrescritas e exclusões lógicas, mas não impede exclusão permanente por quem tiver essa permissão. Não há Object Lock nem replicação externa.

Retenho bucket e política na exclusão e substituição da stack. A preservação evita uma limpeza automática destrutiva, mas exige inventário posterior: recursos antigos podem ficar fora da stack e continuar custando. Não prometo exclusão completa ao excluir a stack. Não há função de autoesvaziamento.

## Implantação futura — não executada

1. Confirmar conta, região, autorização, permissões mínimas e custos esperados. O valor da tag Ambiente não faz essa validação.
2. Validar template e revisar um change set, incluindo qualquer substituição. Conferir quotas e configurações da conta.
3. Somente com implantação aprovada, criar a stack e acompanhar eventos até o estado final. `CREATE_COMPLETE` do recurso não substitui todos os testes de acesso.
4. Conferir configuração efetiva de acesso público, propriedade, criptografia, versionamento e política. Verificar os outputs e registrar IDs reais em inventário privado.
5. Com dados sintéticos e identidade de teste restrita, verificar escrita e leitura autorizadas, tentativa não autorizada, transporte inseguro e restauração de versão. Planejar propagação do versionamento conforme a documentação S3 antes de fazer operações de escrita.
6. Para desativar, inventariar versões, requisitos de retenção e recursos retidos. Qualquer exclusão de dados deve ser uma decisão explícita, precedida de conferência das cópias necessárias.

## Aprendizados

Um template descreve estado pretendido e dependências; o CloudFormation administra operações da stack. JSON válido não basta: esquema, referências, permissões e pré-requisitos importam. Reutilização pede parâmetros pertinentes, nomes lógicos estáveis e revisão das mudanças. A diferença entre exclusão e substituição exige duas políticas distintas de preservação.
