# Backup reNgine

### Backup/Dump database

```bash
sudo docker exec -t rengine_db_1 pg_dumpall -c -U {DB_USER} > rengine_dump_.sql
```

You will be prompted for a database password. This is not your reNgine login password. Please consider checking your `.env` file.

### Backup data volumes [Optional]

Keep a copy of the following data volumes;
- `rengine_scan_results/` : To keep screenshots
- `rengine_gf_patterns/` : To keep custom gf patterns
- `rengine_nuclei_templates/` : To keep custom nuclei templates
- `rengine_tool_config/` : To keep tools config
- `rengine_wordlist/` : To keep custom wordlists

# Restore reNgine

After installation of reNgine, run the following commands;
```bash
sudo docker stop rengine_web_1
sudo docker exec -i rengine_db_1 psql -U {DB_USER} postgres -c "DROP DATABASE rengine;"
sudo docker exec -i rengine_db_1 psql -U {DB_USER} postgres -c "CREATE DATABASE rengine;"
cat {/path/to/rengine_dump_.sql} | sudo docker exec -i rengine_db_1 psql -U {DB_USER} -d rengine
```

- Replace the data volumes, if available.  
- Finally, run the following commands from inside the reNgine directory;

```bash
sudo make build && make up
sudo make up
```

<p align="right">
Contributed by : <a href="https://github.com/nerrorsec">nerrorsec</a>
</p>
