### Overly simplified Netbox installation in a K8s cluster
- Helps with local testing
- Iterative development



Steps:

docker run -it arm64v8/ubuntu:22.04 /bin/bash
apt update -y && apt install -y ansible
ansible localhost -m command -a "uptime"
ansible-playbook -i localhost -e @vars.yaml install_netbox.yaml


docker build . -t sivaramsajeev/netbox-for-k8s
kind load docker-image --name netbox-demo netbox-for-k8s

kubectl port-forward service/netbox-service 8000:80



