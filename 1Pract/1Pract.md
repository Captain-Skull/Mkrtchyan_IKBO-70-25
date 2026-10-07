# Задание 1.

Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd (вам понадобится grep).

Ответ:
```bash
cut -d ':' -f 1 passwd | sort
```

# Задание 2

Вывести данные /etc/protocols в отформатированном и отсортированном порядке для 5 наибольших портов, как показано в примере ниже

Ответ:
```bash
cut -f 1,2 /etc/protocols | sort -k 2 -n -r | awk '{print $2, $1}' | head -n 5
```

# Задание 3

## banner:
```bash
#!/bin/bash
if [[ $# -eq 0 ]]; then
  echo "Use: $0 \"string\"" >&2
  exit 1
fi

input="$1"

printf -v line '%*s' "$(( ${#input} + 2 ))" ''
line="+${line// /-}+"
midleLine="| ${input} |"

echo "$line"
echo "$midleLine"
echo "$line"

```

## banner
```bash
#!/bin/bash
if [[ $# -eq 0 ]]; then
  echo "Use: $0 \"string\"" >&2
  exit 1
fi

len=${#1}
printf "+"

for (( i=0; i < len + 2; i++ )); do
  printf "-"
done

printf "+\n"

printf "| %s |\n" "$1"

printf "+"

for (( i=0; i < len + 2; i++ )); do
  printf "-"
done

printf "+\n"
```

# Задание 4

## identifiers
```bash
#!/bin/bash
if [[ $# -ne 1 ]]; then
  echo "Use: $0 file" >&2
  exit 1
fi

grep -oE '[A-Za-z_][A-Za-z0-9_]*' "$1" | sort -u | tr '\n' ' '
echo

```

# Задание 5

## reg
```bash
#!/bin/bash

if [[ $# -ne 1 ]]; then
  echo "Use: $0 file" >&2
  exit 1
fi

if [[ ! -f "$1" ]]; then
  echo "$0: $1: not a regular file" >&2
  exit 1
fi

chmod 755 "$1"

sudo cp "$1" /usr/local/bin
```

# Задание 6

## comments
```bash
#!/bin/bash

if [[ $# -ne 1 ]]; then
  echo "Use: $0 file" >&2
  exit 1
fi

if [[ ! -f "$1" ]]; then
  echo "$0: $1: not a regular file" >&2
  exit 1
fi

if [[ ! "$1" =~ \.(c|js|py)$ ]]; then
  echo "$0: $1: is not a js/c/py file" >&2
  exit 1
fi

case "$1" in
  *.py)      re='^[[:space:]]*#' ;;
  *.c|*.js)  re='^[[:space:]]*(//|/\*)' ;;
esac

first_line=$(head -n 1 "$1")

if [[ "first_line" =~ $re && "$first_line" != '#!'* ]];then
  echo "$1: комментарий есть"
else
  echo "$1: комментария нет"
fi
```

# Задание 7

## dublicates
```bash
#!/bin/bash

if [[ $# -ne 1 ]]; then
  echo "Use: $0 dir" >&2
  exit 1
fi

if [[ ! -d "$1" ]]; then
  echo "$0: $1: not a directory" >&2
  exit 1
fi

find "$1" -type f -print0 | xargs -0 md5sum | sort | uniq -w 32 -D | cut -c 35-
```

# Задание 8

## archive
```bash
#!/bin/bash

if [[ $# -ne 1 ]]; then
  echo "Use: $0 .extension" >&2
  exit 1
fi

find . -maxdepth 1 -type f -name "*$1" -print0 | tar -cf archive.tar --null -T -
```

# Задание 9

## tab
```bash
#!/bin/bash

if [[ $# -ne 2 ]]; then
  echo "Use: $0 input.txt output.txt" >&2
  exit 1
fi

sed 's/    /\t/g' "$1" > "$2"
```

# Задание 10

## empty
```bash
#!/bin/bash

if [[ $# -ne 1 ]]; then
  echo "Use: $0 dir" >&2
  exit 1
fi

if [[ ! -d "$1" ]]; then
  echo "$0: $1: not a directory" >&2
  exit 1
fi

find "$1" -maxdepth 1 -type f -empty -name "*.txt" -printf '%f\n'
```