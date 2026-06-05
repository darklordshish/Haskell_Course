import json, hashlib, sys

NB_PATH = '/home/jovyan/MonadTransformers.ipynb'
with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

def cid(s):
    return 'cmp' + hashlib.md5(s.encode()).hexdigest()[:8]

def md(src):
    return {"cell_type":"markdown","id":cid(src),"metadata":{},"source":src}

def code(src):
    return {"cell_type":"code","execution_count":None,"id":cid(src),"metadata":{},"outputs":[],"source":src}

new_cells = []
new_cells.append(md("## 12. Порядок имеет значение: разные композиции одних и тех же трансформеров\n\nДва стека из **одних и тех же** трансформеров в **разном порядке** дают принципиально разные монады.\n\n| Стек | Тип результата | При ошибке/`Nothing` |\n|------|----------------|------------------------|\n| `MaybeT (State s) a` | `State s (Maybe a)` | состояние **сохраняется** |\n| `StateT s Maybe a` | `Maybe (a, s)` | состояние **теряется** |\n| `ExceptT e (State s) a` | `State s (Either e a)` | состояние **сохраняется** |\n| `StateT s (Either e) a` | `Either e (a, s)` | состояние **теряется** |\n| `WriterT w (State s) a` | `State s (a, w)` | состояние внешнее |\n| `StateT s (Writer w) a` | `(a, s, w)` развернуто | лог внешний |\n\n> **Правило:** при сбое внешнего трансформера пропадает всё, что лежит **внутри** него.\n> `T1 (T2 m) a` — при сбое T1 теряется содержимое T2 и m."))
print("Header cell OK, writing...")
