from locust import HttpUser, task, between
from faker import Faker
import base64

fake = Faker('pt_BR')

class TipoIngressoUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.token = None
        self.tipo_id = "1"
        
        self.default_user = "user"
        self.default_pass = "eaaebac8-0942-4e8c-86f1-c0ab65316493"
        auth_str = f"{self.default_user}:{self.default_pass}"
        self.basic_auth = base64.b64encode(auth_str.encode()).decode()

        email_fake = f"ticket_{fake.uuid4()[:8]}@test.com"
        reg_payload = {"nome": fake.name(), "email": email_fake, "password": "pass123"}
        
        with self.client.post("/auth/register", json=reg_payload, catch_response=True) as resp:
            if resp.status_code in [200, 201]:
                login_data = {"email": email_fake, "password": "pass123"}
                with self.client.post("/auth/login", json=login_data) as log_resp:
                    if log_resp.status_code == 200:
                        self.token = f"Bearer {log_resp.json().get('token')}"

            if not self.token:
                self.token = f"Basic {self.basic_auth}"
                resp.success()

        self.prepare_tipo()

    def prepare_tipo(self):
        headers = {"Authorization": self.token, "Content-Type": "application/xml", "Accept": "application/xml"}
        t_xml = f"<?xml version='1.0' encoding='UTF-8'?><tipoIngresso><descricao>Tipo_Init</descricao><fatorPreco>1.0</fatorPreco><categoriaTecnica>2D</categoriaTecnica></tipoIngresso>"
        with self.client.post("/tipos-ingresso", data=t_xml, headers=headers) as tr:
            if tr.status_code == 201:
                loc = tr.headers.get("Location")
                if loc: self.tipo_id = loc.split("/")[-1]

    @task
    def fluxo_tipo_ingresso(self):
        headers = {"Authorization": self.token, "Content-Type": "application/xml", "Accept": "application/xml"}
        self.client.get(f"/tipos-ingresso/{self.tipo_id}", headers=headers, name="GET /tipos-ingresso/[id]")
        
        novo_t = f"<?xml version='1.0' encoding='UTF-8'?><tipoIngresso><descricao>Load_{fake.uuid4()[:4]}</descricao><fatorPreco>1.5</fatorPreco><categoriaTecnica>3D</categoriaTecnica></tipoIngresso>"
        self.client.post("/tipos-ingresso", data=novo_t, headers=headers, name="POST /tipos-ingresso")
