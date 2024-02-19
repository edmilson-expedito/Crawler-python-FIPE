from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import sqlite3

def popCarsResult(result):
    carros = []
    print('B')
    lista_resultado = result.text.split("\n")

    for i in range(1, len(lista_resultado), 1):
        if lista_resultado[i] == 'Marca:':
            fipe = lista_resultado[i-1]
            marca = lista_resultado[i+1]
            modelo = lista_resultado[i+3]
            ano = lista_resultado[i+5]
            preco = lista_resultado[i+11]

            carros.append({
                "Fipe": fipe,
                "Marca": marca,
                "Modelo": modelo,
                "Ano": ano,
                "Preço": preco
            })
    print(carros)
    return carros

def getCars():
    dados_carros = []
    service = Service()
    options = webdriver.FirefoxOptions()

    # Inicialização do webdriver com as opções configuradas
    driver = webdriver.Firefox(service=service, options=options)
    
    driver.get("https://veiculos.fipe.org.br/")

    # Aguardar até que a página seja completamente carregada
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-slug="carro"]')))

    for i in range(2):

        # Clique no tipo de veículo (carro)
        driver.find_element(By.CSS_SELECTOR, '[data-slug="carro"]').click()

        # Selecionar uma marca aleatória
        # Aguardar até que o seletor de marca esteja disponível
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "selectMarcacarro_chosen"))).click()

        # Selecionar uma marca aleatória
        random.choice(WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#selectMarcacarro_chosen ul.chosen-results li')))).click()

        # Selecionar um ano/modelo aleatório
        # Aguardar até que o seletor de ano/modelo esteja disponível
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "selectAnoModelocarro_chosen"))).click()

        # Selecionar um ano/modelo aleatório
        ano_modelo_options = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#selectAnoModelocarro_chosen ul.chosen-results li')))
        random.choice(ano_modelo_options).click()

        # Selecionar um ano aleatório
        # Aguardar até que o seletor de ano esteja disponível
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "selectAnocarro_chosen"))).click()

        # Selecionar um ano aleatório
        ano_options = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#selectAnocarro_chosen ul.chosen-results li')))
        random.choice(ano_options).click()
        
        # Clicar em pesquisar
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "buttonPesquisarcarro"))).click()

        # Aguardar até que o resultado da consulta seja carregado
        result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "resultadoConsultacarroFiltros")))

        # Extrair e adicionar os dados dos carros à lista
        dados_carros.extend(popCarsResult(result))

        # Limpar a seleção atual para realizar uma nova pesquisa
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "buttonLimparPesquisarcarro"))).click()

        driver.refresh()

        time.sleep(5)

    driver.quit()  # Fechar o navegador completamente

    return dados_carros

def saveDB(dados_carros):
    # Conectar-se ao banco de dados SQLite (criará um novo banco de dados se não existir)
    conn = sqlite3.connect('dados_carros.db')

    # Criar um cursor
    cursor = conn.cursor()

    # Criar a tabela se ainda não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS carros (
            Fipe TEXT,
            Marca TEXT,
            Modelo TEXT,
            Ano TEXT,
            Preço TEXT
        )
    ''')

    # Inserir os dados dos carros na tabela
    for carro in dados_carros:
        cursor.execute('''
            INSERT INTO carros (Fipe, Marca, Modelo, Ano, Preço)
            VALUES (?, ?, ?, ?, ?)
        ''', (carro['Fipe'], carro['Marca'], carro['Modelo'], carro['Ano'], carro['Preço']))

    # Commit para salvar as mudanças
    conn.commit()

    # Fechar a conexão
    conn.close()
    print("save OK!")


dados_carros = getCars()
saveDB(dados_carros)
print(dados_carros)
