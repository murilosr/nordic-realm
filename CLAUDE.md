# CLAUDE.md

Este arquivo fornece orientações ao Claude Code (claude.ai/code) ao trabalhar com o código deste repositório.

## Comandos

```bash
# Rodar a aplicação
python start.py

# Rodar todos os testes
pytest

# Rodar um teste específico
pytest tests/test_auth.py::nome_do_teste

# Lint (imports não utilizados + isort)
ruff check .

# Formatar
ruff format .
```

Os testes exigem um MongoDB em execução. A configuração de conexão vem do `secrets_test.yaml` (copiado de `secrets-template.yaml`). Cada execução de teste cria e destrói seu próprio banco de dados temporário.

## Linguagem

Utilize português para a criação de Modelos/Entidades e suas propriedades (Usuario, Empresa, CNPJ, CPF, etc), porém utilize inglês para o nome de variáveis internas das funções e métodos.


## Arquitetura

**nordic_realm** é um framework personalizado inspirado no Spring, construído sobre o FastAPI. Os diretórios `app/` e `auth_server/` são código da aplicação que consome o framework.

### Injeção de Dependência

As classes são registradas como componentes de DI usando decoradores de `nordic_realm/decorators/controller.py`:

- `@Component()` — injetável genérico
- `@Service()` — camada de serviço
- `@Repository(collection="nome")` — repositório MongoDB, também define `_COLLECTION`
- `@Controller(path="/prefixo")` — controller HTTP, registrado automaticamente como rotas FastAPI
- `@Implement(BaseClass)` — registra uma classe como implementação de uma interface/classe base

`DIScanner().scan("nome_do_pacote")` percorre os arquivos Python de um pacote e registra no `ComponentStore` qualquer classe que tenha `_NR_component = True`. Deve ser chamado na inicialização para cada pacote de nível superior (`auth_server`, `app`).

`DIInjector` resolve dependências inspecionando os `__annotations__` da classe. Campos anotados com um tipo de classe são auto-injetados. Campos anotados com `Annotated[str, Config("chave.caminho")]` são injetados a partir do YAML de configuração.

### Application Context

`ApplicationContext` é um singleton global (via `.set_global()` / `.get()`) que contém:

- `config_store` — lê `config.yaml` + `secrets.yaml` (acesso por caminho com ponto, ex: `"mongodb.db"`)
- `component_store` — componentes de DI registrados
- `singleton_store` — singletons (ex: o `MongoClient`)
- `mongo_conns` — `MongoConnections` indexado por nome
- `fastapi_app` — a instância do FastAPI
- `websocket_conns` — `WebsocketConnectionManager` (baseado em Redis pub/sub)

### Sequência de inicialização (`nordic_realm/launcher.py`)

1. `bootstrap_application_context()` — cria todos os stores e conecta ao MongoDB
2. `DIScanner().scan("auth_server")` e `DIScanner().scan("app")` — registra os componentes
3. `add_controllers(context)` — itera o component store e registra as classes `@Controller` como rotas FastAPI
4. `singleton_store.register(mongo_client)` — torna o `MongoClient` injetável
5. `OAuthSecurityMiddleware.install_middleware(context)` — adiciona o middleware de autenticação JWT
6. `FastAPIExceptionHandler.install_exception_handler(context)` — mapeia exceções para respostas HTTP

### Controllers HTTP

Os métodos de uma classe `@Controller` são decorados com `@Get`, `@Post`, `@Put`, `@Patch`, `@Delete` ou `@WS`. Use `public=True` para que uma rota ignore o middleware de autenticação. As rotas são descobertas e adicionadas ao FastAPI na inicialização por `add_controllers`.

### MongoDB

`MongoBaseModel[ID_TYPE]` (Pydantic) é a base para todos os documentos MongoDB. `MongoRepository[MODEL, ID_TYPE]` é a base genérica para repositórios — as subclasses recebem os métodos CRUD (`save`, `find_by_id`, `get_by_id`, `get_all`, `delete`, `bulk_save`). O `_DB` é lido de `mongodb.db` na configuração, a menos que seja sobrescrito no nível do `@Repository`.

### Autenticação

`auth_server` fornece gerenciamento de sessões via JWT. `OAuthSecurityMiddleware` valida `Authorization: Bearer <token>` em todas as rotas não públicas. O middleware resolve o usuário via `UserRepositoryProvider` (deve ser implementado em `app/`). `PasswordHashProvider` (bcrypt) também é uma interface que `app/` deve implementar.

### Arquivos de configuração

- `config.yaml` — configurações não secretas (logging, etc.)
- `secrets.yaml` — segredos (URI do MongoDB, chave JWT, host do Redis) — ignorado pelo git, copiar de `secrets-template.yaml`
- `secrets_test.yaml` — segredos separados para os testes
