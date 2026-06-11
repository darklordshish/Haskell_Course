# Haskell Course

Интерактивный курс по Haskell на базе Jupyter-ноутбуков с IHaskell-ядром.

Темы: базовый Haskell, функторы, монады, трансформеры монад, комонады, стрелки, оптики, профункторы, лемма Йонеды, расширения Кана, топосы, сопряжения, алгебры/коалгебры и многое другое.

## Структура

```
src/
  notebooks/        — Jupyter-ноутбуки (.ipynb)
  diagrams/         — SVG-диаграммы по темам
  scripts/          — вспомогательные скрипты
    deps/           — генерация шапок зависимостей
      dictionary.json    — единый источник правды (расширения, пакеты, модули)
      gen_headers.js     — генератор ячейки deps_header (идемпотентный)
      build_extensions.js — сборка Extensions.ipynb
  lib/              — git-сабмодуль: библиотека категорного ядра
  README.ipynb      — стартовый ноутбук
  ROADMAP.md        — план курса
docker-compose.yml
```

**Начинать курс рекомендуется с `src/notebooks/Extensions.ipynb`** — нулевой ноутбук с обзором всех расширений GHC, используемых в курсе (26 расширений с пояснениями и примерами).

## Шапки зависимостей

Каждый ноутбук содержит автогенерируемую ячейку `deps_header` («📦 Зависимости») с перечнем пакетов, модулей `src/lib` и расширений GHC. После изменения setup-ячейки или импортов — перегенерировать:

```bash
node src/scripts/deps/gen_headers.js
```

## Запуск через Docker

### Требования
- [Docker](https://docs.docker.com/get-docker/) и Docker Compose

### Быстрый старт

```bash
git clone https://github.com/darklordshish/Haskell_Course.git
cd Haskell_Course
docker compose up
```

Откройте в браузере: [http://localhost:8889](http://localhost:8889)

Ноутбуки находятся в папке `pwd/src/notebooks/` внутри JupyterLab.

### Остановка

```bash
docker compose down
```

### Примечания

- Первый запуск может занять несколько минут (загрузка образа `gibiansky/ihaskell`).
- Токен авторизации отключён — доступ открыт напрямую по localhost.
- Порт: `8889` на хосте → `8888` в контейнере.

## Легаси-версия

Предыдущая версия курса (слайды/конспекты) хранится в ветке [`legacy`](https://github.com/darklordshish/Haskell_Course/tree/legacy).
