from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from article import models
from article import myforms
import logging
import markdown

logger = logging.getLogger(__name__)


# Create your views here.


def get_valid_img(request):
    # with open("valid_code.png", "rb") as f:
    #     data = f.read()
    # 自己生成一个图片
    from PIL import Image, ImageDraw, ImageFont
    import random

    # 获取随机颜色的函数
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 生成一个图片对象
    img_obj = Image.new(
        'RGB',
        (220, 35),
        get_random_color()
    )
    # 在生成的图片上写字符
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件， 得到一个字体对象
    font_obj = ImageFont.truetype("static/font/kumo.ttf", 28)
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(5):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)
        draw_obj.text((20 + 40 * i, 0), tmp, fill=get_random_color(), font=font_obj)

    print("".join(tmp_list))
    print("生成的验证码".center(120, "="))
    # 不能保存到全局变量
    # global VALID_CODE
    # VALID_CODE = "".join(tmp_list)

    # 保存到session
    request.session["valid_code"] = "".join(tmp_list)
    # 加干扰线
    # width = 220  # 图片宽度（防止越界）
    # height = 35
    # for i in range(5):
    #     x1 = random.randint(0, width)
    #     x2 = random.randint(0, width)
    #     y1 = random.randint(0, height)
    #     y2 = random.randint(0, height)
    #     draw_obj.line((x1, y1, x2, y2), fill=get_random_color())

    # # 加干扰点
    # for i in range(40):
    #     draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color())

    # 将生成的图片保存在磁盘上
    # with open("s10.png", "wb") as f:
    #     img_obj.save(f, "png")
    # # 把刚才生成的图片返回给页面
    # with open("s10.png", "rb") as f:
    #     data = f.read()

    # 不需要在硬盘上保存文件，直接在内存中加载就可以
    from io import BytesIO
    io_obj = BytesIO()
    # 将生成的图片数据保存在io对象中
    img_obj.save(io_obj, "png")
    # 从io对象里面取上一步保存的数据
    data = io_obj.getvalue()
    return HttpResponse(data)


def index(request):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    article_list = models.Article.objects.all().order_by('-create_time')
    # print(request.user.username)

    p = Paginator(article_list, 4, )
    laws = p.page(page)
    return render(request, 'index.html', locals())


def login(request):
    next = request.GET.get('next', '')
    if request.method == 'POST':
        ret = {"status": 0, "msg": ""}
        user = request.POST.get('username')
        password = request.POST.get('password')

        valid_code = request.POST.get('valid_code')
        print(valid_code, '*' * 120)
        if user:
            if password:
                if valid_code and valid_code.upper() == request.session.get('valid_code').upper():
                    user_obj = auth.authenticate(username=user, password=password)
                    if user_obj:
                        auth.login(request, user_obj)
                        if next:
                            ret["msg"] = next
                        else:
                            ret["msg"] = "/index/"
                    else:
                        ret['status'] = '1'
                        ret['msg'] = '用户名或密码错误'
                else:
                    ret['status'] = '1'
                    ret['msg'] = '验证码错误'
            else:
                ret['status'] = '1'
                ret['msg'] = '密码不能为空'
        else:
            ret['status'] = '1'
            ret['msg'] = '用户名不能为空'
        return JsonResponse(ret)
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        ret = {'statue': 0, 'msg': ''}
        form_obj = myforms.RegForm(request.POST)
        if form_obj.is_valid():
            form_obj.cleaned_data.pop('re_password')
            avatar_img = request.FILES.get('avatar')
            if avatar_img:
                models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)
            else:
                models.UserInfo.objects.create_user(**form_obj.cleaned_data)
            ret["msg"] = "/login/"
            return JsonResponse(ret)
        else:
            print(form_obj.errors)
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            print(ret)
            print("=" * 120)
            return JsonResponse(ret)
    form_obj = myforms.RegForm()
    return render(request, "register.html", {"form_obj": form_obj})


def logout(request):
    auth.logout(request)
    return redirect("/login/")


from django.contrib.auth.decorators import login_required


@login_required
def home(request, user):
    username = models.UserInfo.objects.filter(username=user).first()
    if not username:
        logger.warning("又有人访问不存在页面了...")
        return HttpResponse('404')
    article_list = models.Article.objects.filter(user=username)
    # 获取当前页, 有则为page,无则默认为1
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(article_list, 5)
    page_list = p.page(page)
    return render(request, 'home.html', locals())


def article_detail(request, user, pk):
    user = models.UserInfo.objects.filter(username=user).first()
    if not user:
        return HttpResponse("404")
    blog = user.blog
    # 找到当前的文章
    article_obj = models.Article.objects.filter(pk=pk).first()

    # conenet  = models.ArticleDetail.objects.filter(article=article_obj)

    content = markdown.markdown(article_obj.articledetail.content,
                                                          extensions=[
                                                              # 包含 缩写、表格等常用扩展
                                                              'markdown.extensions.extra',
                                                              # 语法高亮扩展
                                                              'markdown.extensions.codehilite',
                                                          ])
    # 所有评论列表
    comment_list = models.Comment.objects.filter(article_id=pk)

    return render(
        request,
        "article_detail.html",
        locals()
    )


def article_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('article_content')
        user = request.user
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(content, 'html.parser')
        if len(bs) > 150:
            desc = bs.text[0:150] + "..."
        else:
            desc = bs.text[0:150]
        article_obj = models.Article.objects.create(user=user, desc=desc, title=title)
        models.ArticleDetail.objects.create(content=content, article_id=article_obj.nid)
        return redirect('/index/')

    return render(request, 'add_article.html')

def article_del(request,pk):
    models.Article.objects.filter(pk=pk).delete()
    return redirect('/index/')
