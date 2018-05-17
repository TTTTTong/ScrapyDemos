from scrapy import cmdline
import subprocess

name = 'DBMovie'

subprocess.call('rm *.json *.csv *.xml', shell=True)

cmd = '~/.pyenv/versions/3.6.3/envs/ScrapyEnv/bin/scrapy crawl {0} -o douban.xml'.format(name)
cmdline.execute(cmd.split())
