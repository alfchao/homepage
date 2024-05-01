import os
import re
import shutil

api_replace_str = r'/api/(widgets|ping|docker|services|hash|bookmarks|(re)?validate|releases|config)'

href_str = r'href="/'

src_str = r'src="/'

cur_path = os.path.dirname(os.path.abspath(__file__))

# 遍历当前目录下的所有文件和文件夹
for root, dirs, files in os.walk(cur_path):
    for file in files:
        file_path = os.path.join(root, file)
        if file_path.endswith('js') or file_path.endswith('jsx'):
            # 打开文件并读取内容
            # print(file_path)
            with open(file_path, 'r') as f:
                content = f.read()

            # 使用正则表达式匹配replace_str，并将匹配到的字符串替换掉开头的"/"
            api_ret = re.search(api_replace_str, content)
            href_ret = re.search(href_str, content)
            src_ret = re.search(src_str, content)
            flag = False
            if api_ret:
                flag = True
                print(api_ret.group(), api_ret.group().lstrip('/'))
                print('api_ret 匹配到%s' % file_path)
                content = re.sub(api_replace_str, lambda match: match.group().lstrip('/'), content)
            if href_ret:
                flag = True
                print(href_ret.group(), href_ret.group().rstrip('/'))
                print('href_ret 匹配到%s' % file_path)
                content = re.sub(href_str, lambda match: match.group().rstrip('/'), content)
            if src_ret:
                flag = True
                print(src_ret.group(), src_ret.group().rstrip('/'))
                print('src_ret 匹配到%s' % file_path)
                content = re.sub(src_str, lambda match: match.group().rstrip('/'), content)
            
            if flag:
                # 将替换后的内容写回文件
                with open(file_path, 'w') as f:
                    f.write(content)

# 打开 next.config.js, 在第5行增加 assetPrefix: '.', 
print('修改next.config.js')
filename = os.path.join(cur_path, 'next.config.js')
add_line = "  assetPrefix: '.',\n"
with open(filename, 'r') as file:
    lines = file.readlines()

lines.insert(4, add_line)

with open(filename, 'w') as file:
    file.writelines(lines)

print('拷贝dockerhub.yml文件')
shutil.rmtree(os.path.join(cur_path, '.github/workflows/*'), ignore_errors=True)
os.mkdir(os.path.join(cur_path, '.github/workflows/'))
shutil.copy(os.path.join(cur_path, 'dockerhub.yml'), os.path.join(cur_path, '.github/workflows/'))
