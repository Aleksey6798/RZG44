#!/bin/bash

# Проверяем, что находимся в git-репозитории
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Ошибка: скрипт должен запускаться в git-репозитории."
    exit 1
fi

# Получение последнего тега
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
echo "Последний тег: $LAST_TAG"

# Создание нового тега
IFS='.' read -ra VERSION_PARTS <<< "${LAST_TAG#v}"
NEW_VERSION="v${VERSION_PARTS[0]}.$((VERSION_PARTS[1] + 1)).0"
echo "Новая версия: $NEW_VERSION"

# Получение текущей даты
CURRENT_DATE=$(date +'%Y-%m-%d')

# Сбор коммитов с момента последнего тега
COMMITS=$(git log "$LAST_TAG"..HEAD --pretty=format:"- %s [%h](https://github.com/https://github.com/Aleksey6798/RZG44.git/commit/%h)")

if [ -z "$COMMITS" ]; then
    echo "Нет новых коммитов с момента последнего релиза."
    exit 0
fi

# Добавление новой секции в changelog.md
echo "Обновление changelog.md..."
{
    echo "## $NEW_VERSION - $CURRENT_DATE"
    echo "$COMMITS"
    echo
    cat changelog.md
} > changelog.md.tmp && mv changelog.md.tmp changelog.md

# Создание нового тега
git tag -a "$NEW_VERSION" -m "Release $NEW_VERSION"
git push origin "$NEW_VERSION"

echo "Changelog обновлён и тег $NEW_VERSION создан."
