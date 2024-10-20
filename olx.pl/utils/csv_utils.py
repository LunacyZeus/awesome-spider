import csv

from loguru import logger


def write_csv_file(keyword, data_list):  # 写入到csv文件
    # Ad Library Id	Ad start date	Page Name	Page Link	Page Likes	Page Followers	Address	Contact Number	Contact Email

    # CSV 文件的列标题
    header = ['Keyword', 'Product', 'Price', 'URL']

    # 写入 CSV 文件
    file_name = f'data/output/{keyword}.csv'
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # 写入标题
        writer.writerow(header)

        # 写入数据
        writer.writerows(data_list)

    logger.info(f"{len(data_list)} datas saved to {file_name}")
