import { Button } from '../../../components/shared/ui/Button'

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
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-xl font-semibold">Start with an initial idea</h2>
      <p className="mt-2 text-sm text-slate-600">
        Enter a simple idea and generate the first set of variants.
      </p>

      <div className="mt-4 space-y-4">
        <textarea
          value={ideaInput}
          onChange={(event) => onIdeaInputChange(event.target.value)}
          placeholder="Describe your idea..."
          className="min-h-[140px] w-full rounded-lg border border-slate-300 p-3 outline-none focus:border-slate-500"
        />

        <Button
          type="button"
          onClick={onGenerateVariants}
          disabled={isLoading || ideaInput.trim().length < 3}
          loading={isLoading}
        >
          {isLoading ? 'Generating...' : 'Generate Variants'}
        </Button>

        {errorMessage ? (
          <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">
            {errorMessage}
          </div>
        ) : null}
      </div>
    </section>
  )
}