# original = "datasets/tcga.db"
# destination = "datasets/new_tcga.db"
# content = ''
# outsize = 0
#
# with open(original, 'rb') as infile:
#     content = infile.read()
# with open(destination, 'wb') as output:
#     for line in content.splitlines():
#         outsize += len(line) + 1
#         output.write(line + str.encode('\n'))
# print("Done. Saved %s bytes." % (len(content) - outsize))



#!/usr/bin/env python
#-*- coding:utf-8 -*-
import pickle


accounts = {
 1000:{
 'name':'xiaoming',
 'email':'10000@qq.com',
 'balance':100,
 'bank_acc':{
 'ICBC':100,
 'ABC':1000
 }
 }
 }
f = open('account.db','wb')
f.write(pickle.dumps(accounts))
f.close()


f = open('account.db','rb')
print(f.read())
account_db = pickle.load(f)
print (account_db)