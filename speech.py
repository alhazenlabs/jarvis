from data_api.text_to_speech_dao import TextToSpeechDao
from audio_io.player import Player


text = """As an AI, I don't have personal experiences or opinions. However, there are several widely regarded places on Earth for skydiving that offer exceptional experiences. Some of these locations include:

1. Lake Taupo, New Zealand: Known for its stunning landscapes, Lake Taupo offers breathtaking views of mountains, lakes, and the majestic Huka Falls.

2. Fox Glacier, New Zealand: Skydiving over Fox Glacier provides an unparalleled experience with panoramic views of the Southern Alps, ice formations, and the Tasman Sea.

3. Hawaii, USA: Skydiving in Hawaii allows you to enjoy stunning views of the Pacific Ocean, lush greenery, and volcanic landscapes, creating a unique and memorable experience.

4. Namib Desert, Namibia: Skydiving over the Namib Desert offers a surreal experience with vast sand dunes, the Atlantic coastline, and captivating sunsets.    

5. Interlaken, Switzerland: Nestled in the Swiss Alps, Interlaken provides an unforgettable skydiving experience with breathtaking views of snow-capped mountains, lakes, and picturesque landscapes.

It is important to research and choose a highly reputable skydiving center that meets safety standards and offers professional instructors to ensure a safe and enjoyable adventure."""

text1 = "Sorry, I am having trouble connecting to the servers. Please try again later."
text2= "Sorry,  I couldn't understand what you are trying to say. Can you speak again."
if __name__ == "__main__":
    out = TextToSpeechDao.synthesize(text1)
    TextToSpeechDao.synthesize(text2)
