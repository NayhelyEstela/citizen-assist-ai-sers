"""Cálculos de energia, custo e CO2 do deslocamento até o trabalho."""

MJ_POR_KWH = 3.6

# Faixa de tamanhos em que temos preço de sistema solar (estudo Greener 2026)
POTENCIA_PRECO_PEQUENA_KWP = 2
POTENCIA_PRECO_GRANDE_KWP = 4

# ----------------------------------------------------------------------
# 1. Viagens e distância do mês
# ----------------------------------------------------------------------
def viagens_no_mes(dias_por_semana, semanas_por_mes, viagens_por_dia):
    """Quantas viagens a pessoa faz em 1 mês.

    Exemplo: 5 dias x 4,4 semanas x 2 viagens = 44 viagens.
    """
    return dias_por_semana * semanas_por_mes * viagens_por_dia


def km_no_mes(km_por_viagem, viagens_mes):
    """Distância total percorrida no mês (km)."""
    return km_por_viagem * viagens_mes


# ----------------------------------------------------------------------
# 2. Conversões de unidade (tudo vira kWh)
# ----------------------------------------------------------------------
def mj_para_kwh(mj):
    """Converte megajoules (MJ) em quilowatts-hora (kWh)."""
    return mj / MJ_POR_KWH


def kwh_do_combustivel(litros, kwh_por_litro):
    return litros * kwh_por_litro


def kwh_por_litro(densidade_kg_l, pci_kcal_kg):
    """Energia de 1 litro de combustível, em kWh."""
    kcal_por_litro = densidade_kg_l * pci_kcal_kg
    kj_por_litro = kcal_por_litro * 4.1868
    return kj_por_litro / 3600


# ----------------------------------------------------------------------
# 3. Consumo real (a vida real gasta mais que o teste de laboratório)
# ----------------------------------------------------------------------
def litros_por_km_real(km_por_litro_laboratorio, fator_uso_real):
    """Consumo real da gasolina, em litros por km.

    O Inmetro mede em laboratório (km/L). Primeiro viramos "litros por km"
    (1 ÷ km/L) e depois dividimos pelo fator (ex.: 0,8), porque no trânsito
    real o carro gasta MAIS: 0,0694 L/km ÷ 0,8 = 0,0868 L/km.
    """
    litros_por_km_lab = 1 / km_por_litro_laboratorio
    return litros_por_km_lab / fator_uso_real


def kwh_por_km_real(kwh_por_km_laboratorio, fator_uso_real):
    """Consumo real do carro elétrico, em kWh por km (mesma ideia acima)."""
    return kwh_por_km_laboratorio / fator_uso_real


# ----------------------------------------------------------------------
# 4. Transporte próprio
# ----------------------------------------------------------------------
def calcular_gasolina(km_mes, litros_por_km, preco_litro,
                      kwh_por_litro_gasolina, co2_kg_por_litro):

    litros = km_mes * litros_por_km
    return {
        "energia_kwh": kwh_do_combustivel(litros, kwh_por_litro_gasolina),
        "custo_reais": litros * preco_litro,
        "co2_kg": litros * co2_kg_por_litro,
        "litros": litros,   # número extra, útil para mostrar na tela
    }


def calcular_eletrico_rede(km_mes, kwh_por_km, tarifa_kwh, co2_kg_por_kwh):
    """Carro elétrico carregado na tomada de casa (energia da rede)."""
    energia = km_mes * kwh_por_km
    return {
        "energia_kwh": energia,
        "custo_reais": energia * tarifa_kwh,
        "co2_kg": energia * co2_kg_por_kwh,
    }


def parte_renovavel_da_rede(energia_kwh, percentual_renovavel):
    return energia_kwh * percentual_renovavel / 100


def calcular_eletrico_solar(km_mes, kwh_por_km):
    """Carro elétrico carregado com painéis solares em casa.

    A energia é a mesma do elétrico na rede. A diferença é a origem:
    a energia vem do sol, então o custo mensal de eletricidade para o carro
    é R$ 0 e o CO2 de operação é 0 (o custo dos painéis aparece à parte,
    em dimensionar_solar). Não contamos emissões de fabricar os painéis.
    """
    return {
        "energia_kwh": km_mes * kwh_por_km,
        "custo_reais": 0.0,
        "co2_kg": 0.0,
    }


# ----------------------------------------------------------------------
# 5. Transporte público (funções diferentes: a pessoa paga TARIFA)
# ----------------------------------------------------------------------
def custo_transporte_publico(tarifa_viagem, viagens_mes):
    return tarifa_viagem * viagens_mes


def calcular_onibus_diesel(km_mes, viagens_mes, tarifa_viagem, litros_por_km,
                           lotacao, kwh_por_litro_diesel, co2_kg_por_litro):
    """Ônibus a diesel.

    O ônibus gasta combustível por km rodado, mas a energia é dividida
    entre os passageiros. Por isso: litros por passageiro = litros ÷ lotação.
    A lotação é uma ESTIMATIVA do grupo.
    """
    litros_do_onibus = km_mes * litros_por_km
    litros_por_passageiro = litros_do_onibus / lotacao
    return {
        "energia_kwh": kwh_do_combustivel(litros_por_passageiro,
                                          kwh_por_litro_diesel),
        "custo_reais": custo_transporte_publico(tarifa_viagem, viagens_mes),
        "co2_kg": litros_por_passageiro * co2_kg_por_litro,
    }


def calcular_onibus_eletrico(km_mes, viagens_mes, tarifa_viagem,
                             kwh_por_km_onibus, lotacao, co2_kg_por_kwh):
    """Ônibus elétrico: mesma ideia do diesel, mas o consumo já é em kWh."""
    kwh_do_onibus = km_mes * kwh_por_km_onibus
    kwh_por_passageiro = kwh_do_onibus / lotacao
    return {
        "energia_kwh": kwh_por_passageiro,
        "custo_reais": custo_transporte_publico(tarifa_viagem, viagens_mes),
        "co2_kg": kwh_por_passageiro * co2_kg_por_kwh,
    }


def calcular_metro(km_mes, viagens_mes, tarifa_viagem,
                   kwh_por_passageiro_km, co2_kg_por_kwh):
    """Metrô: o dado já vem "por passageiro e por km", sem usar lotação."""
    energia = km_mes * kwh_por_passageiro_km
    return {
        "energia_kwh": energia,
        "custo_reais": custo_transporte_publico(tarifa_viagem, viagens_mes),
        "co2_kg": energia * co2_kg_por_kwh,
    }


# ----------------------------------------------------------------------
# 6. Solar (dimensionamento simples: sem sombra e sem bateria)
# ----------------------------------------------------------------------
def geracao_mensal_por_kwp(horas_sol_pleno, desempenho, dias_no_mes=30):
    """Quantos kWh 1 kWp de painéis gera em 1 mês."""
    return horas_sol_pleno * dias_no_mes * desempenho


def preco_por_wp_solar(kwp, preco_2kwp, preco_4kwp):
    """Preço do sistema em R$ por Wp, conforme o tamanho.

    Sistemas menores custam mais por Wp. Para tamanhos entre 2 e 4 kWp
    fazemos uma média proporcional (interpolação linear). Abaixo de 2 kWp
    usamos o preço de 2 kWp; acima de 4 kWp usamos o de 4 kWp.
    """
    if kwp <= POTENCIA_PRECO_PEQUENA_KWP:
        return preco_2kwp
    if kwp >= POTENCIA_PRECO_GRANDE_KWP:
        return preco_4kwp
    faixa = POTENCIA_PRECO_GRANDE_KWP - POTENCIA_PRECO_PEQUENA_KWP
    avanco = (kwp - POTENCIA_PRECO_PEQUENA_KWP) / faixa   # vai de 0 a 1
    return preco_2kwp + (preco_4kwp - preco_2kwp) * avanco


def dimensionar_solar(kwh_mes_carro, kwh_por_kwp_mes, potencia_minima_kwp,
                      preco_2kwp, preco_4kwp, tarifa_kwh, fracao_compensada):
    """Dimensiona os painéis para carregar o carro e calcula o retorno."""
    kwp_necessario = kwh_mes_carro / kwh_por_kwp_mes
    kwp_instalado = max(kwp_necessario, potencia_minima_kwp)

    preco_wp = preco_por_wp_solar(kwp_instalado, preco_2kwp, preco_4kwp)
    investimento = kwp_instalado * 1000 * preco_wp

    economia_mensal = kwh_mes_carro * tarifa_kwh * fracao_compensada

    if economia_mensal > 0:
        retorno_meses = investimento / economia_mensal
    else:
        retorno_meses = None   # sem economia, não existe retorno

    return {
        "kwp_necessario": kwp_necessario,
        "kwp_instalado": kwp_instalado,
        "geracao_mensal_kwh": kwp_instalado * kwh_por_kwp_mes,
        "investimento_reais": investimento,
        "economia_mensal_reais": economia_mensal,
        "retorno_meses": retorno_meses,
        "retorno_anos": None if retorno_meses is None else retorno_meses / 12,
        # True quando passa de 4 kWp: não temos preço para esse porte
        "acima_da_faixa_de_preco": kwp_instalado > POTENCIA_PRECO_GRANDE_KWP,
    }


# ----------------------------------------------------------------------
# 7. Comparação entre duas alternativas
# ----------------------------------------------------------------------
def diferenca_percentual(valor_referencia, valor_alternativa):
    """Quanto a alternativa é menor (+) ou maior (-) que a referência, em %."""
    if valor_referencia == 0:
        return 0.0
    return (valor_referencia - valor_alternativa) / valor_referencia * 100