# Haskell Course

Интерактивный курс по Haskell на базе Jupyter-ноутбуков с IHaskell-ядром.

Темы: базовый Haskell, функторы, монады, трансформеры монад, комонады, стрелки, оптики, профункторы, лемма Йонеды, расширения Кана, топосы, сопряжения, алгебры/коалгебры и многое другое.

## Структура

```
src/
  notebooks/        — Jupyter-ноутбуки (.ipynb)
    course_map.svg  — карта курса (схема метро), генерируется
  diagrams/         — SVG-диаграммы по темам
  scripts/          — вспомогательные скрипты
    deps/           — генерация шапок зависимостей
      dictionary.json    — единый источник правды (расширения, пакеты, модули)
      gen_headers.js     — генератор ячейки deps_header (идемпотентный)
      build_extensions.js — сборка Extensions.ipynb
    coursemap/      — карта курса
      build_map.js       — генератор notebooks/course_map.svg (схема метро)
      restructure_readme.js — перестройка README.ipynb по модулям
  lib/              — git-сабмодуль: библиотека категорного ядра
  README.ipynb      — стартовый ноутбук
  ROADMAP.md        — план курса
docker-compose.yml
```

**Начинать курс рекомендуется с `src/notebooks/Extensions.ipynb`** — нулевой ноутбук с обзором всех расширений GHC, используемых в курсе (26 расширений с пояснениями и примерами).

## Структура курса

Курс выстроен модулями; внутри модуля — усложнение. Ствол проходится по порядку, после `ComonadTransformers` ветки можно изучать в любом порядке (карта курса — `src/notebooks/course_map.svg`):

- **0. Старт** — Extensions, BaseHaskell, TypeAlgebra
- **I. Функторы** — FunctorHierarchy, FoldableTraversable
- **II. Эффекты** — Monads, MonadTransformers, Comonads, ComonadTransformers
- **III. Структуры и оптики** — AlgebrasCoalgebras, Profunctors, Optics, Arrows
- **IV. Теория категорий** — YonedaLemma, Adjunctions, KanExtensions
- **V. Практика** — MetaProgramming, Concurrency, DistributedHaskell, GPUHaskell
- **VI. Топосы и неопределённость** — Toposes, Uncertainty, SubjectiveModeling

Карта генерируется и не правится руками:

```bash
node src/scripts/coursemap/build_map.js
```

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
