arg=ultralytics

python3 -m venv ~/pyvenv/${arg}
. ~/pyvenv/${arg}/bin/activate

mkdir models

model=/home/cvsys/contents/models/yolov8s.pt
if [ ! -e $model ]; then
    wget -P models https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8s.pt
fi

pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cpu

mkdir src
cd src 
git clone https://github.com/ultralytics/ultralytics.git
cd ultralytics
pip install -e .
pip install pika
cd ~/contents
python app/yolo_app.py