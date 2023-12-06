python -m eval.eval \
       --model_dir /data1/yumingdong/model/ \
       --model_type finetuned \
       --model_index 4 \
       --dataset_dir /data2/yumingdong/data \
       --data_index 8 \
       --export_dir /data1/yumingdong/whisper/whisper-eval/exp \
       --batch_size 32 \
       --language zh \
       --int8 False \
       --num_workers 16 \
       --gpu 7 \
       --pipeline 1
