import yaml
import base64

VAR_FILE_PATH = 'vars.yaml'
SECRET_FILE_PATH = 'db-secrets-class.yaml'
VAR_MAPPING = {
    '__name': 'db-secret',
    'db_name': 'POSTGRES_DB',
    'db_user': 'POSTGRES_USER',
    'db_user_password': 'POSTGRES_PASSWORD'
}

generate_base64 = lambda x: base64.b64encode(x.encode()).decode()

class Secret():
    def __init__(self, mapping: dict) -> None:
        self.vars = dict()
        self.mapping = mapping
        self.k8s_secret =  {
                "apiVersion": "v1",
                "kind": "Secret",
                "metadata": {
                    "name": self.mapping.get('__name', 'generated-secret')
                },
                "type": "Opaque",
                "data": {}
            }
        
    def load(self, var_file_path) -> 'Secret':
        try:
            with open(var_file_path, "r") as yaml_file:
                self.vars = yaml.load(yaml_file, Loader=yaml.FullLoader)
                return self 
        except Exception as e:
            raise e
        
    def do_mapping(self) -> 'Secret':
        self.k8s_secret['data'] = {v: generate_base64(self.vars.get(k, '')) for k, v in self.mapping.items() if not k.startswith('__')}
        return self

    def save(self):
        file_path = f"{self.k8s_secret.get('metadata').get('name')}.yaml"
        try:
            secret_yaml = yaml.dump(self.k8s_secret, default_style='"')
            with open(file_path, "w") as secret_file:
                secret_file.write(secret_yaml)
            print(f"Kubernetes secret manifest has been generated in {file_path}.")
        except Exception as e:
            raise e

def main():
    Secret(VAR_MAPPING).load(VAR_FILE_PATH).do_mapping().save()


if __name__ == '__main__':
    main()
