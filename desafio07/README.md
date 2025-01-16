## Ítem 7: Padrões de Projeto para Normalização de Serviços de Terceiros

> Qual ou quais Padrões de Projeto/Design Patterns você utilizaria para normalizar serviços de terceiros (tornar múltiplas interfaces de diferentes fornecedores uniforme), por exemplo serviços de disparos de e-mails, ou então disparos de SMS


# Benefício do Padrão Strategy para Normalização de Serviços de Terceiros

O padrão de projeto **Strategy** é uma escolha ideal para normalizar múltiplos serviços de terceiros que possuem interfaces diferentes. Ele permite encapsular comportamentos em classes separadas, promovendo flexibilidade e escalabilidade. 

## Benefícios do Padrão Strategy

1. **Flexibilidade**: Cada estratégia é implementada numa classe separada, possibilitando alterações ou adições de novas estratégias sem impactar no código existente.
2. **Reduz Complexidade**: O código do cliente que utiliza as estratégias permanece simples, já que não precisa lidar diretamente com as particularidades de cada serviço.
3. **Escalabilidade**: É fácil adicionar novos serviços (como envio de mensagens por Telegram ou Slack) criando novas classes que implementam a interface comum.
4. **Reuso e Testabilidade**: Como cada estratégia é uma classe independente, ela pode ser reutilizada em diferentes contextos e é fácil de testar isoladamente.

## Facilidade em Adicionar Novas Estratégias

A implementação do padrão Strategy organiza o código de forma que, para adicionar um novo tipo de serviço, basta criar uma nova classe concreta que implemente a ‘interface’ comum. Isso elimina a necessidade de modificar o código existente, seguindo o princípio do **Open/Closed Principle**.

Por exemplo, para adicionar um novo serviço como envio de mensagens por **Slack**, basta implementar a interface e configurar no serviço principal.

## Exemplo de Código com o Padrão Strategy

```python
from abc import ABC, abstractmethod

# Interface de Comunicação
class CommunicationStrategy(ABC):
    @abstractmethod
    def send_message(self, message: str):
        pass

# Estratégia de envio por SMS
class SMSCommunication(CommunicationStrategy):
    def send_message(self, message: str):
        print(f"Enviando SMS: {message}")

# Estratégia de envio por E-mail
class EmailCommunication(CommunicationStrategy):
    def send_message(self, message: str):
        print(f"Enviando Email: {message}")

# Estratégia de envio por Slack
class SlackCommunication(CommunicationStrategy):
    def send_message(self, message: str):
        print(f"Enviando mensagem no Slack: {message}")

# Serviço que utiliza a estratégia
class CommunicationService:
    def __init__(self, engine: CommunicationStrategy):
        self.strategy = engine

    def send(self, message: str):
        self.strategy.send_message(message)

# Exemplo de uso
if __name__ == "__main__":
    sms_strategy = SMSCommunication()
    email_strategy = EmailCommunication()
    slack_strategy = SlackCommunication()

    service  = CommunicationService(engine=sms_strategy)
    service.send("Olá, esta é uma mensagem via SMS!")
    
    service  = CommunicationService(engine=email_strategy)
    service.send("Olá, esta é uma mensagem de e-mail!")
    
    service  = CommunicationService(engine=slack_strategy)
    service.send("Olá, esta é uma mensagem via Slack!")


```

### Simplicidade na Manutenção e Leitura
1. Adição de Novos Serviços: Para incluir um novo serviço, basta criar uma classe que implemente a interface CommunicationStrategy.
2. Teste Modular: Cada estratégia pode ser testada de forma isolada, o que facilita a manutenção e a detecção de problemas.
3. 
3. Facilidade de Leitura: O código é intuitivo, separando responsabilidades de forma clara e organizada.

Com o padrão Strategy, é possível criar soluções robustas, escaláveis e fáceis de manter, promovendo boas práticas de engenharia de software.

