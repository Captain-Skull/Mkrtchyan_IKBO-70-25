# Соответствие заданию

| Этап и требование | Где реализовано / как показать |
|---|---|
| 1. GUI | `gui.py`, класс `Terminal`; `python3 main.py`. |
| 1. Имя VFS в заголовке | `root.title` показывает имя CSV из `--vfs`. |
| 1. Разделение команды и аргументов по пробелам | `shell.py`, `parse_command`, `line.split()`. |
| 1. Неизвестная команда и неверные аргументы | `Shell.execute`, примеры `unknown`, `cd a b`, `exit extra`. |
| 1. Заглушки ls, cd | Коммит `66aac2b`; в итоговой версии заменены настоящей логикой на этапе 4. |
| 1. exit | `Result(exit=True)` и `root.destroy()`. |
| 1. Интерактивная демонстрация всей функциональности | Сценарий в README версии этапа 1; итоговый ручной сценарий в `DEFENSE.md`, раздел 11. |
| 1. Стандартный коммит | `66aac2b feat(shell): implement stage 1 GUI REPL and command stubs`. |
| 2. Путь VFS и стартового скрипта через CLI | `config.py`: `--vfs`, `--script`; справка `--help`. |
| 2. Отладочный вывод параметров | Начало истории окна: `[config] VFS`, `[config] Стартовый скрипт`. |
| 2. Последовательный скрипт, ввод и вывод, продолжение после ошибки | `startup.py`, `script_events`; `Terminal.script_step`. |
| 2. Сообщение об ошибке скрипта | Путь и номер ошибочной строки; отдельная ошибка чтения файла. |
| 2. Несколько скриптов реальной ОС | `scripts/test_config.sh`, `scripts/test_errors.sh`. |
| 2. Стандартный коммит | `e0c1cd7 feat(shell): add stage 2 CLI configuration and startup scripts`. |
| 3. Все операции VFS в памяти, без распаковки | `VFS.nodes`; `move` меняет словарь, `read_text` читает байты узла. |
| 3. CSV, двоичные данные, вложенность | `vfs.py`; заголовок `path,type,content`, base64 и абсолютные пути. |
| 3. Ошибки загрузки | `VFS.load` и обработчик `VFSError` в GUI; отсутствующий и неверный CSV в `test_errors.sh`. |
| 3. vfs-save | `Shell.execute` → `VFS.save`; сохранение в исходном формате. |
| 3. Минимальная VFS, несколько файлов, ≥3 уровней каталогов | `minimal.csv`, `files.csv`, `demo.csv`; `test_vfs.sh` и `test_config.sh`/`test_errors.sh` для других вариантов запуска. |
| 3. Стартовый скрипт всех команд этапов 1–3 | `examples/startup/stage3.txt`; успешный выход отдельно в `exit.txt`, чтобы остальные результаты оставались видимыми. |
| 3. Стандартный коммит | `00bcb47 feat(vfs): implement stage 3 in-memory CSV filesystem and saving`. |
| 4. Логика ls и cd | `shell.py` и `VFS.resolve`, `VFS.list_directory`. |
| 4. rev, echo, clear | Соответствующие ветки в `Shell.execute`. |
| 4. Скрипт режимов и ошибок | `examples/startup/stage4.txt`; запуск `test_commands.sh`. |
| 4. Стандартный коммит | `cfe6f41 feat(shell): implement stage 4 ls cd rev echo and clear commands`. |
| 5. mv, изменение только в памяти | `VFS.move`; обновление текущего пути в `Shell.execute`. |
| 5. Скрипт режимов и ошибок | `examples/startup/stage5.txt`; запуск `test_commands.sh`. |
| 5. Стандартный коммит | `2b708e8 feat(vfs): implement stage 5 file and directory moves`. |

Дополнительно подготовлены общий стартовый скрипт `all.txt`, автоматические
тесты логики и GUI, инструкция запуска и руководство для защиты.

## Перед сдачей

1. Запустить `python3 -m unittest discover -s tests -v`.
2. Запустить `python3 -m tests.gui_smoke` в графическом сеансе.
3. Показать интерактивный сценарий из `DEFENSE.md`.
4. Показать `sh scripts/demo.sh`, `sh scripts/test_vfs.sh`, `sh scripts/test_errors.sh`.
5. Показать `git log --oneline -- shell_emulator` из корня репозитория.
6. Убедиться, что можешь объяснить `parse_command`, `resolve` и `move`.
