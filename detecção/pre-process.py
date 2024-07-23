import pandas as pd
import subprocess
import numpy as np
import itertools
import time
import datetime
from tqdm import tqdm
import sys
import os
import subprocess
from collections import Counter

def run_tshark(command):
    """Executa um comando tshark e retorna a saída."""
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"Erro ao executar comando tshark: {result.stderr}")
    return result.stdout

def find_gateway(pcap_file):
    print("Procurando pelo gateway na rede...")
    command = ["tshark", "-r", pcap_file, "-Y", "arp.opcode==2", "-T", "fields", "-e", "arp.src.proto_ipv4"]
    output = run_tshark(command)
    
    ip_counter = Counter(output.splitlines())
    most_common_ip, _ = ip_counter.most_common(1)[0]  # Pega o IP mais comum
    print(f"Gateway encontrado: {most_common_ip}")
    return [most_common_ip]


def timeSeries(pcap_path, nome_do_arquivo, ipGateway, indicador):

    # Comandos tshark para extrair informações do arquivo PCAP
    tshark_cmd = [
        'tshark',
        '-r', pcap_path,
        '-T', 'fields',
        '-e', 'eth.src',
        '-e', 'eth.dst',
        '-e', 'frame.time_relative',
        '-e', 'frame.len',
        '-e', 'ip.src',
        '-e', 'ip.dst',
        '-e', 'tcp.dstport',
        '-e', 'udp.dstport',
        '-Y', "(tcp or udp)"
    ]
    print(tshark_cmd)
    # Executar o tshark e capturar a saída
    try:
        result = subprocess.run(tshark_cmd, stdout=subprocess.PIPE, text=True)
        output = result.stdout

    except subprocess.CalledProcessError as e:
        print("Erro ao executar o tshark:", e.stderr)
        exit(1)

    # Criar um DataFrame pandas com os dados capturados
    df = pd.DataFrame([line.strip().split('\t') for line in output.splitlines()],
                      columns=['eth.src', 'eth.dst', 'frame.time_relative', 'frame.len', 'ip_src','ip_dst', 'dstPort_tcp', 'dstPort_udp'])

    df['dstPort_udp'].fillna(0, inplace = True)
    df['dstPort_tcp'].fillna(0, inplace = True)

    #df.drop(df[(df['eth.dst'] == 'ff:ff:ff:ff:ff:ff') | (df['ip_dst'] == '255.255.255.255')].index, inplace=True)
    
    df['port'] = df['dstPort_tcp'].astype(str) + df['dstPort_udp'].astype(str)
    
    df= df.drop(columns=['dstPort_udp','dstPort_tcp'])

    # Filtrar os pacotes com os endereços MAC de teste
    filtered_df = df[df['ip_src'].isin(ipGateway) | df['ip_dst'].isin(ipGateway)]

    # Converter o campo 'frame.time_relative' para float
    filtered_df['frame.time_relative'] = filtered_df['frame.time_relative'].astype(float)

    # Adicionar a coluna de direção do pacote (0 para enviado, 1 para recebido)
    filtered_df['direction'] = filtered_df.apply(lambda row: 0 if row['ip_src'] == ipGateway else 1, axis=1)

    # Adicionar a coluna de endereço MAC do dispositivo
    filtered_df['device_mac'] = filtered_df.apply(lambda row: row['eth.src'] if row['direction'] == 0 else row['eth.dst'], axis=1)

    # Criar um DataFrame com as características selecionadas
    selected_features = filtered_df[['frame.time_relative', 'direction', 'frame.len', 'device_mac']]
    
    del filtered_df, df
    
    selected_features['label_name'] = nome_do_arquivo
    
    if indicador == 0:
        selected_features['label'] = 0
    elif indicador == 1:
        selected_features['label'] = 1

    return selected_features


if __name__ == "__main__":

    all_devices_samples = []
    
    localPcap = 'pcaps/'   

    nome_do_arquivo, extensao = os.path.splitext(os.path.basename(localPcap))
    print(nome_do_arquivo)

    for root, dirs, files in os.walk(localPcap):
            for filename in files:
                if filename.endswith(".pcap") or filename.endswith(".pcapng"):
                    pcap_path = os.path.join(root, filename)
                    nome_do_arquivo, extensao = os.path.splitext(os.path.basename(pcap_path))

                    if "port_scan" in root:
                        indicador = 1
                    elif "trafego_normal" in root:
                        indicador = 0
                    else:
                        indicador = -1  # Caso não esteja em nenhuma das pastas especificadas

                    gateway = find_gateway(pcap_path)
                    dfTimeseries = timeSeries(pcap_path, nome_do_arquivo, gateway, indicador)
                    all_devices_samples.append(dfTimeseries)

    if all_devices_samples:
        df_total = pd.concat(all_devices_samples, ignore_index=True)

        df_teste = df_total[df_total['label_name'].isin(['MSCAD-Scan-1', 'cenarioexperimental'])]
        df_treino = df_total[~df_total['label_name'].isin(['MSCAD-Scan-1', 'cenarioexperimental'])]
        
        # Salvar os DataFrames em arquivos CSV
        df_teste.to_csv("teste-preProcessamento.csv", index=False)
        df_treino.to_csv("treino-preProcessamento.csv", index=False)


