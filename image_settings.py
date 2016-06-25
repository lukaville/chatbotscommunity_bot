import os

RESOURCE_BASE_DIR = 'resources'

IMAGE_BASE_DIR = os.path.join(RESOURCE_BASE_DIR, 'images')
FONT_BASE_DIR = os.path.join(RESOURCE_BASE_DIR, 'fonts')

CARD_PATH = os.path.join(IMAGE_BASE_DIR, 'card.png')
STAR_ACTIVE_PATH = os.path.join(IMAGE_BASE_DIR, 'star_active.png')
STAR_INACTIVE_PATH = os.path.join(IMAGE_BASE_DIR, 'star_inactive.png')

ROBOTO_LIGHT_PATH = os.path.join(FONT_BASE_DIR, 'Roboto-Light.ttf')
ROBOTO_MEDIUM_PATH = os.path.join(FONT_BASE_DIR, 'Roboto-Medium.ttf')
ROBOTO_REGULAR_PATH = os.path.join(FONT_BASE_DIR, 'Roboto-Regular.ttf')

OUTPUT_PATH = os.path.join(RESOURCE_BASE_DIR, 'output/temp.png')
