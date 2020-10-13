# API Azul e Rosa Personalizados

> Desenvolvimento de API para mostruário on-line de produtos da **Azul e Rosa Personalizados**. 
Será utitlizando o framework [Flask RESTX](https://github.com/python-restx/flask-restx), banco de dados [PostgreSQL](https://www.postgresql.org/) e [Docker](https://www.docker.com/).

![Badge](https://img.shields.io/static/v1?label=Python&message=3.8&color=green&style=flat&logo=PYTHON) ![Badge](https://img.shields.io/static/v1?label=Flask&message=1.1.2&color=blue&style=flat&logo=Flask) ![Badge](https://img.shields.io/github/license/andrersp/azulerosa)

> Status do Projeto e Documentação: Em desenvolvimento :warning:

O Projeto consiste em **3 etapas**:
- Desenvolvimento da API
- [Desenvolvimento de Software Desktop utilizando](https://github.com/andrersp/azulerosadesktop) [QT](https://www.qt.io/)
- Desenvolvimento de Página Web utilizazndo [Flask](https://flask.palletsprojects.com/en/1.1.x/)

# Features
### Gerenciamento
- [x] Cadastro de produtos
- [x] Cadastro de categorias de produtos
- [x] Cadastro de fornecedores
- [x] Cadastro de clientes
- [ ] Compras
- [ ] Vendas
- [ ] Controle de estoque
- [ ] Contas a pagar
- [ ] Contas a receber
- [ ] Relatório de Venda
- [ ] Relatorio de Compra
- [ ] Integração com meios de pagamento

### Consumo
- [ ] Cadastro Cliente
- [ ] Meios de pagamento
- [ ] Carrinho de compras



## Deploy
Desenvolvimento:
```sh
git clone https://github.com/andrersp/azulerosa
cd azulerosa
sudo docker-compose up -d --build

```
Produção:
```sh
git clone https://github.com/andrersp/azulerosa
cd azulerosa
sudo docker-compose -f docker-compose.prod.yml up -d --build

```

### Maintainers:
* André França                rsp.assistencia@gmail.com

### Contributing

1. Faça o _fork_ do projeto (<https://github.com/yourname/yourproject/fork>)
2. Crie uma _branch_ para sua modificação (`git checkout -b feature/fooBar`)
3. Faça o _commit_ (`git commit -am 'Add some fooBar'`)
4. _Push_ (`git push origin feature/fooBar`)
5. Crie um novo _Pull Request_



