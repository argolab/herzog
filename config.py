#-*- coding: utf-8 -*-

SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

O = {}

site = {
    'navhead' : (
        ('fresh', O, u'新鲜发言', u'新鲜发言'),
        ('topten', O, u'今日十大', u'今日十大'),
        ('board', { 'boardname' : 'Lecture' }, u'讲座信息', u'讲座信息'),
        ('board', { 'boardname' : 'Say' }, u'不吐不快', u'吐槽'),
        ('board', { 'boardname' : 'Love' }, u'Love版', u'情感'),
        ('board', { 'boardname' : 'Search' }, u'寻人寻物版', u'失物招领')
    )
}
