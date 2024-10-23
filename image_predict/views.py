import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import json
import logging
import datetime

# 配置模型服务器的URL
MODEL_SERVER_URL = 'http://58.199.157.203:12345'

logger = logging.getLogger(__name__)


@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        openid = request.POST.get('openid')  # 获取openid
        image = request.FILES.get('image')  # 获取上传的图片
        print('OpenID:', openid)
        print('Image:', image)

        if not openid or not image:
            return JsonResponse({
                'status': 'error',
                'message': 'openid and image are required.'
            }, status=400)

        # 保存图片到本地（可选）
        image_name = default_storage.save(image.name, image)
        image_path = os.path.join(default_storage.location, image_name)

        try:
            # 上传图片和 openid 到模型服务器的 /upload 端点
            with open(image_path, 'rb') as img_file:
                files = {
                    'image': img_file,
                    'openid': (None, openid)  # 将 openid 作为表单数据发送
                }
                upload_response = requests.post(f'{MODEL_SERVER_URL}/upload', files=files)

            # 检查上传是否成功
            if upload_response.status_code == 200:
                # 构造报告请求的 JSON 数据
                time_now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # 获取当前时间
                report_data = {
                    "openid": openid,
                    # "time": time_now
                }
                headers = {
                    'Content-Type': 'application/json'
                }
                # 调用报告接口
                report_response = requests.post(f'{MODEL_SERVER_URL}/report', json=report_data, headers=headers)
                logger.info(
                    f'Report response: {report_response.status_code}, {report_response.text}')  # Log report response

                # 打印报告内容
                report_text = report_response.text
                print(report_text)  # 输出文本内容

                if report_response.status_code == 200:
                    return JsonResponse({
                        'status': 'success',
                        'report': report_text
                    })
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Failed to generate report from the model server.'
                    }, status=500)

        except requests.exceptions.RequestException as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'No image provided.'
        }, status=400)
