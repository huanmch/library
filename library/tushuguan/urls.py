# coding: utf-8

from django.conf.urls import patterns,url

urlpatterns = patterns('',
    #url(r'^ajax_search/$', ajax_search_page),
    #url(r'^search/$', search_page),
    #url(r'^stack/$',stack_page),
    #url(r'^ajax_stack/$',ajax_stack_page),
    #url(r'^logout/$',logout),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'tushuguan.views.auto_index'),
    url(r'^index/$', 'tushuguan.views.index_page', name='home'),
    #url(r'^ajax_index_/$', 'tushuguan.views.ajax_index_page', name='ajax_index_page'),
    #url(r'^borrow/$','tushuguan.views.borrow_page', name='borrow_page'),
    #url(r'^ajax_borrow_/','tushuguan.views.ajax_borrowed_page', name='ajax_borrowed_page'),
    #url(r'^ajax_needreturn_/','tushuguan.views.ajax_needreturn_page', name='ajax_needreturn_page'),
    #url(r'^ajax_returned_/','tushuguan.views.ajax_returned_page', name='ajax_returned_page'),

    #url(r'^ajax_returning_/','tushuguan.views.ajax_returning_page', name='ajax_returning_page'),
    #url(r'^ajax_borrowing_/','tushuguan.views.ajax_borrowing_page', name='ajax_borrowing_page'),
#自动添加数据，慎用！！
    #url(r'^insert_books/', 'tushuguan.mix.insert'),

    #url(r'^enter_add/','tushuguan.views.enter_add', name='enter_add'),
    #url(r'^AddInStockBill/', 'tushuguan.views.addinstock', name='addinstock'),
)
