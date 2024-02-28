cont_1=yolo
cont_2=mmdet
install_sh1=requirements_${cont_1}.sh
install_sh2=requirements_${cont_2}.sh

chmod +x requirements/${install_sh1}
chmod +x requirements/${install_sh2}

docker build -t cvsys:0.0.0 .

docker run -it -d --net=host --ipc=host \
            --name cvsys_${cont_1} \
            -v $(pwd):/home/cvsys/contents \
            cvsys:0.0.0 \
            bash -c /home/cvsys/contents/requirements/${install_sh1}

docker run -it -d --net=host --ipc=host \
            --name cvsys_${cont_2} \
            -v $(pwd):/home/cvsys/contents \
            cvsys:0.0.0 \
            bash -c /home/cvsys/contents/requirements/${install_sh2}