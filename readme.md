
# 邮件小爬虫

imap协议抓取邮件中的邮件打印到控制台中，并标记该邮件为已读。

用新浪(sina)和网易(163)邮箱测试通过。

打印示例：

```
------------------------HEADER------------------------
||          From: somebody <somebody@gmail.com>
||          To:  <yyccqwer@sina.com>
||          Subject: 测试邮件
------------------------HEADER------------------------
------------------------CONTENT1------------------------
邮件内容
------------------------CONTENT2------------------------
<div dir="auto"><span>邮件内容<br><br></span></div>
```