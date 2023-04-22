from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot


class Poll(StatesGroup):
    question = State()
    options = State()
    answer = State()
    add_func = State()
    explanation = State()


async def create_poll_start(message: types.Message, state: FSMContext):
    """ Начало создания опроса. """
    await message.answer("Введите вопрос для опроса:")
    await Poll.question.set()
    await state.update_data(options=[])


async def process_question(message: types.Message, state: FSMContext):
    """ Функция для создания вопроса. """
    await state.update_data(question=message.text)
    await message.answer(
        "Введите вариант ответа или отправьте команду"
        " /done, чтобы завершить создание опроса:")
    await Poll.options.set()


async def process_options(message: types.Message, state: FSMContext):
    """ Функция для создания вариантов ответа опросу. """
    async with state.proxy() as data:

        if message.text == "/done":  # пользователь ввел команду /done
            options = data["options"]  # Берем все ответы
            if len(options) < 2:
                await message.answer(
                    "У опроса должно быть не менее 2 вариантов ответа. \n "
                    "Введите еще варианты ответов.")
                return
            await message.answer(
                "Если хотите анонимный опрос, введите /is_anonymous_poll \n "
                "Если хотите выбор множество ответов /allows_multiple_answers"
                " \n Если хотите продолжить, введите /done"
            )
            await Poll.add_func.set()
            await state.update_data(add_func=[
                {"allows_multiple_answers": False,
                 "is_anonymous_poll": False,
                 "explanation": None
                 }])
        else:
            # Получаем вариант ответа для опроса
            data["options"].append(message.text)  # сохраняем ответ
            await message.answer(
                "Введите вариант ответа или отправьте команду"
                " /done, после последнего варианта ответа:"
            )


async def additional_functions(message: types.Message, state: FSMContext):
    """ Функция для добавления некоторых возможностей в опрос. """
    async with state.proxy() as data:
        if message.text == "/done":  # пользователь ввел команду /done
            await message.answer(
                "Введите развернутый ответ. \n "
                "Если не хотите добавлять развернутый ответ: /done"
            )
            await Poll.explanation.set()
        # пользователь ввел команду /allows_multiple_answers
        elif message.text == "/allows_multiple_answers":
            # сохраняем в хранилище состояний
            data["add_func"][0]["allows_multiple_answers"] = True
            await message.answer(
                "Теперь у опроса есть функция множественного ответа. \n "
                "Если вы хотите завершить создание опроса напишите /done"
            )
        # пользователь ввел команду /is_anonymous_poll
        elif message.text == "/is_anonymous_poll":
            # сохраняем в хранилище состояний
            data["add_func"][0]["is_anonymous_poll"] = True
            await message.answer(
                "Теперь опрос анонимный. \n "
                "Если вы хотите завершить создание опроса напишите /done"
            )
        else:
            # Если пользователь ввел неизвестную команду или сообщение
            await message.answer(
                "Если хотите анонимный опрос, введите /is_anonymous_poll \n "
                "Если хотите выбор множество ответов /allows_multiple_answers"
                " \n Если хотите продолжить, введите /done"
            )


async def get_explanation(message: types.Message, state: FSMContext):
    """ Функция которая добавляет развернутый ответ. """
    async with state.proxy() as data:

        if message.text == "/done":  # пользователь ввел команду /done
            pass
        else:
            explanation = message.text
            # сохраняем развернутый ответ в хранилище состояний
            data["add_func"][0]["explanation"] = explanation
            await message.answer(
                "Вы добавили развернутый ответ к опросу. \n"
            )
        # Функция для ввода развернутого ответа завершена
        await message.answer(
            "Введите номер правильного ответа"
        )
        await Poll.answer.set()


async def create_poll(message: types.Message, state: FSMContext):
    """ Функция в которой создается Опрос."""
    async with state.proxy() as data:
        options = data["options"]  # Получаем все варианты ответов

        # Проверяем введенные данные
        if message.text.isnumeric():  # пользователь ввел номер ответа
            answer = int(message.text)  # а не другие данные
            if answer > len(options):
                await message.answer(
                    f"{answer} больше, чем вариантов ответа в опросе")
                return
        else:
            await message.answer(
                "напишите номер правильного ответа. \n "
                "Например: 2")
            return
        # Присваиваем введенные значения для создания Опроса
        question = data["question"]
        addition_func = data["add_func"][0]
        is_anonymous = addition_func["is_anonymous_poll"]
        allows_multiple_answers = addition_func["allows_multiple_answers"]
        explanation = addition_func["explanation"]

        # Создаем опрос и отправляем его пользователю который прислал сообщение
        await bot.send_poll(
            chat_id=message.chat.id,  # Сюда вы можете ввести id чата
            question=question,
            options=options,
            type=types.PollType.QUIZ,
            correct_option_id=answer-1,
            explanation=explanation,
            is_anonymous=is_anonymous,
            allows_multiple_answers=allows_multiple_answers
        )
        # Сбрасываем состояние FSM
        await state.finish()


def register_handlers_poll(dp: Dispatcher):
    """ Регистрируем обработчики для создания Опроса. """
    dp.register_message_handler(create_poll_start, commands=["poll"])
    dp.register_message_handler(process_question, state=Poll.question)
    dp.register_message_handler(process_options, state=Poll.options)
    dp.register_message_handler(additional_functions, state=Poll.add_func)
    dp.register_message_handler(get_explanation, state=Poll.explanation)
    dp.register_message_handler(create_poll, state=Poll.answer)
