const en = {
  app: {
    languageSwitch: {
      ariaLabel: "Visual language switch",
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
      "A guided system to incubate an idea, branch variants, transform versions, and consolidate a final synthesis inside a living creative environment.",
    badges: {
      seed: "Seed",
      branch: "Branch",
      evolve: "Evolve",
    },
    zones: {
      zone1Label: "Zone 01",
      zone1Value: "Incubation",
      zone2Label: "Zone 02",
      zone2Value: "Transformation",
      zone3Label: "Zone 03",
      zone3Value: "Synthesis",
    },
  },
  slides: {
    hero: {
      label: "Workspace home",
      shortLabel: "Home",
    },
    system: {
      label: "System control",
      shortLabel: "Control",
    },
    seed: {
      label: "Idea incubation",
      shortLabel: "Idea",
    },
    branch: {
      label: "Initial variants",
      shortLabel: "Variants",
    },
    core: {
      label: "Main transformation",
      shortLabel: "Transform",
    },
    evolution: {
      label: "Map and history",
      shortLabel: "Evolution",
    },
    analysis: {
      label: "Comparison and analysis",
      shortLabel: "Analysis",
    },
    synthesis: {
      label: "Final synthesis",
      shortLabel: "Synthesis",
    },
  },
  viewport: {
    ariaLabel: "Workspace slides viewport",
    previousSlide: "Previous slide",
    nextSlide: "Next slide",
    previous: "Previous",
    next: "Next",
  },
    workspaceNavbar: {
    ariaLabel: "Workspace horizontal navigation",
    deckBadge: "Navigation deck",
    linkedSlidesBadge: "{{count}} linked slides",
    orchestrationLabel: "Horizontal orchestration",
    available: "Available",
    blockedByFlow: "Blocked by flow",
  },
  workspaceHero: {
    badges: {
      creativeEvolution: "Creative evolution",
      systemContinuity: "System continuity",
      livingWorkspace: "Living workspace",
    },
    kicker: "Main orchestration zone",
    title: "An environment where ideas can breathe, change, and mature.",
    description:
      "The main MVP flow already allows sessions to be created, ideas to be registered, variants to be generated, versions to be selected, transformed, analyzed, and synthesized, now organized as a more alive, clearer, and more memorable system.",
    bannerAlt: "Idea Evolution Engine visual banner",
    stages: {
      stage1: {
        badge: "Stage 1",
        title: "Initial incubation",
        description:
          "Define the working container and register the creative seed that will give rise to the flow.",
      },
      stage2: {
        badge: "Stage 2",
        title: "Branching and focus",
        description:
          "Explore alternatives, choose a promising direction, and turn it into the system's live version.",
      },
      stage3: {
        badge: "Stage 3",
        title: "Transformation and closure",
        description:
          "Evolve, compare, analyze, and consolidate a structured synthesis of the final result.",
      },
    },
  },
    sectionCard: {
    eyebrowPrimary: "System zone",
    eyebrowSecondary: "Idea Evolution Engine",
  },
  workspaceSystem: {
    kicker: "System controls",
    title: "Workspace control and context",
  },
  languageSelector: {
    title: "Flow language",
    description:
      "Configure how the system should behave when interpreting and producing content during AI operations.",
    badges: {
      control: "Language control",
    },
    hints: {
      es: "Fixed language: Spanish",
      en: "Fixed language: English",
      auto: "Automatic detection active",
    },
    outputMode: "Output mode",
    modeLabel: "Language mode",
    options: {
      auto: "Auto detect",
      es: "Spanish",
      en: "English",
    },
    descriptions: {
      es: "The system will force Spanish for the main AI operations.",
      en: "The system will force English for the main AI operations.",
      auto: "The system will automatically detect the most suitable language based on context.",
    },
    expectedBehaviorTitle: "Expected behavior",
    behaviors: {
      auto: {
        title: "Auto",
        description: "The system decides the most suitable language based on context.",
      },
      manual: {
        title: "Manual",
        description: "Forces linguistic consistency in variants, analysis, and synthesis.",
      },
    },
  },
  flowStatus: {
    title: "Flow status",
    description:
      "Monitor the current workspace state and quickly locate the key identifiers in the process.",
    clearWorkspace: "Clear local workspace",
    badges: {
      status: "Flow status",
    },
    states: {
      processing: "Processing...",
      ready: "Ready",
    },
    controlBoard: "Control board",
    items: {
      session: {
        label: "Session",
        empty: "No session yet.",
      },
      idea: {
        label: "Idea",
        empty: "No idea yet.",
      },
      activeVersion: {
        label: "Active version",
        empty: "No active version yet.",
      },
    },
    operationalStateTitle: "Operational state",
    operationalMessages: {
      active: "The system is ready to continue the flow or run a new operation.",
      empty: "There is no active flow yet. Create a session to begin the journey.",
    },
  },
    workspaceSeed: {
    kicker: "Seed stage",
    title: "Session and base idea incubation",
  },
  ideaInput: {
    contextLabel: "Context",
    session: {
      badges: {
        container: "Seed container",
        stage: "Stage 01",
      },
      title: "Create session",
      description:
        "Define the initial container for the process. This session will be the starting point where the full evolution of the idea will live.",
      status: "Start",
      fields: {
        titleLabel: "Session title",
        titlePlaceholder: "Write a title for the session",
      },
      hint: {
        title: "Master space",
        description:
          "This is where the flow container is born. Everything else depends on this foundation existing first.",
      },
      footerText:
        "This action prepares the base space for the creative flow and enables the capture of the seed idea.",
      submit: "Create session",
    },
    idea: {
      badges: {
        seed: "Creative seed",
        stage: "Stage 02",
      },
      title: "Register idea",
      description:
        "Enter the base idea that the system will use to generate branches, transformations, and a clearer final synthesis.",
      status: "Core",
      fields: {
        titleLabel: "Idea title",
        titlePlaceholder: "Write a title for the idea",
        contentLabel: "Idea content",
        contentPlaceholder: "Describe your main idea",
      },
      hint: {
        title: "Creative seed",
        description:
          "The clearer the initial formulation is, the more powerful and useful the later variants and transformations will be.",
      },
      footerNeedsSession: "You need a session first to activate this stage.",
      footerReady: "This idea will become the seed that feeds the rest of the system.",
      submit: "Register idea",
    },
  },
    emptyState: {
    initialState: "Initial state",
    waitingState: "Waiting state",
  },
  workspaceBranch: {
    kicker: "Branch stage",
    title: "Initial directions of evolution",
  },
  variantsList: {
    title: "Generated variants",
    description:
      "Explore different directions born from the base idea and choose the one that deserves to become the next focus of evolution.",
    empty: {
      title: "No variants have been generated yet",
      description:
        "Once you register an idea, different initial branches will appear here to begin the flow's evolution.",
    },
    badges: {
      branchStage: "Branch stage",
      alternatives: "{{count}} alternatives",
      guidedSelection: "Guided selection",
    },
    routesSlide: "Routes slide",
    mainDescription:
      "Here you define the system's first major direction. Only one variant can become the next live version of the flow.",
    currentStateLabel: "Current state",
    currentState: {
      selected: "A route has already been chosen",
      waiting: "Waiting for selection",
    },
  },
  variantCard: {
    routeBadge: "Route {{index}}",
    variantBadge: "Variant",
    selectedBadge: "Selected",
    availableBadge: "Available",
    branchLabel: "Branch",
    proposedDirectionLabel: "Proposed direction",
    functionLabel: "Function",
    function: {
      selected: "Governing route",
      candidate: "Candidate route",
    },
    resultLabel: "Result",
    result: {
      selected: "Converted into current focus",
      available: "Can become a real version",
    },
    footer: {
      selected: "This branch has already been converted into the system's chosen direction.",
      available: "Select this route to turn it into a live version of the flow.",
    },
    actions: {
      selected: "Chosen route",
      select: "Choose this route",
    },
  },
    workspaceCore: {
    kicker: "Core stage",
    title: "Focused version and transformation engine",
  },
  activeVersion: {
    title: "Focused version",
    description:
      "This is the current core you are observing inside the system. It may be the real active version or a temporarily focused version for inspection.",
    empty: {
      title: "No version selected yet",
      description:
        "Once there is an active version or you focus one from the history or graph, the current textual core of the flow will appear here.",
    },
    badges: {
      coreVersion: "Core version",
      versionNumber: "Version {{number}}",
      realActive: "Real active",
      inspection: "Under inspection",
    },
    headers: {
      realActive: "Current point of evolution",
      inspection: "Version focused for observation",
    },
    messages: {
      realActive:
        "This version represents the real and current state of the creative flow at this moment.",
      inspection:
        "This version was focused from the history or graph to review its content without replacing the active one yet.",
    },
    visualModeLabel: "Visual mode",
    visualModes: {
      activeCore: "Active core",
      temporaryInspection: "Temporary inspection",
    },
    info: {
      versionId: "Version identifier",
      appliedTransformation: "Applied transformation",
      versionNumber: "Version number",
    },
    contentBadges: {
      versionContent: "Version content",
      readableCore: "Readable core",
      currentState: "Current state",
      focusedView: "Focused view",
    },
    centralContentLabel: "Central content",
  },
  versionTransform: {
    title: "Transformation engine",
    description:
      "Apply operations to the active version to expand it, divert it, or refine it with a more precise intention.",
    empty: {
      title: "You need an active version first",
      description:
        "Select a variant to create the first version and unlock the transformation engine.",
    },
    badges: {
      engine: "Transformation engine",
      versionNumber: "Version {{number}}",
      active: "Active",
    },
    activeDescription:
      "The active version is the current point of the flow. From here you can grow it progressively, push it toward a riskier direction, or correct it through a controlled instruction.",
    liveNodeLabel: "Live system node",
    actionHintLabel: "Ideal for",
    languageModes: {
      en: "English mode",
      es: "Spanish mode",
      auto: "Auto mode",
    },
    evolution: {
      badgePrimary: "Evolution",
      badgeSecondary: "Progressive change",
      title: "Deepen the current line",
      description:
        "It keeps the conceptual direction and makes it more mature, richer, and better developed.",
      hintTitle: "Stability with growth",
      hintDescription:
        "when you have already found a valuable route and want to strengthen it without breaking its identity.",
      action: "Apply evolution",
    },
    mutation: {
      badgePrimary: "Mutation",
      badgeSecondary: "Disruptive change",
      title: "Shift the creative course",
      description:
        "Introduces a more aggressive alteration to open new trajectories and discover less obvious possibilities.",
      hintTitle: "Radical exploration",
      hintDescription:
        "when you feel the current direction needs a shake-up or an unexpected reading.",
      action: "Apply mutation",
    },
    refinement: {
      badgePrimary: "Guided refinement",
      badgeTertiary: "Fine control",
      title: "Specify how it should improve",
      description:
        "Use a clear instruction to say what the next version should preserve, correct, summarize, expand, or emphasize.",
      instructionLabel: "Refinement instruction",
      placeholder: "Write how you want to refine the current version",
      usageTitle: "Usage suggestion",
      tips: {
        clarity: {
          title: "Improve clarity",
          description: "Ask for a more concrete, direct, and easier-to-understand version.",
        },
        focus: {
          title: "Change focus",
          description: "Indicate the target context: academic, business, product, or user.",
        },
        depth: {
          title: "Control depth",
          description:
            "Specify whether you want to summarize, expand, organize, or emphasize key parts.",
        },
      },
      footerText:
        "The more specific the instruction, the more control you will have over the system's next result.",
      action: "Apply refinement",
    },
    processingBadge: "Processing",

    successOverlay: {
      evolution: "Evolution applied",
      mutation: "Mutation applied",
      refinement: "Refinement applied",
      versionNumber: "New version {{number}}",
    },
  },
    workspaceEvolution: {
    kicker: "Evolution stage",
    title: "Historical journey and growth map",
  },
  versionHistory: {
    title: "Version history",
    description:
      "Walk through the stages the idea has gone through and observe how it changed over time.",
    actions: {
      expandAll: "Expand all",
      collapseAll: "Collapse all",
      viewFull: "View full",
      hideDetail: "Hide detail",
      focus: "Focus",
      alreadyActive: "Already active",
      makeActive: "Make active",
      expandVersionAria: "Expand version {{number}}",
      collapseVersionAria: "Collapse version {{number}}",
    },
    empty: {
      title: "No versions have been generated yet",
      description:
        "Once you select a variant and start transforming the idea, its evolutionary path will appear here.",
    },
    badges: {
      trail: "Evolution trail",
      records: "{{count}} records",
      timeline: "Conceptual timeline",
    },
    liveHistory: "Live history",
    intro:
      "Here you can review each created stage in a linear way, focus it for reading, or reactivate it as the current core of the flow.",
    versionBadge: "Version {{number}}",
    activeBadge: "Active",
    selectedBadge: "Selected",
    compactViewBadge: "Compact view",
    expandedViewBadge: "Expanded view",
    stateLabels: {
      current: "Current state",
      observing: "Node under observation",
      previous: "Previous record",
    },
    stateMessages: {
      current: "This version represents the real and current state of the creative flow.",
      observing: "This version was focused for inspection and contextual reading.",
      previous: "This stage is part of the previous path of evolution.",
    },
    meta: {
      position: "Position",
      node: "Node {{index}}",
      origin: "Origin",
      state: "State",
      identity: "Identity",
    },
    origin: {
      root: "Start of history",
      derived: "Derived from a previous stage",
    },
    states: {
      governing: "Governs the flow",
      reading: "Being read",
      archived: "Archived",
    },
    content: {
      stageContent: "Stage content",
      compactView: "Compact view",
      readableSnapshot: "Readable snapshot",
      hiddenTemporarily: "Content temporarily hidden",
      stageLabel: "Content of this stage",
      compactMessagePrefix:
        "This version is compacted to keep the history clean. Use",
      compactMessageSuffix: "to display its full content.",
    },
  },
  versionGraph: {
    title: "Evolution map",
    description:
      "Visually observe how the idea branched and transformed through its different versions.",
    empty: {
      title: "There are no versions to visualize yet",
      description:
        "Once you select a variant and begin transforming the idea, you will see the evolution map here.",
    },
    badges: {
      visualMap: "Visual evolution map",
      potentialNodes: "{{count}} potential nodes",
      interactivePath: "Interactive path",
    },
    graphView: "Graph view",
    intro:
      "The map remains here as an observation module. You can use it to detect branches, review connections between versions, and reactivate a previous node.",
    node: {
      versionBadge: "V{{number}}",
      titles: {
        active: "Active node",
        focused: "Focused node",
        evolutionary: "Evolutionary node",
      },
      messages: {
        active: "Represents the system's current real state.",
        focused: "It is selected for inspection.",
        evolutionary: "It is part of the growth map.",
      },
      badges: {
        active: "Active",
        selected: "Selected",
      },
    },
    detail: {
      badges: {
        nodeInspection: "Node inspection",
        interactiveFocus: "Interactive focus",
        reactivationControl: "Reactivation control",
      },
      title: "Selected node detail",
      description:
        "Click on a node to review its main information and decide whether it should become the new active version of the flow.",
      actions: {
        alreadyActive: "Already active",
        makeActive: "Make active",
      },
      noSelection:
        "There is no focused node yet. Select one within the map to read its context and content.",
      blocks: {
        nodeReading: "Node reading",
        structureRelation: "Structural relation",
        nodeId: "Node ID",
      },
      reading: {
        active:
          "This node matches the version currently governing the flow.",
        available:
          "This node represents a stage available for inspection or reactivation.",
      },
      structure: {
        derived:
          "It comes from a previous version within the growth tree.",
        root:
          "It corresponds to the starting point of the evolutionary journey.",
      },
      contentBadges: {
        associated: "Associated content",
        focusedReading: "Focused reading",
      },
      contentLabel: "Associated content",
    },
  },
    workspaceAnalysis: {
    kicker: "Observation stage",
    title: "Comparison and conceptual reading",
  },
  versionComparison: {
    title: "Version comparison",
    description:
      "Place two stages of the idea face to face to better understand what remained, what changed, and where its meaning shifted.",
    versionLabel: "Version {{number}} · {{transformation}}",
    empty: {
      title: "Comparison not available yet",
      description:
        "You need at least two versions in the history to contrast their evolution.",
    },
    badges: {
      dualReading: "Dual reading",
      comparativeLens: "Comparative lens",
      conceptualTension: "Conceptual tension",
    },
    contrastMode: "Contrast mode",
    intro:
      "Select two different versions to observe linearly how the idea changes between a previous state and a more recent one.",
    leftVersionLabel: "Left version",
    rightVersionLabel: "Right version",
    selectVersionPlaceholder: "Select a version",
    leftVersionHelp: "It works as the starting point or conceptual reference.",
    rightVersionHelp:
      "It represents the stage against which you want to measure changes and continuity.",
    sameVersionWarning:
      "You must select two different versions to generate a comparative reading.",
    compareAction: "Compare versions",
    compareHelp: "The system will generate a contrasted reading of the conceptual change.",
    preview: {
      showContent: "Show content",
      hideContent: "Hide content",
      associatedContent: "Associated content",
      collapsedView: "Collapsed view",
      closedMessage:
        "This card is closed to keep the visual comparison clean.",
      referenceTitle: "Reference version",
      contrastedTitle: "Contrasted version",
      leftSide: "Left side",
      rightSide: "Right side",
      versionBadge: "Version {{number}}",
    },
    result: {
      badges: {
        comparativeResult: "Comparative result",
        dualReading: "Dual reading",
        generated: "Comparison generated",
        dualAnalysis: "Dual analysis",
      },
      title: "Interpretation of the contrast",
      empty:
        "A comparison has not been generated yet. When you do, a structured reading of differences, continuities, and shifts between both versions will appear here.",
      outputLabel: "Resulting reading",
      noText: "The comparison did not return text.",
    },
  },
  perspectiveExplorer: {
    title: "Perspective analysis",
    description:
      "Apply a conceptual lens to the active version to enrich its reading from a more specific angle.",
    empty: {
      title: "No active version",
      description:
        "You need an active version before you can analyze it from different perspectives.",
    },
    badges: {
      conceptLens: "Concept lens",
      focusedReading: "Focused reading",
      version: "Version {{number}}",
    },
    intro:
      "Choose a perspective to change the way the system interprets the active version.",
    perspectiveLabel: "Perspective",
    options: {
      businessPotential: "Business potential",
      userValue: "User value",
      innovation: "Innovation",
      feasibility: "Feasibility",
    },
    descriptions: {
      businessPotential:
        "Examines whether the idea has room to become a proposal with economic or strategic value.",
      userValue:
        "Looks at the real usefulness of the idea from the user's experience, need, and perceived benefit.",
      innovation:
        "Evaluates the level of novelty, differentiation, and conceptual freshness of the proposal.",
      feasibility:
        "Considers whether the idea can be executed with realistic resources, time, and conditions.",
      default: "Analyze the idea from a specific angle.",
    },
    analyzeAction: "Analyze perspective",
    expectedReadingTitle: "Expected reading",
    expectedReadingDescription:
      "This analysis does not transform the version: it examines it from a specific criterion to enrich your interpretation before continuing to evolve.",
    cards: {
      business: {
        title: "Business",
        description:
          "Evaluates projection, strategic usefulness, and potential economic value.",
      },
      user: {
        title: "User",
        description:
          "Looks at need, clarity of benefit, and perceived experience.",
      },
      execution: {
        title: "Execution",
        description:
          "Contrasts feasibility, resources, and implementation realism.",
      },
    },
    result: {
      badges: {
        perspectiveReading: "Perspective reading",
        generated: "Analysis generated",
      },
      title: "Result of the selected lens",
      empty:
        "An analysis has not been generated yet. When you do, a focused reading of the active version from the chosen perspective will appear here.",
      outputLabel: "Analytical reading",
    },
  },
    workspaceSynthesis: {
    kicker: "Closure stage",
    title: "Final result consolidation",
  },
  finalSynthesis: {
    title: "Final synthesis",
    description:
      "Consolidates the active version into a structured reading that closes the main cycle of the creative flow.",
    generateAction: "Generate synthesis",
    empty: {
      title: "No synthesis yet",
      description:
        "When you generate the synthesis, the final consolidation of the structured result will appear here.",
    },
    badges: {
      flowClosure: "Flow closure",
      generated: "Synthesis generated",
      consolidatedResult: "Consolidated result",
    },
    headerTitle: "Structured closure of evolution",
    headerDescription:
      "This section gathers the system's final reading of the active version and turns it into a clearer, more presentable, and actionable form.",
    summaryCards: {
      state: {
        label: "State",
        value: "Flow closure",
      },
      base: {
        label: "Base",
        value: "Version {{number}}",
      },
      result: {
        label: "Result",
        value: "Structured reading",
      },
    },
    blocks: {
      summary: "Summary",
      valueProposition: "Value proposition",
      targetAudience: "Target audience",
      nextSteps: "Next steps",
      structuredDescription: "Structured description",
    },
  },
} as const;

export default en;