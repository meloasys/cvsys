# https://www.rabbitmq.com/tutorials/tutorial-one-python
import pika, sys, os, yaml, functools, time, shutil
from pathlib import Path
# sys.path.append('../models')

def on_msg_yolo(cfg, ch, method, properties, body):
    print(f" [x] Received {body}")
    source = cfg['img_source'] # To do
    save_dir = Path(cfg['ultralytics_save_root']) / str(int(time.time()))
    os.makedirs(save_dir, exist_ok=True)
    model = YOLO(cfg['ultralytics_chkpoint_source'])
    inf_res = model.predict(source,
                            save_dir=save_dir,
                            save=True, imgsz=640, conf=0.5)
    os.makedirs(Path(cfg['save_dir']), exist_ok=True)
    backup_from = save_dir / os.path.split(source)[-1]
    backup_to = Path(cfg['save_dir']) / os.path.split(source)[-1]
    shutil.copyfile(backup_from, backup_to)
    ################# pub mesg #################
    # publish_body = 'do your thg'
    # ch.basic_publish(exchange='', 
    #                  routing_key=cfg['ultralytics_pubs_name'], 
    #                  body=publish_body)
    # print(" [x] Published inference result message! ")
    # ch.close()

def main(cfg):
    credentials = pika.PlainCredentials(
                        username=cfg['mq_usr'],
                        password=cfg['mq_passwd']
                        )
    connection = pika.BlockingConnection(
                        pika.ConnectionParameters(
                                    host=cfg['host'],
                                    credentials=credentials, 
                                    heartbeat=500)
                                    )
    channel = connection.channel()
    channel.queue_declare(queue=cfg['ultralytics_cons_name'])
    # channel.queue_declare(queue=cfg['ultralytics_pubs_name'])
    callback_fn = functools.partial(on_msg_yolo, cfg)
    channel.basic_consume(queue=cfg['ultralytics_cons_name'], on_message_callback=callback_fn, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        dir = 'config.yaml'
        with open(dir) as f:
            config = yaml.load(f,Loader=yaml.FullLoader)
        dir = 'src/ultralytics/ultralytics/cfg/default.yaml'
        dir2 = 'src/ultralytics/ultralytics/cfg/default-original.yaml'
        if not os.path.exists(dir2):
            shutil.copyfile(dir, dir2)
        with open(dir) as f:
            model_cfg = yaml.load(f,Loader=yaml.FullLoader)
        if list(model_cfg.keys())[-1] != 'save_dir':
            with open(dir, 'w') as f:
                model_cfg['save_dir'] = None
                yaml.dump(model_cfg, f)
        from ultralytics import YOLO
        main(config)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)