import gzip, os, sys
import urllib.parse

class gzip_utility(object):

    def __init__(self, dir, ext):
        self.dir = dir
        self.ext = ext

    def parse_dir(self):

        file_list = os.listdir(self.dir)
        for file in file_list:
            if file[-4:] in self.ext:
                file = os.path.join(self.dir,file)
                self.parse_file(file)

    def parse_file(self, file):
        """
        http://xahlee.info/python/gzip.html
        :param file:
        :return:
        """
        input = open(file, 'rb')
        s = input.read()
        s = urllib.parse.quote(s)
        s = bytes(s, "utf-8")
        input.close()

        out = "%s_compressed.gz" % file
        output = gzip.GzipFile(out, 'wb')
        output.write(s)
        output.close()
        in_file = os.stat(file).st_size
        out_file = os.stat("%s_compressed.gz" % file).st_size
        comp_ratio = out_file / in_file * 100
        print("%s,%s,%s,%s" % (os.path.split(file)[1], in_file, out_file, comp_ratio))

if __name__ == "__main__":
    cp = gzip_utility("C:\\dev_stuff\\gp2gp\\my_large_files", [".jpg",".png"])
    cp.parse_dir()
