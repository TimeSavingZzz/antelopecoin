import os
import shutil
import random

def random_sample_images(src, dest, sample_count):
    if not os.path.exists(dest):
        os.makedirs(dest)

    # 获取所有文件夹
    first_level_folders = os.listdir(src)

    count = 0
    while count < sample_count:
        # 随机选择一个文件夹
        first_level_folder = random.choice(first_level_folders)
        second_level_path = os.path.join(src, first_level_folder)
        second_level_folders = os.listdir(second_level_path)

        # 随机选择一个第二层文件夹
        second_level_folder = random.choice(second_level_folders)
        image_folder_path = os.path.join(second_level_path, second_level_folder)
        image_files = os.listdir(image_folder_path)

        # 随机选择一张图片
        selected_image = random.choice(image_files)
        src_image_path = os.path.join(image_folder_path, selected_image)
        dest_image_path = os.path.join(dest, f"{count}_{selected_image}")

        # 复制所选图片到目标文件夹
        shutil.copy2(src_image_path, dest_image_path)
        count += 1

# 使用示例
src = "第一层"
dest = "随机抽样图片"
sample_count = 9000
random_sample_images(src, dest, sample_count)