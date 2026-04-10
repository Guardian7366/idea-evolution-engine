import { useState } from 'react'

import {
  compareVersions,
  createIdea,
  createSession,
  explorePerspective,
  generateFinalSynthesis,
  generateVariants,
  selectVariant,
  transformVersion,
} from '../services/idea.service'
import { normalizeUserText } from '../shared/utils/text'
import type {
  ActiveIdeaVersion,
  FinalSynthesisResult,
  IdeaVariantItem,
  PerspectiveAnalysisResult,
  PerspectiveType,
  VersionComparisonResult,
} from '../types/idea'
import type {
  IdeaHistoryItem
} from '../features/session/components/IdeaHistorySidebar'

export function useIdeaFlow() {
  const [ideaInput, setIdeaInput] = useState('')
  const [sessionId, setSessionId] = useState('')
  const [ideaId, setIdeaId] = useState('')
  const [variants, setVariants] = useState<IdeaVariantItem[]>([])
  const [baseVersion, setBaseVersion] = useState<ActiveIdeaVersion | null>(null)
  const [activeVersion, setActiveVersion] = useState<ActiveIdeaVersion | null>(
    null,
  )
  const [ideasHistory, setIdeasHistory] = useState<IdeaHistoryItem[]>([])
  const [activeIdeaId, setActiveIdeaId] = useState<string | null>(null)
  const [comparisonResult, setComparisonResult] =
    useState<VersionComparisonResult | null>(null)
  const [selectedPerspective, setSelectedPerspective] =
    useState<PerspectiveType>('user_value')
  const [perspectiveResult, setPerspectiveResult] =
    useState<PerspectiveAnalysisResult | null>(null)
  const [synthesisResult, setSynthesisResult] =
    useState<FinalSynthesisResult | null>(null)
  const [transformInstruction, setTransformInstruction] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isSelectingVariant, setIsSelectingVariant] = useState(false)
  const [isTransformingVersion, setIsTransformingVersion] = useState(false)
  const [isComparingVersions, setIsComparingVersions] = useState(false)
  const [isExploringPerspective, setIsExploringPerspective] = useState(false)
  const [isGeneratingSynthesis, setIsGeneratingSynthesis] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')

  const handleStartFlow = async () => {
    const normalizedIdeaInput = normalizeUserText(ideaInput)

    if (normalizedIdeaInput.length < 3) {
      setErrorMessage('Please enter a more complete idea before continuing.')
      return
    }

    setIsLoading(true)
    setErrorMessage('')

    // Reset the previous flow results before starting a new one.
    setSessionId('')
    setIdeaId('')
    setVariants([])
    setBaseVersion(null)
    setActiveVersion(null)
    setComparisonResult(null)
    setPerspectiveResult(null)
    setSynthesisResult(null)
    setTransformInstruction('')

    try {
      // Step 1: create session
      const sessionResponse = await createSession()

      // Step 2: create idea
      const ideaResponse = await createIdea({
        session_id: sessionResponse.session_id,
        initial_prompt: normalizedIdeaInput,
      })

      // Step 3: generate variants
      const variantsResponse = await generateVariants({
        session_id: sessionResponse.session_id,
        idea_id: ideaResponse.idea_id,
        initial_prompt: normalizedIdeaInput,
      })

      setIdeaInput(normalizedIdeaInput)
      setSessionId(sessionResponse.session_id)
      setIdeaId(ideaResponse.idea_id)
      setVariants(variantsResponse.variants)

      const trimmedIdea = ideaInput.trim()

      if (trimmedIdea.length < 3) return

      const newIdeaId = crypto.randomUUID()

      setIdeasHistory((prev) => [
        {
          ideaId: newIdeaId,
          input: trimmedIdea,
          createdAt: new Date().toISOString(),
        },
        ...prev,
      ])

      setActiveIdeaId(newIdeaId)
    } catch (error) {
      console.error('Frontend flow error:', error)
      setErrorMessage(
        'Failed to connect with backend API. Check browser console for details.',
      )
    } finally {
      setIsLoading(false)
    }
  }

  const handleSelectHistoryIdea = (ideaId: string) => {
    const selectedIdea = ideasHistory.find((idea) => idea.ideaId === ideaId)
    if (!selectedIdea) return

    setActiveIdeaId(ideaId)
    setIdeaInput(selectedIdea.input)

  }

  const handleSelectVariant = async (variantId: string) => {
    if (!sessionId || !ideaId) {
      setErrorMessage('Session and idea must exist before selecting a variant.')
      return
    }

    setIsSelectingVariant(true)
    setErrorMessage('')
    setComparisonResult(null)
    setPerspectiveResult(null)
    setSynthesisResult(null)

    try {
      const response = await selectVariant({
        session_id: sessionId,
        idea_id: ideaId,
        variant_id: variantId,
      })

      // The selected variant becomes both the base version and current active version.
      setBaseVersion(response.active_version)
      setActiveVersion(response.active_version)
      setTransformInstruction('')
    } catch (error) {
      console.error('Variant selection error:', error)
      setErrorMessage(
        'Failed to select variant. Check browser console for details.',
      )
    } finally {
      setIsSelectingVariant(false)
    }
  }

  const handleRefineVersion = async () => {
    if (!sessionId || !ideaId || !activeVersion) {
      setErrorMessage('An active version is required before refining it.')
      return
    }

    const normalizedInstruction = normalizeUserText(transformInstruction)

    if (normalizedInstruction.length < 3) {
      setErrorMessage('Please write a clearer transformation instruction.')
      return
    }

    setIsTransformingVersion(true)
    setErrorMessage('')
    setComparisonResult(null)
    setPerspectiveResult(null)
    setSynthesisResult(null)

    try {
      const response = await transformVersion({
        session_id: sessionId,
        idea_id: ideaId,
        version_id: activeVersion.version_id,
        transformation_type: 'refine',
        instruction: normalizedInstruction,
      })

      setTransformInstruction(normalizedInstruction)
      setActiveVersion(response.new_active_version)
    } catch (error) {
      console.error('Version transformation error:', error)
      setErrorMessage(
        'Failed to transform version. Check browser console for details.',
      )
    } finally {
      setIsTransformingVersion(false)
    }
  }

  const handleCompareVersions = async () => {
    if (!sessionId || !ideaId || !baseVersion || !activeVersion) {
      setErrorMessage('Two comparable versions are required before comparing.')
      return
    }

    if (baseVersion.version_id === activeVersion.version_id) {
      setErrorMessage('Transform the active version before comparing it.')
      return
    }

    setIsComparingVersions(true)
    setErrorMessage('')

    try {
      const response = await compareVersions({
        session_id: sessionId,
        idea_id: ideaId,
        version_id_a: baseVersion.version_id,
        version_id_b: activeVersion.version_id,
      })

      setComparisonResult(response.comparison)
    } catch (error) {
      console.error('Version comparison error:', error)
      setErrorMessage(
        'Failed to compare versions. Check browser console for details.',
      )
    } finally {
      setIsComparingVersions(false)
    }
  }

  const handleExplorePerspective = async () => {
    if (!sessionId || !ideaId || !activeVersion) {
      setErrorMessage('An active version is required before exploring it.')
      return
    }

    setIsExploringPerspective(true)
    setErrorMessage('')

    try {
      const response = await explorePerspective({
        session_id: sessionId,
        idea_id: ideaId,
        version_id: activeVersion.version_id,
        perspective_type: selectedPerspective,
      })

      setPerspectiveResult(response.analysis)
    } catch (error) {
      console.error('Perspective exploration error:', error)
      setErrorMessage(
        'Failed to explore perspective. Check browser console for details.',
      )
    } finally {
      setIsExploringPerspective(false)
    }
  }

  const handleGenerateFinalSynthesis = async () => {
    if (!sessionId || !ideaId || !activeVersion) {
      setErrorMessage('An active version is required before generating synthesis.')
      return
    }

    setIsGeneratingSynthesis(true)
    setErrorMessage('')

    try {
      const response = await generateFinalSynthesis({
        session_id: sessionId,
        idea_id: ideaId,
        version_id: activeVersion.version_id,
      })

      setSynthesisResult(response.synthesis)
    } catch (error) {
      console.error('Final synthesis generation error:', error)
      setErrorMessage(
        'Failed to generate final synthesis. Check browser console for details.',
      )
    } finally {
      setIsGeneratingSynthesis(false)
    }
  }

  return {
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
    ideasHistory,
    activeIdeaId,
    handleSelectHistoryIdea,
  }
}