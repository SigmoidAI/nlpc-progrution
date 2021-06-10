'''
Made with love by Sigmoid.

@author - Păpăluță Vasile (papaluta.vasile@isa.utm.md)
'''
# Importing all needed libraries and modules.
import json
import requests
import random
from database import Messages
from googleapiclient.discovery import build

# Predifined phrases.
greetings = ["Hi"]
farewells = ['Bye', 'Bye-Bye', 'Goodbye', 'Have a good day', 'Stop']
thank_you = ['Thanks', 'Thank you', 'Thanks a bunch', 'Thanks a lot.', 'Thank you very much', 'Thanks so much',
             'Thank you so much']
thank_response = ['You\'re welcome.', 'No problem.', 'No worries.', ' My pleasure.', 'It was the least I could do.',
                  'Glad to help.']

# The telegram bot class.
class telegram_bot:
    def __init__(self, tech_nontech_pipeline : 'sklearn.pipeline.Pipeline', sentiment_pipeline : 'sklearn.pipeline.Pipeline', tech_cls_pipeline : 'sklearn.pipeline.Pipeline') -> None:
        '''
            The constructor of the telegram bot.
        :param pipeline: 'sklearn.pipeline.Pipeline'
            The sklearn Pipeline implemented for classifying messages.
        :param db: 'shelve.DbfilenameShelf'
            The data storing object from shelve.
        '''
        # Setting up the token and the url for the bot.
        self.token = '956587904:AAG8PfZl5hQmbou_f8IvqQT7Tf2unyvJ1LY'
        self.url = f"https://api.telegram.org/bot{self.token}"

        # google api keys and token
        #  The api_key can be acquired from https://developers.google.com/custom-search/v1/overview
        self.api_key = 'AIzaSyA6YferwfRzHqtBkmZSM5dVXmVMZbpNDjM'

        # You can create a custom search engine and select what web pages to search on https://cse.google.com/cse/all
        # from there you can also acquire the search_engine_id
        self.search_engine_id = '90c5898ceb36f6a9d'

        # database
        self.db_manager = Messages()

        # memes kekw hehedoge
        self.memes_list = [
            'https://assets3.thrillist.com/v1/image/2625863/1584x3000/scale;jpeg_quality=60.jpg',
            'https://pbs.twimg.com/media/B7Q9Fx7CMAAywPR?format=jpg&name=900x900',
            'https://pbs.twimg.com/media/C25DGOBXUAEsUy1?format=jpg&name=large',
            'https://pbs.twimg.com/media/DIBql-6VYAEKAXz?format=jpg&name=medium'
        ]

        # Setting up the pipeline and the pseudo data base.
        self.tech_nontech_pipeline = tech_nontech_pipeline
        self.sentiment_pipeline = sentiment_pipeline
        self.tech_cls_pipeline = tech_cls_pipeline

        # encouraging messages
        self.pep_talk = [
            'Everything is going to be ok', 'Rome wasn\'t built in one day', 'Sleep, Eat, Code, Repeat', 'Just *ucking do it'
        ]

    def google_search(self, search_term : str, **kwargs):
        '''
            This functions queries a custom google based search engine.
        :param search_term: str
            The query term
        '''
        service = build("customsearch", "v1", developerKey=self.api_key)
        result = service.cse().list(q=search_term, cx=self.search_engine_id, **kwargs).execute()
        return [ r['link'] for r in result['items'][ : 3]]

    def send_meme(self, chat_id : int, photo=None):
        '''
            This function sends a photo to a telegram chat
        :param chat_id: int
            The id of the chat where the bot sends the picture
        '''
        if photo is None:
            photo = random.choice(self.memes_list)
        res = requests.post(
            f'https://api.telegram.org/bot{self.token}/sendPhoto?chat_id={chat_id}&photo={photo}',
        )
        res = json.loads(res.content)

    def choose_reply(self, user_msg : str, chat_id : int, user_id : int, name : str) -> None:
        '''
            This function chooses what function to send.
        :param user_msg: str
            The user message extracted from the request.
        :param chat_id: int
            The id of the chat.
        :param user_id: int
            The id of user.
        :param name: str
            The name of the user that send this message.
        '''
        # Checking if message is not a farewell.
        if user_msg not in farewells:

            # If message is a /start command we will sent greeting message.
            if user_msg == '/start':
                bot_resp = f"""Hi! {name}. I am proTexter. \nI'll keep the bad guys out. \nType Bye to Exit."""
                self.send_message(bot_resp, chat_id)
            # If message is a thank you form we wil send to the user a thank you response.
            elif user_msg in thank_you:
                bot_response = random.choice(thank_response)
                self.send_message(bot_response, chat_id)
            # If message is a greeting we will send the user a random greeting back.
            elif user_msg in greetings:
                bot_response = random.choice(greetings)
                self.send_message(bot_response, chat_id)
            # If the text message is nothing above we will verify if it isn't prostitute offer using the pipeline.
            else:
                # Verifying the message.
                bot_response = self.verify_msg(user_msg, chat_id, user_id, name)

                # Sending the last message.
                self.send_message(bot_response, chat_id)
        else:
            # If message si a farewell then we will send bye to the user.
            bot_response = random.choice(farewells)
            self.send_message(bot_response, chat_id)

    def verify_msg(self, user_msg, chat_id, user_id, name):
        '''
            This function chooses finds out using the model.
        :param user_msg: str
            The user message extracted from the request.
        :param chat_id: int
            The id of the chat.
        :param user_id: int
            The id of user.
        :param name: str
            The name of the user that send this message.
        '''
        # Getting the prediction from the tech-non-tech pipeline.
        prediction = self.tech_nontech_pipeline.predict([user_msg])

        # Acquiring the sentiment score from the sentiment pipeline
        sentiment_score = self.sentiment_pipeline.predict_proba([ user_msg ])[0][1]

        if sentiment_score < 0.5:
            # sending to the user a pep talk and a meme
            self.send_message(random.choice(self.pep_talk), chat_id=chat_id)
            self.send_meme(chat_id=chat_id)
            new_prediction = 'Nontech'

        elif prediction[0] == 'Nontech':
            # doing nothing just setting things
            message = 'Nontech'
            new_prediction = 'Nontech'

        else:
            # getting which technology the user talks about 
            message = 'Tech'
            new_prediction = self.tech_cls_pipeline.predict([user_msg])[0]
            # asking google for help :)
            links = self.google_search(search_term=user_msg)
            self.send_message('This may be helpful for you: ', chat_id)
            # sending the list of results
            for link in links:
                self.send_message(link, chat_id)

        # saving message related information in the database
        self.db_manager.insertOne(chat_id=chat_id, user_id=user_id, content=user_msg, score=sentiment_score, technology=new_prediction)
        # sending a meme aleatorilly
        if random.choice([ 1, 0, 0, 0, 0 ]):
            mean_score = self.db_manager.userMeanScore(user_id=user_id)
            if mean_score < 0.7:
                self.send_meme(chat_id=chat_id)

    def get_updates(self, offset : int =None) -> dict:
        '''
            THis function is getting the last messages in the chat
        :param offset: int
            The offset for requesting the data.
        :return: dict
            The last messages data.
        '''
        url = self.url + "/getUpdates?timeout=100"
        if offset:
            url = url + f"&offset={offset + 1}"
        url_info = requests.get(url)
        return json.loads(url_info.content)

    def send_message(self, msg : str, chat_id : int) -> None:
        '''
            This function allows the chatbot to send messages in the chat.
        :param msg: str
            The user message extracted from the request.
        :param chat_id: int
            The id of the chat.
        '''
        url = self.url + f'/sendMessage?chat_id={chat_id}&text={msg}'
        if msg is not None:
            requests.get(url)