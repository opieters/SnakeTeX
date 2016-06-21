import jinja2
import os, yaml
from jinja2 import Template
import subprocess, shutil, hashlib, time

class SnakeTeX:
    def __init__(self,config_file="config.yml", debug=True,max_move_up=3):
        self.debug = debug

        moved_up, config, self.config = 0, "config.yml", None
        while self.config is None:
            try:
                self.config = yaml.load(open(config))
            except FileNotFoundError:
                if moved_up > max_move_up:
                    raise FileNotFoundError("A configuration file must be specified in the top directory.")
            config = os.path.join("../", config)

        SnakeTeX.__check_config__(self.config)
        self.log("[check] Config file valid")

        # set directories
        self.build_directory = self.config["build_directory"] if "build_directory" in self.config else "./build"
        self.source_file = self.config["source_file"] if self.config["source_file"].endswith('.stex') else self.config["source_file"] + ".stex"
        self.build_file = self.config["build_file"] if "build_file" in self.config else self.source_file[:-5] + ".tex"
        self.assets_directory = self.config["assets_directory"] if "assets_directory" in self.config else "./assets"
        self.output_pdf = self.config["output_pdf"] if "output_pdf" in self.config else self.source_file[:-5] + ".pdf"
        self.status_file = self.config["status_file"] if "status_file" in self.config else "status.yml"

        content_dirs = [jinja2.FileSystemLoader(os.path.abspath('.')),
                        jinja2.FileSystemLoader(os.path.abspath('./templates')),
                        jinja2.FileSystemLoader(os.path.abspath('./content'))]

        if "content_dirs" in self.config:
            for directory in self.config["content_dirs"]:
                content_dirs.append(jinja2.FileSystemLoader(os.path.abspath(directory)))

        windows = os.name == "nx"
        self.env = jinja2.Environment(
            block_start_string = '{:',
            block_end_string = ':}',
            variable_start_string = '{.',
            variable_end_string = '.}',
            comment_start_string = '%[',
            comment_end_string = '%]',
            line_statement_prefix = '%:',
            line_comment_prefix = '%#',
            trim_blocks = True,
            autoescape = False,
        	newline_sequence = "\r\n" if windows else "\n",
            loader = jinja2.ChoiceLoader(content_dirs))

        if os.path.isfile(os.path.join(self.build_directory,self.status_file)):
            self.status = yaml.load(open(os.path.join(self.build_directory,self.status_file)))
        else:
            self.status = {}
        if not "time" in self.status:
            self.status["time"] = str(int(time.time()))

        # create build directory if none existent
        if not os.path.exists(self.build_directory):
            os.makedirs(self.build_directory)

    def log(self, debug_message):
        if self.debug:
            print(debug_message)

    @staticmethod
    def __check_config__(config):
        if "source_file" not in config:
            raise KeyError("The confguration file must specify a source file (`source_file` variable).")

    @staticmethod
    def __copytree__(src, dst, symlinks=False, ignore=None):
        # http://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                SnakeTeX.__copytree__(s, d, symlinks, ignore)
            else:
                if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                    shutil.copy2(s, d)

    def compile(self, update_time=True):

        self.log("[compile] " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))

        if update_time:
            self.status["time"] = str(int(time.time()))

        template = self.env.get_template(self.source_file)

        with open(os.path.join(self.build_directory,self.build_file),'w') as f:
            f.write(template.render(document=self.config["document"]))


    def build(self):
        SnakeTeX.__copytree__(os.path.join(".",self.assets_directory),self.build_directory)

        self.log("[build] " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))

        shell_env = os.environ.copy()
        shell_env["SOURCE_DATE_EPOCH"] = self.status["time"]

        process = subprocess.Popen([str(self.config["compiler"]), str(self.config["compiler_options"]),self.build_file],cwd=self.build_directory,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, env=shell_env)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            self.log(stdout)
            self.log(stderr)

        output_build_pdf = os.path.join(self.build_directory, self.build_file[:-4] + ".pdf")
        file_hash = hashlib.sha256(open(output_build_pdf,'rb').read()).hexdigest()
        if "file_hash" in self.status and self.status["file_hash"] == file_hash:
            pass
        else:
            self.log("[build] Updated hash: %s" % file_hash)
            self.status["file_hash"] = file_hash
            self.build()

        with open(os.path.join(self.build_directory,self.status_file),'w') as f:
            f.write(yaml.dump(self.status))

s = SnakeTeX()
s.compile()
s.build()
# http://jinja.pocoo.org/docs/dev/api/
