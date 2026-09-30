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
