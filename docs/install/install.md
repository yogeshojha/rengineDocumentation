# Detailed Installation Instructions

If you have met all the [Prerequisites](#prerequisites), you can begin installing **reNgine**.

* Let's begin by cloning the **reNgine**.

```
git clone https://github.com/yogeshojha/rengine
```

```
cd rengine
```

### dotenv file

Before we begin installing reNgine, it is necessary to make changes to the [dotenv](https://github.com/yogeshojha/rengine/blob/master/.env) file. You can edit the file using your favourite editor

```
nano .env
```

or

```
vim .env
```

The sample [.env](https://github.com/yogeshojha/rengine/blob/master/.env) file can be found [here](https://github.com/yogeshojha/rengine/blob/master/.env).

```
COMPOSE_PROJECT_NAME=rengine

AUTHORITY_NAME=reNgine
AUTHORITY_PASSWORD=nSrmNkwT
COMPANY=reNgine
DOMAIN_NAME=recon.example.com
COUNTRY_CODE=US
STATE=Georgia
CITY=Atlanta

POSTGRES_DB=rengine
POSTGRES_USER=postgres
POSTGRES_PASSWORD=set_db_pass
POSTGRES_PORT=5432
POSTGRES_HOST=db
```

### Generating SSL Certificates

reNgine runs on https unless otherwise used for development purpose. Using https is recommended. To generate the certificates you can use

```
make certs
```

!!! danger ""
    Please note, while running any `make` command, you must be inside the rengine/ directory.

### Build reNgine

To build the reNgine, use the following command

```
make build
```

The build process is a lengthy process and expected to take some time.

!!! info ""
    Thanks to [Baptiste MOINE](https://github.com/Creased) for sending the PR that made build process so much simpler.

### Run reNgine

Once the build process is successful, we're good to run reNgine. This can be done using below command

```
make up
```

**reNgine can now be accessed from https://127.0.0.1 or if you're on the VPS https://your_vps_ip_address**

### Registering an account

You will need to create a username and password in order to login to the reNgine. To register reNgine, please run the following command

```
make username
```

You will now be prompted with some personal details(optional), username and password. **We highly recommend that you set a strong password for reNgine.**

![](../static/username.png)

You may now login to the reNgine web portal using the username and password that you just provided.

## Checking logs

If you need to observe the logs, it can be done so by running the commmand

```
make logs
```

!!! note
    If you encounter any issues while setup or scan, we advice you to [raise an issue in Github](https://github.com/yogeshojha/rengine/issues) and attach the log. While raising any new issues on Github, it is also adviced that you to look for any open issues on Github as well.

## Stopping the reNgine

If you wish to stop the reNgine, it can be done so by using the command

```
make stop
```

## Restarting the reNgine

reNgine can be restarted using the command

```
make restart
```

## Removing all the reNgine Data

If you wish to delete all your recon data, it can be done using

!!! danger
    This is a irreversible process and once pruned, you may never get back your recon data.
    Use with caution.

```
make prune
```
