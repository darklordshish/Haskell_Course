# Haskell Course

Интерактивный курс по Haskell на базе Jupyter-ноутбуков с IHaskell-ядром.

Темы: базовый Haskell, функторы, монады, трансформеры монад, комонады, стрелки, оптики, профункторы, лемма Йонеды, расширения Кана, топосы, сопряжения, алгебры/коалгебры и многое другое.

## Структура

```
src/
  notebooks/   — Jupyter-ноутбуки (.ipynb)
  diagrams/    — SVG-диаграммы по темам
  scripts/     — вспомогательные Python-скрипты
  README.ipynb — стартовый ноутбук
  ROADMAP.md   — план курса
docker-compose.yml
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
