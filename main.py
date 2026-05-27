"""Application entry point for the FastAPI backend.

This module bootstraps the server, installs signal handlers, and manages
startup and shutdown for the async runtime.
"""

import asyncio
import contextlib
import signal

from src.setup import create_api_server
from src.utils.logging.setup import setup_logging, stop_logging


async def main() -> None:
    """Start the API server and keep it running until shutdown.

    Returns:
        Nothing. The coroutine runs the server until a shutdown signal is
        received.
    """
    # Set up logging
    logger = setup_logging()
    # Create API Server
    server = create_api_server()
    server_task = asyncio.create_task(server.serve())

    loop = asyncio.get_running_loop()

    def shutdown() -> None:
        """Request a graceful server shutdown from the signal handler."""

        logger.info("Shutdown signal received. Stopping the server...")
        server.should_exit = True

    # Register signal handlers
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, shutdown)

    try:
        await server_task
    except asyncio.CancelledError:
        logger.info("Server task was cancelled.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        # Cleanup resources
        logger.info("API has been stopped.")
        stop_logging()


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
