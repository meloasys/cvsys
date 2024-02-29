# https://www.rabbitmq.com/tutorials/tutorial-one-python
import pika, sys, os, yaml, functools, time, shutil
from pathlib import Path
from mmdet.apis import DetInferencer

def on_msg_mmdet(cfg, ch, method, properties, body):
    print(f" [x] Received {body}")
    source = cfg['img_source'] # To do
    save_dir = Path(cfg['mmdet_save_root']) / str(int(time.time()))
    model_cfg = cfg['mmdet_config']
    model = DetInferencer(
                    model=cfg['mmdet_config'],
                    weights=cfg['mmdet_chkpoint_source'],
                    device='cpu'
                    )
    inf_res = model(source,
                    out_dir=save_dir,
                    no_save_pred=False,
                    return_datasamples=True,
                    )
    os.makedirs(Path(cfg['save_dir']), exist_ok=True)
    backup_from = save_dir / 'vis' /os.path.split(source)[-1]
    backup_to = Path(cfg['save_dir']) / os.path.split(source)[-1]
    try:
        shutil.copyfile(backup_from, backup_to)
    except Exception as e:
        print(e)
    ################# pub mesg #################
    # publish_body = 'do your thg'
    # ch.basic_publish(exchange='', routing_key=cfg['mmdet_pubs_name'], body=publish_body)
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
    channel.queue_declare(queue=cfg['mmdet_cons_name'])
    # channel.queue_declare(queue=cfg['mmdet_pubs_name'])
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