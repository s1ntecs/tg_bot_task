from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import TELEGRAM_CHAT_ID, bot


class Poll(StatesGroup):
    question = State()
    options = State()
    answer = State()


async def create_poll_start(message: types.Message, state: FSMContext):
    await message.answer("Введите вопрос для опроса:")
    await Poll.question.set()
    await state.update_data(options=[])


async def process_question(message: types.Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer(
        "Введите вариант ответа или отправьте команду"
        " /done, чтобы завершить создание опроса:")
    await Poll.options.set()


async def process_options(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "/done":
            options = data["options"]
            print(options)
            await message.answer(
                "Введите номер правильного ответа, "
                "если правильных несколько, отправьте ответы по одному"
                "отправьте команду /done, чтобы завершить создание опроса:"
            )
            await Poll.answer.set()
            await state.update_data(answer=[])
        else:
            data["options"].append(message.text)
            await message.answer(
                "Введите вариант ответа или отправьте команду"
                " /done, после последнего варианта ответа:"
            )


async def additional_functions(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "/is_anonymous_poll":
            data["answer"].append({"/is_anonymous_poll": True})


async def create_poll(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        answer = int(message.text)
        options = data["options"]
        question = data["question"]
        if len(options) < 2:
            await message.answer(
                "У опроса должно быть не менее 2 вариантов ответа")
            return
        await bot.send_poll(
            chat_id=TELEGRAM_CHAT_ID,
            question=question,
            options=options,
            type=types.PollType.QUIZ,
            correct_option_id=answer-1,
            explanation=None,
            is_anonymous=False,
            allows_multiple_answers=True
        )
        await state.finish()
        elif message.text == "/is_anonymous_poll":
            data["answer"].append({"/is_anonymous_poll": True})


def register_handlers_poll(dp: Dispatcher):
    dp.register_message_handler(create_poll_start, commands=["poll"])
    dp.register_message_handler(process_question, state=Poll.question)
    dp.register_message_handler(process_options, state=Poll.options)
    dp.register_message_handler(create_poll, state=Poll.answer)
