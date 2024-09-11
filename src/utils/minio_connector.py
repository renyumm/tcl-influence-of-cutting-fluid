'''
LastEditors: renyumm strrenyumm@gmail.com
Date: 2024-09-11 13:30:33
LastEditTime: 2024-09-11 17:47:03
FilePath: /tcl-influence-of-cutting-fluid/src/utils/minio_connector.py
'''
from minio import Minio
from minio.commonconfig import CopySource

# 创建Minio客户端
client = Minio(
    '10.202.114.56:31743',  # MinIO服务器的URL
    access_key='AKIAIOSFODNN7EXAMPLA',  # 访问密钥
    secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEA',  # 秘密密钥
    secure=False
)


def copy_and_rename_folder(source_bucket, destination_bucket, source_folder, destination_folder, client=client):
    """
    复制 MinIO 中的整个“文件夹”（通过对象前缀模拟）到另一个文件夹。

    :param client: MinIO 客户端实例
    :param source_bucket: 源桶名称
    :param source_folder: 源文件夹路径（例如 "folder/subfolder/"，必须以斜杠结尾）
    :param destination_bucket: 目标桶名称
    :param destination_folder: 目标文件夹路径（例如 "newfolder/subfolder/"，必须以斜杠结尾）
    :return: None
    """
    objects = client.list_objects(source_bucket, prefix=source_folder, recursive=True)

    for obj in objects:
        # 构建源对象路径
        source_object = obj.object_name.split('/')[-1]

        # 构建目标对象路径（将源文件夹替换为目标文件夹）
        destination_object = destination_folder+source_object

        # 创建 CopySource 对象
        copy_source = CopySource(source_bucket, obj.object_name[1:])

        # 复制对象到目标位置
        client.copy_object(
            bucket_name=destination_bucket,
            object_name=destination_object[1:],
            source=copy_source
        )



if __name__ == '__main__':
    import io  
    import dill

    bucket_name = 'rym-gold-machine'
    file_name = '/latest/test.dill'

    # # 下载文件 
    # download_path = './test.dill'
    # client.fget_object(bucket_name, file_name, download_path)
    # print(f"'{file_name}' is successfully downloaded to '{download_path}'")
    
    # 从流中加载
    # 从MinIO中获取对象
    response = client.get_object(bucket_name, file_name)

    # 将对象内容读取到BytesIO流中
    file_stream = io.BytesIO(response.read())
    
    # 使用dill包加载流数据
    loaded_object = dill.load(file_stream)

    print(loaded_object)