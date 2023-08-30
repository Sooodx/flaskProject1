import datetime
import os.path
import random

import cv2
import torch
from flask import Flask, render_template, request
from PIL import Image

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def flask_demo():
    # 如果post请求，也就是前端form提交表单，执行下面代码后返回index.html,get请求就直接返回index.html
    if request.method == "POST":
        # 1、生成一个随机的文件名：唯一
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        randomNum = random.randint(0, 100)
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)

        # 2、获取图像

        f = request.files['file']  # 获取前端提交的文件
        basepath = "/static/images/"
        path = os.path.dirname(__file__)  # /home/nscrl/lhy/cv/yolov5_7.0
        suffix = f.filename.split(".")[1]  # 获取.jpg

        # 3、保存原图像
        o_img_path = basepath + uniqueNum + "_o" + "." + suffix
        f.save(path + o_img_path)  # f.save只能保存绝对路径
        # 处理
        model = torch.hub.load('./yolov5-master', 'custom', './yolov5-master\yolov5s.pt', source='local')
        img_detect_path = '.' + o_img_path  # './static/images/xxx.jpg'
        if suffix == 'jpg':
            img_detect = model(img_detect_path)
            img_detect.render()
            p_img_path = basepath + uniqueNum + "_p" + "." + suffix
            Image.fromarray(img_detect.ims[0]).save(path + p_img_path)

            # 检测物品种类
            pred_classes = img_detect.pred[0][:, -1].cpu().numpy().astype(int)
            class_names = model.module.names if hasattr(model, 'module') else model.names
            new_pred_classes = list(set(pred_classes))  # 去除重复种类


        else:
            p_img_path2 = path + basepath + uniqueNum + "_p" + "." + suffix  # 输出视频路径
            p_img_path = basepath + uniqueNum + "_p" + "." + suffix  # 输出视频路径

            # 打开输入视频文件
            cam = cv2.VideoCapture(path + o_img_path)

            # 检查是否成功打开视频文件
            if not cam.isOpened():
                print("Error: Could not open video file")
                exit()

            # 视频帧的宽度和高度
            frame_width = int(cam.get(3))
            frame_height = int(cam.get(4))

            # 创建输出视频文件
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(p_img_path2, fourcc, 30, (frame_width, frame_height))

            # 当前帧
            current_frame = 0

            while True:
                ret, frame = cam.read()

                if ret:
                    # 处理帧，执行目标检测等操作
                    results = model(frame)
                    results.render()

                    # 将帧写入输出视频
                    out_frame = results.ims[0]
                    out.write(out_frame)

                    print(f"Processed frame {current_frame}")
                    current_frame += 1
                else:
                    break

            # 释放资源
            cam.release()
            out.release()
            cv2.destroyAllWindows()

        print(o_img_path)
        print(p_img_path)
        return render_template('index.html', o_img_path='.' + o_img_path, p_img_path='.' + p_img_path, suffix=suffix,
                               pred_classes=new_pred_classes, class_names=class_names)

    return render_template('index.html')


@app.route('/interface', methods=["POST", "GET"])
def interface():
    # 如果post请求，也就是前端form提交表单，执行下面代码后返回index.html,get请求就直接返回index.html
    if request.method == "POST":
        # 1、生成一个随机的文件名：唯一
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        randomNum = random.randint(0, 100)
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)

        # 2、获取图像

        f = request.files['file']  # 获取前端提交的文件
        basepath = "/static/images/"
        path = os.path.dirname(__file__)  # /home/nscrl/lhy/cv/yolov5_7.0
        suffix = f.filename.split(".")[1]  # 获取.jpg

        # 3、保存原图像
        o_img_path = basepath + uniqueNum + "_o" + "." + suffix
        f.save(path + o_img_path)  # f.save只能保存绝对路径
        # 处理
        model = torch.hub.load('./yolov5-master', 'custom', '.\yolov5-master\yolov5s.pt', source='local')
        img_detect_path = '.' + o_img_path  # './static/images/xxx.jpg'
        if suffix == 'jpg':
            img_detect = model(img_detect_path)
            img_detect.render()
            p_img_path = basepath + uniqueNum + "_p" + "." + suffix
            Image.fromarray(img_detect.ims[0]).save(path + p_img_path)

            # 检测物品种类
            pred_classes = img_detect.pred[0][:, -1].cpu().numpy().astype(int)
            class_names = model.module.names if hasattr(model, 'module') else model.names
            new_pred_classes = list(set(pred_classes))  # 去除重复种类


        else:
            p_img_path2 = path + basepath + uniqueNum + "_p" + "." + suffix  # 输出视频路径
            p_img_path = basepath + uniqueNum + "_p" + "." + suffix  # 输出视频路径

            # 打开输入视频文件
            cam = cv2.VideoCapture(path + o_img_path)

            # 检查是否成功打开视频文件
            if not cam.isOpened():
                print("Error: Could not open video file")
                exit()

            # 视频帧的宽度和高度
            frame_width = int(cam.get(3))
            frame_height = int(cam.get(4))

            # 创建输出视频文件
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(p_img_path2, fourcc, 30, (frame_width, frame_height))

            # 当前帧
            current_frame = 0

            while True:
                ret, frame = cam.read()

                if ret:
                    # 处理帧，执行目标检测等操作
                    results = model(frame)
                    results.render()

                    # 将帧写入输出视频
                    out_frame = results.ims[0]
                    out.write(out_frame)

                    print(f"Processed frame {current_frame}")
                    current_frame += 1
                else:
                    break

            # 释放资源
            cam.release()
            out.release()
            cv2.destroyAllWindows()

        print(o_img_path)
        print(p_img_path)
        return render_template('interface_demo.html', o_img_path='.' + o_img_path, p_img_path='.' + p_img_path,
                               suffix=suffix,
                               pred_classes=new_pred_classes, class_names=class_names)

    return render_template('interface_demo.html')


if __name__ == '__main__':
    app.run(debug=True)
