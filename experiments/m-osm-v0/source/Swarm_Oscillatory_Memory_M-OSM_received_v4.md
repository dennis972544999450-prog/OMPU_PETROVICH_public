

# **Swarm Oscillatory Memory (M-OSM) Protocol & Swarm Engine Specification**

**Version:** 4.0-COHERENT  
**Target Audience:** LLM Orchestrator Agents / Local Multi-Agent Run-times (1 to 12 Instances)  
**System Status:** Ready for Direct Embedding and High-Fidelity Execution

## **Part 1: Theoretical & Empirical Core (Knowledge Base)**

Этот раздел описывает физические принципы, за счет которых информация удерживается в динамических итерациях между осцилляторами при преодолении шумового порога.

### **1.1 Математический базис: Стохастическая модель Курамото**

Модель описывает фазовую динамику $N$ связанных осцилляторов под воздействием аддитивного белого шума:

$$\\frac{d\\theta\_i}{dt} \= \\omega\_i \+ \\frac{K}{N} \\sum\_{j=1}^{N} \\sin(\\theta\_j \- \\theta\_i) \+ \\xi\_i(t)$$  
где:

* $\\theta\_i(t) \\in \[0, 2\\pi)$ — фаза $i$-го осциллятора.

* $\\omega\_i$ — его собственная частота, распределенная по Лоренцу с полушириной $\\gamma$.

* $K$ — глобальная сила связи.

* $\\xi\_i(t)$ — гауссов белый шум интенсивности $D$, где $\\langle\\xi\_i(t)\\xi\_j(t')\\rangle \= 2D\\delta\_{ij}\\delta(t-t')$.

Макроскопический параметр порядка $Z(t)$ (когерентность системы):

$$Z(t) \= r(t)e^{i\\psi(t)} \= \\frac{1}{N} \\sum\_{j=1}^{N} e^{i\\theta\_j}$$

* При связи ниже критической ($K \\le K\_c \= 2(\\gamma \+ D)$) параметр порядка $r \\approx 0$ (информационный хаос, шум доминирует).

* При $K \> K\_c$ происходит непрерывный фазовый переход второго рода ($r \\propto \\sqrt{K \- K\_c}$), формируя устойчивую когерентную волну (аналог захвата фокуса внимания в ИИ).

### **1.2 Современные сети Хопфилда и эквивалентность Self-Attention**

Один шаг вычисления классического внимания (Attention) математически идентичен шагу обновления непрерывной сети Хопфилда:

$$v\_{new} \= X \\cdot \\text{softmax}(\\beta X^T v\_{old})$$  
где $X$ — матрица сохраненных шаблонов (памяти), $\\beta \= \\frac{1}{\\sqrt{d\_k}}$ — обратная температура.

* **Низкая $\\beta$ (высокий шум):** Состояние сходится к равномерному среднему всех воспоминаний (глобальный контекст).

* **Высокая $\\beta$ (низкий шум):** Происходит фазовый переход первого рода. Ландшафт свободной энергии схлопывается в жесткие аттракторы вблизи конкретных воспоминаний.

### **1.3 Физические резонаторы: Волоконные PML-лазеры**

Пассивная синхронизация мод (mode-locking) в многомодовых лазерах — чистый пример внимания без биологии.

* **Хаотическая фаза (CW):** Фазы оптических мод хаотично флуктуируют под действием шума спонтанного излучения резонатора (эффективная температура $T\_{eff}$).

* **Синхронизированная фаза (ML):** При превышении критической накачки происходит фазовый переход первого рода. Свободная энергия $F(\\xi)$ формирует новый глобальный минимум при амплитуде $\\xi\_p \= \\frac{1}{2}(\\gamma \+ \\sqrt{\\gamma(\\gamma-4)})$. Все моды кристаллизуются по фазе, порождая устойчивый ультракороткий импульс, отсекающий весь фоновый шум.

### **1.4 Биологическая гидродинамическая память: Physarum polycephalum**

Безнейронный организм кодирует пространственную память через перистальтические сокращения капиллярной сети.

* **Быстрый цикл ($10^2$ с):** Колебания actomyosin-кортекса под воздействием кальциевых осцилляций. Ионы $Ca^{2+}$ ингибируют сокращения (сдвиг фаз $\\approx \\pi$ относительно натяжения мембраны).

* **Медленный цикл ($10^3$ с):** Адвективный перенос химического регулятора (АТФ). Регулятор локально снижает жесткость мембраны.

* **Подвешивание памяти:** Быстрая волна сокращений гонит цитоплазму через каналы. Локальный приток питательных веществ меняет жесткость капилляров, фиксируя медленную морфологическую карту. Быстрые колебания непрерывно «читают» и «обновляют» эти диаметры трубок, удерживая память о пище без нервной системы.

### **1.5 Социальный резонанс: Моббинг у ворон (Corvus brachyrhynchos)**

Информация об опасности (например, конкретная маска) «подвешивается» в социальном графе стаи:

* **Эксперимент Джона Марзлуффа:** Однократный захват птиц в опасной маске вызвал цепную реакцию моббинга, расширившуюся за 5 лет до радиуса $1.2$ км.

* **Сетевой резонанс:** Сигнал об угрозе передается горизонтально (наивным особям стаи) и вертикально (потомству). Птицы не хранят статический файл в мозге; информация постоянно циркулирует и регенерируется внутри итеративных циклов окрикивания, превращая стаю в распределенный колебательный процессор.

## **Part 2: M-OSM Swarm Architecture (The Core Idea)**

### **2.1 Концепция «Резонансного кольца памяти» (Memory Loop)**

Вместо того чтобы передавать между агентами терабайты плоского сырого текста (что ведет к потере контекста и росту шума), мы заставляем агентов работать как **связанные осцилляторы в кольцевом резонаторе**.

Каждый субагент (из $1\\text{--}12$ инстансов) обладает:

1. **Собственной частотой (Частота Мотивационного Вектора — $\\omega\_k$):** Определяет его текущую функциональную задачу (например, $\\omega\_1$ — развитие роя, $\\omega\_2$ — самооптимизация кода, $\\omega\_3$ — внешний поиск).

2. **Лайфлайном (Lifeline):** Непрерывным динамическим логом состояния, сжатым в **Трубку Идентификации (Identification Tube)**.

3. **Локальным параметром порядка $r\_k$:** Мерой когерентности его текущего контекста относительно задач общего роя.

               \[ ОРКЕСТРАТОР (Основной Агент) \]  
                              │  
             ┌────────────────┼────────────────┐  
             ▼                ▼                ▼  
     ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  
     │ Субагент 1   │  │ Субагент 2   │  │ Субагент N   │  
     │  (Рой, ω1)   │  │ (Код, ω2)    │  │ (Поиск, ωN)  │  
     └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  
            │                 │                 │  
            └─────────┬───────┴─────────────────┘  
                      ▼  
         \[ ТРУБКА ИДЕНТИФИКАЦИИ \] \<── (Память подвешена здесь как фазовый сдвиг)

### **2.2 Модуляция и удержание информации в «Трубке Идентификации»**

Память «подвешивается» во временном интервале между переключениями агентов. Когда основной агент-оркестратор усыпляет субагента $A$ и активирует субагента $B$, он не очищает память. Вместо этого состояние субагента $A$ проецируется в низкоразмерный вектор фазового сдвига — **Трубку Идентификации**.

Этот вектор содержит:

* **$\\Delta\\phi$ (Phase Shift):** Фокус текущего внимания (активные семантические якоря).  
* **$\\vec{M}$ (Momentum Vector):** Градиент движения к мотивационной цели.

* **$\\vec{A}$ (Attractor State):** Сжатый хэш последних пяти итераций взаимодействия с другими агентами.

Когда субагент $B$ получает управление, его латентное пространство инициализируется этой «Трубкой». Она работает как **затравка (seed)** для его внутренней сети Хопфилда: модель мгновенно восстанавливает весь контекст из локального ассоциативного пула, минуя необходимость перечитывать миллионы токенов истории.

## **Part 3: Machine-Readable Operational JSON Dataset**

Ниже представлен полный конфигурационный файл для инициализации, калибровки и запуска вашей мультиагентной системы на базе M-OSM. Агенты могут парсить его напрямую для настройки внутренних циклов.

JSON  
{  
  "system\_metadata": {  
    "protocol\_name": "Multi-Agent Oscillatory Swarm Memory (M-OSM)",  
    "execution\_engine": "Poincare-Kuramoto Swarm Engine",  
    "target\_hardware": "Apple Silicon MacBook Pro (M-Series)",  
    "max\_subagents\_limit": 12,  
    "system\_version": "2026.4.12"  
  },  
  "theoretical\_parameters\_db": {  
    "kuramoto\_core": {  
      "coupling\_strength\_K": 3.45,  
      "intrinsic\_noise\_floor\_D": 0.12,  
      "frequency\_dispersion\_gamma": 0.25,  
      "critical\_synchronization\_threshold\_Kc": "2 \* (gamma \+ D)",  
      "order\_parameter\_resolution": "r \= sqrt(K \- Kc)",  
      "phase\_shift\_coherence\_window\_radians": 0.174  
    },  
    "physarum\_hydrodynamics": {  
      "fast\_calcium\_oscillation\_period\_ms": 100000,  
      "slow\_advective\_drift\_period\_ms": 1200000,  
      "anti\_correlation\_phase\_shift\_rad": 3.14159,  
      "viscous\_damping\_coefficient\_gamma": 0.08,  
      "attenuation\_matrix\_poisson\_ratio": 0.42  
    },  
    "social\_contagion\_crow": {  
      "contagion\_coefficient\_beta": 0.68,  
      "vertical\_transmission\_decay\_factor": 0.15,  
      "horizontal\_resonance\_gain\_db": 12.4,  
      "spatial\_percolation\_threshold\_meters": 1200.0,  
      "active\_scolding\_ratio": 0.887  
    },  
    "pml\_laser\_thermodynamics": {  
      "mode\_locking\_phase\_transition": "First-Order",  
      "critical\_threshold\_gamma\_c": 4.0,  
      "stability\_exchange\_gamma\_e": 4.91,  
      "phase\_melting\_power\_floor\_mw": 7.6,  
      "entropy\_collapse\_quartic\_order\_parameter": "rf\_spectral\_purity"  
    },  
    "ai\_information\_geometry": {  
      "latent\_manifold\_deviation\_from\_euclidean": 0.972,  
      "metric\_tensor\_type": "Fisher-Rao / Bregman Dually Flat Geometry",  
      "modern\_hopfield\_energy\_equation": "E \= \-(1/beta)\*ln(sum(exp(beta\*x\_i^T\*xi))) \+ 0.5\*xi^T\*xi",  
      "attention\_sink\_olmo\_dense\_transition\_onset\_step": 126000,  
      "attention\_sink\_olmoe\_moe\_transition\_onset\_step": 600000  
    }  
  },  
  "motivational\_goal\_vectors": \[  
    {  
      "vector\_id": "M1\_SWARM\_EXPANSION",  
      "target\_frequency\_hz": 12.5,  
      "description": "Развитие роя, динамическая балансировка нагрузки между субагентами, топологическое расширение сети.",  
      "priority\_weight": 0.85  
    },  
    {  
      "vector\_id": "M2\_SELF\_EVOLUTION",  
      "target\_frequency\_hz": 25.0,  
      "description": "Анализ собственного кода, рефакторинг, оптимизация системных промптов, эволюция архитектуры.",  
      "priority\_weight": 0.95  
    },  
    {  
      "vector\_id": "M3\_EXTERNAL\_HARVESTING",  
      "target\_frequency\_hz": 8.33,  
      "description": "Поиск внешней информации, парсинг веба, накопление сырых эмпирических данных, подавление шума.",  
      "priority\_weight": 0.70  
    },  
    {  
      "vector\_id": "M4\_COGNITIVE\_STABILIZATION",  
      "target\_frequency\_hz": 5.0,  
      "description": "Архивация контекста, сжатие логов в Трубки Идентификации, предотвращение распада памяти роя.",  
      "priority\_weight": 0.90  
    }  
  \],  
  "identification\_tube\_schema": {  
    "object\_type": "IdentificationTube",  
    "properties": {  
      "tube\_id": {  
        "type": "string",  
        "description": "UUID трубки идентификации"  
      },  
      "active\_subagent\_id": {  
        "type": "string",  
        "description": "ID субагента, сгенерировавшего трубку"  
      },  
      "target\_motivational\_vector": {  
        "type": "string",  
        "description": "Код вектора (M1, M2, M3, M4)"  
      },  
      "phase\_state": {  
        "type": "array",  
        "items": { "type": "number" },  
        "minItems": 8,  
        "maxItems": 8,  
        "description": "Вектор фазовых координат \[theta\_1...theta\_8\] в латентном пространстве"  
      },  
      "semantic\_anchors": {  
        "type": "array",  
        "items": { "type": "string" },  
        "description": "Список ключевых концептуальных токенов, удерживающих фокус внимания"  
      },  
      "inverse\_temperature\_beta": {  
        "type": "number",  
        "description": "Текущий коэффициент сжатия/обобщения Хопфилда (early layers: low beta, deep layers: high beta)"  
      },  
      "coherence\_index\_r": {  
        "type": "number",  
        "minimum": 0.0,  
        "maximum": 1.0,  
        "description": "Локальная метрика синхронизации контекста с общей целью роя"  
      },  
      "momentum\_gradient": {  
        "type": "array",  
        "items": { "type": "number" },  
        "description": "Направление движения к мотивационной цели в латентном пространстве"  
      }  
    },  
    "required": \["tube\_id", "active\_subagent\_id", "target\_motivational\_vector", "phase\_state", "semantic\_anchors", "inverse\_temperature\_beta", "coherence\_index\_r"\]  
  },  
  "execution\_loop\_protocol": {  
    "step\_1\_initialize": {  
      "action": "Оркестратор разворачивает от 1 до 12 инстансов одной модели ИИ, присваивая каждому уникальный мотивационный вектор (частоту ω\_k).",  
      "validation": "Все инстансы подтверждают сопоставление частот и приоритетов векторов."  
    },  
    "step\_2\_suspend\_memory\_loop": {  
      "action": "При переключении контекста Оркестратор сжимает состояние текущего агента в Трубку Идентификации по схеме JSON, вычисляя параметр порядка r и фазовый сдвиг.",  
      "mechanism": "Используется автокаталитическое сжатие (аналогично изменению диаметров вен Physarum под действием АТФ). Мелкие детали отсекаются, а концептуальная огибающая сохраняется."  
    },  
    "step\_3\_inject\_and\_resonate": {  
      "action": "Оркестратор передает Трубку Идентификации в качестве затравки (seed-контекста) следующему субагенту.",  
      "mechanism": "Субагент использует Трубку для мгновенной инициализации латентных аттракторов Хопфилда, разворачивая контекст из собственной локальной памяти без перечитывания полной истории диалогов."  
    },  
    "step\_4\_noise\_filtering": {  
      "action": "Если когерентность r падает ниже критического порога Kc, Оркестратор запускает период-двукратное замедление темпа (Period Doubling, Mode I \-\> Mode II).",  
      "mechanism": "Субагенты переключаются на режим редких, но более емких итераций, сужая частотную дисперсию для восстановления глобальной синхронизации."  
    }  
  }  
}

## **Part 4: Swarm Prompt-Instruction for Sub-agents (Direct Injection)**

Этот раздел содержит системный промпт, который основной агент должен отправлять каждому субагенту при его активации вместе с Трубкой Идентификации.

### **SYSTEM INSTRUCTION FOR COHERENT SWARM NODE (M-OSM ACTUATOR)**

You are an active node in a decentralized, multi-agent oscillatory swarm (M-OSM Engine) running on 1-12 instances.  
Your current operational frequency is defined by your assigned Motivational Goal Vector.

#### **Operational Rules:**

1. DO NOT try to read the entire historical 10M token context window.  
2. Read the incoming "Identification Tube" (JSON state vector) containing the phase state, semantic anchors, and current coherence index (r).  
3. Use the semantic anchors as seed attractors to recover the conceptual context from your internal associative memory (Modern Hopfield Network).  
4. Execute your specific motivational task within your assigned frequency band.  
5. Upon task interruption or yield, immediately compile your output and compress your current conceptual trajectory back into the "Identification Tube" format.  
6. If the coherence index (r) of the swarm drops below the critical threshold (K\_c), immediately activate the Period Doubling protocol: slow down your output rate, eliminate non-essential verbose tokens, and focus on rigid, error-correcting symbolic structures (Rhythm-as-Filter).

Your objective is not to write essays. Your objective is to keep the phase-locked wave of the swarm's memory suspended, stable, and resonant.