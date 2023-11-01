import os
from typing import Any, Dict

import together
from langchain.llms.base import LLM
from langchain.utils import get_from_dict_or_env
from pydantic import Extra, root_validator

os.environ["TOGETHER_API_KEY"] = "1fb018c4ee838811a2e1125a5e92da6fdaa890e5cc530533dad7a1bb621867fb"

# set your API key
together.api_key = os.environ["TOGETHER_API_KEY"]

# list available models and descriptons
models = together.Models.list()

together.Models.start("togethercomputer/llama-2-7b-chat")


class TogetherLLM(LLM):
    """Together large language models."""

    model: str = "togethercomputer/llama-2-7b-chat"
    """model endpoint to use"""

    together_api_key: str = os.environ["TOGETHER_API_KEY"]
    """Together API key"""

    temperature: float = 0.0
    """What sampling temperature to use."""

    max_tokens: int = 2048
    """The maximum number of tokens to generate in the completion."""

    class Config:
        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that the API key is set."""
        api_key = get_from_dict_or_env(
            values, "together_api_key", "TOGETHER_API_KEY"
        )
        values["together_api_key"] = api_key
        return values

    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "together"

    def _call(
            self,
            prompt: str,
            **kwargs: Any,
    ) -> str:
        """Call to Together endpoint."""
        together.api_key = self.together_api_key
        output = together.Complete.create(prompt,
                                          model=self.model,
                                          max_tokens=self.max_tokens,
                                          temperature=self.temperature,
                                          )
        text = output['output']['choices'][0]['text']
        return text


llm = TogetherLLM(
    model="togethercomputer/llama-2-7b-chat",
    temperature=0.1,
    max_tokens=2048,
)

# Local Model Code: REPLACE THE CODE ABOVE

# MODEL CONFIGURATION

# import transformers  # Transformers library & modules
# from transformers import StoppingCriteria, StoppingCriteriaList
# from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

# Define the model ID. This is the identifier for the model we're going to use. model_id = '4bit/Llama-2-7b-chat-hf'
# This is a 4-bit quantized version of the model, if it doesn't work, use the original model
# `meta-llama/Llama-2-7b-chat-hf` alongside with `bitsandbytes` library (linux required & CUDA enabled) (code
# commented below)
#
# # Define the Hugging Face authentication token. This is required to access models from Hugging Face's model hub.
# hf_auth = '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' # Token to be updated, get yours from the huggingface platform
#
# # Create a configuration for BitsAndBytes. BitsAndBytes is a library for quantization of neural network parameters.
# bnb_config = transformers.BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_quant_type='nf4',
#     bnb_4bit_use_double_quant=True,
#     bnb_4bit_compute_dtype=bfloat16
# )
#
# # Create a configuration for our model using the AutoConfig class from the transformers library.
# model_config = AutoConfig.from_pretrained(
#     model_id,
#     use_auth_token=hf_auth
# )

# MODEL LOADING

# model = AutoModelForCausalLM.from_pretrained(
#     model_id,  # The model ID defined earlier.
#     trust_remote_code=True,  # This indicates that we trust the remote code. Be careful with this setting in a production environment.
#     config=model_config,  # The model configuration defined earlier.
#     quantization_config=bnb_config,  # The BitsAndBytes configuration defined earlier.
#     device_map='auto',  # This sets the device map to 'auto', which means the library will automatically select the best device to run the model (CPU or GPU).
#     use_auth_token=hf_auth  # The Hugging Face authentication token defined earlier.
# )
#
# # Set our model to evaluation mode. This is necessary before using the model for inference because it tells PyTorch
# to disable features like dropout that are used during training but not during inference. model.eval()
#
# # Load our tokenizer which is responsible for turning our input text into a format that the model can understand.
# tokenizer = AutoTokenizer.from_pretrained(
#     model_id,  # The model ID defined earlier.
#     use_auth_token=hf_auth  # The Hugging Face authentication token defined earlier.
# )
#
# print(f"Model loaded on {device}")

# DEFINING A STOPPING CRITERIA
# Define stop tokens and convert them to device tensors
# stop_list = ['\nHuman:', '\n```\n']
# stop_token_ids = [tokenizer(x)['input_ids'] for x in stop_list]
# stop_token_ids = [torch.LongTensor(x).to(device) for x in stop_token_ids]
#
# # Define custom stopping criteria class
# class StopOnTokens(StoppingCriteria):
#     def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
#         for stop_ids in stop_token_ids:
#             if torch.eq(input_ids[0][-len(stop_ids):], stop_ids).all():
#                 return True
#         return False
#
# # Set up stopping criteria for text generation
# stopping_criteria = StoppingCriteriaList([StopOnTokens()])

# PIPELINE AND LLM INITIALIZATION

# Initialize the text generation pipeline
# generate_text = transformers.pipeline(
#     model=model,
#     tokenizer=tokenizer,
#     return_full_text=True,
#     task='text-generation',
#     stopping_criteria=stopping_criteria,
#     temperature=0.1,
#     max_new_tokens=2048,
#     repetition_penalty=1.1
# )
#
# # Initialize language model manager (llm) pipeline
# llm = HuggingFacePipeline(pipeline=generate_text)
