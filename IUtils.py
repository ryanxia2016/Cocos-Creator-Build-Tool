
'''
    Uitls.py
    

    author: ChenJC
    email: isysprey@foxmail.com
    twitter: https://twitter.com/JackChe78220965
'''

from genericpath import exists
from IPlatform import Debug
import json  # json相关
import os  # 文件流相关
import zipfile  # zip文件
import shutil  # 删除整个文件夹
from jsmin import jsmin  # js压缩
import base64


def get_file_from_folder(dir,exList):
    '''
        递归获取一个文件夹下 指定格式的文件
        @param dir: 指定文件夹
        @param exList: 格式列表
    '''
    urls = []
    for root,dirs,files in os.walk(dir):
        for f in files:
            for _ in exList:
                if f.endswith(_):
                    urls.append(f)
    return urls


def get_image_from_folder(file_name):
    '''
        获取一个文件下的所有图片路径
    '''
    imagelist = []
    for parent, dirnames, filenames in os.walk(file_name):
        for filename in filenames:
            if filename.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                imagelist.append(os.path.join(parent, filename))
        return imagelist



def str2obj(s, s1=';', s2='='):

   li = s.split(s1)

   res = {}

   for kv in li:

       li2 = kv.split(s2)

       if len(li2) > 1:

           res[li2[0]] = li2[1]

   return res


def str2Dict(str1, __map=None, assign='='):
    '''
        将文本标签转换成字典
        <script src="src/import-map.json" type="systemjs-importmap" charset="utf-8"> </script>
        
        map{
            src="src/import-map.json",
            type="systemjs-importmap"
            charset="utf-8"
        }
    '''
    try:
        index = str1.find(assign)
        s = 0
        e = 0
        if __map != None:
            __map.clear()
        _map = __map if __map != None else {}
        while(index != -1):
            s = str1.find(' ', s) + 1
            e = str1.find('"', index)+1
            e2 = str1.find('"', e)

            _s = str1[s:index]
            _e = str1[e:e2]
            s = e
            _map[_s] = _e
            index = str1.find(assign, s)  # next
        return _map
    except:
        Debug.LogExcept()


def fromFile(url,mode = 'r',encode='utf-8'):
    '''
        从文件中读文本
    '''
    try:
        with open( url,mode,encoding=encode) as fp:
            return fp.read()
    except:
        fp = None
    finally:
        if fp != None:
            fp.close()

def fromFile2Base64(url):
    try:
        with open(url, 'rb') as f1:
            return str(base64.b64encode(f1.read()), encoding='utf-8')
    finally:
        f1.close()

def writeInFile(toFile, content):
    '''
        将文本写入文件
    '''
    try:
        with open(toFile, 'w', encoding='utf-8') as fp:
            fp.write(content)
    finally:
        fp.close()

def fromJsonAsDict(url):
    '''
        从本地加载json转换成字典对象
    '''
    return json.loads((fromFile(url)))

def writeDictInFile(url, dict1):
    '''
        将字典对象写入本地
    '''
    writeInFile(url, json.dumps(dict1, ensure_ascii=False, indent=2))


def revealInFileExplorer(targetDir):
    '''
        弹出本地指定文件夹
    '''
    try:
        os.startfile(targetDir)
    except:
        os.system("explorer.exe %s" % targetDir)


# def zipFile(outPath, srcFilePath, name):
#     '''
#         @outPath: zip路径及zip名称 案例: ./test.zip
#         @srcFilePath: 需要亚索的文件 案例: D:/test.txt
#         @name: 压缩后的文件名 案例:test.txt  如果不填压缩后 会是一层一层的绝对路径套娃
#     '''
#     zip = zipfile.ZipFile(outPath, "w", zipfile.ZIP_DEFLATED)
#     zip.write(srcFilePath, name)
#     zip.close()


def ZIP(url):
    '''
        压缩文件
    '''
    try:

        if os.path.isfile(url):

            name = os.path.splitext(url)[0] + '.zip'
            file_name = os.path.split(url)[1]
            
            
            with zipfile.ZipFile(name,'w',zipfile.ZIP_DEFLATED) as p:
                p.write(url,file_name)
        else:
            if url.endswith('/'):
                url = os.path.dirname(url)
            name = url + '.zip'
            with zipfile.ZipFile(name,'w',zipfile.ZIP_DEFLATED) as p:
                for root,dirs,files in os.walk(url):
                    fpath = root.replace(url,'')
                    fpath = fpath and fpath + os.sep or ''
                    for file in files:
                        p.write( os.path.join(root, file),fpath+file )          
    except:
        Debug.LogExcept()

    finally:
        if 'p' in locals().keys() and None != p:
            p.close()
    # with zipfile.ZipFile(zipfile_name, 'w') as zfile:
    #     for foldername, subfolders, files in os.walk(file):
    #         fpath = foldername.replace(file, '')
    #         if file == foldername:
    #             for i in files:
    #                 zfile.write(os.path.join(foldername, i),
    #                             os.path.join(fpath, i))
    #                 continue
    #                 zfile.write(foldername, fpath)
    #                 for i in files:
    #                     zfile.write(os.path.join(foldername, i),
    #                                 os.path.join(fpath, i))
    #     zfile.close()


def removeFile(url):
    '''
        删除一个文件 如果它时文件夹 则删除整个文件夹
    '''
    if os.path.isdir(url):
        shutil.rmtree(url)
    else:
        os.remove(url)


def del_children_folder(url):
    '''
        删除一个路径下的所有文件包括文件夹
    '''
    ls = os.listdir(url)
    for i in ls:
        dir = os.path.join(url,i)
        removeFile(dir)
    

def del_children_file(url):
    '''
        删除一个路径下的所有文件 并保留文件夹 近删除文件
    '''
    ls = os.listdir(url)
    for i in ls:
        dir = os.path.join(url, i)
        if os.path.isdir(dir):
            del_children_file(dir)
        else:
            os.remove(dir)


def JavaScript(content, min=True):
    '''
        将一段js代码封装成 <script> ... </script>
    '''
    return '<script charset="utf-8">\n'+jsmin(content)+'\n</script>\n' if min else '<script charset="utf-8">\n'+content+'\n</script>\n'


def StyleScript(content, min=True):
    '''
        将一段css 代码封装成 <style> ... </style>
    '''
    return '\t<style type="text/css">\n'+jsmin(content) + '\n</style>\n' if min else '<style>\n'+content + '\n</style>\n'
