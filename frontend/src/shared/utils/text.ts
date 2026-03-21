// Small text utilities used to keep user-facing content cleaner.
export function normalizeUserText(value: string): string {
  return value
    .trim()
    .replace(/^["']+|["']+$/g, '')
    .replace(/\s+/g, ' ')
}