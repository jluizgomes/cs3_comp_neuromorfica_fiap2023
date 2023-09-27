# Challenge Spring 3 - Computação Neuromórfica e Supercomputadores

### Criar a imagem no docker
```
docker build -t previsao_tempo_amazonia_image:v1
```

### Deployment no Kubernets
```
kubectl apply -f deployment.yaml
```

### Aplicando o serviço no NodePort
```
kubectl apply -f service.yaml
```

### Source dos dados
```
https://data.amerigeoss.org/dataset/previsao-climatica-do-censipam/resource/175fd55b-3bb8-4472-8c19-0de0e868dd7f
```