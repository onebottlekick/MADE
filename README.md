# MADE(Multi-Agent Development)

## Requirements

- Python 3.9+
- Ollama installed and running

## installation

### From PyPI

```bash
pip install llm-made
```

### From Source

```bash
git clone https://github.com/onebottlekick/MADE
cd MADE
pip install -e .
```

## Components

### Engine

The engine module contains the core logic and entities required for the multi-agent system.

```python
@dataclass
class OllamaConfig:
    base_url: str = "http://127.0.0.1:11434/v1/"
    model: str = MODEL_NAME
    api_key: str = "anything would be fine"
    max_tokens: int = 40000
    temperature: float = 1.0
    top_p: float = 1.0
```

The `OllamaConfig` class is used to configure the Ollama API. The `base_url` is the URL of the Ollama API, the `model` is the name of the model to be used, the `api_key` is the API key for the Ollama API, and the `max_tokens` is the maximum number of tokens that can be generated by the Ollama API. The `temperature` and `top_p` parameters are used to control the randomness of the generated text.

### Agent

The agent module manages the different agents involved in the system, including their entities, repositories, and services.

```python
@dataclass(frozen=True)
class ChatAgentResponse:
    messages: List[BaseChatMessage]
    terminated: bool
    info: Dict[str, Any]
```

The `ChatAgentResponse` class is used to store the response from the chat agent. The `messages` attribute is a list of chat messages, the `terminated` attribute is a boolean value indicating whether the chat is terminated, and the `info` attribute is a dictionary containing additional information.

### Role Playing

The role-playing module simulates interactions between different roles, such as programmers and reviewers, to facilitate various phases of software development.

```python
@dataclass
class RoleType:
    CEO: str = "Chief Executive Officer"
    CPO: str = "Chief Product Officer"
    CTO: str = "Chief Technology Officer"
    COUNSELOR: str = "Counselor"
    PROGRAMMER: str = "Programmer"
    REVIEWER: str = "Code Reviewer"
    TESTER: str = "Software Test Engineer"
```

The `RoleType` class is used to define the different roles that can be played in the system. The roles include CEO, CPO, CTO, Counselor, Programmer, Reviewer, and Tester.

```python
@dataclass
class RolePrompt:
    CEO: str = ...
    CPO: str = ...
    CTO: str = ...
    COUNSELOR: str = ...
    PROGRAMMER: str = ...
    REVIEWER: str = ...
    TESTER: str = ...
"""
```

The `RolePrompt` class is used to define the prompts for each role. The prompts are used to guide the interactions between the different roles. You can see the full implementation in the code.

### Phase

The phase module handles different phases of the software development lifecycle, such as code review and error summarization.

```python
@dataclass
class PhasePrompt:
    demand_analysis: str = ...
    language_choose: str = ...
    coding: str = ...
    code_complete: str = ...
    code_review_comment: str = ...
    code_review_modification: str = ...
    test_error_summary: str = ...
    test_modification: str = ...
    manual: str = ...
```

The `PhasePrompt` class is used to define the prompts for each phase of the software development lifecycle. The prompts are used to guide the interactions between the different roles during each phase. The full implementation can be found in the code.

```python
@dataclass
class PhaseStates:
    task: str = ""
    description: str = ""
    modality: str = ""
    language: str = ""
    ideas: str = ""
    codes: str = ""
    comments: str = ""
    review_comments: str = ""
    test_reports: str = ""
    exist_bugs_flag: bool = False
    error_summary: str = ""
    cycle_index: int = 1
    unimplemented_file: str = ""
    max_num_implement: int = 5
    num_tried: int = 0
    modification_conclusion: str = ""
    gui: bool = False
    code_files: List[str] = ""
    requirements: str = ""
```

The `PhaseStates` class is used to store the state of each phase of the software development lifecycle. The state includes the task, description, modality, language, ideas, codes, comments, review comments, test reports, error summary, cycle index, unimplemented file, maximum number of implementations, number of tried implementations, modification conclusion, GUI flag, code files, and requirements.

```python
@dataclass
class PhaseChatTurnLimit:
    demand_analysis: int = 2
    language_choose: int = 2
    coding: int = 5
    code_complete: int = 3
    code_review_comment: int = 1
    code_review_modification: int = 1
    test_error_summary: int = 1
    test_modification: int = 1
    manual: int = 4
```

The `PhaseChatTurnLimit` class is used to define the maximum number of chat turns allowed for each phase of the software development lifecycle.

```python
@dataclass
class PhaseEngineConfig:
    demand_analysis: EngineParams = EngineParams(temperature=0.7, top_p=0.8)
    language_choose: EngineParams = EngineParams(temperature=0.3, top_p=0.1)
    coding: EngineParams = EngineParams(temperature=0.2, top_p=0.1)
    code_complete: EngineParams = EngineParams(temperature=0.1, top_p=0.1)
    code_review_comment: EngineParams = EngineParams(temperature=0.1, top_p=0.1)
    code_review_modification: EngineParams = EngineParams(temperature=0.2, top_p=0.1)
    test_error_summary: EngineParams = EngineParams(temperature=0.1, top_p=0.1)
    test_modification: EngineParams = EngineParams(temperature=0.1, top_p=0.1)
    manual: EngineParams = EngineParams(temperature=0.7, top_p=0.4)
```

The `PhaseEngineConfig` class is used to configure the engine parameters for each phase of the software development lifecycle. The parameters include the temperature and top_p values for each phase.

#### Custom Phase

```python
from made.chat_env.repository.chat_env_repository_impl import ChatEnvRepositoryImpl
from made.engine import ModelConfig
from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl

@PhaseRegistry.register()
class ExamplePhase(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config: ModelConfig,
        phase_prompt: str = "discuss about multi llm agents",
        assistant_role_name: str = "assistant",
        assistant_role_prompt: str = "You are a helpful {assistant_role}",
        user_role_name: str = "user",
        user_role_prompt: str = "You are discussing about {task} with {assistant_role}",
        chat_turn_limit: int = 5
        temperature=0.1,
        top_p=0.2,
    ):
        super().__init__(
            model_config=model_config,
            phase_prompt=phase_prompt,
            assistant_role_name=assistant_role_name,
            assistant_role_prompt=assistant_role_prompt,
            user_role_name=user_role_name,
            user_role_prompt=user_role_prompt,
            chat_turn_limit=chat_turn_limit
            temperature=temperature,
            top_p=top_p,
        )

    def update_phase_states(self, env: ChatEnvRepositoryImpl):
        ...

    def update_env_states(self, env: ChatEnvRepositoryImpl):
        ...
```

To create a custom phase, you need to create a class that inherits from `BasePhaseRepositoryImpl` and decorate it with the `@PhaseRegistry.register()` decorator. You can then implement the `update_phase_states` and `update_env_states` methods to update the phase and environment states, respectively.

```python
custom_phase = phase_service.get_phase(phase_name="Example")
```

You can then use the `get_phase` method of the `PhaseService` class to get an instance of the custom phase.

### Chat Chain

The chat chain module manages the chat interactions between different agents and roles. Interactions with tools are not implemented yet.

```python
@dataclass
class EnvConfig:
    task_prompt: str
    directory: str = "project_zoo"
    background_prompt: str = (
        "SI-follow is a software company powered by LLM multi-agent"
    )
    clear_structure: bool = True
    incremental_develop: bool = False
    git_management: bool = False
    gui_design: bool = True
```

The `EnvConfig` class is used to configure the environment for the chat chain. The `task_prompt` is the prompt for the task, the `directory` is the directory where the project files are stored, the `background_prompt` is the background prompt for the chat, the `clear_structure` flag indicates whether the project structure should be cleared, the `incremental_develop` flag indicates whether incremental development should be used, the `git_management` flag indicates whether Git management should be used, and the `gui_design` flag indicates whether GUI design should be used.

```python
@dataclass
class EnvStates:
    task_description: str = ""
    modality: str = ""
    ideas: str = ""
    language: str = ""
    review_comments: str = ""
    error_summary: str = ""
    test_reports: str = ""
    codes: Dict[str, str] = field(default_factory=dict)
    manual: str = ""
    requirements: str = ""
```

The `EnvStates` class is used to store the state of the environment for the chat chain. The state includes the task description, modality, ideas, language, review comments, error summary, test reports, codes, manual, and requirements.

```python
chain = ChatChainServiceImpl(
    task_prompt="Discuss about AI technologies.",
    directory="project_zoo/test_dir",
    base_url="https://si-follow.loca.lt/v1/",
    model="llama3.2",
    phases=[
        "First",
        "Second",
    ],
    env_states=ExampleEnvStates(),
    save_chain=True,
    git_management=True
)
chain.run()
```

You can create an instance of the `ChatChainServiceImpl` class to run the chat chain. You can configure the task prompt, directory, base URL, model, phases, environment states, save chain flag, and Git management flag. Loading saved chain is automatically handled. Default name of the saved chain is `chain`. You can change it by passing `save_name` parameter.

## Playground

Everything is in examples folder. You can modify all the configs explained above and run the examples to see the results. The full pipeline is implemented in the `examples/pipeline`

## this repository was modified from [ChatDev:https://github.com/OpenBMB/ChatDev]
