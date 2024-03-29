import os
import re
import opencc
from .num2char import num_to_char
import multiprocessing
from utils import get_file, save_file

'''

标准化测试输出的reg_orig.trn和std_orig.trn
包括[删除特殊符号, 中文字符繁体转简体, 英文字母大写转小写, 阿拉伯数字转为中文数字]
输出结果为同一目录下的reg.trn和std.trn

'''

def norm_single_sentence(sentence: str) -> str:
    converter = opencc.OpenCC('t2s.json')
    sentence = sentence.strip()
    # filter special symbol
    sentence = re.sub(r'[^\w\s]', '', sentence).replace(' ', '')
    # simplified -> traditional Chinese
    sentence = converter.convert(sentence)
    # lower English character
    sentence = sentence.lower()
    # digit -> Chinese character
    sentence = num_to_char(sentence)
    return sentence


def single_normalization(args):
    trans, refs, start, end = args
    trans_result, refs_result = [], []
    for i in range(start, end):
        trans_s = trans[i].strip().split('(')
        refs_s = refs[i].strip().split('(')

        trans_idx = trans_s[-1][: -1]
        refs_idx = refs_s[-1][: -1]

        trans_norm = norm_single_sentence(''.join(trans_s[:-1]))
        refs_norm = norm_single_sentence(refs_s[0])

        trans_result.append(f'{trans_norm} ({trans_idx})')
        refs_result.append(f'{refs_norm} ({refs_idx})')
    return trans_result, refs_result


def normalize_cantonese(path: str) -> None:
    trans = get_file(os.path.join(path, 'reg_orig.trn'))
    refs = get_file(os.path.join(path, 'std_orig.trn'))
    num_processes = multiprocessing.cpu_count()
    length = len(trans)
    chunk_size = length // num_processes
    process_args = []

    for i in range(num_processes):
        start = i * chunk_size
        end = length if i == num_processes - 1 else (i + 1) * chunk_size
        process_args.append((trans, refs, start, end))

    with multiprocessing.Pool(num_processes) as pool:
        results = pool.map(single_normalization, process_args)

    final_trans = [item for sublist, _ in results for item in sublist]
    final_refs = [item for _, sublist in results for item in sublist]

    save_file(os.path.join(path, 'reg.trn'), final_trans)
    save_file(os.path.join(path, 'std.trn'), final_refs)

    print(path + ' done')


if __name__ == '__main__':
    file_dir = '/data1/yumingdong/whisper/whisper-eval/exp/whisper-large-v3-lora700+700-90000-test_datatang500h'
    normalize_cantonese(file_dir)
