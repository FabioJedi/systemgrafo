#SystemGrafo

API para criação e manipulação de redes metabólicas através de grafos.

[![Build Status](https://travis-ci.org/FabioJedi/systemgrafo.svg?branch=master)](https://travis-ci.org/FabioJedi/systemgrafo)

## Como desenvolver?

1. Clone o repositário.
2. Crie um virtualenv com Python 3.7.2
3. Ative o virtualenv.
4. Instale as dependências.
5. Configure a instância com o .env
6. Execute os testes.

'''Console
git clone git@github.com:FabioJedi/systemgrafo.git fiocruz
cd fiocruz
python -m venv .fiocruz
source .wttd/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
'''

## Como fazer o deploy

1. Crie uma instância no Heroku.
2. Envie as configurações para o Heroku.
3. Define uma SECRET_KEY segura para instância.
4. Defina DEBUG=False
5. Configure o serviço de email.
6. Envie o código para o Heroku.

'''Console
heroku create minhainstancia
heroku config:push
heroku config:set SECRET_KEY='python contrib/secret_gen.py'
heroku config:set DEBUG=False
# configure o email
git push heroku master --force
'''