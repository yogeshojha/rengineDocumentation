# Quick Install reNgine on Ubuntu

1. Clone reNgine

   ```
   git clone https://github.com/yogeshojha/rengine && cd rengine
   ```

   !!! danger "Attention"
   **please make sure to change the password for postgresql POSTGRES_PASSWORD !**

2. Edit the dotenv file using `nano .env` or `vi .env` or `vim .env`.

   **Sample .env file**

   ```
   #
   # General
   #
   COMPOSE_PROJECT_NAME=rengine

   #
   # SSL specific configuration
   #
   AUTHORITY_NAME=reNgine
   AUTHORITY_PASSWORD=nSrmNkwT
   COMPANY=reNgine
   DOMAIN_NAME=recon.example.com
   COUNTRY_CODE=US
   STATE=Georgia
   CITY=Atlanta

   #
   # Database configurations
   #
   POSTGRES_DB=rengine
   POSTGRES_USER=rengine
   POSTGRES_PASSWORD=hE2a5@K&9nEY1fzgA6X
   POSTGRES_PORT=5432
   POSTGRES_HOST=db

   #
   # Celery CONCURRENCY Autoscaling
   # The number of CONCURRENCY defines how many scans will run in parallel
   # Please always keep minimum of 5
   #
   MIN_CONCURRENCY=5
   MAX_CONCURRENCY=30
   ```

## .env Explained

   - **COMPOSE_PROJECT_NAME**: This will help reNgine name docker containers as rengine_web_1, rengine_celery_1 etc. <small>(Making changes is Optional)</small>

   - **AUTHORITY_NAME**: SSL Authority Name
   - **AUTHORITY_PASSWORD**: SSL Authority Password
   - **COMPANY**: Company Name to generate SSL to
   - **DOMAIN_NAME**: Domain where reNgine is going to be installed
   - **COUNTRY_CODE, STATE, CITY**: SSL Speciffc

   - **POSTGRES_DB**: DB name for Postgres <small>(Making changes is Optional)</small>
   - **POSTGRES_USER**: Postgres Username for DB auth purpose <small>(Making changes is Optional)</small>
   - **POSTGRES_PASSWORD**: Postgres Password for DB auth purpose <strong>(Please change the default Postgres Password)</strong>
   - **POSTGRES_PORT**: Postgres Port <small>(Making changes is Optional)</small>
   - **POSTGRES_HOST**: Postgres HOST <small>(Making changes is Optional)</small>

   - **MIN_CONCURRENCY**: Minimum number of Concurrency for Celery.
   - **MAX_CONCURRENCY**: Maximum number of Concurrency for Celery. This determines how many maximum number of scans to run in parallel.

## Determining CONCURRENCY Values

   Here is the ideal value for MIN_CONCURRENCY and MAX_CONCURRENCY depending on the number of RAM your machine has:

   - <strong>4GB</strong>: `MAX_CONCURRENCY=10`
   - <strong>8GB</strong>: `MAX_CONCURRENCY=30`
   - <strong>16GB</strong>: `MAX_CONCURRENCY=50`

   This is just an ideal value which developers have tested and tried out and works! But feel free to play around with the values.

   Maximum number of scans is determined by various factors, your network bandwith, RAM, number of CPUs available. etc

3. Run the installation script, Please keep an eye for any prompt, you will also be asked for username and password for reNgine UI.

   ```
   sudo ./install.sh
   ```

   if `./install.sh` does not have install permission, please add executable permission, `chmod +x install.sh`

4. You will be asked to create account for reNgine, please choose a strong password.

   ![](../static/username.png)

**reNgine can now be accessed from [https://127.0.0.1](https://127.0.0.1) or if you're on the VPS <https://your_vps_ip_address>**
