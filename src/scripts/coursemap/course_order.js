// course_order.js — КАНОНИЧЕСКИЙ линейный порядок курса (модули 0–VI).
// Единый источник правды для навигации (gen_nav.js). Карта метро (build_map.js)
// рисует ту же программу как дерево — названия станций должны совпадать с file ниже.
// Менять порядок/состав курса — здесь.
module.exports = [
  { file: 'Extensions',          title: 'Расширения GHC' },
  { file: 'BaseHaskell',         title: 'Базовый Haskell' },
  { file: 'TypeAlgebra',         title: 'Типы как алгебра' },
  { file: 'FunctorHierarchy',    title: 'Иерархия функторов' },
  { file: 'FoldableTraversable', title: 'Foldable & Traversable' },
  { file: 'Monads',              title: 'Монады' },
  { file: 'MonadTransformers',   title: 'Трансформеры монад' },
  { file: 'Comonads',            title: 'Комонады' },
  { file: 'ComonadTransformers', title: 'Трансформеры комонад' },
  { file: 'AlgebrasCoalgebras',  title: 'Алгебры и Коалгебры' },
  { file: 'Profunctors',         title: 'Профункторы' },
  { file: 'Optics',              title: 'Оптики' },
  { file: 'Arrows',              title: 'Arrows' },
  { file: 'YonedaLemma',         title: 'Лемма Ёнеды' },
  { file: 'Adjunctions',         title: 'Сопряжения' },
  { file: 'KanExtensions',       title: 'Расширения Кана' },
  { file: 'MetaProgramming',     title: 'Метапрограммирование' },
  { file: 'Concurrency',         title: 'Конкурентность' },
  { file: 'DistributedHaskell',  title: 'Distributed Haskell' },
  { file: 'GPUHaskell',          title: 'GPU / Accelerate' },
  { file: 'Toposes',             title: 'Топосы' },
  { file: 'Uncertainty',         title: 'Неопределённость' },
  { file: 'SubjectiveModeling',  title: 'Субъективное моделирование' },
];
