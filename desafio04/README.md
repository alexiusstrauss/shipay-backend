## Ítem 4:

> Você ficou responsável por mentorar um novo membro do time que além de novo na empresa possui o perfil de nível junior. Ele está finalizando o desenvolvimento de um novo microserviço e está com dúvidas quanto a possíveis implementações de "anti-patterns" em seu código e gostaria da sua avaliação... Quantos anti-patterns você consegue identificar no código dele (se é que existe algum), e caso tenha encontrado por qual motivo você categorizou a implementação como sendo um anti-pattern?

# Relatório de Análise de Código

Este documento apresenta os resultados de uma análise detalhada do código no repositório fornecido. Foram encontrados diversos pontos que violam princípios de Clean Code, SOLID e boas práticas de desenvolvimento.

---

## Pontos de Correção e Melhorias

### 1. Anti-pattern encontrado
**Arquivo:** `src/config.py`, linha 4  
```python
class Config:
```
**Motivo:** Classe sem um construtor explícito dificulta o entendimento das dependências.  
**Correção:** Adicione um construtor, mesmo vazio, para melhorar a clareza:  
```python
class Config:
    def __init__(self):
        pass
```

---

### 2. Anti-pattern encontrado
**Arquivo:** `src/endpoints/registration/models.py`, linha 9  
```python
class Customers(Base):
```
**Motivo:** Classe sem um construtor explícito, dificultando a inicialização de valores padrão.  
**Correção:** Inclua um construtor com explicação dos campos principais:  
```python
class Customers(Base):
    def __init__(self, uuid=None):
        self.uuid = uuid or str(uuid.uuid4())
```

---

### 3. Ponto de melhoria
**Arquivo:** `src/endpoints/registration/controllers.py`, linha 12  
```python
async def get_customers(request: Request, orchestrator: Orchestrator = Depends(Provide[Container.registration_service]),):
```
**Motivo:** Ausência de tipagem explícita no retorno.  
**Correção:** Adicione o tipo retornado pela função:  
```python
async def get_customers(request: Request, orchestrator: Orchestrator = Depends(Provide[Container.registration_service]),) -> list:
```

---

### 4. Ponto de melhoria
**Arquivo:** `src/endpoints/registration/controllers.py`, linha 17  
```python
def configure(app: FastAPI):
```
**Motivo:** Ausência de tipagem explícita no retorno.  
**Correção:**  
```python
def configure(app: FastAPI) -> None:
```

---

### 5. Anti-pattern encontrado
**Arquivo:** `src/endpoints/registration/exceptions.py`, linha 1  
```python
class CustomerValidationException(Exception):
```
**Motivo:** Classe sem construtor explícito para mensagens padrão ou códigos de erro.  
**Correção:**  
```python
class CustomerValidationException(Exception):
    def __init__(self, message="Validation failed"):
        super().__init__(message)
```

---

### 6. Anti-pattern encontrado
**Arquivo:** `src/endpoints/registration/repository.py`, linha 8  
```python
class RegistrationRepository(SqlRepository):
```
**Motivo:** Classe sem construtor explícito dificulta a identificação de dependências.  
**Correção:**  
```python
class RegistrationRepository(SqlRepository):
    def __init__(self, session):
        super().__init__(session)
```

---

### 7. Anti-pattern encontrado
**Arquivo:** `src/endpoints/registration/service.py`, linha 11  
```python
customer = await self._repository.filter_by({'id': customer_id})
```
**Motivo:** Repositórios não devem expor estruturas internas do banco. Isso viola o encapsulamento.  
**Correção:** Crie métodos mais descritivos no repositório:  
```python
customer = await self._repository.get_customer_by_id(customer_id)
```

---

### 8. Ponto de erro de implementação
**Arquivo:** `src/config.py`, linha 10  
```python
SQL_POOL_SIZE = getenv('SQL_POOL_SIZE', 5)
```
**Motivo:** O valor padrão de `SQL_POOL_SIZE` deveria ser convertido em inteiro.  
**Correção:**  
```python
SQL_POOL_SIZE = int(getenv('SQL_POOL_SIZE', 5))
```

---

### 9. Anti-pattern encontrado
**Arquivo:** `src/middlewares/tools.py`, linha 6  
```python
def log_request(request):
    print(f"Request received: {request}")
```
**Motivo:** Uso de `print` em produção ao invés de um sistema de log estruturado.  
**Correção:** Substituir por um logger apropriado:  
```python
import logging
logger = logging.getLogger(__name__)

def log_request(request):
    logger.info(f"Request received: {request}")
```

---

### 10. Ponto de erro de implementação
**Arquivo:** `src/middlewares/exception_handler.py`, linha 8  
```python
class ExceptionHandlerMiddleware:
```
**Motivo:** A classe mistura responsabilidades de log e tratamento de exceções, violando o SRP.  
**Correção:** Separe as responsabilidades em classes distintas.  
```python
class ExceptionLogger:
    def log_exception(self, exception: Exception):
        # Lógica de log

class ExceptionHandlerMiddleware:
    def handle_exception(self, exception: Exception):
        # Lógica de tratamento
```

---

### 11. Anti-pattern encontrado
**Arquivo:** `src/endpoints/registration/exceptions.py`, linha 5  
```python
class CustomerNotFoundException(Exception):
    pass
```
**Motivo:** Exceção sem mensagem padrão pode ser confusa.  
**Correção:** Adicione uma mensagem padrão.  
```python
class CustomerNotFoundException(Exception):
    def __init__(self, message="Customer not found."):
        super().__init__(message)
```

---

### 12. Anti-pattern encontrado
**Arquivo:** `src/app.py`, linha 22  
```python
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'])
```
**Motivo:** Configuração de CORS excessivamente permissiva.  
**Correção:** Restringir permissões conforme a necessidade do projeto.  

---

### 13. Anti-pattern encontrado
**Arquivo:** `src/app.py`, linha 13  
```python
from endpoints.health import controllers as health_module
```
**Motivo:** Importação dentro de função principal pode causar problemas de dependência circular.  
**Correção:** Faça as importações no topo do arquivo.  

---

### 14. Anti-pattern encontrado
**Arquivo:** `src/endpoints/health/repository.py`, linha 4  
```python
class HealthSqlRepository(SqlRepository):
```
**Motivo:** Classe sem construtor explícito dificulta a identificação de dependências ou customizações.  
**Correção:**  
```python
class HealthSqlRepository(SqlRepository):
    def __init__(self, session):
        super().__init__(session)
```

---

### 15. Anti-pattern encontrado
**Arquivo:** `src/endpoints/health/controllers.py`, linha 14  
```python
async def get_beat():
```
**Motivo:** Falta de tipagem explícita no retorno.  
**Correção:**  
```python
async def get_beat() -> dict:
```

---

### 16. Ponto de melhoria
**Arquivo:** `src/endpoints/health/controllers.py`, linha 20  
```python
async def get_health(health_service: HealthService = Depends(Provide[Container.health_service]),):
```
**Motivo:** Ausência de tipagem explícita no retorno.  
**Correção:**  
```python
async def get_health(health_service: HealthService = Depends(Provide[Container.health_service]),) -> dict:
```

---

### 17. Anti-pattern encontrado
**Arquivo:** `src/endpoints/health/controllers.py`, linha 28  
```python
def configure(app: FastAPI):
```
**Motivo:** Ausência de tipagem explícita no retorno.  
**Correção:**  
```python
def configure(app: FastAPI) -> None:
```

---

### 18. Ponto de erro de implementação
**Arquivo:** `src/endpoints/registration/models.py`, linha 10  
```python
uuid = Column(String(36), default=lambda x: str(uuid.uuid4()))
```
**Motivo:** O parâmetro `x` no `lambda` é desnecessário e pode causar erro de runtime.  
**Correção:**  
```python
uuid = Column(String(36), default=lambda: str(uuid.uuid4()))
```

---

### 19. Anti-pattern encontrado
**Arquivo:** `src/infrastructure/repositories/sql_repository.py`, linha 15  
```python
def filter_by(self, criteria: dict):
```
**Motivo:** Receber um dicionário como argumento pode dificultar a validação de parâmetros.  
**Correção:** Use argumentos nomeados ou classes para critérios.  

---

### 20. Anti-pattern encontrado
**Arquivo:** `src/middlewares/tools.py`, linha 1  
```python
class Tools(SqlRepository):
```
**Motivo:** O nome `Tools` é genérico e não reflete o propósito da classe, violando o Clean Code e SRP. Além disso, herdar de `SqlRepository` sugere responsabilidades inconsistentes.  
**Correção:** Renomear para um nome mais claro e verificar a necessidade de herança.  
```python
class CustomerRepository(SqlRepository):
    def __init__(self, session):
        super().__init__(session)
```
Ou, se for um utilitário genérico:  
```python
class Tools:
    def __init__(self):
        pass
```

---

Esses pontos abordam problemas de nomenclatura, tipagem, estrutura e responsabilidade, promovendo um código mais claro, manutenível e alinhado aos princípios de Clean Code e SOLID.