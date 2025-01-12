import asyncio
import slack_app
import api


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(api.run_async(), slack_app.run_async()))


if __name__ == "__main__":
    main()
