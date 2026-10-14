"""Replace an unsent working prompt with clear prose; source excerpts unchanged."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
path=HERE/'build_device_lifecycle_conference.py'
text=path.read_text(encoding='utf-8')
start=text.index('header="""')
end=text.index('parts=[header]',start)
text=text[:start]+"header=(HERE/'DEVICE_LIFECYCLE_QUESTIONS.md').read_text(encoding='utf-8')\n"+text[end:]
path.write_text(text,encoding='utf-8')
print('Prepared readable source-conference questions.')
