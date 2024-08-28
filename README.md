# Инструкция по установке

1. Обновите систему:

    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

2. Установите пакет curl:

    ```bash
    sudo apt install curl -y
    ```

3. Загрузите скрипт nodepay_setup.sh:

    ```bash
    curl -O https://gist.githubusercontent.com/twojded/ee529c048afaf68cd4fdadb54e97b54f/raw/b2640b1ed7d8d065bbc00339e45b96461c6ab4b4/nodepay_setup.sh

    ```

4. Дайте загруженному скрипту права на выполнение:

    ```bash
    chmod +x nodepay_setup.sh
    ```

5. Запустите новую сессию screen:

    ```bash
    screen -S nodepay
    ```

6. Запустите скрипт:

    ```bash
    ./nodepay_setup.sh
    ```
7. Дайте необходимые права на выполнение:

    ```bash
    chmod +X Nodepay-cli/nodepay.py
    ```

8. Запустите скрипт:

    ```bash
    python3 Nodepay-cli/nodepay.py
    ```

В последней команде от вас потребуется ввести np token. Для этого войдите на Nodepay Dashboard, откройте инструменты разработчика (нажмите F12) и получите токен, как показано на скриншоте (np token действует 14 дней, поэтому его нужно обновлять каждые 14 дней).
    ![np](https://github.com/user-attachments/assets/731dd642-46f2-41f4-9de5-60df7e34a1bf)

9. Чтобы изменить токен, удалите старый и вставьте новый, затем сохраните файл с помощью CTRL+X, Y:
    
    ```bash
    cd Nodepay-cli && nano token.txt
    ```
