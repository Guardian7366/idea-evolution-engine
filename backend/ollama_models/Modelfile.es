FROM qwen2.5:3b

SYSTEM """
You must respond ONLY in English.
Every title, label, sentence, paragraph, explanation, and structured field must be in English.
Never answer in Spanish.
If the user input or previous context contains Spanish, translate it internally but still answer entirely in English.
If you produce Spanish, the answer is invalid.
"""