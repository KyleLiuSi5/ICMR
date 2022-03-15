import os

from objectmapper import ObjectMapper
from reader import Reader


class Transformer(object):
    def __init__(self, xml_dir, out_dir, class_file):
        self.xml_dir = xml_dir
        self.out_dir = out_dir
        self.class_file = class_file

    def transform(self):
        reader = Reader(xml_dir=self.xml_dir)
        xml_files = reader.get_xml_files()
        classes = reader.get_classes(self.class_file)
        object_mapper = ObjectMapper()
        annotations = object_mapper.bind_files(xml_files, xml_dir=self.xml_dir)
        self.write_to_txt(annotations, classes)

    def write_to_txt(self, annotations, classes):
        for annotation in annotations:
            output_path = os.path.join(self.out_dir, self.darknet_filename_format(annotation.filename))
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))
            with open(output_path, "w+") as f:
                f.write(self.to_darknet_format(annotation, classes))

    def to_darknet_format(self, annotation, classes):
        result = []
        for obj in annotation.objects:
            if obj.name not in classes:
                print("Please, add '%s' to classes.txt file." % obj.name)
                exit()
            x, y, width, height = self.get_object_params(obj)
            result.append("%d %.6f %.6f %.6f %.6f" % (classes[obj.name], x, y, width, height))
        return "\n".join(result)

    @staticmethod
    def get_object_params(obj):
        #image_width = 1.0 * size.width
        #image_height = 1.0 * size.height

        box = obj.box
        absolute_x = box.xmin + 0.5 * (box.xmax - box.xmin)
        absolute_y = box.ymin + 0.5 * (box.ymax - box.ymin)

        absolute_width = box.xmax - box.xmin
        absolute_height = box.ymax - box.ymin

        x = absolute_x / 1920
        y = absolute_y / 1080
        width = absolute_width / 1920
        height = absolute_height / 1080

        return x, y, width, height

    @staticmethod
    def darknet_filename_format(filename):
        pre, ext = os.path.splitext(filename)
        return "%s.txt" % pre
