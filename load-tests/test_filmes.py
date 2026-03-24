from locust import HttpUser, task, between
from faker import Faker
import base64

fake = Faker('pt_BR')

class FilmeUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.token = None
        self.filme_id = "1"

        self.default_user = "user"
        self.default_pass = "eaaebac8-0942-4e8c-86f1-c0ab65316493"
        auth_str = f"{self.default_user}:{self.default_pass}"
        self.basic_auth = base64.b64encode(auth_str.encode()).decode()

        email_fake = f"film_{fake.uuid4()[:8]}@test.com"
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

        self.prepare_filme()

    def prepare_filme(self):
        headers = {"Authorization": self.token, "Content-Type": "application/xml", "Accept": "application/xml"}
        f_xml = f"<?xml version='1.0' encoding='UTF-8'?><filme><titulo>Movie_Init</titulo><duracaoMin>120</duracaoMin><ano>2024</ano></filme>"
        with self.client.post("/filmes", data=f_xml, headers=headers) as fr:
            if fr.status_code == 201:
                loc = fr.headers.get("Location
