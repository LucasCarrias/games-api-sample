# Games Api Sample :video_game:
<br>
API exemplo de caso de estudo do Django Rest Framework.
Esta API foi desenvolvida durante atividades acadêmicas de Programação para internet.

----
### Requisitos
Você precisa do Python 3.8 :snake: ou superior instalado para executar os scripts

### Dependências
Para instalação das depedências você precisa executar o seguinte comando:
```
pipenv install
```
Para ativação do ambiente virtual:
```
pipenv shell
```
---

## Uso da API
Até o momento atual apenas o app de Games foi criado. Um crud básico foi desenvolvido.
<br>
Com o avançar da API os endpoints serão devidamente documentados.

### Regras de negócio
Método | Descrição
|---|---|
**POST, PUT**| Jogos não podem ter nomes repetidos
**DELETE**| Jogos que já foram lançados não podem ser excluídos

Para verificar se o crud e as regras de negócio estão funcionado de acordo você só precisa executar:
```
python manage.py test
```
