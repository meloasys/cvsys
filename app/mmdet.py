# https://www.rabbitmq.com/tutorials/tutorial-one-python
import pika, sys, os, yaml, functools, time
from pathlib import Path
sys.path.append('../models')

def on_msg_mmdet(cfg, ch, method, properties, body):
    print(f" [x] Received {body}")
    # To do ##############################################
    source = cfg['sample_img'] # To do



    ######################################################
    save_dir = Path(cfg['mmdet_save_root']) / str(time.time())
    
    # call model
    # model = YOLO(cfg['mmdet_model_source'])
    # inf_res = model.predict(source,
    #                         save_dir=save_dir,
    #                         save=True, imgsz=640, conf=0.5)
    
    # To do ##############################################
    publish_body = 'do your thg'




    ######################################################
    ch.basic_publish(exchange='', routing_key=cfg['mmdet_pubs_name'], body=publish_body)
    print(" [x] Published inference result message! ")
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
    channel.queue_declare(queue=cfg['mmdet_cons_name'])
    channel.queue_declare(queue=cfg['mmdet_pubs_name'])
    callback_fn = functools.partial(on_msg_mmdet, cfg)
    channel.basic_consume(queue=cfg['mmdet_cons_name'], on_message_callback=callback_fn, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        dir = 'config.yaml'
        with open(dir) as f:
            config = yaml.load(f,Loader=yaml.FullLoader)
        main(config)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)