set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

python_dir := ".venv/" + if os_family() == "windows" { "Scripts" } else { "bin" }
python := python_dir + if os_family() == "windows" { "/python.exe" } else { "/python3" }

format:
    {{ python }} -m isort .
    {{ python }} -m black .

install:
    uv venv
    uv pip install "."

install-dev:
    uv sync # `--group dev`` is the default

demo:
    uv run demo.py

init APIKEY:
    uv run shodan init {{ APIKEY }}

shodan *ARGS:
    uv run shodan {{ ARGS }}