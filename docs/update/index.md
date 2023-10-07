# Updating reNgine


!!! tips
    You can always update reNgine to the latest release unless otherwise [stated in the changelog](/changelog).

    [Please ensure backwards compatibility before updating reNgine.](/changelog/#backwards-compatibility-check)

!!! warning "What happens is reNgine is not backwards compatible?"
      Like major release 1.0, reNgine is not backwards compatible. This is due to many changes added in reNgine and to skip worrying about django migrations and other configuration issues, sometimes (some major releases) may not be backwards compatible.

      In this case, please do not update/upgrade reNgine. Please do a fresh installation.

## ⚡ Quick Update

Updating is as simple as running the following command:

1. Go to your reNgine root directory.
    ```bash
    cd script
    sudo ./update.sh
    ```
2. Follow the update prompts

3. Rebuild the latest changes
    ```bash
    make build
    ```

4. Start reNgine services
    ```bash
    make up
    ```
