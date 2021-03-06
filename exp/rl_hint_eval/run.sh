#!/bin/sh

export CUDA_VISIBLE_DEVICES=""

python -u ../../rl.py \
  --test \
  --n_epochs=20 \
  --predict_hyp=true \
  --infer_hyp=true \
  --restore="../rl_hint" \
  > eval.out \
  2> eval.err

