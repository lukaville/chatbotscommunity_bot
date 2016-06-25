from PIL import Image, ImageDraw, ImageFont

from image_settings import *


def draw_text(image, title, location, is_active, rating):
    LEFT_MARGIN = 38
    mask = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(mask, mode='RGBA')

    # Название
    text_color = (118, 118, 118, 255)
    text_position = (LEFT_MARGIN, LEFT_MARGIN)
    font = ImageFont.truetype(ROBOTO_MEDIUM_PATH, 50)
    draw.text(
        text_position,
        title,
        font=font,
        fill=text_color
    )
    # Расположение
    text_color = (118, 118, 118, 255)
    text_position = (LEFT_MARGIN, 93)
    font = ImageFont.truetype(ROBOTO_REGULAR_PATH, 32)
    draw.text(
        text_position,
        location,
        font=font,
        fill=text_color
    )
    # Рейтинг
    text_color = (118, 118, 118, 255)
    text_position = (237, 136)
    font = ImageFont.truetype(ROBOTO_REGULAR_PATH, 32)
    draw.text(
        text_position,
        str(rating),
        font=font,
        fill=text_color
    )
    # Работает
    text_color = (112, 191, 49, 255) if is_active else (205, 52, 31, 255)
    text_position = (LEFT_MARGIN, 256)
    font = ImageFont.truetype(ROBOTO_MEDIUM_PATH, 32)
    draw.text(
        text_position,
        'Сейчас работает' if is_active else 'Закрыто',
        font=font,
        fill=text_color
    )

    result_image = Image.alpha_composite(image, mask)
    result_image.show()
    return result_image


def draw_stars(image, stars_count):
    mask = Image.new('RGBA', image.size, (255, 255, 255, 0))


def handle_image(title, location, is_active, rating):
    image = Image.open(CARD_PATH).convert('RGBA')
    image = draw_text(image, title, location, is_active, rating)
    draw_stars(image, rating)


handle_image(
    title='McDonalds',
    location='ТЦ "Охотный ряд", Манежная пл., 1,',
    rating=4.1,
    is_active=True
)
