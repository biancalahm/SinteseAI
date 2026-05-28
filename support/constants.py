#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import getenv
from dotenv import load_dotenv
load_dotenv()


class Constants: 

    ELASTIC_SEARCH_URL = getenv("ELASTIC_SEARCH_URL")
    INDEX_NAME = getenv("INDEX_NAME")
    EMBEDDING_MODEL = getenv("EMBEDDING_MODEL")
    OLLAMA_MODEL = getenv("OLLAMA_MODEL")
    