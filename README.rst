Сборка выполняемого файла::

    pip install -r requirements.txt
    pyinstaller --onefile --collect-all bitstring zabbix_ping.py


Сборка новых зависимостей (по желанию)::

    pip install pip-tools
    pip-compile requirements.in


Установка:

1. Зайти на машину с Zabbix-агентом.
2. Создать папку "C:\Program Files\Zabbix Ping".
3. Скопировать в неё "zabbix_ping.exe".
4. В папку "C:\Program Files\Zabbix Agent\zabbix_agentd.d" скопировать "zabbix_ping.conf".
5. Открыть веб-интерфейс Zabbix-сервера.
6. Перейти в "Configuration" → "Hosts".
7. Найти нужный хост и нажать ссылку "Items".
8. Нажать кнопку "Create item".
9. Заполнить форму. Например:

   * Name: Ping check to example.com
   * Type: Zabbix agent
   * Key: custom.ping[example.com]
   * Type of information: Numeric (float)
   * Units: ms

10. Нажать кнопку "Test", затем "Get value and test".
11. Убедиться, что в "Result" в правом углу отображается числовое значение.
12. Закрыть окно тестирования, нажав кнопку "Cancel".
13. Подтвердить добавление, нажав кнопку "Add".
14. Подождать 60 секунд.
15. Перейти в "Monitoring" → "Latest data".
16. В фильтре в поле "Hosts" указать нужный хост, в поле "Name" ввести "ping" и нажать кнопку Apply.
17. Убедиться, что "Last value" содержит значение.
