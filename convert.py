import os
import random
import sys

import numpy as np
import tensorflow as tf
from PIL import Image

import config

# 验证集数量
_NUM_TEST = 500
# 随机种子
_RANDOM_SEED = 0
# 数据集路径
DATASET_DIR = config.IMAGE_DIR
# tfrecord文件存放路径
TFRECORD_DIR = config.TF_RECORD_DIR


# 判断tfrecord文件是否存在
def _dataset_exists(dataset_dir):
    for split_name in ['train', 'test']:
        output_filename = os.path.join(dataset_dir, split_name + '.tfrecords')
        if not tf.gfile.Exists(output_filename):
            return False
    return True


# 获取所有验证码图片
def _get_filenames_and_classes(dataset_dir):
    photo_file_names = []
    for filename in os.listdir(dataset_dir):
        # 获取文件路径
        path = os.path.join(dataset_dir, filename)
        photo_file_names.append(path)
    return photo_file_names


def int64_feature(values):
    if not isinstance(values, (tuple, list)):
        values = [values]
    return tf.train.Feature(int64_list=tf.train.Int64List(value=values))


def bytes_feature(values):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[values]))


def image_to_tfexample(image_data, label0, label1, label2, label3):
    # Abstract base class for protocol messages.
    return tf.train.Example(features=tf.train.Features(feature={
      'image': bytes_feature(image_data),
      'label0': int64_feature(label0),
      'label1': int64_feature(label1),
      'label2': int64_feature(label2),
      'label3': int64_feature(label3),
    }))


# 把数据转为TFRecord格式
def _convert_dataset(split_name, filenames):
    assert split_name in ['train', 'test']
    with tf.Session() as sess:
        output_filename = os.path.join(TFRECORD_DIR, split_name + '.tfrecords')
        with tf.io.TFRecordWriter(output_filename) as tf_record_writer:
            for i, filename in enumerate(filenames):
                try:
                    sys.stdout.write('\r>> Converting image %d/%d' % (i + 1, len(filenames)))
                    sys.stdout.flush()
                    # 读取图片
                    image_data = Image.open(filename)
                    # 根据模型的结构resize
                    image_data = image_data.resize((224, 224))
                    # 由于验证码是彩色的，但是我们识别验证码并不需要彩色，灰度图就可以。这样可以减少计算量
                    image_data = np.array(image_data.convert('L'))
                    # 将图片转化为bytes
                    image_data = image_data.tobytes()

                    # 获取label 文件名前4位
                    labels = filename.split('/')[-1][0:4]
                    num_labels = []
                    for j in range(4):
                        num_labels.append(config.convert_to_num(labels[j]))

                    # 生成protocol数据类型
                    example = image_to_tfexample(image_data, num_labels[0], num_labels[1], num_labels[2], num_labels[3])
                    tf_record_writer.write(example.SerializeToString())
                except IOError as e:
                    print('Could not read:', filename)
                    print('Error:', e)
                    print('Skip it\n')
    sys.stdout.write('\n')
    sys.stdout.flush()


if __name__ == '__main__':
    # 判断tfrecord文件是否存在
    if _dataset_exists(TFRECORD_DIR):
        print('tfcecord文件已存在')
    else:
        # 获得所有图片
        photo_filenames = _get_filenames_and_classes(DATASET_DIR)

        # 把数据切分为训练集和测试集,并打乱
        random.seed(_RANDOM_SEED)
        random.shuffle(photo_filenames)
        training_filenames = photo_filenames[_NUM_TEST:]
        testing_filenames = photo_filenames[:_NUM_TEST]

        # 数据转换
        _convert_dataset('train', training_filenames)
        _convert_dataset('test', testing_filenames)
        print('生成tfcecord文件')
