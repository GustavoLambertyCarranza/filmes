# Gestão de Cinema - API REST

Este projeto consiste no desenvolvimento de uma API REST para um Mini-ERP voltado à gestão de Cinema. Construída com **Spring Boot** e arquitetura MVC, a aplicação utiliza o formato **XML** para troca de dados e foca no controle operacional completo: desde o cadastro de filmes e salas até a validação técnica de exibição, agendamento de sessões e venda de ingressos.

## Camada de Segurança (JWT)

A API implementa um sistema de autenticação **Stateless** baseado em **Bearer Tokens (JWT)** com **Spring Security**.

### Como Utilizar:

1.  **Registro**: Crie um usuário através do endpoint `POST /auth/register`.
2.  **Login**: Autentique-se em `POST /auth/login` para obter o token de acesso.
3.  **Autorização**: Para acessar endpoints protegidos, inclua o token no cabeçalho da requisição:
    *   **Header**: `Authorization`
    *   **Valor**: `Bearer <seu_token_aqui>`

### Usuários de Teste (Configurados via `data.sql`):
*   **E-mail**: `joao.silva@example.com` | **Senha**: `password`
*   **E-mail**: `maria.santos@example.com` | **Senha**: `password`

## Tecnologias e Padrões

*   **Java 21** & **Spring Boot 3.5.7**
*   **Spring Security** & **JWT** (JJWT 0.11.5)
*   **BCrypt**: Hashing seguro de senhas.
*   **H2 Database**: Banco de dados em memória para desenvolvimento.
*   **Jackson XML**: Serialização principal dos dados.

## Gerenciamento do Banco de Dados

O console do H2 está habilitado para conferência de dados:
*   **URL**: `http://localhost:8080/h2-console`
*   **JDBC URL**: `jdbc:h2:mem:cinema`
*   **User**: `sa` | **Password**: *(vazio)*

---

##  Equipe de Desenvolvimento

*   **Mariana Gabriely (@mariana-gabriely)**
*   **Gustavo Lamberty Carranza (@GustavoLambertyCarranza)**
*   **Gustavo Montanini Victor (@gustavomcfly)**
*   **Nicholas Gabriel Soares Yamasita Sales (@zalanha)**
*   **Nycolas Rozisca Moreno (@Nycolas64)**
*   **Lia Naomi Hoida**
