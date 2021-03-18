# CSV parser
import string, sys, os


class csv_parser(object):
    def __init__(self, dir, sep, attachmentsize, outputfile):
        """
        Attempt to open source csv file and initialise class vars
        dir = base directory where files are located
        sep = separator for fields in the csv
        attachmentsize = size of file (in MB) that need to be filtered out (those larger than the size specified)
        """
        self.sep = sep

        self.field_dict = {"id": 0,
                     "time": 1,
                     "attachment_id": 2,
                     "conversation_id": 3,
                     "from_system": 4,
                     "to_system": 5,
                     "attachment_type": 6,
                     "compressed": 7,
                     "content_type": 8,
                     "large_attachment": 9,
                     "length": 10,
                     "original_base64,internal_id": 11
            }

        self.dir = dir
        self.attachmentsize = float(attachmentsize * 1024 * 1024)
        self.output_file = open("%s_%s.csv" % (outputfile, attachmentsize), "w")
        self.largeAttachment_count = 0


    def parse_dir(self):
        print("process started...")
        self.output_file.write("id,length,content_type,compressed\n")
        file_list = os.listdir(self.dir)
        for file in file_list:
            if file[-4:] == ".csv":
                try:
                    print("processing %s" % file)
                    self.csv_file = open(os.path.join(self.dir, file), "r")
                except:
                    print("could not open file %s" % file)
                    sys.exit()
                self.parse_file(file)
                print("processing of %s complete" % file)
        self.output_file.close()
        print("process completed...")

        print("Count of attachments over %sMB = %s" % (float(self.attachmentsize / 1024 / 1024), self.largeAttachment_count))

    def parse_file(self, file):
        """
        Reads through each line in the current file
        IN - no args
        OUT - no return value
        """
        # var to skip over first 3 lines
        csv_data = self.csv_file.readlines()
        for line in csv_data:
            self.parse_line(line)


    def parse_line(self, line):
        """
        split into an array
        """
        line = str.split(line, self.sep)
        attSize = 0.0
        compressed = str.upper(line[self.field_dict.get("compressed")])
        try:
            if compressed == "FALSE":
                if line[self.field_dict.get("content_type")] == "application/pdf":
                    attSize = float(line[self.field_dict.get("length")]) * 0.88
                elif line[self.field_dict.get("content_type")] == "image/tiff":
                    attSize = float(line[self.field_dict.get("length")]) * 0.78
                elif line[self.field_dict.get("content_type")] == "image/png":
                    attSize = float(line[self.field_dict.get("length")]) * 0.99
                elif line[self.field_dict.get("content_type")] == "image/jpg":
                    attSize = float(line[self.field_dict.get("length")]) * 0.82
                else:
                    attSize = float(line[self.field_dict.get("length")])
            else:
                attSize = float(line[self.field_dict.get("length")])


            if attSize > self.attachmentsize:
                #and line[self.field_dict.get("to_system")] == 'EMIS Web': # not run yet with this condition 15/3/21
                outputline = str.join(",", ((line[self.field_dict.get("id")],
                                             str(attSize),
                                             line[self.field_dict.get("content_type")],
                                             line[self.field_dict.get("compressed")])))
                self.output_file.write("%s\n" % outputline)
                self.largeAttachment_count +=1
        except TypeError:
            pass #to deal with header line!
        except ValueError:
            pass  #to deal with header line!


if __name__ == "__main__":
    cp = csv_parser("C:\\dev_stuff\\gp2gp\\attachmentsdata\\", ',',5, "gp2gp_attachment_report_with_base64_encoding")
    cp.parse_dir()
