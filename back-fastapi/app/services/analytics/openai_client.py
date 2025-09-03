from openai import AsyncOpenAI
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

from app.config import Settings
from app.logger_config import logger


class OpenAIClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def chat_completion(
        self,
        messages: list[ChatCompletionMessageParam],
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> str | None:
        try:
            response: ChatCompletion = await self.client.chat.completions.create(
                model=self.settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=max_tokens or self.settings.OPENAI_MAX_TOKENS,
                temperature=temperature or self.settings.OPENAI_TEMPERATURE,
            )

            if response.choices:
                content = response.choices[0].message.content
                logger.info(
                    f"OpenAI API response received, tokens used: "
                    f"{response.usage.total_tokens if response.usage else 'unknown'}"
                )
                return content

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return None

        return None

    async def analyze_expenses(self, prompt: str, data: str, max_tokens: int | None = None) -> str | None:
        messages: list[ChatCompletionMessageParam] | list[dict[str, str]] = [
            {
                "role": "system",
                "content": ("You are a financial advisor analyzing expense data.\n"
                            "Provide clear, actionable insights in Russian language.\n"
                            "Use bullet points and summaries where appropriate.\n"
                            "make response in HTML format. without <!DOCTYPE html>\n"
                            "only root <div></div> and its content.\n"),
            },
            {"role": "user", "content": f"{prompt}\n\nExpenses data:\n{data}"},
        ]

        ai_response = await self.chat_completion(messages, max_tokens)
        ai_response = ai_response.strip()
        ai_response = ai_response.replace("\n", " ")
        ai_response = ai_response.strip("````html").strip("```").strip()

        return ai_response
