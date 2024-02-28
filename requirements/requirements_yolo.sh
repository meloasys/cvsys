arg=ultralytics

python3 -m venv ~/pyvenv/${arg}
. ~/pyvenv/${arg}/bin/activate

pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cpu

cd src 
git clone https://github.com/ultralytics/ultralytics.git
cd ultralytics
pip install -e .
bash