from pathlib import Path
import os
import tomllib
from pydantic import BaseModel


class _DeepSeekModel(BaseModel):
    deepseek_model: str
    deepseek_base_url: str
    deepseek_api_key: str

class _ToolsKeysModel(BaseModel):
    tavily_api_key:str

class _Config(BaseModel):
    DeepSeekModel: _DeepSeekModel
    ToolsKeysModel: _ToolsKeysModel


toml_path = Path(__file__).parent.parent / "config\\config.toml"
with open(toml_path, "rb") as f:
    Config = _Config(**tomllib.load(f))

# if deepseek_model := os.environ.get("DEEPSEEK_MODEL"):
#     Config.DeepSeekModel.deepseek_model = deepseek_model
#
# if deepseek_base_url := os.environ.get("DEEPSEEK_BASE_URL"):
#     Config.DeepSeekModel.deepseek_base_url = deepseek_base_url
#
# if deepseek_api_key := os.environ.get("DEEPSEEK_API_KEY"):
#     Config.DeepSeekModel.deepseek_api_key = deepseek_api_key

overrides = {
    k:v for k,v in {
        "deepseek_model": os.environ.get("DEEPSEEK_MODEL"),
        "deepseek_base_url" : os.environ.get("DEEPSEEK_BASE_URL"),
        "deepseek_api_key" : os.environ.get("DEEPSEEK_API_KEY")
    }.items() if v
}
if overrides:
    Config.DeepSeekModel = Config.DeepSeekModel.model_copy(update=overrides)

DeepSeekModel = Config.DeepSeekModel
ToolsModel = Config.ToolsKeysModel