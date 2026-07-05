"""Minimal settings for running makemigrations without dev-only packages."""
from config.settings.base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = ["*"]
