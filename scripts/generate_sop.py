import yaml
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# Load the config
cfg_path = Path("config/config.yaml")
cfg = yaml.safe_load(cfg_path.read_text())

# For each phase, read its .md content into a string
for idx, phase in enumerate(cfg["phases"], start=1):
    md_path = Path(f"phases/phase{idx}/{phase['framework']}.md")
    phase["content"] = md_path.read_text()

# Set up Jinja environment
env = Environment(loader=FileSystemLoader("layouts"))
template = env.get_template("sop.md.j2")

# Render and write to combined.md
output = template.render(cfg)
Path("combined.md").write_text(output)
