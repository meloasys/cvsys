arg=mmdet

python3 -m venv ~/pyvenv/${arg}
. ~/pyvenv/${arg}/bin/activate

mkdir models

model=models/dino-4scale_r50_improved_8xb2-12e_coco_20230818_162607-6f47a913.pth
if [ ! -e $model ]; then
    wget -P models https://download.openmmlab.com/mmdetection/v3.0/dino/dino-4scale_r50_improved_8xb2-12e_coco/dino-4scale_r50_improved_8xb2-12e_coco_20230818_162607-6f47a913.pth
fi

pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cpu

mkdir src
cd src
pip install -U openmim
mim install mmengine
mim install "mmcv>=2.0.0"
git clone https://github.com/open-mmlab/mmdetection.git
cd mmdetection
pip install -v -e .
pip install pika
cd ~/contents
python app/mmdet_app.py
# bash