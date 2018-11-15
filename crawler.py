import requests
import json
import jsonpickle
import flask
import re
import os
import urllib 
from flask import request, json
from flask import Response
from selenium import webdriver
from decimal import Decimal
from planos import Plano

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/v1/planos', methods=['GET'])
def api_name():
    if 'lines' in request.args:
        lines = request.args['lines']
        gbRequest = float(request.args['gb'])
        priceRequest = request.args['price']

        options = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"))
        options.add_argument("headless")
        driver = webdriver.Chrome(chrome_options=options)
        driver.get('https://melhorplano.net/planos-de-celular/resultado?n={}&c=vivo%2Coi%2Ctim%2Cclaro%2Cnextel&t=controle%2Cpost&i0=&m0=&ps=vivo%2Coi%2Ctim%2Cclaro%2Cnextel&mn=1&p=mobile'.format(lines))
        p_element = driver.find_elements_by_class_name(name='result-card')
        planos = []
        
        for plano in p_element:
            name = plano.find_element_by_class_name(name='carrier-logo').get_attribute('alt')
            desc = plano.find_element_by_class_name(name='single-solution-title').text
            price = float(str(plano.find_element_by_class_name(name='solution-price-value').text).replace(",", "."))
            gb = plano.find_element_by_class_name(name='single-solution-value').text.replace(" Giga", "").replace(",", ".")
            link = 'http://www.' + name.lower() + '.com.br'

            if price <= float(priceRequest) and float(gb) > gbRequest:
                planos.append(Plano(name, desc, price, gb, link))

        driver.quit()
        js = jsonpickle.encode(planos, unpicklable=False)
        return Response(js, status=200, mimetype='application/json')

port = int(os.environ.get("PORT", 80))
app.run(host='0.0.0.0', port=port)