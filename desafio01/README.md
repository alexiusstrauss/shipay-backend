# 🎯 Shipay-desafio


## 📋 Sumário

- [📋 Sumário](#-sumário)
- [📖 Sobre](#-sobre)
- [📦 Como usar esse template?](#-como-usar-esse-template)
- [🛠 Tecnologias utilizadas](#-tecnologias-utilizadas)
- [🗂 Estrutura de pastas](#-estrutura-de-pastas)
- [▶️Executando o projeto](#-executando-o-projeto)
- [⚙ Comnandos extras](#-comandos-extras)
- [🗃 Versionamento](#-versionamento)
- [📚 Estrutura do projeto](#-estrutura-do-projeto)


## 📖 Sobre
Este projeto para resolver o desafio 1 da Shipay: [Desafio 1](https://github.com/shipay-pag/tech-challenges/blob/master/back_end/waimea/challenge.md)

## 🛠 Tecnologias e Padrões utilizados

Para o desenvolvimento deste projeto, as seguintes tecnologias foram usadas:

- **Python 3.12**
- **FastAPI (Rest API)**
- **Uv** (Gerenciador de pacotes python e ambientes virtuais)
- **SQLAlchemy** (ORM)
- **Pydantic** (Validação de dados)
- **Alembic** (Migrations)
- **AioRedis** (Cache Async)
- **Pytest** (Testes)


Esse projeto possui uma estrutura que visa o máximo desacoplamento entre camadas para dar
suporte para criação de componentes que sejam reutilizaveis por todo o domínio. Também possui um CRUD simples com
exemplos de organização de pacotes e testes.

Além de outros, o principal pattern que guia este projeto é o Hexagonal (+ Clean Architecture), em resumo, esse padrão
fornece uma maneira de organizar o código de forma que a lógica de negócio seja encapsulada, mas separada do mecanismo de
entrega. Isso permite uma melhor manutenção e menos dependências.

A estrutura do código segue uma organização de pacote por domínio, ou seja, vamos supor que customer_validation seja um domínio
mapeado na nossa estrutura de domínios, nesse caso, teremos na pasta `src.packages` a pasta `customer_validation` que conterá todo o
código necessário para o tratamento de validacao de `clientes via cnpj e cep` com baixo acoplamento e contexto bem delimitado.

## 🗂 Estrutura de pastas

```bash
alemic/
  migrations/ # Migrations geradas pelo alembic
  scripts/ # Scripts de inicialização do banco de dados
  alembic.ini # Configuração do alembic
/src
  /adapters # Adaptadores globais (inbound ou outbound adapters)
  /database # Caso opte por usar banco de dados, aqui ficam armazenados as migrations, regra de conexão e também os modelos de ORM
  /exceptions # Classes de exceção globais
  /packages # Cada pasta dentro de packages diz respeito a um domínio
    /customer_validation # Dominio consula de cnpj e cep com validcao de dados com apis externas
      /controllers # Ou inbound adapters
      /exceptions # Classes de exceções específicas do domínio
      /ports # Interfaces dos quais nossos adapters e services devem implementar
      /repository # Ou outbound adapters
      /schemas # Entidades do domínio, que podem ou não contem regras de negócio (A critério)
      /services # Camada de casos de uso que podem implementar regras de negócio, ou regras da aplicação
  /ports # Interfaces globais
  /system
    /settings # Configurações globais
    /middlewares # Middlewares globais
    /utils # Funções utilitárias
  /tests
```

## 📊 Cobertura de Testes

A cobertura de testes foi gerada utilizando o plugin `pytest-cov`. Abaixo estão os resultados detalhados:

| Arquivo                                                                                  | Linhas Totais | Linhas Não Cobertas | Cobertura de Linhas | Branches Totais | Branches Não Cobertas | Cobertura de Branches |
|------------------------------------------------------------------------------------------|---------------|----------------------|---------------------|-----------------|------------------------|-----------------------|
| src/packages/customer_validation/adapters/cnpj_service_adapter.py                       | 13            | 8                    | 33.33%              | 2               | 0                      | 100.00%              |
| src/packages/customer_validation/adapters/primary_cep_strategy.py                       | 18            | 9                    | 50.00%              | 0               | 0                      | -                    |
| src/packages/customer_validation/controllers/customer_validation_controller.py          | 20            | 7                    | 54.17%              | 4               | 0                      | 100.00%              |
| src/packages/customer_validation/repositories/customer_validation_repository.py         | 14            | 6                    | 57.14%              | 0               | 0                      | -                    |
| src/packages/customer_validation/services/validation_service.py                         | 49            | 14                   | 69.81%              | 4               | 2                      | 50.00%               |
| src/packages/customer_validation/adapters/fallback_cep_strategy.py                      | 18            | 4                    | 77.78%              | 0               | 0                      | -                    |
| src/packages/customer_validation/ports/cep_strategy_interface.py                        | 9             | 2                    | 77.78%              | 0               | 0                      | -                    |
| src/packages/customer_validation/ports/cnpj_service_interface.py                        | 5             | 1                    | 80.00%              | 0               | 0                      | -                    |
| src/packages/customer_validation/ports/validation_service_interface.py                  | 15            | 3                    | 80.00%              | 0               | 0                      | -                    |
| src/packages/customer_validation/repositories/customer_validation_repository_interface.py | 10            | 2                    | 80.00%              | 0               | 0                      | -                    |
| src/packages/customer_validation/schemas/validation_schemas.py                          | 20            | 2                    | 83.33%              | 4               | 2                      | 50.00%               |
| src/packages/customer_validation/factories/service_factory.py                           | 22            | 2                    | 90.91%              | 0               | 0                      | -                    |
| src/database/models/customer_validation.py                                              | 14            | 1                    | 92.86%              | 0               | 0                      | -                    |
| src/packages/customer_validation/services/cep_service.py                                | 17            | 0                    | 95.24%              | 4               | 1                      | 75.00%               |
| src/packages/customer_validation/repositories/validation_request_repository.py          | 11            | 0                    | 100.00%             | 0               | 0                      | -                    |

**Cobertura Total ✅**: 73.63% (Linhas), 72.22% (Branches)  
**Cobertura Requerida**: 55.00%


---
## Para mais detalhes, execute
```bash
make coverage-html
```


## ▶️ Executando o projeto

### Opção 1 - Via Docker Compose
Se você deseja executar o projeto através do docker-compose, este projeto utiliza esta dockernizado e possui um Makefile com comandos úteis.

#### Execute o docker-compose com ajuda do Makefile no alias

Por fim, execute o projeto e as suas dependências em segundo plano através do comando
```bash
make up-log
```

### Preparando as dependêncas

Para esse projeto, utilizamos o **Uv** como gerenciador de pacotes. A sua escolha foi devida a simplicidade em manipular pacotes
e a sua impresisonante capacidade de resolver problema de dependências.

Após importar o projeto, instale o poetry conforme a documentação https://docs.astral.sh/uv/getting-started/installation/


Você poderá encontrar mais instruções sobre o uv na sua [documentação oficial](https://docs.astral.sh/uv/getting-started/installation/).



### Criando ambiente local rode a sequencia de comandos:
    
```bash
    make setup
    make migrate
    make run-dev
```
### Acesse a documentação da API
```
    http://localhost:8000/docs
```


Com a lib `uv` instalada, execute o comando para criar o ambiente virtual na raiz do seu projeto:
```bash
uv sync
```

ative o ambiente ou configure no Pycharm

```bash
uv shell
```

## ⚙️ Comandos Extras

O projeto possui um arquivo `Makefile` com alguns comandos make que facilitam a preparação de dependências.

Criar uma nova migration:
```bash
make migrate-revision
```

Executar as migrations:
```bash
make migrate-upgrade
```

Levantar todas as dependências:
```bash
make up
```

Executar todos os testes:
```bash
make tests
```

## 📜 Licença

Este projeto está sob uma licença restritiva. Consulte o arquivo [LICENSE](./LICENSE.md) para mais informações.

## Referências

- [Hexagonal Architecture](https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/)
- [Domain Driven Design - DDD](https://lyz-code.github.io/blue-book/architecture/domain_driven_design/)
- [Repository Pattern](https://lyz-code.github.io/blue-book/architecture/repository_pattern/)
- [Service Layer Pattern](https://www.cosmicpython.com/book/chapter_04_service_layer.html)
- [SQL Alchemy](https://docs.sqlalchemy.org/en/14/orm/quickstart.html)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)