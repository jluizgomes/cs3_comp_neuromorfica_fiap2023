# Challenge Spring 3 - Computação Neuromórfica e Supercomputadores

## Instruções para Executar a API de Ingestão de Dados no MicroK8s

Este guia descreve como implantar e executar a API de Ingestão de Dados em um cluster Kubernetes gerenciado pelo MicroK8s. A solução permite a ingestão dinâmica de dados de um arquivo CSV em um banco de dados relacional e fornece endpoints para configurar a ingestão e ler os dados.

## Pré-requisitos

- MicroK8s instalado em sua máquina local. Você pode seguir as instruções de instalação em [https://microk8s.io/docs](https://microk8s.io/docs).

## Configuração do Banco de Dados

1. Certifique-se de que o MicroK8s esteja em execução. Você pode iniciar o MicroK8s com o seguinte comando:

   ```bash
   microk8s start
   microk8s enable ingress

   ```

2. Crie um banco de dados PostgreSQL no MicroK8s.

   ```bash
   microk8s.kubectl create configmap api-config --from-file=app.py
   microk8s.kubectl create -f api-config.yaml
   ```

3. Implante o PostgreSQL no MicroK8s.
   ```bash
   microk8s.kubectl apply -f postgres-deployment.yaml
   ```

4. Teste a conexão com o PostgreSQL.
   ```bash
   microk8s.kubectl get svc postgres-service
   ```

5. Use o psql para se conectar ao banco de dados.
   ```bash
   psql -h SEU_IP_DO_SERVICO -p 5432 -U cs3neuro -d previsao_tempo_amazonia
   ```

## Implantação da API

1. Clone este repositório em sua máquina local:

   ```bash
   git clone https://github.com/jluizgomes/cs3_comp_neuromorfica_fiap2023.git
   cd cs3_comp_neuromorfica_fiap2023
   ```

2. Construa a imagem Docker da aplicação:

   ```bash
   docker build -t previsao_tempo_amazonia:v1 .
   ```

3. Crie a imagem .tar do Docker

   ```bash
   docker save previsao_tempo_amazonia > previsao_tempo_amazonia.tar
   ```

4. Carregue a imagem para o registro local do MicroK8s:

   ```bash
   microk8s ctr images import previsao_tempo_amazonia.tar
   ```

5. Implante a aplicação no cluster Kubernetes:

   ```bash
   microk8s.kubectl apply -f api-deployment.yaml
   ```

6. Exponha a API usando NodePort:

   ```bash
   microk8s.kubectl apply -f api-service.yaml
   ```

7. Verifique se a aplicação está em execução:

   ```bash
   microk8s.kubectl get pods
   ```

8. Obtenha o endereço IP e a porta do serviço NodePort:

   ```bash
   microk8s.kubectl get svc previsao-tempo-amazonia-api-service
   ```

Agora, a API de Ingestão de Dados está implantada e exposta no MicroK8s. Você pode acessar a API usando o endereço IP e a porta fornecidos.

## Uso da API

- `POST /configurations`: Configure a ingestão dinâmica de dados.
- `POST /read`: Leia os dados do arquivo CSV e insira-os no banco de dados.

## Encerrando a Aplicação

Para encerrar a aplicação e liberar os recursos do MicroK8s, você pode excluir os recursos implantados:

```bash
microk8s.kubectl delete -f api-service.yaml
microk8s.kubectl delete -f api-deployment.yaml
microk8s.kubectl delete configmap api-config
```

Para encerrar o MicroK8s, execute o seguinte comando:

```bash
microk8s stop
```


### Source dos dados
```
https://data.amerigeoss.org/dataset/previsao-climatica-do-censipam/resource/175fd55b-3bb8-4472-8c19-0de0e868dd7f
```



### microk8s token

```
eyJhbGciOiJSUzI1NiIsImtpZCI6IlA4VWo1LTgtcVZZX3RfNU14bVMwQ1dSc1dJaDJLN0cycV9nWkNiNUdmQmcifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJtaWNyb2s4cy1kYXNoYm9hcmQtdG9rZW4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjdkYWI3ZTY2LTNmZDUtNGY3Yy1hMWMzLWViMWVlMjc4NDZmOCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTpkZWZhdWx0In0.G9TWIXuYpUacwlCgwet1KtTDL4ZXlC-KVY8-212WpRlIT8sLBQjLuDiXwWYocpz8WqG5nR26Am-65OxazDksqijArVV4R_wd-4jEG7p-3YjlBbj5Mt0NKyoSo2YUx4OUd-Sq1MIUtDc4FkF4ZxM4_KHjQ032BrAeIIixZai4kOjxBi3me-E4g74ER9zH27ucmiw84555LjH9zUZzWkq8wWh3LCPvtJA4dQ8FSDo468LZdmG1lfx6tSB-gf3zfIxqGxm89YjprIlgtEWjg3W-9HRPPJtiArq7r2x7vCSoLOOwF4M6fxJ8DeziPrtD4kxdMS0GRjnz9Mzy0u1DioRUXA
```