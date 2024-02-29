arg=mmdet

python3 -m venv ~/pyvenv/${arg}
. ~/pyvenv/${arg}/bin/activate

mkdir models
wget -P models https://github.com/RistoranteRist/mmlab-weights/releases/download/dino-swinl/dino-5scale_swin-l_8xb2-36e_coco-5486e051.pth

pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cpu

cd src
pip install -U openmim
mim install mmengine
mim install "mmcv>=2.0.0"
git clone https://github.com/open-mmlab/mmdetection.git
cd mmdetection
pip install -v -e .
bash