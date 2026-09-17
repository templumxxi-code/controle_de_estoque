# Manual rápido

## Entrar

Abra o Streamlit e entre com o administrador configurado em `ADMIN_EMAIL` e `ADMIN_PASSWORD` no `.env` local. Depois, acesse `Usuários` para criar os demais logins.

## Dashboard

A tela inicial mostra faturamento, lucro bruto, resultado líquido, despesas, valor do estoque e alertas de estoque mínimo. Os botões de atalho levam direto às operações mais frequentes.

## Produto

Abra `Produtos`, preencha código, nome, custo, preço e estoque mínimo e salve. O preço sugerido é calculado pela margem informada.

## Entrada

Abra `Estoque`, selecione o produto, informe quantidade e custo unitário e registre. O saldo e o custo do produto são atualizados.

## Venda

Abra `Vendas`, escolha o produto, informe quantidade e forma de pagamento e conclua. O sistema só permite vender o que está disponível. O estoque é baixado e o financeiro recebe a receita automaticamente.

## Financeiro

Use `Financeiro` para cadastrar despesas e receitas que não sejam vendas. Informe categoria, descrição e valor.

## Ajuste e histórico

Em `Estoque`, use `Ajuste manual`, informe o tipo, quantidade e uma justificativa. O sistema registra saldo anterior, saldo novo e diferença. O histórico aparece na mesma tela.

## Relatórios e exportação

Abra `Relatórios`, escolha o tipo e baixe o resultado em Excel, CSV ou PDF.

## Importação

Em `Importação`, baixe o template, preencha a planilha e carregue o arquivo. Revise a prévia e os erros. A importação só acontece após `Confirmar importação`.

## Anexos e configurações

Anexos podem ser enviados pela API para documentos PDF e imagens, ficando armazenados em `UPLOAD_DIR` com referência persistida no banco. `Configurações` permite alterar o nome da empresa e a informação exibida sobre backup.

## Sair

Use `Sair` no menu lateral para invalidar a sessão local.
