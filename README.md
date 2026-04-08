# NEPA Admin

Interface administrativa para o banco de dados PostgreSQL local do NEPA-api

# Executando como Serviço systemd

Você pode executar a aplicação como um serviço `systemd` para
implantações em produção.

## Arquivo de Serviço

Crie o seguinte arquivo:

`/etc/systemd/system/nepa-admin.service`

``` ini
[Unit]
Description=NEPA Admin instance
After=network.target

[Service]
User=nepa
WorkingDirectory=/home/nepa/NEPA-admin
Environment="PATH=/home/nepa/NEPA-admin/.venv/bin"
ExecStart=/home/nepa/NEPA-admin/.venv/bin/gunicorn
Restart=always

[Install]
WantedBy=multi-user.target
```

## Habilitar e Iniciar o Serviço

Após criar o arquivo de serviço, recarregue o systemd:

``` bash
sudo systemctl daemon-reload
```

Habilite o serviço para iniciar com o sistema:

``` bash
sudo systemctl enable nepa-admin
```

Inicie o serviço:

``` bash
sudo systemctl start nepa-admin
```

### Verificar Status do Serviço

``` bash
sudo systemctl status nepa-admin
```

### Visualizar Logs

``` bash
journalctl -u nepa-admin -f
```

### Reiniciar Serviço

``` bash
sudo systemctl restart nepa-admin
```

# Comandos CLI

## Criar Usuário Administrador

Você pode criar um usuário administrador usando o comando CLI do Flask:

``` bash
flask create-admin
```

Este comando solicitará as seguintes informações:

- **Name:** Nome do usuário administrador
- **Email:** Email do usuário administrador
- **Password:** Senha do usuário administrador (entrada oculta com
  confirmação)
- **Role:** Nível de permissão do usuário (padrão: `admin`)

## Exemplo

``` bash
$ flask create-admin

Name: John Doe
Email: john@example.com
Password:
Repeat for confirmation:
```

Se já existir um administrador com o email informado, o comando será
interrompido:

``` bash
An admin with this email already exists.
```

## Opções

Você também pode fornecer os valores diretamente pela linha de comando:

``` bash
flask create-admin \
  --name "John Doe" \
  --email "john@example.com" \
  --password "securepassword" \
  --role "admin"
```

## Requisitos

Certifique-se de que sua aplicação Flask esteja corretamente configurada
e que as migrações do banco tenham sido aplicadas antes de executar este
comando:

``` bash
flask db upgrade
```

## Observações

- A entrada da senha é ocultada por segurança\
- O comando evita emails duplicados de administradores\
- A role padrão é `admin` caso não seja informada
