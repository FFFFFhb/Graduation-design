# _*_ coding:utf-8 _*_
from .models import Article
from users.models import UserProfile
import xadmin
import pandas as pd
import xlrd

class ArticleAdmin(object):
    #author,title,desc,detail,click_num,fav_nums,image,score,add_time
    list_display = ['title', 'desc', 'detail', 'score', 'fav_nums', 'image', 'click_num', 'add_time']
    search_fields = ['title', 'desc', 'detail', 'score', 'fav_nums', 'image', 'click_num']
    list_filter = ['title', 'desc', 'detail', 'score', 'fav_nums', 'image', 'click_num', 'add_time']
    import_excel = True

    def post(self,request,*args,**kwargs):
        if 'excel' in request.FILES:
            df = pd.read_csv("C:\\Users\\Administrator\\Desktop\\fitdata.csv",encoding = 'gb18030')
            for i in range(df.shape[0]):
                article = Article()
                author = 1
                article.author = UserProfile.objects.get(id=int(author))
                article.title = df.ix[i, 'title']
                article.desc = df.ix[i, 'desc']
                article.detail = df.ix[i, 'content']
                article.click_num = 0
                article.fav_nums = 0
                article.score = df.ix[i, 'score']
                # author,title,desc,detail,click_num,fav_nums,image,score,add_time
                article.save()

                

        return super(ArticleAdmin,self).post(request,args,kwargs)

xadmin.site.register(Article, ArticleAdmin)