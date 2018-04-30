# _*_ coding:utf-8 _*_
from .models import Article
from users.models import UserProfile
import xadmin
import xlrd
import json

class ArticleAdmin(object):
    #author,title,desc,detail,click_num,fav_nums,image,score,add_time
    list_display = ['title', 'desc', 'detail', 'score', 'fav_nums', 'image', 'click_num', 'add_time']
    search_fields = ['title', 'desc', 'detail', 'score', 'fav_nums', 'image', 'click_num']
    list_filter = ['title', 'desc', 'detail', 'score', 'fav_nums', 'image', 'click_num', 'add_time']
    import_excel = True

    def post(self,request,*args,**kwargs):
        if 'excel' in request.FILES:
            # df = pd.read_csv("C:\\Users\\Administrator\\Desktop\\fitdata.csv",encoding = 'gb18030')
            # for i in range(df.shape[0]):
            #     article = Article()
            #     author = 1
            #     article.author = UserProfile.objects.get(id=int(author))
            #     article.title = df.ix[i, 'title']
            #     article.desc = df.ix[i, 'desc']
            #     article.detail = df.ix[i, 'content']
            #     article.click_num = 0
            #     article.fav_nums = 0
            #     article.score = df.ix[i, 'score']
            #     # author,title,desc,detail,click_num,fav_nums,image,score,add_time
            #     article.save()
            # 初始化course

            # 读取excel文件
            # 设置GBK编码
            xlrd.Book.encoding = "gb18030"
            data = xlrd.open_workbook("C:\\Users\\Administrator\\Desktop\\%s"%request.FILES['excel'].name)
            # 获取excel第一个表
            table = data.sheets()[0]
            # 获取该表行数
            nrows = table.nrows
            # json.jump(data.sheet_names(), ensure_ascii=False, encoding="gb2312")
            # 第一行一般为表头，故从该表第二行开始循环取值
            for j in range(1, nrows):
                # 获取机构名称,根据表具体内容调整下标
                article = Article()
                author = 1
                # 获取其他字段值,根据表具体内容调整下标
                article.title = table.row_values(j)[1]
                article.desc = table.row_values(j)[4]
                article.author = UserProfile.objects.get(id=int(author))
                article.detail = table.row_values(j)[3]
                article.click_num = 0
                article.fav_nums = 0
                article.score = table.row_values(j)[8]
                # author,title,desc,detail,click_num,fav_nums,image,score,add_time
                article.save()

            # with open("C:\\Users\\Administrator\\Desktop\\fitdata.csv", 'r') as f:
            #     for line in f.readlines():
            #         article = Article()
            #         author = 1
            #         article_list = line.strip().split(',')
            #         if article_list[0] == 'id':
            #             continue
            #         article.title = article_list[1]
            #         article.desc = article_list[-5]
            #         article.author = UserProfile.objects.get(id=int(author))
            #         article.detail = article_list[3:-5]
            #         article.click_num = 0
            #         article.fav_nums = 0
            #         article.score = float(article_list[-1])
            #         # author,title,desc,detail,click_num,fav_nums,image,score,add_time
            #         article.save()


        return super(ArticleAdmin,self).post(request,args,kwargs)

xadmin.site.register(Article, ArticleAdmin)