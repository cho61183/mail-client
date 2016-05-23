# -*- coding: utf-8 -*-

import sys
import poplib
import imaplib
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import requests
import time
import json

reload(sys)
sys.setdefaultencoding('utf-8')

# 配置邮箱信息
print("确保你的邮箱允许imap协议链接。\n")
email = raw_input("输入邮箱：")
password = raw_input("输入密码：")
imap_server = raw_input("输入imap地址(如:imap.sina.com)：")
print("开始抓取...\n")

def guess_charset(msg):
	charset = msg.get_charset()
	if charset is None:
		content_type = msg.get("Content-Type", "").lower()
		pos = content_type.find("charset=")
		if pos >= 0:
			charset = content_type[pos + 8:].strip()
	return charset

def decode_str(s):
	value, charset = decode_header(s)[0]
	if charset:
		value = value.decode(charset)
	return value


def ps_msg(msg, indent = 0):
	
	if indent == 0:
		print('------------------------HEADER------------------------')
		for header in ["From", "To", "Subject"]:
			value = msg.get(header, "")

			if value:
				if header=="Subject":
					value = decode_str(value)
					
				else:
					hdr, addr = parseaddr(value)
					name = decode_str(hdr)

					value = u"%s <%s>" % (name, addr)
			print("||%s%s: %s" % ("  " * 5, header, value))
		
		print('------------------------HEADER------------------------')
		
	if (msg.is_multipart()):
		parts = msg.get_payload()
		for n, part in enumerate(parts):
			
			print('------------------------CONTENT%s------------------------' % (n+1))
			ps_msg(part, indent=indent + 1)
	else:
		content_type = msg.get_content_type()

		# 文本格式打印
		if content_type=="text/plain":
			content = msg.get_payload(decode=True)
			charset = guess_charset(msg)
			if charset:
				content = content.decode(charset)
			# content = content.split(cur_string)[0]

			print content

		# html格式
		elif content_type=="text/html":
			content = msg.get_payload(decode=True)
			charset = guess_charset(msg)
			if charset:
				content = content.decode(charset)
			
			print content
		# 附件暂不处理
		else:
			print("%sAttachment: %s" % ("  " * indent, content_type))

	
# imap
def main(server):
	typ, allData = server.search(None, 'UNSEEN')
	if typ == 'OK':
		for num in allData[0].split():
			typ, data = server.fetch(num, '(RFC822)')
			msg_content = Parser().parsestr(data[0][1])

			# 处理
			ps_msg(msg_content)


	# 标记为已读
	for num in allData[0].split():
		server.store(num, '+FLAGS', '\Seen')

	server.expunge()
	

def start():
	# 链接服务器
	server = imaplib.IMAP4_SSL(imap_server, 993)
	server.login(email, password)
	server.select("INBOX")

	while True:
		try:
			main(server)
		except Exception,e:
			# 错误处理
			print e
		time.sleep(3)


if __name__ == "__main__":
	start()
