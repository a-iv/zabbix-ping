Сборка выполняемого файла::

    pip install -r requirements.txt
    pyinstaller --onefile --collect-all bitstring zabbix_ping.py


Сборка новых зависимостей (по желанию)::

    pip install pip-tools
    pip-compile requirements.in


Для работы под Windows 7 64-bit последней версией является Python 3.8.10 64-bit.

Установка:

1. Зайти на машину с Zabbix-агентом.
2. Создать папку "C:\\Program Files\\Zabbix Ping".
3. Скопировать в неё "zabbix_ping.exe".
4. В папку "C:\\Program Files\\Zabbix Agent\\zabbix_agentd.d" скопировать "zabbix_ping.conf".
5. Перезапустить сервис Zabbix-агента.
6. Открыть веб-интерфейс Zabbix-сервера.
7. Перейти в "Configuration" → "Hosts".
8. Найти нужный хост и нажать ссылку "Items".
9. Нажать кнопку "Create item".
10. Заполнить форму. Например:

   * Name: Ping check to example.com
   * Type: Zabbix agent
   * Key: custom.ping[example.com]
   * Type of information: Numeric (float)
   * Units: ms

11. Нажать кнопку "Test", затем "Get value and test".
12. Убедиться, что в "Result" в правом углу отображается числовое значение.
13. Закрыть окно тестирования, нажав кнопку "Cancel".
14. Подтвердить добавление, нажав кнопку "Add".
15. Подождать 60 секунд.
16. Перейти в "Monitoring" → "Latest data".
17. В фильтре в поле "Hosts" указать нужный хост, в поле "Name" ввести "ping" и нажать кнопку Apply.
18. Убедиться, что "Last value" содержит значение.
