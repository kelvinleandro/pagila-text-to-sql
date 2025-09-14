import time


def create_stream_effect(text: str):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.025)
