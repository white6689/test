from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from requests import get
from django.shortcuts import render, redirect
from home.models import Instance
import urllib.request, json
import paramiko
import json
import wget
import os,sys

# SSH 정보
server = ""
user = ""
pwd = ""
def base(request):
    return render(request, 'base.html')
def input(request):
    return render(request, 'input.html')
def getPost(request):
    # 누르면 ssh 동작
    page_name=request.POST.get('page_name', None)
    service=request.POST.get('service_name', None)
    git_url=request.POST.get('git_url', None)
    index_folder=request.POST.get('index_folder', None)
    test_val=ssh_connect(page_name, service, git_url, index_folder)
    return redirect('/home/read')
def readPage(request):
    pages=Instance.objects.all()
    context = {
         'pages' : pages
    }
    return render(request, 'base.html', context)
def refreshCommit(request, iid):
    instance=Instance.objects.get(id=iid)
    new_commit=get_commit(instance.git_url)
    # DB에 git_commit내역이 없을경우 또는 기존 commit 번호와 다를 경우 clone을 한 뒤, db에 git_commit 업데이트
    if (instance.git_commit == "") or (instance.git_commit != new_commit):
         # DB 넣기
         instance.git_commit=new_commit
         instance.save()
         print("Todo: pagename, git commit 번호도 함께 보내준다. 그래서 Vagrant server에서 clone도하면서 DB도 업데이트하게 함")
         # ssh로 git 갱신 명령어 보내기
    ssh_connect_git(instance.page_name, instance.index_folder)
    return redirect('/home/read')
def deletePage(request, iid):
    instance=Instance.objects.get(id=iid)
    ssh_connect_delete(instance.page_name)
    instance.delete()
    return redirect('/home/read')
# ssh 연결을 위한 함수, arg: page_name, service type, git_url, index_folder
def ssh_connect(pn, srv, gu, idxf):
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    server = "192.168.1.201"
    user = "root"
    pwd = "test123"
    cli.connect(server, port=22, username=user, password=pwd)
    command="/root/vagrant-ansible-kubernetes-1.21/insert.sh "+pn+" "+srv+" "+gu+" "+idxf
    # command="cd /root/vagrant-ansible-kubernetes-1.21; vagrant ssh k8s-master -- -t 'touch /home/vagrant/ingress/test_juyeon/text1.txt'"
    stdin, stdout, stderr = cli.exec_command(command)
    lines = stdout.readlines()
    print(''.join(lines))
    val=''.join(lines)
    cli.close()
    return val
# git 갱신할 때 필요한 ssh, page name, index folder
def ssh_connect_git(pn, idxf):
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    server = "192.168.1.201"
    user = "root"
    pwd = "test123"
    cli.connect(server, port=22, username=user, password=pwd)
    # 파일 경로
    command="/root/vagrant-ansible-kubernetes-1.21/giturl.sh "+pn+" "+idxf
    stdin, stdout, stderr = cli.exec_command(command)
    lines = stdout.readlines()
    print(''.join(lines))
    val=''.join(lines)
    cli.close()
# page 삭제할 때 필요한 ssh
def ssh_connect_delete(pn):
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    server = "192.168.1.201"
    user = "root"
    pwd = "test123"
    cli.connect(server, port=22, username=user, password=pwd)
    # 파일 경로
    command="cd /root/vagrant-ansible-kubernetes-1.21; /root/vagrant-ansible-kubernetes-1.21/delete.sh "+pn
    stdin, stdout, stderr = cli.exec_command(command)
    lines = stdout.readlines()
    print(''.join(lines))
    val=''.join(lines)
    cli.close()

# commit 번호 불러오기, arg: git_url
def get_commit(gu):
    list_url=gu.split('/')
    url_str="https://api.github.com/repos/"+list_url[3]+"/"+list_url[4].split('.')[0]+"/commits"
    str=""
    with urllib.request.urlopen(url_str) as url:
        data = json.load(url)
        str=data[0]['sha'][:8]
    return str
