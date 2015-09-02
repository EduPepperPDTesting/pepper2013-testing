from HTMLParser import HTMLParser

def strip_tags(html):
    html = html.strip()
    html = html.strip("\n")
    result = []
    parse = HTMLParser()
    parse.handle_data = result.append
    parse.feed(html)
    parse.close()
    return "".join(result)

def send_html_mail(subject, html, fr, to, attaches=None):
    from django.core.mail import EmailMultiAlternatives
    text=strip_tags(html)
    msg = EmailMultiAlternatives(subject, text, fr, to)
    msg.attach_alternative(html, "text/html")
    if attaches:
        for a in attaches:
            msg.attach(a['filename'], a['data'], a['mimetype'])
    msg.send()
