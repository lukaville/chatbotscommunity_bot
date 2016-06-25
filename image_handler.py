from PIL import Image, ImageDraw, ImageFont

from image_settings import *

LEFT_MARGIN = 38


def draw_text(image, title, phone, location, is_active, rating):
    mask = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(mask, mode='RGBA')
    # Название
    text_color = (118, 118, 118, 255)
    text_position = (LEFT_MARGIN, LEFT_MARGIN)
    font = ImageFont.truetype(ROBOTO_MEDIUM_PATH, 42)
    draw.text(
        text_position,
        title,
        font=font,
        fill=text_color
    )
    # Расположение
    text_color = (118, 118, 118, 255)
    text_position = (LEFT_MARGIN, 97)
    font = ImageFont.truetype(ROBOTO_REGULAR_PATH, 24)
    draw.text(
        text_position,
        location,
        font=font,
        fill=text_color
    )
    # Рейтинг
    text_color = (118, 118, 118, 255)
    text_position = (237, 140)
    font = ImageFont.truetype(ROBOTO_REGULAR_PATH, 24)
    draw.text(
        text_position,
        str(rating),
        font=font,
        fill=text_color
    )
    # Телефон
    if phone:
        text_color = (118, 118, 118, 255)
        text_position = (LEFT_MARGIN, 189)
        font = ImageFont.truetype(ROBOTO_LIGHT_PATH, 42)
        draw.text(
            text_position,
            phone,
            font=font,
            fill=text_color
        )
    # Работает
    text_color = (112, 191, 49, 255) if is_active else (205, 52, 31, 255)
    text_position = (LEFT_MARGIN, 256)
    font = ImageFont.truetype(ROBOTO_MEDIUM_PATH, 24)
    draw.text(
        text_position,
        'Сейчас работает' if is_active else 'Закрыто',
        font=font,
        fill=text_color
    )

    result_image = Image.alpha_composite(image, mask)
    return result_image


def draw_stars(image, rating):
    star_active = Image.open(STAR_ACTIVE_PATH).convert('RGBA')
    star_inactive = Image.open(STAR_INACTIVE_PATH).convert('RGBA')
    if rating is not None:
        stars_count = int(rating)
    else:
        stars_count = 0
    for i in range(5):
        star_left_margin = LEFT_MARGIN + 39 * i
        star_image = star_active if stars_count > i else star_inactive
        image.paste(star_image, (star_left_margin, 140), star_image)
    return image


def handle_image(title, location, phone, is_active, rating):
    image = Image.open(CARD_PATH).convert('RGBA')
    image = draw_text(image, title, phone, location, is_active, rating)
    image = draw_stars(image, rating)
    image.show()
    image.save(OUTPUT_PATH, quality=100, optimize=True, progressive=True)


# Пример
# handle_image(
#     title='McDonalds',
#     location='ТЦ "Охотный ряд", Манежная пл., 1',
#     phone='8 (495) 123-12-12',
#     rating=4.1,
#     is_active=True
# )
