import shlex
from typing import Optional

import docker
from docker.errors import DockerException


def run_playwright_docker(input_text: str) -> Optional[str]:
    if not input_text or not input_text.strip():
        raise ValueError("Input text cannot be empty")

    try:
        client = docker.from_env()
        container = client.containers.run(
            "web-automation",
            shlex.quote(input_text),  # Properly escape the input string
            detach=True,
        )

        logs = container.logs(stream=True)
        for log in logs:
            print(log.strip().decode("utf-8"))

        container.wait()
        return container.logs().decode("utf-8")

    except DockerException as e:
        print(f"Docker error: {e}")
        return None


if __name__ == "__main__":
    input_text = "test name"
    if result := run_playwright_docker(input_text):
        print("Result from Docker container:", result)
    else:
        print("Failed to get result from container")
