# Pumphouseup

MVP de gestão de estoque e resultado financeiro da Pumphouseup Suplementos.

## Arquitetura

- `backend/`: FastAPI, SQLAlchemy, autenticação JWT e regras de negócio.
- `frontend/`: Streamlit responsivo consumindo a API.
- `database/schema.sql`: schema explícito para MySQL 8+.
- `pumphouseup-logo.png.jpeg`: logo fornecida pelo proprietário.

O backend aceita SQLite por padrão para desenvolvimento local sem serviço externo, mas a configuração de produção deve usar MySQL via `DATABASE_URL`.

## Requisitos

Python 3.11+, MySQL 8+ (produção), pip e um ambiente virtual.

## Instalação

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
pip install -r frontend\requirements.txt
Copy-Item .env.example .env
```

Edite `.env` com a conexão MySQL antes da publicação. A homologação local utilizou MySQL Community Server 8.4.9 em `127.0.0.1:3307`. SQLite permanece somente como suporte aos testes rápidos.

Para aplicar a migration MySQL:

```powershell
$env:MYSQL_PWD = "senha-do-usuario"
Get-Content database\migrations\001_initial.sql -Raw | & "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe" --protocol=TCP --host=127.0.0.1 --port=3307 -u pumphouseup_app
Remove-Item Env:MYSQL_PWD
```

## Inicialização

Terminal 1:

```powershell
$env:PYTHONPATH = "backend"
uvicorn app.main:app --reload --app-dir backend
```

Terminal 2:

```powershell
streamlit run frontend\app.py
```

Abra `http://localhost:8501` e informe as credenciais configuradas em `ADMIN_EMAIL` e `ADMIN_PASSWORD` no arquivo `.env` local. Nunca publique esse arquivo. Depois do login, o administrador pode criar os demais usuários no menu `Usuários`.

## Funcionalidades implementadas

1. Cadastre produto.
2. Registre entrada.
3. Confirme o saldo no Estoque.
4. Realize venda.
5. A venda baixa o estoque, grava custo histórico, lucro, movimentação e receita automaticamente.
6. O Dashboard mostra os indicadores.

Também estão disponíveis: CRUD de categorias e produtos com inativação, ajustes rastreáveis e histórico de estoque, receitas/despesas, relatórios de estoque/vendas/financeiro, exportação CSV/XLSX/PDF, importação CSV/XLSX com prévia e validação, anexos locais com referência no banco, configurações básicas e dashboard com quatro gráficos reais.

O backend rejeita quantidade zero/negativa, estoque insuficiente, credencial inválida e dados monetários negativos.

## Testes

```powershell
$env:PYTHONPATH = "backend"
pytest backend\tests -q
```

Teste de integração MySQL:

```powershell
$env:PYTHONPATH = "backend"
$env:MYSQL_TEST_DATABASE_URL = $env:DATABASE_URL
pytest backend\tests\test_mysql_integration.py -q
Remove-Item Env:MYSQL_TEST_DATABASE_URL
```

## Banco e backup

Para criar o banco MySQL:

```powershell
mysql -u root -p < database\schema.sql
```

Backup:

```powershell
$env:MYSQL_PWD = "senha-do-usuario"
& "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqldump.exe" --no-tablespaces --protocol=TCP --host=127.0.0.1 --port=3307 -u pumphouseup_app pumphouseup > backup.sql
Remove-Item Env:MYSQL_PWD
```

Restauração:

```powershell
$env:MYSQL_PWD = "senha-do-usuario"
Get-Content backup.sql -Raw | & "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe" --protocol=TCP --host=127.0.0.1 --port=3307 -u pumphouseup_app pumphouseup_restore
Remove-Item Env:MYSQL_PWD
```

Preserve também o diretório configurado em `UPLOAD_DIR`, pois anexos são armazenados fora das tabelas.

## Decisões do MVP

A margem desejada usa margem sobre o preço de venda: `preço sugerido = custo / (1 - margem)`. A venda usa o custo vigente do produto e grava snapshot no item. Vendas geram receita automática; receitas manuais devem ser usadas somente para outras entradas, evitando duplicidade.

## Validação atual

O runtime local foi validado com Python 3.12.14, FastAPI em `http://127.0.0.1:8000` e Streamlit em `http://127.0.0.1:8501`. A suíte local possui 3 testes e todos passaram.

MySQL Community Server 8.4.9 foi instalado e validado em instância local isolada. Docker não é necessário para essa configuração. A senha permanece somente no `.env` ignorado.

## Próximas etapas técnicas

Falta validar o schema e o fluxo ponta a ponta contra um servidor MySQL real e executar uma validação visual em navegador desktop/mobile. Essas etapas dependem do serviço MySQL e de um navegador automatizado ou validação manual.
