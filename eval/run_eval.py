import argparse
from . import eval_whisper_openai
from . import eval_whisper_huggingface
from . import eval_faster_whisper
from . import eval_whisper_pipeline
from utils import get_eval_info


def eval_whisper(args):
    eval_options = {
        'openai': eval_whisper_openai,
        'faster': eval_faster_whisper,
        'huggingface': eval_whisper_huggingface,
        'pipeline': eval_whisper_pipeline,
    }
    eval_type, kwargs = get_eval_info(args)
    eval_options[eval_type](**kwargs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='eval whisper')
    parser.add_argument('--config',                 help='config path',                type=str)
    parser.add_argument('--model_type',             help='type of model',              type=str)
    parser.add_argument('--model_index',            help='index of model list',        type=int)
    parser.add_argument('--lora_dir', default=None, help='directory of LoRA file',     type=str)
    parser.add_argument('--data_index',             help='index of dataset list',      type=int)
    parser.add_argument('--language',               help='whisper inference language', type=str)
    parser.add_argument('--batch_size',             help='batch size',                 type=int)
    parser.add_argument('--use_cpu', default=False, help='ct2: use cpu of ct2model',   type=bool)
    parser.add_argument('--compute_type',           help='ct2: auto/int8/float16...',  type=str)
    parser.add_argument('--num_workers',            help='num of workers          ',   type=int)
    parser.add_argument('--pipeline',               help='use transformers pipeline',  type=int)
    parser.add_argument('--use_flash_attention_2',  help='whether use flash attn 2',   type=int)
    parser.add_argument('--torch_dtype',            help='fp16, bf16',                 type=str)
    parser.add_argument('--use_bettertransformer',  help='pipeline options',           type=int)
    parser.add_argument('--use_compile',            help='pipeline options',           type=int)
    parser.add_argument('--assistant_model_path',   help='pipeline options',           type=str)
    parser.add_argument('--preheat',                help='whether preheat first',      type=int)
    parser.add_argument('--gpu',     default=0,     help='gpu id',                     type=str)
    args = parser.parse_args()

    eval_whisper(args)
