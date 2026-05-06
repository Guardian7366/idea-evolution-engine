const es = {
  app: {
    languageSwitch: {
      ariaLabel: "Selector de idioma visual",
      es: "ES",
      en: "EN",
    },
  },
  header: {
    pills: {
      workspace: "Living Evolution Workspace",
      system: "Frutiger-inspired creative system",
    },
    kicker: "Creative flow orchestration",
    title: "Idea Evolution Engine",
    subtitle:
      "Sistema guiado para incubar una idea, ramificar variantes, transformar versiones y consolidar una síntesis final dentro de un entorno creativo vivo.",
    badges: {
      seed: "Seed",
      branch: "Branch",
      evolve: "Evolve",
    },
    zones: {
      zone1Label: "Zona 01",
      zone1Value: "Incubación",
      zone2Label: "Zona 02",
      zone2Value: "Transformación",
      zone3Label: "Zona 03",
      zone3Value: "Síntesis",
    },
  },
  slides: {
    hero: {
      label: "Inicio del entorno",
      shortLabel: "Inicio",
    },
    system: {
      label: "Control del sistema",
      shortLabel: "Control",
    },
    seed: {
      label: "Incubación de idea",
      shortLabel: "Idea",
    },
    branch: {
      label: "Variantes iniciales",
      shortLabel: "Variantes",
    },
    core: {
      label: "Transformación principal",
      shortLabel: "Transformar",
    },
    evolution: {
      label: "Mapa e historial",
      shortLabel: "Evolución",
    },
    analysis: {
      label: "Comparación y análisis",
      shortLabel: "Análisis",
    },
    synthesis: {
      label: "Síntesis final",
      shortLabel: "Síntesis",
    },
  },
  viewport: {
    ariaLabel: "Viewport de slides del workspace",
    previousSlide: "Slide anterior",
    nextSlide: "Slide siguiente",
    previous: "Anterior",
    next: "Siguiente",
  },
    workspaceNavbar: {
    ariaLabel: "Navegación horizontal del workspace",
    deckBadge: "Navigation deck",
    linkedSlidesBadge: "{{count}} linked slides",
    orchestrationLabel: "Horizontal orchestration",
    available: "Disponible",
    blockedByFlow: "Bloqueado por flujo",
  },
  workspaceHero: {
    badges: {
      creativeEvolution: "Creative evolution",
      systemContinuity: "System continuity",
      livingWorkspace: "Living workspace",
    },
    kicker: "Main orchestration zone",
    title: "Un entorno para hacer que las ideas respiren, cambien y maduren.",
    description:
      "El flujo principal del MVP ya permite crear sesiones, registrar ideas, generar variantes, seleccionar versiones, transformarlas, analizarlas y sintetizarlas, pero ahora organizado como un sistema más vivo, más claro y más memorable.",
    bannerAlt: "Banner visual de Idea Evolution Engine",
    stages: {
      stage1: {
        badge: "Etapa 1",
        title: "Incubación inicial",
        description:
          "Define el contenedor de trabajo y registra la semilla creativa que dará origen al flujo.",
      },
      stage2: {
        badge: "Etapa 2",
        title: "Ramificación y foco",
        description:
          "Explora alternativas, elige una dirección prometedora y conviértela en versión viva del sistema.",
      },
      stage3: {
        badge: "Etapa 3",
        title: "Transformación y cierre",
        description:
          "Evoluciona, compara, analiza y consolida una síntesis estructurada del resultado final.",
      },
    },
  },
    sectionCard: {
    eyebrowPrimary: "Zona del sistema",
    eyebrowSecondary: "Idea Evolution Engine",
  },
  workspaceSystem: {
    kicker: "System controls",
    title: "Control y contexto del entorno",
  },
  languageSelector: {
    title: "Idioma del flujo",
    description:
      "Configura cómo debe comportarse el sistema al interpretar y producir contenido durante las operaciones de IA.",
    badges: {
      control: "Language control",
    },
    hints: {
      es: "Idioma fijo: Español",
      en: "Fixed language: English",
      auto: "Detección automática activa",
    },
    outputMode: "Output mode",
    modeLabel: "Modo de idioma",
    options: {
      auto: "Auto detectar",
      es: "Español",
      en: "English",
    },
    descriptions: {
      es: "El sistema responderá forzando español en las operaciones principales de IA.",
      en: "The system will force English for the main AI operations.",
      auto: "El sistema detectará automáticamente el idioma más conveniente según el contexto.",
    },
    expectedBehaviorTitle: "Comportamiento esperado",
    behaviors: {
      auto: {
        title: "Auto",
        description: "El sistema decide el idioma más conveniente según el contexto.",
      },
      manual: {
        title: "Manual",
        description: "Fuerza consistencia lingüística en variantes, análisis y síntesis.",
      },
    },
  },
  flowStatus: {
    title: "Estado del flujo",
    description:
      "Monitorea el estado actual del workspace y ubica rápidamente los identificadores clave del proceso.",
    clearWorkspace: "Limpiar workspace local",
    badges: {
      status: "Flow status",
    },
    states: {
      processing: "Procesando...",
      ready: "Listo",
    },
    controlBoard: "Control board",
    items: {
      session: {
        label: "Sesión",
        empty: "Sin sesión todavía.",
      },
      idea: {
        label: "Idea",
        empty: "Sin idea todavía.",
      },
      activeVersion: {
        label: "Versión activa",
        empty: "Sin versión activa todavía.",
      },
    },
    operationalStateTitle: "Estado operativo",
    operationalMessages: {
      active: "El sistema está listo para continuar el flujo o ejecutar una nueva operación.",
      empty: "Todavía no hay un flujo activo. Crea una sesión para comenzar el recorrido.",
    },
  },
    workspaceSeed: {
    kicker: "Seed stage",
    title: "Incubación de la sesión y la idea base",
  },
  ideaInput: {
    contextLabel: "Contexto",
    session: {
      badges: {
        container: "Seed container",
        stage: "Stage 01",
      },
      title: "Crear sesión",
      description:
        "Define el contenedor inicial del proceso. Esta sesión será el punto de partida donde vivirá la evolución completa de la idea.",
      status: "Inicio",
      fields: {
        titleLabel: "Título de la sesión",
        titlePlaceholder: "Escribe un título para la sesión",
      },
      hint: {
        title: "Espacio maestro",
        description:
          "Aquí nace el contenedor del flujo. Todo lo demás depende de que esta base exista primero.",
      },
      footerText:
        "Esta acción prepara el espacio base para el flujo creativo y habilita la captura de la idea semilla.",
      submit: "Crear sesión",
    },
    idea: {
      badges: {
        seed: "Creative seed",
        stage: "Stage 02",
      },
      title: "Registrar idea",
      description:
        "Introduce la idea base que el sistema usará para generar ramificaciones, transformaciones y una síntesis final más clara.",
      status: "Núcleo",
      fields: {
        titleLabel: "Título de la idea",
        titlePlaceholder: "Escribe un título para la idea",
        contentLabel: "Contenido de la idea",
        contentPlaceholder: "Describe tu idea principal",
      },
      hint: {
        title: "Semilla creativa",
        description:
          "Mientras más clara sea la formulación inicial, más potentes y útiles serán las variantes y transformaciones posteriores.",
      },
      footerNeedsSession: "Primero necesitas una sesión para activar esta etapa.",
      footerReady: "Esta idea se convertirá en la semilla que alimentará el resto del sistema.",
      submit: "Registrar idea",
    },
  },
    emptyState: {
    initialState: "Estado inicial",
    waitingState: "Waiting state",
  },
  workspaceBranch: {
    kicker: "Branch stage",
    title: "Direcciones iniciales de evolución",
  },
  variantsList: {
    title: "Variantes generadas",
    description:
      "Explora distintas direcciones nacidas de la idea base y elige la que merezca convertirse en el siguiente foco de evolución.",
    empty: {
      title: "Todavía no se han generado variantes",
      description:
        "Cuando registres una idea, aquí aparecerán distintas bifurcaciones iniciales para comenzar la evolución del flujo.",
    },
    badges: {
      branchStage: "Branch stage",
      alternatives: "{{count}} alternativas",
      guidedSelection: "Selección guiada",
    },
    routesSlide: "Slide de rutas",
    mainDescription:
      "Aquí defines la primera gran dirección del sistema. Solo una variante puede convertirse en la siguiente versión viva del flujo.",
    currentStateLabel: "Estado actual",
    currentState: {
      selected: "Ya existe una ruta elegida",
      waiting: "Esperando selección",
    },
  },
  variantCard: {
    routeBadge: "Ruta {{index}}",
    variantBadge: "Variante",
    selectedBadge: "Seleccionada",
    availableBadge: "Disponible",
    branchLabel: "Branch",
    proposedDirectionLabel: "Dirección propuesta",
    functionLabel: "Función",
    function: {
      selected: "Ruta gobernante",
      candidate: "Ruta candidata",
    },
    resultLabel: "Resultado",
    result: {
      selected: "Convertida en foco actual",
      available: "Puede volverse versión real",
    },
    footer: {
      selected: "Esta bifurcación ya fue convertida en la dirección elegida del sistema.",
      available: "Selecciona esta ruta para convertirla en una versión viva del flujo.",
    },
    actions: {
      selected: "Ruta elegida",
      select: "Elegir esta ruta",
    },
  },
    workspaceCore: {
    kicker: "Core stage",
    title: "Versión enfocada y motor de transformación",
  },
  activeVersion: {
    title: "Versión enfocada",
    description:
      "Este es el núcleo actual que estás observando dentro del sistema. Puede ser la versión activa real o una versión enfocada temporalmente para inspección.",
    empty: {
      title: "Sin versión seleccionada todavía",
      description:
        "Cuando exista una versión activa o enfoques una desde el historial o el grafo, aquí aparecerá el núcleo textual actual del flujo.",
    },
    badges: {
      coreVersion: "Core version",
      versionNumber: "Versión {{number}}",
      realActive: "Activa real",
      inspection: "En inspección",
    },
    headers: {
      realActive: "Punto actual de evolución",
      inspection: "Versión enfocada para observación",
    },
    messages: {
      realActive:
        "Esta versión representa el estado real y vigente del flujo creativo en este momento.",
      inspection:
        "Esta versión fue enfocada desde el historial o el grafo para revisar su contenido sin reemplazar todavía a la activa.",
    },
    visualModeLabel: "Modo visual",
    visualModes: {
      activeCore: "Core activo",
      temporaryInspection: "Inspección temporal",
    },
    info: {
      versionId: "Identificador de versión",
      appliedTransformation: "Transformación aplicada",
      versionNumber: "Número de versión",
    },
    contentBadges: {
      versionContent: "Version content",
      readableCore: "Readable core",
      currentState: "Estado vigente",
      focusedView: "Vista enfocada",
    },
    centralContentLabel: "Contenido central",
  },
  versionTransform: {
    title: "Motor de transformación",
    description:
      "Aplica operaciones sobre la versión activa para expandirla, desviarla o refinarla con una intención más precisa.",
    empty: {
      title: "Primero necesitas una versión activa",
      description:
        "Selecciona una variante para crear la primera versión y desbloquear el motor de transformación.",
    },
    badges: {
      engine: "Transformation engine",
      versionNumber: "Versión {{number}}",
      active: "Activa",
    },
    activeDescription:
      "La versión activa es el punto vigente del flujo. Desde aquí puedes hacerla crecer de forma progresiva, empujarla hacia una dirección más arriesgada o corregirla mediante una instrucción controlada.",
    liveNodeLabel: "Nodo vivo del sistema",
    actionHintLabel: "Ideal para",
    languageModes: {
      en: "English mode",
      es: "Modo español",
      auto: "Auto mode",
    },
    evolution: {
      badgePrimary: "Evolución",
      badgeSecondary: "Cambio progresivo",
      title: "Profundizar la línea actual",
      description:
        "Mantiene la dirección conceptual y la vuelve más madura, más rica y mejor desarrollada.",
      hintTitle: "Estabilidad con crecimiento",
      hintDescription:
        "cuando ya encontraste una ruta valiosa y quieres fortalecerla sin romper su identidad.",
      action: "Aplicar evolución",
    },
    mutation: {
      badgePrimary: "Mutación",
      badgeSecondary: "Cambio disruptivo",
      title: "Desviar el curso creativo",
      description:
        "Introduce una alteración más agresiva para abrir nuevas trayectorias y descubrir posibilidades menos obvias.",
      hintTitle: "Exploración radical",
      hintDescription:
        "cuando sientes que la dirección actual necesita una sacudida o una lectura inesperada.",
      action: "Aplicar mutación",
    },
    refinement: {
      badgePrimary: "Refinamiento guiado",
      badgeTertiary: "Control fino",
      title: "Precisar cómo debe mejorar",
      description:
        "Usa una instrucción clara para decir qué debe conservar, corregir, resumir, ampliar o enfatizar la siguiente versión.",
      instructionLabel: "Instrucción de refinamiento",
      placeholder: "Escribe cómo quieres refinar la versión actual",
      usageTitle: "Sugerencia de uso",
      tips: {
        clarity: {
          title: "Mejorar claridad",
          description: "Pide una versión más concreta, directa y fácil de entender.",
        },
        focus: {
          title: "Cambiar enfoque",
          description: "Indica el contexto objetivo: académico, negocio, producto o usuario.",
        },
        depth: {
          title: "Controlar profundidad",
          description:
            "Especifica si quieres resumir, expandir, ordenar o enfatizar partes clave.",
        },
      },
      footerText:
        "Mientras más específica sea la instrucción, más control tendrás sobre el siguiente resultado del sistema.",
      action: "Aplicar refinamiento",
    },
    processingBadge: "Procesando",

    successOverlay: {
      evolution: "Evolución aplicada",
      mutation: "Mutación aplicada",
      refinement: "Refinamiento aplicado",
      versionNumber: "Nueva versión {{number}}",
    },
  },
    workspaceEvolution: {
    kicker: "Evolution stage",
    title: "Recorrido histórico y mapa de crecimiento",
  },
  versionHistory: {
    title: "Historial de versiones",
    description:
      "Recorre las etapas que ha atravesado la idea y observa cómo fue cambiando a través del tiempo.",
    actions: {
      expandAll: "Expandir todo",
      collapseAll: "Colapsar todo",
      viewFull: "Ver completa",
      hideDetail: "Ocultar detalle",
      focus: "Enfocar",
      alreadyActive: "Ya activa",
      makeActive: "Hacer activa",
      expandVersionAria: "Expandir versión {{number}}",
      collapseVersionAria: "Colapsar versión {{number}}",
    },
    empty: {
      title: "Todavía no hay versiones generadas",
      description:
        "Cuando selecciones una variante y empieces a transformar la idea, aquí aparecerá su recorrido evolutivo.",
    },
    badges: {
      trail: "Evolution trail",
      records: "{{count}} registros",
      timeline: "Timeline conceptual",
    },
    liveHistory: "Historial vivo",
    intro:
      "Aquí puedes revisar de forma lineal cada etapa creada, enfocarla para lectura o volver a activarla como núcleo actual del flujo.",
    versionBadge: "Versión {{number}}",
    activeBadge: "Activa",
    selectedBadge: "Seleccionada",
    compactViewBadge: "Vista compacta",
    expandedViewBadge: "Vista expandida",
    stateLabels: {
      current: "Estado actual",
      observing: "Nodo en observación",
      previous: "Registro previo",
    },
    stateMessages: {
      current: "Esta versión representa el estado real y vigente del flujo creativo.",
      observing: "Esta versión fue enfocada para inspección y lectura contextual.",
      previous: "Esta etapa forma parte del camino previo de evolución.",
    },
    meta: {
      position: "Posición",
      node: "Nodo {{index}}",
      origin: "Origen",
      state: "Estado",
      identity: "Identidad",
    },
    origin: {
      root: "Inicio del historial",
      derived: "Deriva de una etapa previa",
    },
    states: {
      governing: "Gobierna el flujo",
      reading: "En lectura",
      archived: "Archivada",
    },
    content: {
      stageContent: "Stage content",
      compactView: "Vista resumida",
      readableSnapshot: "Readable snapshot",
      hiddenTemporarily: "Contenido oculto temporalmente",
      stageLabel: "Contenido de esta etapa",
      compactMessagePrefix:
        "Esta versión está compactada para mantener limpio el historial. Usa",
      compactMessageSuffix: "para desplegar todo su contenido.",
    },
  },
  versionGraph: {
    title: "Mapa de evolución",
    description:
      "Observa visualmente cómo se ramificó y transformó la idea a través de sus distintas versiones.",
    empty: {
      title: "Todavía no hay versiones para visualizar",
      description:
        "Cuando selecciones una variante y comiences a transformar la idea, aquí verás el mapa de evolución.",
    },
    badges: {
      visualMap: "Visual evolution map",
      potentialNodes: "{{count}} nodos potenciales",
      interactivePath: "Recorrido interactivo",
    },
    graphView: "Graph view",
    intro:
      "El mapa queda aquí como un módulo de observación. Puedes usarlo para detectar ramificaciones, revisar conexiones entre versiones y reactivar un nodo previo.",
    node: {
      versionBadge: "V{{number}}",
      titles: {
        active: "Nodo activo",
        focused: "Nodo enfocado",
        evolutionary: "Nodo evolutivo",
      },
      messages: {
        active: "Representa el estado real actual del sistema.",
        focused: "Está seleccionado para inspección.",
        evolutionary: "Forma parte del mapa de crecimiento.",
      },
      badges: {
        active: "Activa",
        selected: "Seleccionada",
      },
    },
    detail: {
      badges: {
        nodeInspection: "Node inspection",
        interactiveFocus: "Interactive focus",
        reactivationControl: "Control de reactivación",
      },
      title: "Detalle del nodo seleccionado",
      description:
        "Haz clic sobre un nodo para revisar su información principal y decidir si debe convertirse en la nueva versión activa del flujo.",
      actions: {
        alreadyActive: "Ya es la activa",
        makeActive: "Hacer activa",
      },
      noSelection:
        "Aún no hay un nodo enfocado. Selecciona uno dentro del mapa para leer su contexto y contenido.",
      blocks: {
        nodeReading: "Lectura del nodo",
        structureRelation: "Relación estructural",
        nodeId: "ID del nodo",
      },
      reading: {
        active:
          "Este nodo coincide con la versión que gobierna actualmente el flujo.",
        available:
          "Este nodo representa una etapa disponible para inspección o reactivación.",
      },
      structure: {
        derived:
          "Proviene de una versión previa dentro del árbol de crecimiento.",
        root:
          "Corresponde al punto de arranque del recorrido evolutivo.",
      },
      contentBadges: {
        associated: "Associated content",
        focusedReading: "Focused reading",
      },
      contentLabel: "Contenido asociado",
    },
  },
    workspaceAnalysis: {
    kicker: "Observation stage",
    title: "Comparación y lectura conceptual",
  },
  versionComparison: {
    title: "Comparación de versiones",
    description:
      "Coloca dos etapas de la idea frente a frente para entender mejor qué se mantuvo, qué cambió y hacia dónde se desplazó su sentido.",
    versionLabel: "Versión {{number}} · {{transformation}}",
    empty: {
      title: "Comparación no disponible todavía",
      description:
        "Necesitas al menos dos versiones en el historial para poder contrastar su evolución.",
    },
    badges: {
      dualReading: "Dual reading",
      comparativeLens: "Comparative lens",
      conceptualTension: "Tensión conceptual",
    },
    contrastMode: "Contrast mode",
    intro:
      "Selecciona dos versiones distintas para observar de forma lineal cómo cambia la idea entre un estado previo y otro más reciente.",
    leftVersionLabel: "Versión izquierda",
    rightVersionLabel: "Versión derecha",
    selectVersionPlaceholder: "Selecciona una versión",
    leftVersionHelp: "Funciona como el punto de partida o referencia conceptual.",
    rightVersionHelp:
      "Representa la etapa contra la cual quieres medir cambios y continuidad.",
    sameVersionWarning:
      "Debes seleccionar dos versiones diferentes para generar una lectura comparativa.",
    compareAction: "Comparar versiones",
    compareHelp: "El sistema generará una lectura contrastada del cambio conceptual.",
    preview: {
      showContent: "Mostrar contenido",
      hideContent: "Ocultar contenido",
      associatedContent: "Contenido asociado",
      collapsedView: "Vista colapsada",
      closedMessage:
        "Esta tarjeta está cerrada para mantener limpia la comparación visual.",
      referenceTitle: "Versión de referencia",
      contrastedTitle: "Versión contrastada",
      leftSide: "Lado izquierdo",
      rightSide: "Lado derecho",
      versionBadge: "Versión {{number}}",
    },
    result: {
      badges: {
        comparativeResult: "Resultado comparativo",
        dualReading: "Lectura dual",
        generated: "Comparación generada",
        dualAnalysis: "Análisis dual",
      },
      title: "Interpretación del contraste",
      empty:
        "Todavía no se ha generado una comparación. Cuando lo hagas, aquí aparecerá una lectura estructurada de diferencias, continuidades y desplazamientos entre ambas versiones.",
      outputLabel: "Lectura resultante",
      noText: "La comparación no devolvió texto.",
    },
  },
  perspectiveExplorer: {
    title: "Análisis de perspectiva",
    description:
      "Aplica un lente conceptual sobre la versión activa para enriquecer su lectura desde un ángulo más específico.",
    empty: {
      title: "Sin versión activa",
      description:
        "Necesitas una versión activa antes de poder analizarla desde distintas perspectivas.",
    },
    badges: {
      conceptLens: "Concept lens",
      focusedReading: "Focused reading",
      version: "Versión {{number}}",
    },
    intro:
      "Elige una perspectiva para cambiar la manera en que el sistema interpreta la versión activa.",
    perspectiveLabel: "Perspectiva",
    options: {
      businessPotential: "Potencial de negocio",
      userValue: "Valor para el usuario",
      innovation: "Innovación",
      feasibility: "Factibilidad",
    },
    descriptions: {
      businessPotential:
        "Examina si la idea tiene espacio para convertirse en una propuesta con valor económico o estratégico.",
      userValue:
        "Observa la utilidad real de la idea desde la experiencia, necesidad y beneficio percibido por el usuario.",
      innovation:
        "Evalúa el nivel de novedad, diferenciación y frescura conceptual de la propuesta.",
      feasibility:
        "Considera si la idea puede ejecutarse con recursos, tiempo y condiciones realistas.",
      default: "Analiza la idea desde un ángulo específico.",
    },
    analyzeAction: "Analizar perspectiva",
    expectedReadingTitle: "Lectura esperada",
    expectedReadingDescription:
      "Este análisis no transforma la versión: la examina desde un criterio concreto para enriquecer tu interpretación antes de seguir evolucionando.",
    cards: {
      business: {
        title: "Negocio",
        description:
          "Evalúa proyección, utilidad estratégica y valor económico potencial.",
      },
      user: {
        title: "Usuario",
        description:
          "Observa necesidad, claridad de beneficio y experiencia percibida.",
      },
      execution: {
        title: "Ejecución",
        description:
          "Contrasta viabilidad, recursos y realismo de implementación.",
      },
    },
    result: {
      badges: {
        perspectiveReading: "Perspective reading",
        generated: "Análisis generado",
      },
      title: "Resultado del lente seleccionado",
      empty:
        "Todavía no se ha generado un análisis. Cuando lo hagas, aquí aparecerá una lectura enfocada de la versión activa desde la perspectiva elegida.",
      outputLabel: "Lectura analítica",
    },
  },
    workspaceSynthesis: {
    kicker: "Closure stage",
    title: "Consolidación del resultado final",
  },
  finalSynthesis: {
    title: "Síntesis final",
    description:
      "Consolida la versión activa en una lectura estructurada que cierre el ciclo principal del flujo creativo.",
    generateAction: "Generar síntesis",
    empty: {
      title: "Sin síntesis todavía",
      description:
        "Cuando generes la síntesis, aquí aparecerá la consolidación final del resultado estructurado.",
    },
    badges: {
      flowClosure: "Flow closure",
      generated: "Síntesis generada",
      consolidatedResult: "Resultado consolidado",
    },
    headerTitle: "Cierre estructurado de la evolución",
    headerDescription:
      "Esta sección reúne la lectura final del sistema sobre la versión activa y la convierte en una forma más clara, presentable y accionable.",
    summaryCards: {
      state: {
        label: "Estado",
        value: "Cierre del flujo",
      },
      base: {
        label: "Base",
        value: "Versión {{number}}",
      },
      result: {
        label: "Resultado",
        value: "Lectura estructurada",
      },
    },
    blocks: {
      summary: "Resumen",
      valueProposition: "Propuesta de valor",
      targetAudience: "Público objetivo",
      nextSteps: "Siguientes pasos",
      structuredDescription: "Descripción estructurada",
    },
  },
} as const;

export default es;