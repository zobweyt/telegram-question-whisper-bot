<p align="center">
  <img src="./docs/assets/logo.png" alt="logo" width="96" height="96" />
</p>

<h1 align="center">
  Telegram Question Whisper Bot
</h1>

<p align="center">
  Receive and send anonymous messages in Telegram!
</p>

## Features

- **Complete Anonymous Communication:** Handles all native Telegram message types and interactions, including:

  - **Text Messages:** Send formatted text messages.
  - **Replies:** Supports native reply functionality.
  - **Media:** Send photos, videos, and audio files.
  - **Files:** Share documents like PDFs.
  - **Polls:** Create and send polls.
  - **Stickers:** Use a variety of stickers.
  - **GIFs:** Send animated GIFs.
  - **Emojis:** Include various emojis for expression.
  - **Voice Messages:** Send recorded audio.
  - **Video Messages:** Share short video clips.
  - **Location Sharing:** Send your current location.
  - **Message Reactions:** Add or remove message reactions.
  - **Crypto Wallet Sharing:** Share cryptocurrency details easily.

- **Custom Anonymous Messages Link:** Create and edit personalized links for users to message you directly.

- **Custom Anonymous Messages Link Stats:** Monitor visit counts for your anonymous message links.

- **Direct Messaging:** Message others directly by sharing their contact information while keeping your identity secret if the recipient has previously interacted with the bot.

- **Localization:** Available in English and Russian, utilizing native Telegram localization settings.

- **Free and Open Source:** Easily deploy your own instance of the bot at no cost.

## Tech

### Production dependencies

[![Python Version](https://img.shields.io/badge/python%203.12-3776AB?logo=python&labelColor=gray)](https://www.python.org)
[![Aiogram](https://img.shields.io/badge/Aiogram-009CFB?logo=telegram&labelColor=gray)](https://aiogram.dev/)
[![Pydantic](https://img.shields.io/badge/Pydantic%202.0-E92063?logo=pydantic&labelColor=gray)](https://docs.pydantic.dev)
[![SQLite](https://img.shields.io/badge/SQLite-FFFFFF?logo=sqlite&labelColor=gray)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy%202.0-D71F00?logo=sqlalchemy&labelColor=gray)](https://www.sqlalchemy.org/)

#### Why SQLite?

SQLite is selected due to its straightforward setup and operational simplicity, making it ideal for a basic Telegram bot without the need for additional services.

### Development dependencies

[![just](https://img.shields.io/badge/just-000000?logo=gnometerminal&labelColor=gray)](https://github.com/casey/just)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/mypy-3776AB?logo=python&labelColor=gray)](https://github.com/python/mypy)

### Related Documentation

- [Database Entity-Relationship Diagram](./docs/infrastructure/DATABASE.md)
- [Service Architecture Overview](./docs/infrastructure/ARCHITECTURE.md)

## Deployment

If you'd like to deploy the bot, please visit [`DEPLOYMENT.md`](./docs/DEPLOYMENT.md).

## Contributing

If you'd like to contribute to this project, please visit [`CONTRIBUTING.md`](./docs/CONTRIBUTING.md).
