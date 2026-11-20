import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import BUILD_JOBS, native_go

if __name__ == "__main__":
    native_go(__file__,
        repository='ollama/ollama',
        revision='e4ce68311a64310ece5534ae3a4820b20ea3d42f',
        package='./integration',
        selector='^TestContextExhaustion$',
        flags='-tags=integration',
        requires=['OLLAMA_HOST'],
        env={'CGO_ENABLED': '1', 'OLLAMA_TEST_EXISTING': '1'},
        setup=[['cmake', '--preset', 'CPU'], ['cmake', '--build', '--preset', 'CPU', '--parallel', f'{BUILD_JOBS}']],
        status='system dependency',
    )
