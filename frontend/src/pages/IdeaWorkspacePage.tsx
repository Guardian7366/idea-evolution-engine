import { PerspectiveExplorerPanel } from '../features/analysis/components/PerspectiveExplorerPanel'
import { VersionComparisonPanel } from '../features/analysis/components/VersionComparisonPanel'
import { IdeaInputSection } from '../features/idea-input/components/IdeaInputSection'
import { FlowStatusPanel } from '../features/session/components/FlowStatusPanel'
import { FinalSynthesisPanel } from '../features/synthesis/components/FinalSynthesisPanel'
import { VariantsList } from '../features/variants/components/VariantsList'
import { ActiveVersionPanel } from '../features/versioning/components/ActiveVersionPanel'
import { VersionTransformPanel } from '../features/versioning/components/VersionTransformPanel'
import { useIdeaFlow } from '../hooks/useIdeaFlow'
import { IdeaHistorySidebar } from '../features/session/components/IdeaHistorySidebar'
import { useState } from 'react'

export function IdeaWorkspacePage() {

  const [isHistoryOpen, setIsHistoryOpen] = useState(false)

  const {
    ideasHistory,
    activeIdeaId,
    handleSelectHistoryIdea,
    ideaInput,
    sessionId,
    ideaId,
    variants,
    baseVersion,
    activeVersion,
    comparisonResult,
    selectedPerspective,
    perspectiveResult,
    synthesisResult,
    transformInstruction,
    isLoading,
    isSelectingVariant,
    isTransformingVersion,
    isComparingVersions,
    isExploringPerspective,
    isGeneratingSynthesis,
    errorMessage,
    setIdeaInput,
    setSelectedPerspective,
    setTransformInstruction,
    handleStartFlow,
    handleSelectVariant,
    handleRefineVersion,
    handleCompareVersions,
    handleExplorePerspective,
    handleGenerateFinalSynthesis,
  } = useIdeaFlow()

  return (
    <>
      <IdeaHistorySidebar
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        ideas={ideasHistory}
        activeIdeaId={activeIdeaId}
        onSelectIdea={(ideaId) => {
          handleSelectHistoryIdea(ideaId)
          setIsHistoryOpen(false)
        }}
      />

    <div
      className={`space-y-8 transition-all duration-300 ${
        isHistoryOpen ? 'ml-[320px]' : 'ml-0'
      }`}
    >
      {!isHistoryOpen &&  
      <aside className="fixed left-0 h-screen bg-zinc-300 w-25">  
      <button className="block mt-14 ml-3 text-4xl size-14 rounded-lg hover:bg-slate-100 p-2 size-18" type="button" onClick={() => setIsHistoryOpen(true)}>
          <img src="/src/assets/flowbite--open-sidebar-solid.png" alt="" />
        </button>
        </aside>
      }
      <IdeaInputSection
        ideaInput={ideaInput}
        isLoading={isLoading}
        errorMessage={errorMessage}
        onIdeaInputChange={setIdeaInput}
        onGenerateVariants={handleStartFlow}
      />

      <FlowStatusPanel
        sessionId={sessionId}
        ideaId={ideaId}
        variantsCount={variants.length}
      />

      <VariantsList
        variants={variants}
        isSelecting={isSelectingVariant}
        onSelectVariant={handleSelectVariant}
      />

      <ActiveVersionPanel activeVersion={activeVersion} />

      <VersionTransformPanel
        hasActiveVersion={Boolean(activeVersion)}
        transformInstruction={transformInstruction}
        isTransforming={isTransformingVersion}
        onInstructionChange={setTransformInstruction}
        onRefine={handleRefineVersion}
      />

      <VersionComparisonPanel
        baseVersion={baseVersion}
        activeVersion={activeVersion}
        comparisonResult={comparisonResult}
        isComparing={isComparingVersions}
        onCompare={handleCompareVersions}
      />

      <PerspectiveExplorerPanel
        hasActiveVersion={Boolean(activeVersion)}
        selectedPerspective={selectedPerspective}
        perspectiveResult={perspectiveResult}
        isExploring={isExploringPerspective}
        onPerspectiveChange={setSelectedPerspective}
        onExplore={handleExplorePerspective}
      />

      <FinalSynthesisPanel
        hasActiveVersion={Boolean(activeVersion)}
        synthesisResult={synthesisResult}
        isGenerating={isGeneratingSynthesis}
        onGenerate={handleGenerateFinalSynthesis}
      />
    </div>
    </>
  )
}