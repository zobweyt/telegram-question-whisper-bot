# Contributing

## Prerequisties:

- [`uv`](https://docs.astral.sh/uv/)
- [`just`](https://github.com/casey/just)

## Setup Instructions

1. **Clone the Repository**:

   ```sh
   git clone git@github.com:zobweyt/telegram-question-whisper-bot.git
   ```

2. **Navigate to the Project Directory**:

   ```sh
   cd telegram-question-whisper-bot
   ```

3. **Create a `.env` File from the Example**:

   ```sh
   cp .env.example .env
   ```

   Open the `.env` file and fill in the `TELEGRAM_BOT_TOKEN`. You can obtain this token by chatting with [@BotFather](https://t.me/BotFather).

   You can change the `TELEGRAM_SERVER` to `test` to run the bot on the test Telegram servers.

   Also, you may want to change `TELEGRAM_BOT_SET_MY` from `True` to `False` after first start to avoid rate-limits.

4. **Set up the development environment:** install pre-commit hooks:

   ```sh
   just init
   ```

## Scripts

### Default

List all available recipes.

```sh
just
```

### Init

Set up the development environment by installing pre-commit hooks.

```sh
just init
```

### Style Group

Collection of commands for running style checks on source files.

#### Style

Runs all style-checking recipes sequentially.

```sh
just style
```

or

```sh
just s
```

#### Lint

Runs Mypy to check for type errors in the source files.

```sh
just lint
```

or

```sh
just l
```

#### Check

Runs Ruff to check code quality and fix any issues automatically.

```sh
just check
```

or

```sh
just c
```

#### Format

Runs Ruff to format the source files according to coding standards.

```sh
just format
```

or

```sh
just f
```

### Development Group

Manages commands related to the development server.

#### Dev

Starts the development server and compiles internationalization (i18n) files before running.

```sh
just dev
```

or

```sh
just d
```

### Build Group

Build a production-ready binary for the bot.

#### Build

Uses PyInstaller to create a standalone binary executable.

```sh
just build
```

or

```sh
just b
```

### Internationalization (i18n) Group

Manages internationalization commands.

#### i18n-extract

Extracts translatable strings from the source code into a `.pot` files.

```sh
just i18n-extract
```

or

```sh
just ie
```

#### i18n-update

Updates the translation catalog to reflect changes in the `.pot` files.

```sh
just i18n-update
```

or

```sh
just iu
```

#### i18n-compile

Compiles the translation files into a usable format.

```sh
just i18n-compile
```

or

```sh
just ic
```

### Clean Group

Cleans up build artifacts and cache directories.

#### Clean

Removes all cache directories and unnecessary build files.

```sh
just clean
```

or

```sh
just c
```
