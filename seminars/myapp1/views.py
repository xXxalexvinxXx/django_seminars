import logging

from django.http import HttpResponse

logger = logging.getLogger('page_visits')

def index(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Главная</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            h1 { color: #333; }
            p { line-height: 1.6; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Задание 1</h1>
            <p>Добро пожаловать на главную страницу проекта, задание 1!</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur consequat enim ipsum, sit amet sodales
            quam aliquam sit amet. Morbi ante odio, venenatis nec viverra aliquet, blandit bibendum erat. Vivamus
            tincidunt porttitor massa ac dignissim. Vestibulum eu molestie massa, sed aliquet purus. Praesent ac mi
            sit amet neque pellentesque pharetra a vel urna. Proin vitae vestibulum neque. Aliquam finibus ultricies
            felis a vehicula. Nam ac elementum risus. Sed sed dapibus tellus, ac convallis lacus. Nunc pellentesque 
            metus vel libero aliquet facilisis. In at malesuada libero, quis vulputate metus.</p>
            </n>
            <p>Phasellus et leo massa. In convallis tortor pellentesque blandit vehicula. Cras mi dolor, facilisis eu
            orci dapibus, sodales laoreet orci. Duis non lectus quis leo tincidunt tempor. Phasellus at cursus erat,
            eu dapibus eros. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae;
            Vestibulum iaculis mauris ac scelerisque hendrerit. Praesent malesuada nisi semper, blandit sapien in,
            efficitur quam. Suspendisse potenti. Aliquam ut tempus nunc. In tincidunt suscipit sem, non laoreet
            tellus. Quisque volutpat ex nisl, non fermentum nibh commodo eu. Ut vitae odio sed purus ultrices euismod 
            nec eu neque. Nam quis nulla gravida, luctus nisl sed, egestas ipsum.</p>
            </n>
            <p>Quisque nec dapibus odio. Ut ac porta erat, sit amet rutrum leo. Nulla ipsum tellus, vestibulum vel
            commodo vitae, pellentesque ac est. Donec quis tempor arcu. Curabitur porta commodo purus, id vestibulum 
            nunc pellentesque sed. Quisque sed consectetur augue. Mauris justo velit, gravida nec diam lobortis,
            porttitor faucibus lectus. Curabitur facilisis purus in urna vulputate cursus. Aliquam efficitur rutrum 
            ipsum pharetra tincidunt. Nunc cursus neque sed felis interdum, at vestibulum sem tempus. Ut convallis, 
            neque ut vulputate finibus, velit purus elementum dui, sit amet pretium mi odio et metus. Aliquam
            interdum ullamcorper augue, et consequat ligula sagittis ac. Nullam tincidunt iaculis euismod..</p>
            <nav>
                <a href="/about/">Обо мне</a>
            </nav>
        </div>
    </body>
    </html>
    """
    logger.info('Index page accessed')
    return HttpResponse(html)

def about(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Обо мне</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            h1 { color: #333; }
            p { line-height: 1.6; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Обо мне</h1>
            <p>Привет! Меня зовут Александр, я выполняю 1е задание семинара.</p>
            </n>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus justo ligula, finibus id risus ut, tempus dapibus justo. Aliquam lacus turpis, elementum id porttitor nec, finibus sed eros. Vestibulum imperdiet sem ut malesuada tempus. Donec facilisis lacus bibendum mi commodo, ut rutrum odio ornare. Maecenas volutpat enim sit amet tellus pulvinar cursus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Proin in viverra metus. Aenean venenatis turpis auctor dui molestie, vitae iaculis ligula tempus. Vestibulum feugiat viverra enim ac viverra. Suspendisse sit amet nisi blandit, egestas est ac, malesuada nunc. Sed non auctor massa. Nunc imperdiet risus eu vulputate lacinia. Sed eu massa id ante congue suscipit et vitae orci.</p>

            <p>Cras gravida maximus dui quis fermentum. Aliquam mattis consequat nulla, id cursus lorem finibus nec. Curabitur at pulvinar nisi. Quisque accumsan lacus vitae hendrerit semper. Quisque a congue mi. Phasellus felis ligula, sollicitudin vitae faucibus at, feugiat ut augue. Etiam vulputate sit amet elit quis aliquet. Etiam odio lectus, laoreet et accumsan non, consequat at enim. Donec sit amet eleifend nibh. Curabitur dignissim, libero vel fringilla venenatis, magna velit lacinia lectus, et imperdiet enim urna id turpis. Cras a condimentum nisi, sed dictum enim. Cras luctus, sem ut vehicula elementum, dui nunc dignissim erat, ut auctor odio quam tristique urna. Aenean et augue quis elit tincidunt laoreet quis a nisl.</p>
            <nav>
                <a href="/">На главную</a>
            </nav>
        </div>
    </body>
    </html>
    """
    logger.info('About page accessed')
    return HttpResponse(html)