# Эмулятор UNIX-подобной оболочки

Учебный проект на Python и Tkinter. Запуск из этой папки:

```sh
python3 main.py
```

Проверка: `python3 -m unittest discover -s tests -v`.

Этап 1: GUI, простой парсер, заглушки `ls`, `cd`, команда `exit`, ошибки.
Для интерактивной демонстрации введите по очереди `ls`, `ls /home`,
`cd /home`, `cd a b`, `unknown`, `exit extra`, `exit`.

Этап 2: `python3 main.py --vfs examples/vfs/demo.csv --script examples/startup/stage2.txt`.
Пути к VFS и скрипту отображаются при запуске. Пока VFS не загружается.
Ошибочные строки не прерывают выполнение; `exit` завершает приложение.
`sh scripts/test_config.sh` и `sh scripts/test_errors.sh` показывают варианты
параметров. Закрывайте окно для перехода к следующему запуску.
