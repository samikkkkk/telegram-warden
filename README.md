# Telegram Warden - Don't hide, you've already been found.

Telegram Warden - An advanced utility for saving deleted messages, modified text, and even self-deleting messages based on the Telegram Business platform's chatbot system.

## How does this work

<details>
<summary>Deleted messages</summary>
Any message sent to a chat under the chatbot's control is saved to the database. After handling the message deletion event from the business chat, the bot retrieves the message text and other information from the database and then sends a report to its owner.
</details>

<details>
<summary>Edited messages</summary>
Any change to the chat message text under the chatbot's control is recorded in the database. After handling the message change event, the bot retrieves the message text and its change history (updates) from the database, summarizes it all, and sends the log to the owner.
</details>

<details>
<summary>Self-destruting(one-time) messages</summary>
Self-destructing (one-time) messages cannot be caught in any way, so the message object is retrieved by a person's reply to the one-time message.

The detailed algorithm is described in catching/destructing_msgs.py
</details>

## How deep is the logging?

Message logging is limited by the capabilities and basic rights of the Telegram Business chatbot. Logging messages from secret chats, public groups, or other chats is not possible due to Telegram limitations.

## Project structure

```bash
 TELEGRAM-WARDEN/ - root/project
├── catching/ - handlers responsible for catching deletions/changes of messages of the following types
│   ├── deleted.py - handling of deleted messages
│   ├── destructing_msgs.py - handling self-destructing messages
│   ├── doc.py - document handling
│   ├── photo.py - handling photo
│   ├── text.py - text handling
│   ├── video.py - handling video
│   └── voice.py -  voice message handling
├── database/ - database (structure and queries)
│   ├── requests.py - database queries
│   └── structure.py - database structure
├── utils/ - utilities for handlers
│   └── get_file.py - receiving a file (used in catching/destructing_msgs.py)
├── config.py - bot configuration
├── .env.example - .env example
├── docker-compose.yml - Docker Compose configuration
├── Dockerfile - docker configuration
├── main.py - main file
└── requirements.txt - dependencies
```

## How to install

First of all, we need to create a bot in @Botfather and activate business mode for it.

<details>
<summary>Create a bot, activate business mode</summary>
1.Go to @BotFather PM and create a new bot.(Save the bot token!)

![New bot](https://segs.lol/rsEeeT)

2.Go to my bots and select bot
![To settings](https://segs.lol/E4DFWk)

3.Go to "Bot settings"
![Bot settings](https://segs.lol/McSbJs)

4.And "Business Mode"
![Business Mode](https://segs.lol/qtYkqQ)

5.Turn ON Business mode
![Activate business](https://segs.lol/lx8gBX)
</details>

After receiving the token (you should have saved it from point 1), we need to get our ID.

<details>
<summary>Get ID</summary>
1.Enter @usinfobot in the input field and then enter your username.

![Get id](https://segs.lol/rBY6mo)

2.Select the second item and copy the ID displayed to you (just click on it)
</details>

After this, we need to download the bot to our computer and run it.

<details>
<summary>Download</summary>
1.Git clone

```bash
git clone https://github.com/samikkkkk/telegram-warden.git
```

2.Docker
Will be added later
</details>

We can launch the bot in several ways.

But first of all, we need to add the token and our ID to .env

1.Change .env.example to .env

```bash
cd telegram-warden
```

```bash
cp .env.example .env
```

2.Fill .env with your data

```bash
nano .env
```

After that, we run the code either in the usual way or via docker-compose

<details>
<summary>Usual way</summary>

1.Install dependences

```bash
pip install -r requirements.txt
```

2.Launch

```bash
python3 main.py
```

</details>

<details>
<summary>Docker</summary>

1. Run with one command

```bash
docker-compose up -d
```

## Don't forget to start a conversation with your created bot, otherwise the logs won't be sent