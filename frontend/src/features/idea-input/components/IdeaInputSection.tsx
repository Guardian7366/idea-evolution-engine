import { Button } from '../../../components/shared/ui/Button'
import { TextArea } from '../../../components/shared/ui/TextArea'
import { Spinner } from '../../../components/shared/ui/Spinner'

interface IdeaInputSectionProps {
  ideaInput: string
  isLoading: boolean
  errorMessage: string
  onIdeaInputChange: (value: string) => void
  onGenerateVariants: () => void
}

export function IdeaInputSection({
  ideaInput,
  isLoading,
  errorMessage,
  onIdeaInputChange,
  onGenerateVariants,
}: IdeaInputSectionProps) {
  const isDisabled = isLoading || ideaInput.trim().length < 3

  return (
    <section className="relative mt-10 mx-auto w-full max-w-4xl overflow-hidden rounded-[2rem] border border-white/60 bg-white/70 px-6 py-8 shadow-[0_18px_60px_rgba(15,23,42,0.08)] backdrop-blur-sm sm:px-8 sm:py-10">
      <div className="pointer-events-none absolute inset-0 bg-gradient-to-br from-white/60 via-transparent to-slate-100/60" />
      <div className="relative z-10">
        <div className="mb-6 space-y-2 text-center">
          <span className="inline-flex items-center rounded-full border border-slate-200 bg-white px-3 py-1 text-xs font-medium tracking-wide text-slate-600 shadow-sm">
            Start here
          </span>

          <h2 className="text-2xl font-semibold tracking-tight text-slate-900 sm:text-3xl">
            Start with an idea
          </h2>

          <p className="mx-auto max-w-2xl text-sm leading-6 text-slate-600 sm:text-base">
            Write a word, phrase, problem, or concept. The system will expand it into
            variants and help shape it step by step.
          </p>
        </div>

        <div className="mx-auto max-w-3xl">
          <div className="rounded-[1.5rem] border border-slate-200/80 bg-white shadow-sm transition-shadow focus-within:shadow-md">
            <div className="border-b border-slate-100 px-4 pt-4 sm:px-5">
              <p className="text-xs font-medium uppercase tracking-[0.18em] text-slate-500">
                Initial prompt
              </p>
            </div>

            <div className="px-4 py-4 sm:px-5">
              <TextArea
                value={ideaInput}
                onChange={(event) => onIdeaInputChange(event.target.value)}
                placeholder="Describe your idea..."
                className="min-h-[160px] w-full resize-none border-0 bg-transparent p-0 text-base leading-6 text-slate-800 outline-none placeholder:text-slate-400 focus:border-0 focus:outline-none"
              />
            </div>

            <div className="flex flex-col gap-3 border-t border-slate-100 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-5">
              <p className="text-xs text-slate-500">
                Tip: keep it short. One clear concept is enough to begin.
              </p>

              <Button
                type="button"
                onClick={onGenerateVariants}
                disabled={isDisabled}
                loading={isLoading}
                className="inline-flex items-center justify-center gap-2 rounded-full px-5 py-2.5 text-sm font-semibold"
              >
                {isLoading && <Spinner size="sm" />}
                {isLoading ? 'Generating...' : 'Generate variants'}
              </Button>
            </div>
          </div>

          {errorMessage ? (
            <div className="mt-4 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 shadow-sm">
              {errorMessage}
            </div>
          ) : null}
        </div>
      </div>
    </section>
  )
}