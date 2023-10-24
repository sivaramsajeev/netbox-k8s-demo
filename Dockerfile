FROM arm64v8/ubuntu:22.04

RUN apt update -y && apt install -y ansible

# Copy your playbook and variables files into the container
COPY vars.yaml install_netbox.yaml configuration.py.j2 .

RUN ansible-playbook -i localhost -e @vars.yaml -e is_build=true install_netbox.yaml

CMD ansible-playbook -i localhost -e @vars.yaml install_netbox.yaml
