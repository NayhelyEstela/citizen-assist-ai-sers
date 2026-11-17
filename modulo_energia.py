"""Opção 4 do menu: Transporte e energia.

Este arquivo cuida só da CONVERSA com o usuário: faz as perguntas,
valida as respostas e mostra os resultados.
As contas ficam em calculos_energia.py e os números em data/energia_dados.json.

Como o fluxo funciona (em ordem):
    1. Trajeto  : "Ainda não sei" (cenários estimados) ou "Já sei" (usuário informa)
    2. Tipo     : transporte público ou transporte próprio
    3. Opção    : ex.: ônibus a diesel, metrô, veículo a gasolina...
    4. Resultado, comparação, recomendação e avisos (1ª camada, sem as fontes)
    5. Pergunta: "quer ver as fontes dos dados?" (2ª camada, sob pedido)
    6. Se escolheu elétrico + solar: oferta de dimensionamento simples
    7. Extra    : "quer ver como ficaria no outro tipo de transporte?"

Em qualquer pergunta, digitar 0 volta ao menu principal.
"""

import json
import math
import os

import calculos_energia as calc

PASTA = os.path.dirname(os.path.abspath(__file__))
CAMINHO_DADOS = os.path.join(PASTA, "data", "energia_dados.json")

# ----------------------------------------------------------------------
# Limites da validação (valores de IDA; se o usuário informar ida e volta,
# os limites são multiplicados por 2)
# ----------------------------------------------------------------------
KM_IDA_MAXIMO = 150    # acima disso: recusamos o valor
KM_IDA_AVISO = 50      # acima disso: aceitamos, mas avisamos
DIAS_MAXIMO = 7        # uma semana tem 7 dias
DIAS_AVISO = 5         # 6 ou 7 dias por semana: aceitamos, mas avisamos

# ----------------------------------------------------------------------
# Nomes e listas de opções
# ----------------------------------------------------------------------
OPCOES_PUBLICO = ["onibus_diesel", "onibus_eletrico", "metro"]
OPCOES_PROPRIO = ["gasolina", "eletrico_rede", "eletrico_solar"]

NOMES = {
    "onibus_diesel": "Ônibus a diesel",
    "onibus_eletrico": "Ônibus elétrico",
    "metro": "Metrô",
    "gasolina": "Veículo a gasolina",
    "eletrico_rede": "Veículo elétrico (carregado pela rede)",
    "eletrico_solar": "Veículo elétrico + painéis solares",
}

def nome_na_tela(opcao):
    """Nome da opção para mostrar ao usuário (a solar leva o aviso de estimado)."""
    if opcao == "eletrico_solar":
        return NOMES[opcao] + " (ESTIMADO)"
    return NOMES[opcao]


# Cenários do modo "Ainda não sei meu trajeto": (nome, chave no JSON)
CENARIOS = [
    ("curto", "trajeto_curto_ida"),
    ("médio", "trajeto_medio_ida"),
    ("longo", "trajeto_longo_ida"),
]

# Qual dado de tarifa usar: CHAVE_TARIFA[tipo de tarifa][ônibus ou metrô]
CHAVE_TARIFA = {
    "comum": {"onibus": "tarifa_onibus_sptrans",
              "metro": "tarifa_metro_cptm"},
    "estudantil": {"onibus": "tarifa_onibus_estudante_sp",
                   "metro": "tarifa_metro_estudante_sp"},
}

AVISO_GERAL = ("Aviso: são ESTIMATIVAS para orientação (preços e tarifas de\n"
               "São Paulo, capital). Mudam com o tempo e não são garantia de\n"
               "economia nem de geração.")

# Todos os dados que este módulo lê do JSON (conferidos ao carregar)
DADOS_NECESSARIOS = [
    "dias_uteis_mes", "semanas_por_mes", "viagens_por_dia",
    "trajeto_curto_ida", "trajeto_medio_ida", "trajeto_longo_ida",
    "lotacao_media_onibus", "fator_uso_real_veiculo",
    "preco_gasolina_c_sp", "pci_gasolina_c_kwh_l", "pci_diesel_kwh_l",
    "consumo_carro_gasolina_urbano_pbev",
    "consumo_carro_eletrico_pbev_kwh_km",
    "tarifa_energia_com_tributos", "bandeira_tarifaria_novembro_2026",
    "participacao_renovavel_matriz_eletrica", "fator_emissao_rede_eletrica",
    "fator_emissao_gasolina_c_fossil", "fator_emissao_diesel",
    "tarifa_onibus_sptrans", "tarifa_metro_cptm",
    "tarifa_onibus_estudante_sp", "tarifa_metro_estudante_sp",
    "onibus_diesel_consumo_l_km", "onibus_eletrico_energia_kwh_km",
    "metro_energia_kwh_por_passageiro_km",
    "horas_sol_pleno_sao_paulo", "desempenho_sistema_solar",
    "custo_sistema_solar_2kwp", "custo_sistema_solar_4kwp",
    "potencia_minima_sistema_solar", "vida_util_sistema_solar",
    "fracao_tarifa_compensada_scee", "consumo_medio_residencial_kwh_mes"
]

# Dados usados no custo dos painéis (comparação) e no dimensionamento solar
CHAVES_PAINEIS = [
    "horas_sol_pleno_sao_paulo", "desempenho_sistema_solar",
    "custo_sistema_solar_2kwp", "custo_sistema_solar_4kwp",
    "potencia_minima_sistema_solar", "vida_util_sistema_solar",
]
CHAVES_DIMENSIONAMENTO = CHAVES_PAINEIS + [
    "tarifa_energia_com_tributos", "bandeira_tarifaria_novembro_2026",
    "fracao_tarifa_compensada_scee", "consumo_medio_residencial_kwh_mes",
]

class VoltarAoMenu(Exception):
    """Sinal de que o usuário digitou 0 e quer sair do fluxo de energia.

    Usamos uma exceção para não precisar testar "o usuário digitou 0?"
    depois de CADA pergunta. Quem trata isso é a função executar().
    """


# ----------------------------------------------------------------------
# 1. Carregar os dados
# ----------------------------------------------------------------------
def carregar_dados(caminho=CAMINHO_DADOS):
    """Lê o energia_dados.json. Devolve o dicionário de dados, ou None se falhar."""
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)["dados"]
    except FileNotFoundError:
        print("Não encontrei o arquivo data/energia_dados.json.")
        return None
    except (ValueError, KeyError, TypeError, OSError):
        print("O arquivo data/energia_dados.json está ilegível "
              "ou fora do formato esperado.")
        return None

    if not isinstance(dados, dict):
        print("O arquivo data/energia_dados.json está fora do formato esperado.")
        return None

    # Confere se todos os dados que vamos usar existem
    faltando = []
    for nome in DADOS_NECESSARIOS:
        item = dados.get(nome)
        if not isinstance(item, dict) or "valor" not in item:
            faltando.append(nome)
    if faltando:
        print("Faltam dados em energia_dados.json: " + ", ".join(faltando))
        return None
    return dados


def dado(dados, nome):
    """Atalho: devolve só o VALOR de um dado (ex.: dado(dados, 'dias_uteis_mes') -> 22)."""
    return dados[nome]["valor"]


def tarifa_eletricidade(dados):
    """Preço do kWh em casa (R$/kWh): tarifa com tributos + bandeira do mês."""
    return (dado(dados, "tarifa_energia_com_tributos")
            + dado(dados, "bandeira_tarifaria_novembro_2026"))


# ----------------------------------------------------------------------
# 2. Formatação dos números para a tela (padrão brasileiro: 1.234,56)
# ----------------------------------------------------------------------
def numero(valor, casas=1):
    """Formata um número com vírgula decimal e ponto de milhar."""
    texto = f"{valor:,.{casas}f}"       # o Python escreve assim: 1,234.56
    texto = texto.replace(",", "#")     # troca temporária para não misturar
    texto = texto.replace(".", ",")
    return texto.replace("#", ".")      # resultado: 1.234,56


def reais(valor):
    return "R$ " + numero(valor, 2)


def valor_simples(valor):
    """Mostra um valor do JSON como está, só trocando o ponto pela vírgula."""
    return str(valor).replace(".", ",")


# ----------------------------------------------------------------------
# 3. Leitura e validação das respostas
# ----------------------------------------------------------------------
def ler_escolha(assistente, texto, maximo):
    """Pede uma opção de 1 a 'maximo'. Se digitar 0, volta ao menu principal.

    Reaproveita o ler_opcao do assistente, que já repete a pergunta
    até a pessoa digitar um número válido.
    """
    opcao = assistente.ler_opcao(texto, maximo)
    if opcao == 0:
        raise VoltarAoMenu()
    return opcao


def ler_numero(texto, maximo, aviso_acima, unidade, inteiro=False):
    """Pede um número POSITIVO e repete até a resposta ser válida.

    Regras:
      - precisa ser número (aceita vírgula: 12,5);
      - precisa ser maior que 0;
      - acima de 'maximo': recusa;
      - acima de 'aviso_acima': aceita só se a pessoa confirmar;
      - se inteiro=True, não aceita casas decimais;
      - digitar 0 volta ao menu principal.
    """
    while True:
        resposta = input(texto).strip().replace(",", ".")

        if resposta == "0":
            raise VoltarAoMenu()

        try:
            valor = float(resposta)
        except ValueError:
            print("Valor inválido. Digite apenas números (ex.: 12,5).")
            continue

        if not math.isfinite(valor):
            print("Valor inválido. Digite apenas números (ex.: 12,5).")
            continue
        if valor <= 0:
            print("O valor precisa ser maior que zero.")
            continue
        if inteiro and valor != int(valor):
            print("Digite um número inteiro (ex.: 5).")
            continue
        if valor > maximo:
            print(f"Valor muito alto. O máximo aceito é {numero(maximo, 0)} {unidade}.")
            continue

        if valor > aviso_acima:
            print(f"Atenção: {numero(valor, 0 if inteiro else 1)} {unidade} "
                  "é um valor fora do comum.")
            if not _confirmar("Quer usar esse valor mesmo assim? (s/n): "):
                continue

        return int(valor) if inteiro else valor


def _confirmar(texto):
    """Pergunta s/n (usada só dentro de ler_numero, que não recebe o assistente)."""
    while True:
        resposta = input(texto).strip().lower()
        if resposta in ("s", "n"):
            return resposta == "s"
        print("Resposta inválida. Digite s ou n.")


def mostrar_menu(titulo, textos):
    """Imprime um menu numerado a partir de 1, mais a opção 0."""
    print(f"\n{titulo}")
    for numero_opcao, texto in enumerate(textos, 1):
        print(f"{numero_opcao}. {texto}")
    print("0. Voltar ao menu principal")


# ----------------------------------------------------------------------
# 4. Perguntas sobre o trajeto
# ----------------------------------------------------------------------
def perguntar_viagem(assistente, dados):
    """Descobre o trajeto do mês. Devolve um dicionário com os números."""
    mostrar_menu("Como você quer informar o trajeto?", [
        "Ainda não sei meu trajeto (usar cenários estimados)",
        "Já sei meu trajeto (informar distância e dias)",
    ])
    modo = ler_escolha(assistente, "Escolha uma opção: ", 2)
    if modo == 1:
        return viagem_estimada(assistente, dados)
    return viagem_informada(assistente, dados)


def viagem_estimada(assistente, dados):
    """Modo 'Ainda não sei': o usuário escolhe um cenário curto, médio ou longo."""
    textos = []
    for nome, chave in CENARIOS:
        km = numero(dado(dados, chave), 0)
        textos.append(f"Trajeto {nome} ({km} km só de ida)")
    mostrar_menu("Qual cenário se parece mais com o seu?", textos)
    escolha = ler_escolha(assistente, "Escolha um cenário: ", len(CENARIOS))

    chave = CENARIOS[escolha - 1][1]
    km_ida = dado(dados, chave)

    # 22 dias úteis por mês ÷ 4,4 semanas = 5 dias por semana
    semanas = dado(dados, "semanas_por_mes")
    dias_por_semana = round(dado(dados, "dias_uteis_mes") / semanas, 2)
    viagens = calc.viagens_no_mes(dias_por_semana, semanas,
                                  dado(dados, "viagens_por_dia"))
    return montar_viagem(km_ida, viagens, "ESTIMADO", dias_por_semana)


def viagem_informada(assistente, dados):
    """Modo 'Já sei meu trajeto': o usuário informa distância e dias por semana."""
    # Pergunta se o valor é só de ida ou de ida e volta, para não errar o dobro
    mostrar_menu("A distância que você vai informar é:", [
        "Só a IDA (de casa até o trabalho)",
        "IDA E VOLTA (o trajeto completo de um dia)",
    ])
    sentido = ler_escolha(assistente, "Escolha uma opção: ", 2)
    fator = 1 if sentido == 1 else 2     # ida e volta = 2x a distância de ida

    print("\n(Não precisa informar endereço: só a distância e os dias.)")
    distancia = ler_numero(
        "Qual a distância em km? (0 para voltar): ",
        maximo=KM_IDA_MAXIMO * fator,
        aviso_acima=KM_IDA_AVISO * fator,
        unidade="km")
    km_ida = distancia / fator

    dias = ler_numero(
        "Quantos dias por semana você vai ao trabalho? (1 a 7, 0 para voltar): ",
        maximo=DIAS_MAXIMO,
        aviso_acima=DIAS_AVISO,
        unidade="dias por semana",
        inteiro=True)

    viagens = calc.viagens_no_mes(dias, dado(dados, "semanas_por_mes"),
                                  dado(dados, "viagens_por_dia"))
    return montar_viagem(km_ida, viagens, "INFORMADO PELO USUÁRIO", dias)


def montar_viagem(km_ida, viagens_mes, origem, dias_semana):
    """Junta os números do trajeto em um dicionário (usado por todas as contas)."""
    return {
        "km_por_viagem": km_ida,
        "viagens_mes": viagens_mes,
        "km_mes": calc.km_no_mes(km_ida, viagens_mes),
        "origem": origem,    # "ESTIMADO" ou "INFORMADO PELO USUÁRIO"
        "dias_semana": dias_semana,
    }


# ----------------------------------------------------------------------
# 5. Perguntas sobre o tipo de transporte
# ----------------------------------------------------------------------
def perguntar_tipo(assistente):
    """Devolve 'publico' ou 'proprio'."""
    mostrar_menu("Qual tipo de transporte você quer analisar?", [
        "Transporte público (ônibus a diesel, ônibus elétrico, metrô)",
        "Transporte próprio (gasolina, elétrico, elétrico + painéis solares)",
    ])
    escolha = ler_escolha(assistente, "Escolha uma opção: ", 2)
    return "publico" if escolha == 1 else "proprio"


def perguntar_tarifa(assistente):
    """Devolve 'comum' ou 'estudantil'."""
    mostrar_menu("Qual tarifa você utiliza?", [
        "Tarifa comum",
        "Tarifa estudantil (se tiver direito ao benefício)",
    ])
    escolha = ler_escolha(assistente, "Escolha uma opção: ", 2)
    return "comum" if escolha == 1 else "estudantil"


def perguntar_opcao(assistente, opcoes):
    """Mostra as opções do tipo escolhido e devolve a chave da escolhida."""
    textos = [nome_na_tela(opcao) for opcao in opcoes]
    mostrar_menu("Qual opção você quer ver?", textos)
    escolha = ler_escolha(assistente, "Escolha uma opção: ", len(opcoes))
    return opcoes[escolha - 1]


# ----------------------------------------------------------------------
# 6. Cálculo de uma opção (chama as funções do calculos_energia.py)
# ----------------------------------------------------------------------
def chave_da_tarifa(opcao, tipo_tarifa):
    """Qual dado do JSON tem a tarifa dessa opção (ônibus ou metrô)."""
    veiculo = "metro" if opcao == "metro" else "onibus"
    return CHAVE_TARIFA[tipo_tarifa][veiculo]


def calcular_opcao(opcao, viagem, dados, tipo_tarifa):
    """Calcula energia (kWh), custo (R$) e CO2 (kg) de UMA opção no mês."""
    km_mes = viagem["km_mes"]
    viagens_mes = viagem["viagens_mes"]
    fator_uso = dado(dados, "fator_uso_real_veiculo")

    if opcao == "gasolina":
        litros_km = calc.litros_por_km_real(
            dado(dados, "consumo_carro_gasolina_urbano_pbev"), fator_uso)
        return calc.calcular_gasolina(
            km_mes, litros_km,
            dado(dados, "preco_gasolina_c_sp"),
            dado(dados, "pci_gasolina_c_kwh_l"),
            dado(dados, "fator_emissao_gasolina_c_fossil"))

    if opcao in ("eletrico_rede", "eletrico_solar"):
        kwh_km = calc.kwh_por_km_real(
            dado(dados, "consumo_carro_eletrico_pbev_kwh_km"), fator_uso)
        if opcao == "eletrico_rede":
            return calc.calcular_eletrico_rede(
                km_mes, kwh_km, tarifa_eletricidade(dados),
                dado(dados, "fator_emissao_rede_eletrica"))
        kwh_mes_carro = km_mes * kwh_km
        kwh_por_kwp = calc.geracao_mensal_por_kwp(
            dado(dados, "horas_sol_pleno_sao_paulo"),
            dado(dados, "desempenho_sistema_solar"))
        paineis = calc.custo_paineis_do_carro(
            kwh_mes_carro, kwh_por_kwp,
            dado(dados, "potencia_minima_sistema_solar"),
            dado(dados, "custo_sistema_solar_2kwp"),
            dado(dados, "custo_sistema_solar_4kwp"),
            dado(dados, "vida_util_sistema_solar"))
        return calc.calcular_eletrico_solar(km_mes, kwh_km, paineis)

    # A partir daqui são as opções de transporte público (pagam tarifa)
    tarifa = dado(dados, chave_da_tarifa(opcao, tipo_tarifa))
    lotacao = dado(dados, "lotacao_media_onibus")

    if opcao == "onibus_diesel":
        return calc.calcular_onibus_diesel(
            km_mes, viagens_mes, tarifa,
            dado(dados, "onibus_diesel_consumo_l_km"), lotacao,
            dado(dados, "pci_diesel_kwh_l"),
            dado(dados, "fator_emissao_diesel"))

    if opcao == "onibus_eletrico":
        return calc.calcular_onibus_eletrico(
            km_mes, viagens_mes, tarifa,
            dado(dados, "onibus_eletrico_energia_kwh_km"), lotacao,
            dado(dados, "fator_emissao_rede_eletrica"))

    # opcao == "metro"
    return calc.calcular_metro(
        km_mes, viagens_mes, tarifa,
        dado(dados, "metro_energia_kwh_por_passageiro_km"),
        dado(dados, "fator_emissao_rede_eletrica"))


# ----------------------------------------------------------------------
# 7. Mostrar o resultado
# ----------------------------------------------------------------------
def chaves_das_fontes(opcao, tipo_tarifa):
    """Lista os dados do JSON usados no cálculo da opção (para mostrar as fontes)."""
    if opcao == "gasolina":
        return ["preco_gasolina_c_sp", "consumo_carro_gasolina_urbano_pbev",
                "fator_uso_real_veiculo", "pci_gasolina_c_kwh_l",
                "fator_emissao_gasolina_c_fossil"]
    if opcao == "eletrico_rede":
        return ["consumo_carro_eletrico_pbev_kwh_km", "fator_uso_real_veiculo",
                "tarifa_energia_com_tributos", "bandeira_tarifaria_novembro_2026",
                "fator_emissao_rede_eletrica",
                "participacao_renovavel_matriz_eletrica"]
    if opcao == "eletrico_solar":
        return (["consumo_carro_eletrico_pbev_kwh_km", "fator_uso_real_veiculo"]
                + CHAVES_PAINEIS)

    tarifa = chave_da_tarifa(opcao, tipo_tarifa)
    if opcao == "onibus_diesel":
        return [tarifa, "onibus_diesel_consumo_l_km", "lotacao_media_onibus",
                "pci_diesel_kwh_l", "fator_emissao_diesel"]
    if opcao == "onibus_eletrico":
        return [tarifa, "onibus_eletrico_energia_kwh_km", "lotacao_media_onibus",
                "fator_emissao_rede_eletrica"]
    return [tarifa, "metro_energia_kwh_por_passageiro_km",
            "fator_emissao_rede_eletrica"]


def notas_da_opcao(opcao, dados):
    """Limitações e premissas que o usuário precisa saber sobre a opção."""
    if opcao == "gasolina":
        return ["O consumo real é maior que o do teste de laboratório (Inmetro); "
                "o fator de uso real é ESTIMADO.",
                "O CO2 conta só a parte fóssil da gasolina (o etanol da mistura "
                "é biogênico). Produção e distribuição não entram."]
    if opcao == "eletrico_rede":
        pct = numero(dado(dados, "participacao_renovavel_matriz_eletrica"), 1)
        return [f"O carro só é 'renovável' na proporção da rede: média nacional "
                f"de {pct}%, que não garante que a energia de cada hora seja "
                "renovável.",
                "O custo de compra do veículo NÃO foi considerado."]
    if opcao == "eletrico_solar":
        return ["ESTIMADO: sem conta de eletricidade para carregar o carro; o custo "
                "é só a parcela dos painéis que cabe ao carro, diluída na vida útil "
                "estimada (sem juros nem troca do inversor). CO2 de operação zero.",
                "Emissões de fabricar os painéis e o veículo não entram.",
                "Vale para a casa da família ou para o futuro: o jovem pode "
                "não ter casa própria.",
                "O custo de compra do veículo NÃO foi considerado."]


    if opcao in ("onibus_diesel", "onibus_eletrico"):
        return ["A energia é por passageiro: consumo do ônibus ÷ lotação. "
                "A lotação média é ESTIMADA (premissa do grupo).",
                "Considera uma tarifa por viagem, sem integrações."]
    return ["O dado do metrô já considera a ocupação real do estudo "
            "(não usa a lotação estimada do ônibus).",
            "Considera uma tarifa por viagem, sem integrações."]


def mostrar_fontes(dados, chaves, titulo="Dados usados (tipo e fonte):", inicio=1):
    """Mostra as fontes numeradas. Devolve o próximo número livre (para continuar a lista)."""
    print(f"\n{titulo}")
    numero_item = inicio
    for chave in chaves:
        item = dados[chave]
        linha = (f"  {numero_item}. {item['descricao']} "
                 f"{valor_simples(item['valor'])} {item['unidade']} "
                 f"[{str(item.get('tipo', 'estimado')).upper()}] "
                 f"Fonte: {item.get('fonte', 'não informada')}")
        if item.get("data_consulta"):
            linha += f" (consulta em {item['data_consulta']})"
        print(linha)
        if item.get("link"):
            print(f"     Link: {item['link']}")
        numero_item += 1
    return numero_item


def mostrar_fontes_comparacao(escolhida, opcoes, dados, tipo_tarifa, inicio=1):
    """Fontes dos dados das OUTRAS opções (as da escolhida já foram mostradas)."""
    ja_mostradas = chaves_das_fontes(escolhida, tipo_tarifa)
    novas = []
    for opcao in opcoes:
        if opcao == escolhida:
            continue
        for chave in chaves_das_fontes(opcao, tipo_tarifa):
            if chave not in ja_mostradas and chave not in novas:
                novas.append(chave)
    if novas:
        return mostrar_fontes(
            dados, novas,
            "Dados usados nas outras opções comparadas (tipo e fonte):", inicio)
    return inicio


def mostrar_resultado(opcao, viagem, resultado, dados, tipo_tarifa):
    print(f"\n=== Resultado: {nome_na_tela(opcao)} ===")
    print(f"Trajeto: {numero(viagem['km_por_viagem'])} km por viagem | "
          f"{numero(viagem['viagens_mes'],0)} viagens no mês | "
          f"{numero(viagem['km_mes'])} km no mês [{viagem['origem']}]")
    if tipo_tarifa:
        print(f"Tarifa: {tipo_tarifa}")

    print(f"Energia: {numero(resultado['energia_kwh'])} kWh por mês")
    print(f"Custo:   {reais(resultado['custo_reais'])} por mês")
    print(f"CO2:     {numero(resultado['co2_kg'])} kg por mês")

    # Informações extras de algumas opções
    if opcao == "gasolina":
        print(f"Combustível: {numero(resultado['litros'])} litros por mês")
    if opcao == "eletrico_rede":
        pct = dado(dados, "participacao_renovavel_matriz_eletrica")
        renovavel = calc.parte_renovavel_da_rede(resultado["energia_kwh"], pct)
        print(f"Parte renovável (média da rede): {numero(renovavel)} kWh")
    if opcao == "eletrico_solar":
        p = resultado["paineis"]
        print("\nComo o custo foi calculado: você não paga eletricidade da rede para\n"
              "carregar o carro. O valor acima é só a parcela dos painéis que cabe ao\n"
              f"carro ({numero(p['kwp_necessario'], 2)} kWp = {reais(p['investimento_carro'])}), diluída em {numero(p['meses'] / 12, 0)} anos ({numero(p['meses'], 0)} meses).\n"
              "O CO2 de operação dos painéis é zero.")

    print("\nObservações:")
    for nota in notas_da_opcao(opcao, dados):
        print(f"  - {nota}")

    print(f"\n{AVISO_GERAL}")


def mostrar_fontes_da_analise(opcao, opcoes, dados, tipo_tarifa):
    """2ª camada: lista numerada das fontes (da opção escolhida e das comparadas)."""
    proximo = mostrar_fontes(dados, chaves_das_fontes(opcao, tipo_tarifa))
    mostrar_fontes_comparacao(opcao, opcoes, dados, tipo_tarifa, proximo)


def descrever_diferenca(referencia, alternativa):
    """Texto como '30% menor' comparando a alternativa com a referência."""
    if referencia == 0:
        return "igual" if alternativa == 0 else "maior"
    percentual = calc.diferenca_percentual(referencia, alternativa)
    if abs(percentual) < 0.5:
        return "igual"
    if percentual > 0:
        return f"{numero(percentual, 0)}% menor"
    vezes = alternativa / referencia      # referencia nunca é 0 aqui (já tratado acima)
    if vezes >= 3:                        # a partir de 200% maior
        return f"cerca de {numero(vezes, 0)} vezes o valor"
    return f"{numero(-percentual, 0)}% maior"


def mostrar_comparacao(escolhida, resultados, opcoes):
    """Compara as outras opções do mesmo tipo com a que o usuário escolheu."""
    base = resultados[escolhida]
    print(f"\n=== Comparação com {nome_na_tela(escolhida)} ===")
    for opcao in opcoes:
        if opcao == escolhida:
            continue
        r = resultados[opcao]
        print(f"\n{nome_na_tela(opcao)}:")
        print(f"  Energia: {numero(r['energia_kwh'])} kWh "
              f"({descrever_diferenca(base['energia_kwh'], r['energia_kwh'])})")
        print(f"  Custo:   {reais(r['custo_reais'])} "
              f"({descrever_diferenca(base['custo_reais'], r['custo_reais'])})")
        print(f"  CO2:     {numero(r['co2_kg'])} kg "
              f"({descrever_diferenca(base['co2_kg'], r['co2_kg'])})")

        if opcao == "eletrico_solar":
            print("  Obs.: o custo do solar é só a parcela dos painéis que cabe ao\n"
                  "carro, diluída na vida útil estimada. Você não paga eletricidade da rede para\n"
                  "carregar o carro e o CO2 de operação é zero.")

    if "eletrico_solar" in opcoes and escolhida != "eletrico_solar":
        print("Para ver o investimento e o tempo de retorno, escolha "
              "'Veículo elétrico + painéis solares'.")

# ----------------------------------------------------------------------
# 7B. Recomendação (logo abaixo da comparação)
# ----------------------------------------------------------------------
def formatar_custo(valor):
    return reais(valor)


def formatar_energia(valor):
    return numero(valor) + " kWh"


def formatar_co2(valor):
    return numero(valor) + " kg de CO2"


# Os três critérios usados para recomendar. Para todos, MENOR é melhor.
CRITERIOS = [
    {"chave": "custo_reais", "rotulo": "Menor custo mensal",
     "objetivo": "economizar dinheiro", "reduzir": "o custo",
     "formatar": formatar_custo},
    {"chave": "energia_kwh", "rotulo": "Menor consumo de energia",
     "objetivo": "gastar menos energia", "reduzir": "o consumo de energia",
     "formatar": formatar_energia},
    {"chave": "co2_kg", "rotulo": "Menor emissão de CO2",
     "objetivo": "emitir menos CO2", "reduzir": "as emissões",
     "formatar": formatar_co2},
]


def nomes_juntos(chaves, conector="e"):
    """['metro', 'onibus_eletrico'] -> 'Metrô e Ônibus elétrico' (ou 'ou')."""
    nomes = [NOMES[chave] for chave in chaves]   # sem "(ESTIMADO)": a condição já avisa
    if len(nomes) <= 1:
        return "".join(nomes)
    return ", ".join(nomes[:-1]) + f" {conector} " + nomes[-1]


def montar_recomendacao(resultados, opcoes):
    """Descobre a melhor opção em cada critério. Devolve um dicionário por critério."""
    recomendacao = {}
    for criterio in CRITERIOS:
        chave = criterio["chave"]
        valores = {opcao: resultados[opcao][chave] for opcao in opcoes}
        melhores, parecido = calc.melhores_opcoes(valores)
        recomendacao[chave] = {"melhores": melhores, "parecido": parecido,
                               "valor": min(valores.values())}
    return recomendacao


def texto_melhores(item):
    """Texto curto de um critério, usado no CSV."""
    if item["parecido"]:
        return "praticamente igual"
    return " | ".join(NOMES[opcao] for opcao in item["melhores"])


def mostrar_recomendacao(escolhida, resultados, recomendacao):
    """Mostra a recomendação gerada a partir dos resultados calculados."""
    print("\n=== Recomendação para o seu trajeto (ESTIMADA) ===")

    # 1) Melhor opção em cada critério
    for criterio in CRITERIOS:
        item = recomendacao[criterio["chave"]]
        if item["parecido"]:
            print(f"{criterio['rotulo']}: as opções ficam praticamente iguais "
                  "(diferença menor que 5%).")
        else:
            print(f"{criterio['rotulo']}: {nomes_juntos(item['melhores'])} "
                  f"({criterio['formatar'](item['valor'])})")

    # 2) Síntese: uma frase juntando os critérios em que há diferença relevante
    decisivos = [c for c in CRITERIOS if not recomendacao[c["chave"]]["parecido"]]
    print()
    if not decisivos:
        print("Síntese: as opções ficam parecidas em custo, energia e CO2. "
              "Escolha pelo que for mais prático para você.")
    else:
        # opções que são a melhor (ou empatam como melhor) em TODOS os critérios relevantes
        primeira = recomendacao[decisivos[0]["chave"]]["melhores"]
        em_todos = [op for op in primeira
                    if all(op in recomendacao[c["chave"]]["melhores"] for c in decisivos)]
        if em_todos:
            print(f"Síntese: {nomes_juntos(em_todos)} é a opção mais vantajosa "
                  "em custo de uso, energia e CO₂ de operação com diferença relevante.")
        else:
            partes = [f"para {c['objetivo']}, "
                      f"{nomes_juntos(recomendacao[c['chave']]['melhores'])}"
                      for c in decisivos]
            texto = "; ".join(partes)
            print("Síntese: não há uma opção melhor em tudo. "
                  + texto[0].upper() + texto[1:] + ".")

    # 3) O que mudaria em relação à escolha do usuário
    base = resultados[escolhida]
    for criterio in CRITERIOS:
        item = recomendacao[criterio["chave"]]
        if item["parecido"] or escolhida in item["melhores"]:
            continue
        diferenca = base[criterio["chave"]] - item["valor"]
        print(f"  - Em relação à sua escolha ({NOMES[escolhida]}), trocar por "
              f"{nomes_juntos(item['melhores'], 'ou')} reduziria {criterio['reduzir']} em "
              f"{criterio['formatar'](diferenca)} por mês.")

    # 4) Condições da recomendação
    if any(not recomendacao[c["chave"]]["parecido"]
           and "eletrico_solar" in recomendacao[c["chave"]]["melhores"]
           for c in CRITERIOS):
        print("\nCondição: no carro elétrico + painéis solares, o custo é só a\n"
              "parcela dos painéis atribuída ao carro (diluída na vida útil\n"
              "estimada) e o CO2 de operação é zero por premissa. A compra do\n"
              "veículo, a troca do inversor e as emissões de fabricação NÃO\n"
              "entram nessa comparação.")
    print("\nA recomendação compara só as opções deste tipo de transporte e usa "
          "estimativas: não é garantia de economia.")

# ----------------------------------------------------------------------
# 8. Dimensionamento solar simples
# ----------------------------------------------------------------------
def mostrar_dimensionamento(assistente, dados, energia_kwh_mes):
    """Calcula e mostra o tamanho dos painéis e o tempo de retorno."""
    kwh_por_kwp = calc.geracao_mensal_por_kwp(
        dado(dados, "horas_sol_pleno_sao_paulo"),
        dado(dados, "desempenho_sistema_solar"))
    vida = dado(dados, "vida_util_sistema_solar")

    r = calc.dimensionar_solar(
        energia_kwh_mes, kwh_por_kwp,
        dado(dados, "potencia_minima_sistema_solar"),
        dado(dados, "custo_sistema_solar_2kwp"),
        dado(dados, "custo_sistema_solar_4kwp"),
        tarifa_eletricidade(dados),
        dado(dados, "fracao_tarifa_compensada_scee"),
        dado(dados, "consumo_medio_residencial_kwh_mes"))

    print("\n=== Dimensionamento solar simples (ESTIMADO) ===")
    print(f"Energia do carro por mês: {numero(energia_kwh_mes)} kWh")
    print(f"Painéis necessários: {numero(r['kwp_necessario'], 2)} kWp")
    print(f"Painéis considerados: {numero(r['kwp_instalado'], 2)} kWp "
          f"(mínimo de {numero(dado(dados, 'potencia_minima_sistema_solar'), 0)} kWp)")
    print(f"Geração mensal: {numero(r['geracao_mensal_kwh'])} kWh")
    print(f"Investimento estimado: {reais(r['investimento_reais'])}")
    print(f"Custo mensal do sistema todo, diluído em {numero(vida, 0)} anos: "
          f"{reais(r['investimento_reais'] / (vida * 12))}")
    print(f"Economia mensal estimada na conta de luz (carro + casa): {reais(r['economia_mensal_reais'])}")

    if r["retorno_anos"] is None:
        print("Tempo de retorno: não calculável (sem economia).")
    else:
        print(f"Tempo de retorno: {numero(r['retorno_anos'])} anos "
              f"({numero(r['retorno_meses'], 0)} meses)")
        vida = dado(dados, "vida_util_sistema_solar")
        if r["retorno_anos"] > vida:
            print(f"Atenção: o retorno passa da vida útil estimada "
                  f"({numero(vida, 0)} anos).")

    if r["kwp_instalado"] > r["kwp_necessario"]:
        print("\nObs.: A economia considera o carro e uma casa de consumo\n"
              "médio (160 kWh/mês). A maior parte vem do consumo da casa,\n"
              "não do carro. O consumo real da sua família pode ser diferente")
    if r["acima_da_faixa_de_preco"]:
        print("Atenção: esse porte passa de 4 kWp, faixa sem preço pesquisado. "
              "O investimento pode estar subestimado.")

    print("\nSimplificações: sem sombra, sem bateria, sistema ligado à rede,\n"
          "sem considerar o consumo mínimo cobrado pela distribuidora,\n"
          "troca do inversor não incluída. CO2 de operação dos painéis\n"
          "considerado zero. Vale para a casa da família ou para o futuro.")
    print(AVISO_GERAL)

    if assistente.ler_sim_nao("\nQuer ver as fontes dos dados do "
                              "dimensionamento? (s/n): "):
        mostrar_fontes(dados, CHAVES_DIMENSIONAMENTO)


# ----------------------------------------------------------------------
# 9. Fluxo de um tipo de transporte
# ----------------------------------------------------------------------
def fluxo_tipo(assistente, dados, viagem, tipo):
    """Roda os passos 3 a 6 para 'publico' ou 'proprio'.

    Devolve o nome da opção escolhida (para o registro no histórico).
    """
    if tipo == "publico":
        tipo_tarifa = perguntar_tarifa(assistente)
        opcoes = OPCOES_PUBLICO
    else:
        tipo_tarifa = None          # transporte próprio não paga tarifa
        opcoes = OPCOES_PROPRIO

    escolhida = perguntar_opcao(assistente, opcoes)

    # Calcula TODAS as opções do tipo, porque vamos comparar entre elas
    resultados = {}
    for opcao in opcoes:
        resultados[opcao] = calcular_opcao(opcao, viagem, dados, tipo_tarifa)

    mostrar_resultado(escolhida, viagem, resultados[escolhida], dados, tipo_tarifa)
    mostrar_comparacao(escolhida, resultados, opcoes)
    recomendacao = montar_recomendacao(resultados, opcoes)
    mostrar_recomendacao(escolhida, resultados, recomendacao)

    # Fim da 1ª camada. A 2ª camada (só as fontes numeradas) é sob pedido.
    if assistente.ler_sim_nao("\nQuer ver as fontes dos dados usados? (s/n): "):
        mostrar_fontes_da_analise(escolhida, opcoes, dados, tipo_tarifa)

    if escolhida == "eletrico_solar":
        if assistente.ler_sim_nao("\nQuer um dimensionamento simples dos painéis "
                                  "para mais precisão? (s/n): "):
            mostrar_dimensionamento(assistente, dados,
                                    resultados[escolhida]["energia_kwh"])

    r = resultados[escolhida]
    return {
        "tipo": tipo,
        "opcao": NOMES[escolhida],
        "tipo_tarifa": tipo_tarifa or "",
        "energia_kwh": round(r["energia_kwh"], 2),
        "custo_reais": round(r["custo_reais"], 2),
        "co2_kg": round(r["co2_kg"], 2),
        "menor_custo": texto_melhores(recomendacao["custo_reais"]),
        "menor_energia": texto_melhores(recomendacao["energia_kwh"]),
        "menor_co2": texto_melhores(recomendacao["co2_kg"]),
    }

# ----------------------------------------------------------------------
# 10. Função principal (é a que o assistente.py chama)
# ----------------------------------------------------------------------
def executar(assistente):
    """Roda o fluxo completo da opção 4.

    Devolve um dicionário para o assistente registrar no histórico:
        {"descricao": texto, "ajudou": True/False}
    ou None se o usuário saiu antes de ver algum resultado.
    """
    dados = carregar_dados()
    if dados is None:
        return None

    print("\n=== Transporte e energia ===")
    print("Descubra quanta energia, dinheiro e CO2 o seu deslocamento até o "
          "trabalho gasta em 1 mês.")
    print("Não digite endereço: só pedimos distância e dias.")
    print("Digite 0 em qualquer pergunta para voltar ao menu principal.")

    viagem = None
    analises = []

    try:
        viagem = perguntar_viagem(assistente, dados)

        tipo = perguntar_tipo(assistente)
        analises.append(fluxo_tipo(assistente, dados, viagem, tipo))

        # Extra: mostrar o outro tipo de transporte para o mesmo trajeto
        if tipo == "proprio":
            outro, pergunta = "publico", "transporte público"
        else:
            outro, pergunta = "proprio", "transporte próprio"
        if assistente.ler_sim_nao(f"\nQuer ver como ficaria no {pergunta}? (s/n): "):
            analises.append(fluxo_tipo(assistente, dados, viagem, outro))

    except VoltarAoMenu:
        print("\nVoltando ao menu principal.")

    if not analises:             # saiu antes de ver qualquer resultado
        return None

    ajudou = assistente.ler_sim_nao(
        "\nEssas informações foram úteis para você? (s/n): ")

    registros = []
    for a in analises:
        registros.append({
            "descricao": f"Transporte e energia: {a['opcao']} ({viagem['origem']})",
            "extras": {
                "tipo_transporte": a["tipo"],
                "opcao_escolhida": a["opcao"],
                "origem_trajeto": viagem["origem"],
                "km_ida": round(float(viagem["km_por_viagem"]), 1),
                "dias_semana": int(round(viagem["dias_semana"])),
                "viagens_mes": round(viagem["viagens_mes"], 1),
                "km_mes": round(viagem["km_mes"], 1),
                "tipo_tarifa": a["tipo_tarifa"],
                "energia_kwh_mes": a["energia_kwh"],
                "custo_reais_mes": a["custo_reais"],
                "co2_kg_mes": a["co2_kg"],
                "menor_custo": a["menor_custo"],
                "menor_energia": a["menor_energia"],
                "menor_co2": a["menor_co2"],
            },
        })
    return {"ajudou": ajudou, "registros": registros}