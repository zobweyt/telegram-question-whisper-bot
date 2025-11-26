# Deployment

Follow these steps to deploy the bot:

1. Clone the repository:

   ```sh
   git clone git@github.com:zobweyt/telegram-question-whisper-bot.git
   ```

2. Navigate to the project directory:

   ```sh
   cd telegram-question-whisper-bot
   ```

3. Create a `.env` file from the example provided.

   ```sh
   cp .env.example .env
   ```

   Open the `.env` file and fill `TELEGRAM_BOT_TOKEN`. You can get it using [@BotFather](https://t.me/BotFather).

4. Select one of the following options for deployment:

## Docker

To run the bot using Docker, use the commands below:

### Start the Bot

```sh
docker compose up -d
```

### Stop the Bot

```sh
docker compose down -v
```

## Standalone Binary Executable

If you prefer a standalone option, you can use PyInstaller to build the bot for Windows, Linux, or macOS.

1. Make sure you have [`uv`](https://docs.astral.sh/uv/) and [`just`](https://github.com/casey/just) installed on your system as they're required for building.

   ```sh
   uv --version
   just --version
   ```

2. Run the following command to create the executable:

   ```sh
   just build
   ```

3. Execute the bot with this command:

   ```sh
   ./dist/__main__
   ```

   Note: You can safely move this executable to a different location and rename it as needed. Just remember to also relocate the `.env` file and `db.sqlite3`.
