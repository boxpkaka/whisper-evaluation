import os
import sys
from typing import List
from utils.get_save_file import get_file, save_file

'''
修改wav.scp中的音频目录
'''


def main():
    root_dir = sys.argv[1]  # root dir/wav.scp|text|text.fmt
    export_dir = sys.argv[2]  # -> export_dir/wav.scp
    data_tgt_dir = sys.argv[3]  # data_tgt_dir/1.wav, ..., x.wav

    generate(root_dir, export_dir, data_tgt_dir)


def generate(root_dir: str, export_dir: str, data_tgt_dir: str) -> None:
    os.makedirs(export_dir, exist_ok=True)

    origin_wav = get_file(os.path.join(root_dir, 'wav.scp'))

    for i in range(len(origin_wav)):
        origin_wav_split = origin_wav[i].split(' ')
        idx = origin_wav_split[0]
        origin_wav_name = origin_wav_split[1].split('/')[-1]
        new_wav_dir = os.path.join(data_tgt_dir, origin_wav_name)
        new_item = ' '.join([idx, new_wav_dir])
        origin_wav[i] = new_item

    save_file(os.path.join(export_dir, 'wav.scp'), origin_wav)


if __name__ == '__main__':
    main()

