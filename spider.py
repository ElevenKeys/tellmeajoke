# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import re

# Spider class for http://www.qiushibaike.com/
class Qiushibaike:
 
    def __init__(self):
        self.index_url = r'http://www.qiushibaike.com/hot/page/'
        self.regexp = r'''.+?class="article.+?<h2>(.*?)</h2>.+?<div class="content">\s*?<span>(.*?)</span>\s*?</div>.+?<!-- 图片或gif -->(.+?)<span class="stats-vote">.*?(\d+?)</i>'''
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : self.user_agent }
        self.stories = []

    def load(self,pageIndex):
        try:
            url = self.index_url + str(pageIndex)
            request = urllib.request.Request(url,headers = self.headers)
            response = urllib.request.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
 
        except urllib.error.URLError as e:
            if hasattr(e,"reason"):
                print("连接糗事百科失败,错误原因",e.reason)
                return None
  
    def parse(self,pageIndex):
        pageCode = self.load(pageIndex)
        if not pageCode:
            print("页面加载失败....")
            return None
        pattern = re.compile(self.regexp ,re.S)
        items = re.findall(pattern,pageCode)
        pageStories = []

        for item in items:
            #If it contains image
            haveImg = re.search("img",item[2])
            if not haveImg:
                item = {'author':item[0].strip(),'text':item[1].strip(), 'like':item[3].strip()}
                pageStories.append(item)
        return pageStories
 
    def refresh(self):
            if len(self.stories) == 0:
                pageStories = self.parse(self.pageIndex)
                if pageStories != None:
                    self.stories= pageStories
                    self.pageIndex += 1
                else:
                	raise exception('No more stories')
    
    def fetchStory(self):
        command = input()
        if command.upper() == "Q":
            return False

        try:
	        self.refresh()
        except Exception as e:
        	print(e)
        	return False
        story = self.stories.pop(0)
        print("第%d页\t发布人:%s\t赞:%s\r\n%s" %(self.pageIndex-1,story.get('author'),story.get('like'),story.get('text')))
        return True

    def __call__(self):
        print("正在读取糗事百科,按回车查看新段子，Q退出")
        while self.fetchStory():
        	pass

if __name__ == '__main__':
    Qiushibaike()()