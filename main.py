import asyncio
import slack
import api


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(api.run_async(), slack.run_async()))


if __name__ == "__main__":
    main()
