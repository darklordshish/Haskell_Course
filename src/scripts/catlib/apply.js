// Миграция курса на библиотеку категорного ядра (ветка categorical-core-lib).
// Сохраняет весь Phase-14 контент; добавляет :load, библиотечные ячейки и секции 17-18.
const fs = require('fs');
const path = require('path');

const NB_DIR = path.join(__dirname, '..', '..', 'notebooks');
const SRC = __dirname;
const read = f => fs.readFileSync(path.join(SRC, f), 'utf8');

function toLines(s) {
  s = s.replace(/\s+$/, '');
  const parts = s.split('\n');
  return parts.map((x, i) => (i < parts.length - 1 ? x + '\n' : x));
}
const loadNb = n => JSON.parse(fs.readFileSync(path.join(NB_DIR, n), 'utf8'));
const saveNb = (n, nb) => fs.writeFileSync(path.join(NB_DIR, n), JSON.stringify(nb, null, 1) + '\n', 'utf8');
const idxById = (nb, id) => {
  const i = nb.cells.findIndex(c => c.id === id);
  if (i < 0) throw new Error('cell not found: ' + id);
  return i;
};
const getSrc = (nb, i) => nb.cells[i].source.join('');
const setSrc = (nb, i, s) => {
  nb.cells[i].source = toLines(s);
  if (nb.cells[i].cell_type === 'code') { nb.cells[i].outputs = []; nb.cells[i].execution_count = null; }
};
const codeCell = (id, src) => ({ cell_type: 'code', execution_count: null, id, metadata: {}, outputs: [], source: toLines(src) });
const mdCell = (id, src) => ({ cell_type: 'markdown', id, metadata: {}, source: toLines(src) });

// ================= SubjectiveModeling.ipynb =================
{
  const nb = loadNb('SubjectiveModeling.ipynb');

  // setup + миграция четырёх legacy-ячеек на библиотеку
  setSrc(nb, idxById(nb, '5jry916m'), read('sm_setup.txt'));
  setSrc(nb, idxById(nb, 'htb0p13s'), read('sm_s15.hs'));
  setSrc(nb, idxById(nb, 'y5w0bn87'), read('sm_s610.hs'));
  setSrc(nb, idxById(nb, 'yirca393'), read('sm_s1112.hs'));
  setSrc(nb, idxById(nb, 'bu2gr960'), read('sm_s1314.hs'));

  // раздел 2: интервальный билатис (правка markdown + новая code-ячейка)
  {
    const i = idxById(nb, 'tqhh6in8');
    let s = getSrc(nb, i);
    const marker = String.raw`Пара $(L, \bar{L})$ образует **билатис** (bilattice): четыре операции $\max, \min, \bar{\max}, \bar{\min}$ на $[0,1]$ с двумя различными порядками.`;
    if (s.includes(marker)) s = s.replace(marker, read('t4_md.md').replace(/\s+$/, ''));
    else s = s.replace(/\s+$/, '') + '\n\n' + read('t4_md.md').replace(/\s+$/, '');
    setSrc(nb, i, s);
    nb.cells.splice(i + 1, 0, codeCell('cl5bil03', read('sm_bil.hs')));
  }
  // раздел 4: Gamma = Aut квантали
  {
    const i = idxById(nb, '9bhvak76');
    setSrc(nb, i, getSrc(nb, i).replace(/\s+$/, '') + '\n' + read('t5_md.md'));
    nb.cells.splice(i + 1, 0, codeCell('cl5gam04', read('sm_gam.hs')));
  }
  // раздел 7: residuation
  {
    const i = idxById(nb, '1gn0w7ku');
    setSrc(nb, i, getSrc(nb, i).replace(/\s+$/, '') + '\n' + read('t2_md.md'));
    nb.cells.splice(i + 1, 0, codeCell('cl5resd1', read('sm_resd.hs')));
  }
  // раздел 14: честный Bel
  {
    const i = idxById(nb, '6zp1eh4d');
    let s = getSrc(nb, i);
    const a = s.indexOf(String.raw`$\mathcal{P}(X)(E, J(x)) = [x \in E]$;`);
    const endM = String.raw`$\square$`;
    if (a >= 0) {
      const b = s.indexOf(endM, a);
      s = s.slice(0, a) + read('t3_md.md').replace(/\s+$/, '') + s.slice(b + endM.length);
    } else {
      s = s.replace(/\s+$/, '') + '\n\n' + read('t3_md.md').replace(/\s+$/, '');
    }
    setSrc(nb, i, s);
    nb.cells.splice(i + 1, 0, codeCell('cl5bel02', read('sm_bel.hs')));
  }
  // новые секции 17-18 перед итогами
  {
    const i = idxById(nb, 'gznlc5hp');
    nb.cells.splice(i, 0,
      mdCell('cl6mon05', read('t6_md.md')),
      codeCell('cl6mon06', read('sm_mon.hs')),
      mdCell('cl6isb07', read('t7_md.md')),
      codeCell('cl6isb08', read('sm_isb.hs')));
  }
  // TOC: строки 15-18
  {
    const i = idxById(nb, 'vq1fhqjw');
    let s = getSrc(nb, i);
    const row14 = '| 14 | Двойственность Исбелла и гипотеза эквивалентности подходов | Категорное |';
    if (!s.includes(row14)) throw new Error('TOC row14 missing');
    s = s.replace(row14, row14 +
      '\n| 15 | Три сравнительных примера: битопос vs расширения Кана | Практика |' +
      '\n| 16 | Диагностика двигателя: три эксперта | Практика |' +
      '\n| 17 | Монада возможности — поссибилистский двойник монады Гири | Категорное |' +
      '\n| 18 | Обогащённая $\\mathbf{X}$ и нетривиальная двойственность Исбелла | Категорное |');
    setSrc(nb, i, s);
  }
  // Итоги: статус гипотезы + строки 17-18
  {
    const i = idxById(nb, 'gznlc5hp');
    let s = getSrc(nb, i);
    const hypoRow = '| Isbell adjunction $\\mathcal{O} \\dashv \\mathrm{Spec}$ над $[0,1]$ = пара (Pl, Bel) | ⚓ Гипотеза |';
    if (s.includes(hypoRow)) {
      s = s.replace(hypoRow, hypoRow +
        '\n| Кондиционирование = residuation (правый сопряжённый к $\\min(-,a)$) | ✅ Доказано + проверено |' +
        '\n| $\\mathrm{Bel} = \\mathrm{Ran}$ вдоль профунктора дополнения $\\theta J$ | ✅ Дыра закрыта |' +
        '\n| Монада возможности (разд. 17): законы монады | ✅ Проверено численно |' +
        '\n| Isbell-сопряжение на обогащённой $\\mathbf{X}$ (разд. 18) | ✅ Проверено численно |');
    }
    s = s.replace(/\s+$/, '') +
      '\n\nС ветки categorical-core-lib весь код ноутбука — вызовы библиотеки `lib/`' +
      ' (канонический источник: https://github.com/darklordshish/SubjectiveModeling,' +
      ' cabal-пакет с 33 тестами законов и двумя примерами).';
    setSrc(nb, i, s);
  }
  saveNb('SubjectiveModeling.ipynb', nb);
  console.log('SubjectiveModeling: cells', nb.cells.length);
}

// ================= Uncertainty.ipynb =================
{
  const nb = loadNb('Uncertainty.ipynb');
  setSrc(nb, idxById(nb, '82e4316c'), read('un_setup.txt'));
  // S4 + S7: добавки из библиотеки
  for (const [id, f] of [['ef70654e', 'un_s4_append.hs'], ['2ec203a5', 'un_s7_append.hs']]) {
    const i = idxById(nb, id);
    setSrc(nb, i, getSrc(nb, i).replace(/\s+$/, '') + '\n' + read(f));
  }
  // мост из 9.x к библиотеке
  {
    const i = idxById(nb, 'sec9_bridge');
    let s = getSrc(nb, i);
    if (!s.includes('darklordshish/SubjectiveModeling')) {
      s = s.replace(/\s+$/, '') +
        '\n\nОбщее ядро двух теорий вынесено в библиотеку `lib/` (канонический источник —' +
        ' [darklordshish/SubjectiveModeling](https://github.com/darklordshish/SubjectiveModeling)):' +
        ' bind монады распределений над полукольцом (max, min) — это в точности pl-интеграл,' +
        ' см. раздел 17 в [SubjectiveModeling.ipynb](SubjectiveModeling.ipynb); сравнение' +
        ' цепей над (max,min) / (+,×) / (∨,∧) — в конце раздела 7 этого ноутбука.';
      setSrc(nb, i, s);
    }
  }
  saveNb('Uncertainty.ipynb', nb);
  console.log('Uncertainty: cells', nb.cells.length);
}
console.log('COURSE APPLY DONE');
