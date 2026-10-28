# Эмулятор UNIX-подобной оболочки

Учебный проект на Python и Tkinter. Запуск из этой папки:

```sh
python3 main.py
```

Проверка: `python3 -m unittest discover -s tests -v`.

Этап 1: GUI, простой парсер, заглушки `ls`, `cd`, команда `exit`, ошибки.
Для интерактивной демонстрации введите по очереди `ls`, `ls /home`,
`cd /home`, `cd a b`, `unknown`, `exit extra`, `exit`.
