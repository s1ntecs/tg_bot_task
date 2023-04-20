from aiogram import types, Dispatcher
import aiohttp


# URLS = ['http://theoldreader.com/kittens/600/400/',
#         'https://dog.ceo/api/breeds/image/random']


async def get_random_dog_image():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://dog.ceo/api/breeds/image/random') as response:
            response_json = await response.json()
            return response_json


async def send_random_animal_photo(message: types.Message):
    pet = await get_random_dog_image()
    return await message.answer(pet["message"])


def register_handlers_animal_img(dp: Dispatcher):
    dp.register_message_handler(send_random_animal_photo,
                                commands=["cute_animals"])
